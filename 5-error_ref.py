import re
from pathlib import Path
import openmc
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

_BASENAME = os.path.dirname(os.path.abspath(__file__))

xlsx_path  = Path(_BASENAME) / "ref"  / "02-Reference_Solution_v3.xlsx"
state_dir  = Path(_BASENAME) / "data" / "All rods out (ARO)"
out_fig9   = Path(_BASENAME) / "figs" / "err_fig9_ref.png"
out_fig10  = Path(_BASENAME) / "figs" / "err_fig10_ref.png"
out_fig11  = Path(_BASENAME) / "figs" / "err_fig11_ref.png"

sp_files = list(state_dir.glob("statepoint.300.h5"))
parsed = []
for p in sp_files:
    m = re.match(r"statepoint\.(\d+)\.h5$", p.name)
    if m:
        parsed.append((int(m.group(1)), p))
if parsed:
    state_path = max(parsed, key=lambda x: x[0])[1]
else:
    state_path = max(sp_files, key=lambda p: p.stat().st_mtime)

df_rad_ref = pd.read_excel(xlsx_path, sheet_name="rad_pow_ref", header=None, usecols="A:G", nrows=7)
rad_ref = df_rad_ref.to_numpy(dtype=float)

df_pin_ref = pd.read_excel(xlsx_path, sheet_name="pin_pow_ref", header=None, usecols="B:DP", nrows=119)
pin_ref = df_pin_ref.to_numpy(dtype=float)

df_ax = pd.read_excel(xlsx_path, sheet_name="pow_ax")
lower = pd.to_numeric(df_ax["Lower boundary, cm"], errors="coerce")
upper = pd.to_numeric(df_ax["Upper boundary, cm"], errors="coerce")
ax_ref = pd.to_numeric(df_ax["Power, MW"], errors="coerce")
ax_data = pd.DataFrame({"lower": lower, "upper": upper, "power": ax_ref}).dropna()
ax_data = ax_data.sort_values(["lower", "upper"]).reset_index(drop=True)
ax_ref = ax_data["power"].to_numpy(dtype=float)[:21]
z_lower = ax_data["lower"].to_numpy(dtype=float)[:21]
z_upper = ax_data["upper"].to_numpy(dtype=float)[:21]
z_bound = np.concatenate([z_lower[:1], z_upper])

power_w = 160e6
with openmc.StatePoint(str(state_path)) as sp:
    t1 = sp.get_tally(name="as_pow")
    t2 = sp.get_tally(name="pin_pow")
    t3 = sp.get_tally(name="pow_ax")

    rad_calc = (t1.mean * 37.0 / np.sum(t1.mean)).reshape((7, 7))[::-1]
    pin_calc = (t2.mean * power_w / np.sum(t2.mean)).reshape((7 * 17, 7 * 17))[::-1]
    ax_calc = (t3.mean * 160.0 / np.sum(t3.mean)).reshape((-1,))[:21]

rad_calc[rad_calc == 0] = np.nan
pin_calc[pin_calc == 0] = np.nan

variants = []
for k in range(4):
    r = np.rot90(rad_calc, k=k)
    variants.append(r)
    variants.append(np.flipud(r))
scores = []
for v in variants:
    m = np.isfinite(v) & np.isfinite(rad_ref) & (rad_ref != 0)
    if np.any(m):
        scores.append(float(np.nanmean(np.abs((v[m] - rad_ref[m]) / rad_ref[m]))))
    else:
        scores.append(float("inf"))
rad_best = variants[int(np.argmin(scores))]

variants = []
for k in range(4):
    r = np.rot90(pin_calc, k=k)
    variants.append(r)
    variants.append(np.flipud(r))
scores = []
for v in variants:
    m = np.isfinite(v) & np.isfinite(pin_ref) & (pin_ref != 0)
    if np.any(m):
        scores.append(float(np.nanmean(np.abs((v[m] - pin_ref[m]) / pin_ref[m]))))
    else:
        scores.append(float("inf"))
pin_best = variants[int(np.argmin(scores))]

rad_err = (rad_best - rad_ref) / rad_ref * 100.0
rad_err[~np.isfinite(rad_ref) | (rad_ref == 0)] = np.nan

pin_err = (pin_best - pin_ref) / pin_ref * 100.0
pin_err[~np.isfinite(pin_ref) | (pin_ref == 0)] = np.nan

ax_err = (ax_calc - ax_ref) / ax_ref * 100.0
ax_err[~np.isfinite(ax_ref) | (ax_ref == 0)] = np.nan

masked = np.ma.masked_invalid(rad_err)
vmax = float(np.nanpercentile(np.abs(rad_err), 99)) if np.any(np.isfinite(rad_err)) else 1.0
fig, ax = plt.subplots(figsize=(8, 7), constrained_layout=True)
im = ax.imshow(masked, cmap="coolwarm", vmin=-vmax, vmax=vmax, interpolation="nearest")
ax.set_xticks(np.arange(7))
ax.set_yticks(np.arange(7))
ax.set_xticklabels(list("ABCDEFG"))
ax.set_yticklabels(list("1234567"))
ax.tick_params(axis="x", which="both", length=0)
ax.tick_params(axis="y", which="both", length=0)
for i in range(7):
    for j in range(7):
        v = rad_err[i, j]
        if np.isfinite(v):
            ax.text(j, i, f"{v:.3f}", ha="center", va="center", fontsize=10)
cb = fig.colorbar(im, ax=ax)
cb.set_label("Relative error (%)")
out_fig9.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out_fig9, dpi=200)
plt.close(fig)

masked = np.ma.masked_invalid(pin_err)
vmax = float(np.nanpercentile(np.abs(pin_err), 99)) if np.any(np.isfinite(pin_err)) else 1.0
fig, ax = plt.subplots(figsize=(7.5, 7.2), constrained_layout=True)
im = ax.imshow(masked, cmap="coolwarm", vmin=-vmax, vmax=vmax, interpolation="nearest")
ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect("equal")
for k in range(0, 119 + 1, 17):
    ax.axhline(k - 0.5, color="white", linewidth=1.0, alpha=0.6)
    ax.axvline(k - 0.5, color="white", linewidth=1.0, alpha=0.6)
cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cb.set_label("Relative error (%)")
out_fig11.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out_fig11, dpi=200)
plt.close(fig)

err_step = np.append(ax_err, ax_err[-1])
fig = plt.figure(figsize=(12, 5))
plt.step(z_bound, err_step, where="post", linewidth=2.0, color="blue")
plt.axhline(0.0, color="black", linewidth=1.0)
plt.xlabel("Height (cm)")
plt.ylabel("Relative error (%)")
plt.grid(True, alpha=0.35)
plt.xlim(float(z_bound.min()), float(z_bound.max()))
plt.savefig(out_fig10, dpi=200)
plt.close(fig)
