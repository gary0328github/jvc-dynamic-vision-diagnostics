import csv,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'source_data'
sys.stdout.reconfigure(encoding='utf-8')
sys.path[:0]=[str(ROOT/'.deps'),str(Path(__file__).resolve().parent/'support')]
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from audit_panel_alignment import require_matplotlib_panel_alignment
import numpy as np
OUT=ROOT/'outputs';OUT.mkdir(exist_ok=True)
from matplotlib import font_manager
font_family='Liberation Sans' if 'Liberation Sans' in {f.name for f in font_manager.fontManager.ttflist} else 'DejaVu Sans'
plt.rcParams.update({'font.family':font_family,'font.size':7,'pdf.fonttype':42,'svg.fonttype':'none','axes.linewidth':.7,'savefig.facecolor':'white','hatch.linewidth':.5})
BLUE='#3164A0';LIGHT='#BCD3EA';ORANGE='#DE853C';TEAL='#318F89';GREY='#7C8793';INK='#263541'
def schematic_export(fig,n,panels):
    if n==5:
        groups={'row_groups':[['p1','p2'],['p3','p4']],'column_groups':[['p1','p3'],['p2','p4']]}
    else:
        groups={'row_groups':[['p1','p2']]}
    require_matplotlib_panel_alignment(fig,axes=panels,panel_ids=[f'p{i+1}' for i in range(len(panels))],json_out=OUT/f'Figure{n}.alignment.json',strict=True,**groups)
    p=OUT/f'Figure{n}'
    fig.savefig(p.with_suffix('.pdf'));fig.savefig(p.with_suffix('.svg'))
    fig.savefig(p.with_suffix('.png'),dpi=600)
    fig.savefig(p.with_suffix('.tiff'),dpi=600,pil_kwargs={'compression':'tiff_lzw'})
    plt.close(fig)



def verify_data():
    with (DATA/'pump_endpoints.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
    groups={m:[r for r in rows if r['method']==m] for m in ['DARM_FULL','DARM_PP025']}
    stats={}
    for m,rs in groups.items():
        assert len(rs)==36 and len({(r['task_id'],r['seed']) for r in rs})==36
        v=np.array([float(r['target_DAT'])*100 for r in rs]);by=[np.mean([float(r['target_DAT'])*100 for r in rs if int(r['speed'])==s]) for s in [20,30,40]]
        stats[m]={'overall':float(v.mean()),'worst':float(min(by)),'bottom25':float(np.sort(v)[:9].mean()),'speeds':[float(x) for x in by]}
    for m,vals in [('DARM_FULL',[50.23,43.06,21.30]),('DARM_PP025',[51.88,45.37,30.99])]:assert [round(stats[m][k],2) for k in ['overall','worst','bottom25']]==vals
    with (DATA/'pump_paired.csv').open(encoding='utf-8-sig') as f:paired=list(csv.DictReader(f))
    d=np.array([float(r['delta']) for r in paired]);assert [int((d>1e-10).sum()),int((abs(d)<=1e-10).sum()),int((d< -1e-10).sum())]==[11,17,8]
    endpoint_map={(r['method'],r['task_id'],r['seed']):float(r['target_DAT']) for r in rows}
    assert len(paired)==36
    for r in paired:
        for m in ['DARM_FULL','DARM_PP025']:assert abs(float(r[m])-endpoint_map[(m,r['task_id'],r['seed'])])<1e-12
    with (DATA/'rotor_endpoints.csv').open(encoding='utf-8-sig') as f:rr=list(csv.DictReader(f))
    methods=sorted({r['method'] for r in rr});rotor={}
    for m in ['DARM_FULL','DARM_PP025']:
        rs=[r for r in rr if r['method']==m];assert len(rs)==18,(m,methods)
        rotor[m]={'overall':float(np.mean([float(r['target_DAT'])*100 for r in rs])),'by_domain':{dom:float(np.mean([float(r['target_DAT'])*100 for r in rs if r['target_domain']==dom])) for dom in sorted({r['target_domain'] for r in rs})},'by_seed':{seed:float(np.mean([float(r['target_DAT'])*100 for r in rs if r['seed']==seed])) for seed in ['42','2026','3407']}}
    assert [round(rotor[m]['overall'],2) for m in ['DARM_FULL','DARM_PP025']]==[25.93,28.80]
    assert [round(v,2) for v in rotor['DARM_FULL']['by_domain'].values()]==[16.67,38.89,16.67,22.22,20.83,40.28]
    assert [round(v,2) for v in rotor['DARM_PP025']['by_domain'].values()]==[22.22,47.78,22.22,31.94,30.56,18.06]
    assert [round(v,2) for v in rotor['DARM_FULL']['by_seed'].values()]==[29.17,20.14,28.47]
    assert [round(v,2) for v in rotor['DARM_PP025']['by_seed'].values()]==[37.50,16.94,31.94]
    (OUT/'numeric_verification.json').write_text(json.dumps({'pump':stats,'paired_counts':[11,17,8],'rotor':rotor},indent=2),encoding='utf-8')

def quantitative_style(ax,title):
    ax.set_title(title,loc='left',fontsize=8.5,fontweight='bold',pad=10)
    ax.tick_params(labelsize=7,length=3,width=.6,direction='out')
    ax.spines['top'].set_visible(False);ax.spines['right'].set_visible(False)
    ax.set_axisbelow(True)

def paired_bars(ax,full,cal,labels,ymax=80,w=.32):
    x=np.arange(len(labels))
    p=ax.bar(x-w/2,full,w,color=BLUE,edgecolor=INK,lw=.55,label='Full DARM')
    q=ax.bar(x+w/2,cal,w,color=ORANGE,edgecolor=INK,lw=.55,label='Calibrated DARM (PtP = 0.25)')
    ax.set_xticks(x,labels);ax.set_ylim(0,ymax)
    ax.set_ylabel('DAT Macro-F1 (%)',fontsize=8)
    for bars in [p,q]:
        for z in bars:ax.text(z.get_x()+z.get_width()/2,z.get_height()+1.7,f'{z.get_height():.2f}',ha='center',va='bottom',fontsize=7)
    for j,(u,v) in enumerate(zip(full,cal)):
        ax.text(j,max(u,v)+8.2,f'Δ {v-u:+.2f} pp',ha='center',va='bottom',fontsize=7,color=INK)
    return p,q

def figure5():
    s=json.loads((OUT/'numeric_verification.json').read_text())['pump'];f=s['DARM_FULL'];c=s['DARM_PP025']
    with (DATA/'pump_endpoints.csv').open(encoding='utf-8-sig') as h:rows=list(csv.DictReader(h))
    with (DATA/'pump_paired.csv').open(encoding='utf-8-sig') as h:pairs=sorted(csv.DictReader(h),key=lambda r:(int(r['speed']),r['task_id'],int(r['seed'])))
    fig,axs=plt.subplots(2,2,figsize=(7.224,5.418));fig.subplots_adjust(left=.083,right=.985,bottom=.105,top=.94,wspace=.35,hspace=.63)
    a,b,cax,d=axs.ravel()
    quantitative_style(a,'(a) Across Pump speed blocks');p,q=paired_bars(a,f['speeds'],c['speeds'],['20 Hz','30 Hz','40 Hz']);a.set_xlabel('Speed block',fontsize=8)
    quantitative_style(b,'(b) Aggregate and difficult tail');paired_bars(b,[f[k] for k in ['overall','worst','bottom25']],[c[k] for k in ['overall','worst','bottom25']],['Overall mean','Worst speed','Bottom 25%']);b.set_xlabel('Summary metric',fontsize=8)
    quantitative_style(cax,'(c) Separately ranked endpoints')
    for m,col,mark in [('DARM_FULL',BLUE,'o'),('DARM_PP025',ORANGE,'^')]:
        v=sorted(float(r['target_DAT'])*100 for r in rows if r['method']==m)
        cax.scatter(np.arange(1,37),v,c=col,marker=mark,s=14,zorder=3,linewidths=.3,edgecolors='white')
    cax.axvspan(.5,9.5,color='#F2ECD9',zorder=0);cax.text(1.1,94,'Lowest nine',fontsize=7)
    cax.set(xlim=(.5,36.5),ylim=(0,101),xticks=[1,9,18,27,36]);cax.set_xlabel('Rank within each method',fontsize=8);cax.set_ylabel('DAT Macro-F1 (%)',fontsize=8)
    quantitative_style(d,'(d) Matched endpoint changes')
    delta=np.array([float(r['delta'])*100 for r in pairs]);colors=[ORANGE if x>1e-8 else BLUE if x< -1e-8 else GREY for x in delta]
    d.bar(np.arange(36),delta,color=colors,edgecolor=INK,linewidth=.3,width=.7)
    ties=np.where(abs(delta)<1e-8)[0];d.scatter(ties,np.zeros(len(ties)),marker='s',s=7,c=GREY,zorder=3)
    d.set(xlim=(-.8,35.8),ylim=(-62,72),xticks=[5.5,17.5,29.5],xticklabels=['20 Hz','30 Hz','40 Hz'],yticks=[-60,-30,0,30,60])
    d.text(.98,.95,'11 increases / 17 unchanged / 8 decreases',ha='right',va='top',transform=d.transAxes,fontsize=6.4)
    d.set_xlabel('Matched task–seed cells, grouped by speed',fontsize=7);d.set_ylabel('Calibrated − full F1 (pp)',fontsize=8)
    fig.legend([p,q],['Full DARM','Calibrated DARM (PtP = 0.25)'],loc='lower center',bbox_to_anchor=(.55,.008),ncol=2,frameon=False,fontsize=7.6)
    schematic_export(fig,5,list(axs.ravel()))

def figure6():
    r=json.loads((OUT/'numeric_verification.json').read_text())['rotor'];f=r['DARM_FULL'];c=r['DARM_PP025'];dom=list(f['by_domain']);seeds=['42','2026','3407']
    fig=plt.figure(figsize=(7.033,3.517));a=fig.add_axes([.14,.20,.45,.67]);b=fig.add_axes([.70,.20,.285,.67])
    quantitative_style(a,'(a) Six held-out domains');y=np.arange(6);w=.32
    fvals=[f['by_domain'][x] for x in dom];cvals=[c['by_domain'][x] for x in dom]
    p=a.barh(y-w/2,fvals,w,color=BLUE,edgecolor=INK,lw=.55);q=a.barh(y+w/2,cvals,w,color=ORANGE,edgecolor=INK,lw=.55)
    for bars in [p,q]:
        for z in bars:a.text(z.get_width()+.7,z.get_y()+z.get_height()/2,f'{z.get_width():.2f}',ha='left',va='center',fontsize=7)
    for j,(u,v) in enumerate(zip(fvals,cvals)):a.text(64,j,f'{v-u:+.2f}',ha='right',va='center',fontsize=7,color=INK)
    a.text(.975,1.025,'Δ (pp)',transform=a.transAxes,ha='right',fontsize=7)
    a.set(yticks=y,yticklabels=dom,xlim=(0,65),xticks=np.arange(0,61,10));a.invert_yaxis();a.set_xlabel('DAT Macro-F1 (%)',fontsize=8);a.set_ylabel('Held-out domain',fontsize=8)
    quantitative_style(b,'(b) Seed means');paired_bars(b,[f['by_seed'][s] for s in seeds],[c['by_seed'][s] for s in seeds],seeds,ymax=70,w=.42);b.set_xlabel('Training seed',fontsize=8)
    fig.legend([p,q],['Full DARM','Calibrated DARM (PtP = 0.25)'],loc='lower center',bbox_to_anchor=(.55,.012),ncol=2,frameon=False,fontsize=7.6)
    schematic_export(fig,6,[a,b])


def figure4():
    with (DATA/'pump_component_calibration.csv').open(encoding='utf-8-sig') as stream:
        rows=list(csv.DictReader(stream))
    panels=[(30,['DARM_IP_ONLY','DARM_IP_II','DARM_FULL'],['ItP','ItP+ItI','FULL']),
            (40,['DARM_IP_II','DARM_FULL'],['ItP+ItI','FULL'])]
    colors={'DARM_IP_ONLY':'#BCCEE5','DARM_IP_II':'#F2C86D','DARM_FULL':'#365F9F'}
    with plt.rc_context({'font.family':'serif','font.serif':['Times New Roman','DejaVu Serif']}):
        fig,axes=plt.subplots(1,2,figsize=(7.05,2.737))
        fig.subplots_adjust(left=.075,right=.99,bottom=.23,top=.84,wspace=.32)
        for index,(speed,methods,labels) in enumerate(panels):
            axis=axes[index]
            means=[]
            for method in methods:
                values=[float(row['DAT_macro_f1'])*100 for row in rows if int(row['speed'])==speed and row['method']==method]
                if len(values)!=12:
                    raise ValueError('Expected twelve endpoints for each Figure 4 group')
                means.append(float(np.mean(values)))
            bars=axis.bar(np.arange(len(methods)),means,width=.52,color=[colors[method] for method in methods],edgecolor=INK,linewidth=.65)
            axis.set_title(f'({chr(97+index)}) {speed} Hz',loc='left',fontsize=10,fontweight='bold',pad=14)
            axis.set(ylim=(0,75),yticks=np.arange(0,71,10),xticks=np.arange(len(methods)),xticklabels=labels)
            axis.set_xlabel('Objectives retained from update 1',fontsize=8)
            axis.set_ylabel('DAT Macro-F1 (%)',fontsize=8)
            axis.tick_params(labelsize=8)
            axis.set_axisbelow(True)
            axis.grid(axis='y',linestyle='--',color='#E1E1E1',linewidth=.5)
            for bar in bars:
                axis.text(bar.get_x()+bar.get_width()/2,bar.get_height()+1,f'{bar.get_height():.2f}',ha='center',fontsize=8)
            delta=means[-1]-means[-2]
            axis.text(.5,.92,f'Adding PtP: {delta:+.2f} pp',transform=axis.transAxes,ha='center',fontsize=8,color=INK)
        schematic_export(fig,4,list(axes))

if __name__=='__main__':
    verify_data();figure4();figure5();figure6()
    print('Quantitative figures 4, 5 and 6 exported with neutral delta labels; source data verified.')
