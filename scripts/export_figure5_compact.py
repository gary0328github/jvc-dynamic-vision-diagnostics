"""Re-export Figure 5 with additional space above the shared legend."""

import importlib.util
import json
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "plot_figures.py"
OUT = Path(__file__).resolve().parents[1] / "outputs"
OUT.mkdir(exist_ok=True)
spec = importlib.util.spec_from_file_location("original_figure_plots", SOURCE)
plots = importlib.util.module_from_spec(spec)
spec.loader.exec_module(plots)
plots.OUT = OUT
plots.plt.rcParams.update({
    "font.family": "Arial",
    "font.size": 7,
    "pdf.fonttype": 42,
    "svg.fonttype": "none",
})


def export_with_legend_spacing(fig, number, panels):
    assert number == 5
    width, height = fig.get_size_inches()
    extra_height = 0.20
    original_positions = [axis.get_position().frozen() for axis in panels]
    fig.set_size_inches(width, height + extra_height)
    for axis, bounds in zip(panels, original_positions):
        axis.set_position([
            bounds.x0,
            (bounds.y0 * height + extra_height) / (height + extra_height),
            bounds.width,
            bounds.height * height / (height + extra_height),
        ])
    legend = fig.legends[0]
    legend.set_bbox_to_anchor((0.55, 0.008 * height / (height + extra_height)), transform=fig.transFigure)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    legend_top = legend.get_window_extent(renderer).y1
    label_bottom = min(axis.xaxis.label.get_window_extent(renderer).y0 for axis in panels[2:])
    gap_pt = (label_bottom - legend_top) * 72 / fig.dpi
    assert gap_pt >= 10, f"Insufficient legend clearance: {gap_pt:.2f} pt"
    plots.require_matplotlib_panel_alignment(
        fig,
        axes=panels,
        panel_ids=["p1", "p2", "p3", "p4"],
        row_groups=[["p1", "p2"], ["p3", "p4"]],
        column_groups=[["p1", "p3"], ["p2", "p4"]],
        json_out=OUT / "Figure5.alignment.json",
        strict=True,
    )
    fig.savefig(OUT / "JVC_Figure5_Revised.pdf")
    fig.savefig(OUT / "JVC_Figure5_Revised.svg")
    fig.savefig(OUT / "JVC_Figure5_Revised.png", dpi=600)
    fig.savefig(OUT / "preview.png", dpi=300)
    (OUT / "spacing_check.json").write_text(json.dumps({
        "added_height_inches": extra_height,
        "legend_clearance_pt": gap_pt,
        "export_dpi": 600,
        "original_panel_dimensions_preserved": True,
        "physical_panel_dimensions_inches": [
            [position.width * width, position.height * height] for position in original_positions
        ],
    }, indent=2), encoding="utf-8")
    plots.plt.close(fig)


plots.schematic_export = export_with_legend_spacing
plots.verify_data()
plots.figure5()
