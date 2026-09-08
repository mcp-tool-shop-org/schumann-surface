<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/schumann-surface/readme.png" alt="Schumann Surface" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/schumann-surface/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/schumann-surface/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT"></a>
  <a href="https://mcp-tool-shop-org.github.io/schumann-surface/"><img src="https://img.shields.io/badge/landing-page-0ea5e9" alt="Landing page"></a>
  <a href="https://huggingface.co/datasets/mcp-tool-shop/schumann-sierra-nevada"><img src="https://img.shields.io/badge/dataset-Hugging%20Face-ffcc4d" alt="Dataset"></a>
</p>

<p align="center"><a href="README.md">English</a> · <a href="README.ja.md">日本語</a> · <a href="README.zh.md">中文</a> · <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.it.md">Italiano</a> · <a href="README.pt-BR.md">Português (BR)</a></p>

# 舒曼表面

将舒曼共振表示为带有事件通道和真实的、滞后的互相关面板的 3D 时频表面。呈现了一个月的真实超低频 (ELF) 站数据，以便人们可以观察到每日闪电节律、模式带以及地磁暴的影响和未影响。

状态：v1.0.0。2013 年 10 月和 6 月，来自内华达山脉 ELF 站（格拉纳达大学）的数据，针对该站自己发布的频谱和模式拟合，逐个插槽地进行重现；剩余十个月的原始存档数据正在通过相同的流水线进行处理。该可视化工具是一个独立的 HTML 文件，包含四种模式；可在 [登录页面](https://mcp-tool-shop-org.github.io/schumann-surface/viewer/) 处查看。

## 它显示的内容

- **表面**：时间（一个月，30 分钟为一列）× 频率（6–25 Hz，0.125 Hz 为一行）× 以 1 pT/√Hz 为基准的磁场幅度（dB）。NS 和 EW 传感器作为两个可堆叠的图层。
- **模式带**：拟合的模式 1–3 的中心频率，显示在表面上。
- **事件通道**，位于表面前方：Kp 地磁指数（3 小时，GFZ），站点当地时间（根据时间戳计算），M6+ 级地震（USGS）。
- **相关面板**：皮尔逊 r 与任何表面序列（模式幅度、模式频率、频带功率）和任何事件序列之间的滞后（±24 小时）的关系，其中 95% 的零带的有效样本大小已针对两个序列中的自相关性进行校正（Bartlett）。曲线位于该带内，表示结果为零，并显示为一条线。

## 为什么频带为 6–25 Hz

该站点的线圈是一个 RLC 传感器，其谐振频率接近 33 Hz，并且由其作者针对 6–25 Hz 进行了校准。高于 25 Hz 时，原始频谱主要由传感器谐振决定，而不是由谐振腔决定，因此无法从该仪器中分辨出模式 4 及更高的模式。需要一个更宽频带的站点来检测这些模式。

## 验证（2013 年 10 月，每个传感器 4464 个插槽）

| 与该站点发布的 npz 文件进行比较 | NS | EW |
|---|---|---|
| 幅度频谱比率，我们的数据/站点数据，6–25 Hz（中位数、p5、p95） | 1.0000 / 1.0000 / 1.0000 | 1.0000 / 1.0000 / 1.0000 |
| 每个插槽的饱和度，相关性 | 1.000 | 1.000 |
| 模式 1 中心频率，中位数差异 | +0.004 Hz | +0.008 Hz |
| 模式 2 中心频率，中位数差异 | +0.000 Hz | +0.002 Hz |
| 模式 3 中心频率，中位数差异 | -0.000 Hz | +0.001 Hz |
| 模式峰值幅度比率，中位数 | 1.001 / 1.000 / 1.000 | 1.001 / 1.000 / 1.000 |

残余频率散布是两个 Levenberg-Marquardt 实现（站点上的 lmfit，以及这里的 SciPy）在少数插槽上落在不同的局部最小值上；可视化工具会屏蔽那些超出文档中记录的每个模式窗口的拟合结果。

验证器是一个门：除非至少 95% 的插槽在 30 秒内匹配，频谱比率的第 5 和第 95 百分位数位于 1 ± 0.005 范围内，每个模式的中位数频率差异小于 0.02 Hz，并且饱和度序列的相关性高于 0.99，否则它将退出并返回非零值。

## 闪电通道：模型，而非测量

目前没有可公开下载的 2013 年全球闪电序列（WWLLN 需要订阅，Blitzortung 存档需要参与者登录，NASA 的 LIS/OTD 气候学数据位于 Earthdata 网站上）。因此，可视化工具包含一个 **烟囱时间表** 作为模型通道：三个高斯函数，分别对应于 UTC 时间的东南亚、非洲和美洲，基于 Whipple 1929、卡内基曲线（Harrison 2013）和 LIS/OTD 日变化气候学（Blakeslee et al. 2014）。在任何显示的地方，它都会被标记为模型。测量的对应数据也嵌入其中：每个模式在整个月内，每个 UTC 小时的平均幅度。请参见 `docs/data-contract.md`。

## 数据和许可

| 来源 | 内容 | 许可 | 在此处使用 |
|---|---|---|---|
| Salinas et al., Zenodo [10.5281/zenodo.6348930](https://zenodo.org/records/6348930) | 2013 年 3 月至 12 月以及 2017 年 1 月至 2 月的原始 256 Hz 时间序列 | CC BY 4.0 | 输入；派生产品由我们发布，并注明出处 |
| Salinas et al., Digibug [10481/71563](https://digibug.ugr.es/handle/10481/71563) | 站点处理的 10 分钟频谱 + 洛伦兹拟合 | CC BY-NC-ND 3.0 | 仅用于验证，绝不重新分发 |
| Salinas et al. 2022, *Computers & Geosciences* 165:105148；代码 [asalinas62/Sierra_Nevada_SR](https://github.com/asalinas62/Sierra_Nevada_SR) | 校准公式和处理链 | 论文 CC BY-NC-ND；代码按照其存储库中的规定 | 方法在 `scripts/process_month.py` 中重现 |
| GFZ 波茨坦 Kp 指数，Matzka et al. 2021 | 3 小时 Kp | CC BY 4.0 | 事件通道 |
| USGS FDSN 事件服务 | 地震 | 公共领域 | 事件通道 |

`data/` 中没有提交任何内容。Zenodo 存档是一个 26.5 GB 的 zip 文件；提取脚本通过 HTTP 范围请求读取其中心目录，并仅流式传输请求的月份。

## 流水线

```bash
python scripts/fetch_zenodo_month.py 1310          # ~2.4 GB, one month, both sensors
python scripts/process_month.py 1310 0             # NS  -> data/derived/SN_1310_0.npz
python scripts/process_month.py 1310 1             # EW  -> data/derived/SN_1310_1.npz
python scripts/verify_against_granada.py 1310 0    # optional, needs the Digibug npz in data/granada/
python scripts/build_viewer.py 1310                # -> viewer/index.html (+ viewer/artifact.html)
python -m pytest -q tests                          # synthetic checks on the chain
```

固定方法（镜像站点链，以便可以进行验证）：10 秒 Hann 窗口，50% 重叠，零填充 FFT 到 8192（31.25 mHz），丢弃饱和窗口，RLC 校准 `Scal(f) = 1e12/(2500·1.9e6) · sqrt((1-(f/f0)²)² + (2δf/f0)²) / f`，其中 L = 298 kH，C = 77.75 pF，R = 320 kΩ，人工频带直线滤波器，在 6.35–23.75 Hz 范围内，在幅度域中拟合三个洛伦兹函数和一个线性项。

## 标准合规性

根据工作室的六个工作流程标准，评分范围为 0–3。

| 标准 | 分数 | 证据 |
|---|---|---|
| PIN_PER_STEP | 2 | 每个数值选项（窗口、重叠、FFT 大小、校准常数、拟合带、种子）都是 `process_month.py` 顶部的命名常量，并写入 npz `method` 字段。目前尚不能在 NumPy 的不同版本之间进行字节级别的重放；没有库版本的记录。 |
| andon_authority | 2 | `verify_against_granada.py` 是与站点发布的拟合结果不一致时的停止点；提取脚本在写入之前会断言每个 zip 条目的解压后大小。 |
| named_compensators | 2 | 流水线中没有不可逆的外部调用。唯一的发布路径是对源代码进行 git 推送；`data/` 会被忽略。对于不正确的 `viewer/index.html`，可以从 npz 重新构建。 |
| decompose_by_secrets | 2 | 提取、处理、验证和构建是四个脚本，每个脚本执行一项任务；查看器模板不了解站点，并使用与站点无关的 JSON 块。 |
| uncertainty_gated_humans | 1 | 相关性面板显示空带，这是查看器的不确定性门限。流水线本身没有人工检查点。补救措施：使验证器针对声明的容差输出通过/失败结果（负责人：下一个会话）。 |
| external_verifier | 3 | 验证器是站点自己独立生成的输出（不同的代码、不同的作者，lmfit 与 SciPy）。表格中的数字。 |

## 信任与数据

流水线从检出代码库中本地运行。它仅在 `data/` 和 `viewer/` 下读取和写入。
网络访问仅在您要求脚本提取时发生：Zenodo（原始存档）、Digibug（站点的验证器文件）、GFZ（Kp）、USGS（地震）。上传数据集使用您自己的 Hugging Face 登录，该登录信息不在这些脚本之外。不读取或存储任何凭据，不发送任何遥测数据，并且查看器是一个静态页面，它从公共 CDN 加载 Three.js 和两种字体，除此之外没有其他内容。
要求：任何操作系统上，Python 3.11 或更高版本，以及 NumPy、SciPy 和 PyArrow；Node 仅用于可选的登录页面。

## 许可

代码采用 MIT 许可。派生数据产品需要按照其来源的要求进行署名。

---

<p align="center">Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a></p>
