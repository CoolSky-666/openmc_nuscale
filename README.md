# NuScale Benchmark (OpenMC)

[![English](https://img.shields.io/badge/lang-en-blue.svg)](README.md)
[![简体中文](https://img.shields.io/badge/lang-zh--CN-green.svg)](README.zh-CN.md)

This repository helps reproduce/compare selected results of the NuScale benchmark: re-plot paper figures from the reference Excel, read OpenMC statepoints, and compute relative errors against the reference solution.

---

## Project Layout

- `ref/`: reference inputs (`01-Material_Compositions_v3.xlsx`, `02-Reference_Solution_v3.xlsx`, `Changelog.md`)
- `data/`: OpenMC outputs per case (created by the run scripts; each case folder contains `statepoint.*.h5`)
- `figs/`: generated figures (PNG) and `keff_summary.csv`
- `*.py`:
  - run: `1-core_run.py` (six control-rod cases), `1-core_run_single_RE1.py` (`RE1 at D5 in`)
  - post-processing: `2-plot_figs.py`, `3-read_keff.py`, `read_sp.py`, `4-error_cr.py`, `5-error_ref.py`
  - model modules: `constants.py`, `materials.py`, `pins.py`, `lat.py`, `core.py`

## Requirements

- Python 3
- `numpy`, `pandas`, `matplotlib`, `openpyxl`
- `openmc` (required for both running the simulations and reading `statepoint.*.h5`)

## Usage

### 1) Run the benchmark cases (OpenMC)

- All six control-rod configurations: `python 1-core_run.py`
  - Cases: `All rods out (ARO)`, `RE1 in`, `RE2 in`, `SH3 in`, `SH4 in`, `All rods in (ARI)`
  - Each case runs in `data/<case>/` and additionally writes `nuscale_core_<case>_xy.png` / `nuscale_core_<case>_xz.png` there.
- `RE1 at D5 in` (single rod inserted at position D5): `python 1-core_run_single_RE1.py`
- The cross sections path is set inside the run scripts (`openmc.config['cross_sections']`); adjust it to your local installation before running.

### 2) Re-plot paper figures from the reference Excel

- Script: `python 2-plot_figs.py`
- Reads `ref/02-Reference_Solution_v3.xlsx` and writes `figs/fig9-rppf_heatmap.png` (Fig.9), `figs/fig10-pow_ax.png` (Fig.10) and `figs/fig11-pinpower-ref.png` (Fig.11).

### 3) Read keff and compute relative error vs. reference

- Script: `python 3-read_keff.py`
- It scans `data/<case>/statepoint.*.h5` (picks the largest statepoint index), reads `k-eff` from `ref/02-Reference_Solution_v3.xlsx` (`k-eff + CRW` sheet), prints an aligned table, computes `rel_err(%)` and writes `figs/keff_summary.csv`.

### 4) Read tallies from statepoint and plot (rad/pin/ax)

- Script: `python read_sp.py`
- The statepoint file is hard-coded in the script (`statepoint.300.h5`); point it to the case you want to inspect.
- Outputs: `1-rad_pow.png`, `2-pin_pow.png`, `3-ax_pow.png`.

### 5) Relative error plots (Fig.9 / Fig.10 / Fig.11)

- Reference (ARO): `python 5-error_ref.py`
  - Outputs: `figs/err_fig9_ref.png`, `figs/err_fig10_ref.png`, `figs/err_fig11_ref.png`
- CR (`RE1 at D5 in`): `python 4-error_cr.py`
  - Outputs: `figs/err_fig9_cr.png`, `figs/err_fig11_cr.png`

Relative error definition: `(calc - ref) / ref * 100%` (cells with NaN/0 reference are masked).

---

## 01 Figure Examples

**Fig.9: Radial Assembly Power Distribution (Ref/CR)**

![Fig9](./figs/fig9-rppf_heatmap.png)

**Fig.10: Axial Power Distribution**

![Fig10](./figs/fig10-pow_ax.png)

**Fig.11: Pin Power Distribution (Ref/CR)**

![Fig11](./figs/fig11-pinpower-ref.png)

---

## 02 Tally

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

## 03 Relative Error

**Reference Relative Error (Fig.9 / Fig.10 / Fig.11)**
<div align="center">
  <img src="figs/err_fig9_ref.png" width="48%" alt="fig9" />
  <img src="figs/err_fig11_ref.png" width="48%" alt="fig11" />
</div>
![Fig10](figs/err_fig10_ref.png)

**CR (`RE1 at D5 in`) Relative Error (Fig.9 / Fig.10 / Fig.11)**
<div align="center">
  <img src="./figs/err_fig9_cr.png" width="48%" alt="fig9" />
  <img src="./figs/err_fig11_cr.png" width="48%" alt="fig11" />
</div>

---
