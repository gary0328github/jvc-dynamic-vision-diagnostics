# 动态视觉机械故障诊断支持材料

本仓库公开数值源数据、绘图脚本、数值核验脚本及引用信息，对应正在准备投稿的领域泛化机械故障诊断论文。

`source_data`包含270个主实验端点、192个组件／系数端点及对应汇总。不同面板复用已有物理记录，任务和随机种子描述重复评价。

在仓库根目录运行`python scripts/verify_source_data.py`可核对文件哈希、主要均值及图稿数据。运行`python scripts/plot_figures.py`生成图4至图6，随后运行`python scripts/export_figure5_compact.py`得到现稿采用的图5紧凑图例版本。依赖见requirements.txt。

核心训练实现、预处理构建器、模型权重与原始记录保存在仓库之外。实现参考和预处理登记作为审稿材料随论文提供。公开内容用于检查论文数值和重绘定量图。

原始XJTU-DV数据入口为https://doi.org/10.5281/zenodo.17447083，使用时请引用数据创建者及原始论文。原始DARM代码入口为https://github.com/mozhenling/doge-darm。

作者依次为Chengrui Yang、Peng Yu、Hongtao Hao及Xiang Li。引用信息见CITATION.cff。当前MIT许可证适用于仓库中的绘图和核验软件，复用时需保留许可证要求的版权与许可声明。
