# NuScale 基准题（OpenMC）

[![English](https://img.shields.io/badge/lang-en-blue.svg)](README.md)
[![简体中文](https://img.shields.io/badge/lang-zh--CN-green.svg)](README.zh-CN.md)

本仓库用于复现/对比 NuScale 基准题的部分结果：从参考 Excel 重新绘制论文图像、读取 OpenMC 输出（statepoint）并与参考解做相对误差分析。

---

## 目录结构

- `ref/`：参考输入（`01-Material_Compositions_v3.xlsx`、`02-Reference_Solution_v3.xlsx`、`Changelog.md`）
- `data/`：各工况 OpenMC 输出目录（由运行脚本生成，每个工况目录内包含 `statepoint.*.h5`）
- `figs/`：绘图输出（PNG）以及 `keff_summary.csv`
- `*.py`：
  - 运行：`1-core_run.py`（六个控制棒工况）、`1-core_run_single_RE1.py`（`RE1 at D5 in`）
  - 后处理：`2-plot_figs.py`、`3-read_keff.py`、`read_sp.py`、`4-error_cr.py`、`5-error_ref.py`
  - 模型模块：`constants.py`、`materials.py`、`pins.py`、`lat.py`、`core.py`

## 依赖环境

- Python 3
- `numpy`, `pandas`, `matplotlib`, `openpyxl`
- `openmc`（运行模拟与读取 `statepoint.*.h5` 均必需）

## 用法

### 1) 运行基准题工况（OpenMC）

- 六个控制棒配置：`python 1-core_run.py`
  - 工况：`All rods out (ARO)`、`RE1 in`、`RE2 in`、`SH3 in`、`SH4 in`、`All rods in (ARI)`
  - 每个工况在 `data/<case>/` 下运行，并在该目录内额外输出 `nuscale_core_<case>_xy.png` / `nuscale_core_<case>_xz.png`
- `RE1 at D5 in`（单根控制棒插入 D5 位置）：`python 1-core_run_single_RE1.py`
- 截面库路径在运行脚本内设置（`openmc.config['cross_sections']`），运行前请改为本机路径

### 2) 从 Excel 重新绘制论文图像

- 脚本：`python 2-plot_figs.py`
- 读取 `ref/02-Reference_Solution_v3.xlsx`，输出 `figs/fig9-rppf_heatmap.png`（Fig.9）、`figs/fig10-pow_ax.png`（Fig.10）、`figs/fig11-pinpower-ref.png`（Fig.11）

### 3) 读取 keff 并计算相对误差

- 脚本：`python 3-read_keff.py`
- 功能：遍历 `data/<case>/statepoint.*.h5`（自动选编号最大的 statepoint），从 `ref/02-Reference_Solution_v3.xlsx` 的 `k-eff + CRW` 表读取 `k-eff`，输出对齐表格并计算 `rel_err(%)`，同时写入 `figs/keff_summary.csv`

### 4) 从 statepoint 读取功率 tally 并绘图（rad/pin/ax）

- 脚本：`python read_sp.py`
- statepoint 文件名在脚本内写死（`statepoint.300.h5`），请改为需要查看的工况
- 输出：`1-rad_pow.png`、`2-pin_pow.png`、`3-ax_pow.png`

### 5) 相对误差图（Fig.9 / Fig.10 / Fig.11）

- Reference（ARO）工况：`python 5-error_ref.py`
  - 输出：`figs/err_fig9_ref.png`、`figs/err_fig10_ref.png`、`figs/err_fig11_ref.png`
- CR（`RE1 at D5 in`）工况：`python 4-error_cr.py`
  - 输出：`figs/err_fig9_cr.png`、`figs/err_fig11_cr.png`

相对误差定义：`(calc - ref) / ref * 100%`（`ref` 为 NaN/0 的位置会被屏蔽不绘制）。

---

## 01 图像示例

**Fig.9：径向组件功率分布（Ref/CR）**

![Fig9](./figs/fig9-rppf_heatmap.png)

**Fig.10：轴向功率分布**

![Fig10](./figs/fig10-pow_ax.png)

**Fig.11：燃料棒功率分布（Ref/CR）**

![Fig11](./figs/fig11-pinpower-ref.png)

---

## 02 tally

```
case                k-eff    k-eff STD  ref_k-eff  ref STD  rel_err(%)
------------------  -------  ---------  ---------  -------  ----------
All rods out (ARO)  1.02799  0.00021    1.02768    0.00001  0.02998   
RE1 in              1.00699  0.00020    1.00723    0.00001  -0.02348  
RE2 in              1.00354  0.00020    1.00313    0.00001  0.04085   
SH3 in              0.98972  0.00020    0.98978    0.00001  -0.00521  
SH4 in              0.98991  0.00019    0.98971    0.00001  0.02054   
All rods in (ARI)   0.85824  0.00019    0.85791    0.00002  0.03821   
RE1 at D5 in        1.02256  0.00021    1.02207    0.00001  0.04817 
```

---

## 03 ERROR 相对误差

**Reference 相对误差（Fig.9 / Fig.10 / Fig.11）**
<div align="center">
  <img src="figs/err_fig9_ref.png" width="48%" alt="fig9" />
  <img src="figs/err_fig11_ref.png" width="48%" alt="fig11" />
</div>
![Fig10](figs/err_fig10_ref.png)

**CR（`RE1 at D5 in`）相对误差（Fig.9 / Fig.10 / Fig.11）**
<div align="center">
  <img src="./figs/err_fig9_cr.png" width="48%" alt="fig9" />
  <img src="./figs/err_fig11_cr.png" width="48%" alt="fig11" />
</div>

---

## 问题

figs中绘图的相对误差达到5%, 可能是由于以下原因：
+ 对于混合材料是否还需添加`add_s_alpha_beta('c_H_in_H2O')`
+ 原文对控制棒全提情况下B4C与AIC材料的分布高度描述不清晰
+ 软件不同，Serpent属于不开源软件，无法详细对比代码差异

## 参考文献

Fridman, Emil, Yurii Bilodid, and Ville Valtavirta. 2023. "Definition of the Neutronics Benchmark of the NuScale-like Core." *Nuclear Engineering and Technology* 55 (10): 3639–47. doi:[10.1016/j.net.2023.06.029](https://doi.org/10.1016/j.net.2023.06.029).
