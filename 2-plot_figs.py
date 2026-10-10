import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.ticker import ScalarFormatter

_BASENAME = os.path.dirname(os.path.abspath(__file__))

# ──────────────────────────── fig9: rppf heatmap ────────────────────────────
xlsx_path = os.path.join(_BASENAME, "./ref/02-Reference_Solution_v3.xlsx")
out_png   = os.path.join(_BASENAME, "./figs/fig9-rppf_heatmap.png")

df_ref = pd.read_excel(xlsx_path, sheet_name="rad_pow_ref",
                        header=None, usecols="A:G", nrows=7)
df_cr  = pd.read_excel(xlsx_path, sheet_name="rad_pow_CR",
                        header=None, usecols="A:G", nrows=7)

mat_ref = df_ref.to_numpy(dtype=float)
mat_cr  = df_cr.to_numpy(dtype=float)

vmin_ref = float(np.nanmin(mat_ref));  vmax_ref = float(np.nanmax(mat_ref))
vmin_cr  = float(np.nanmin(mat_cr));   vmax_cr  = float(np.nanmax(mat_cr))

fig, axes = plt.subplots(1, 2, figsize=(12, 5), constrained_layout=True)
masked_ref = np.ma.masked_invalid(mat_ref)
masked_cr  = np.ma.masked_invalid(mat_cr)

im0 = axes[0].imshow(masked_ref, cmap="jet", vmin=vmin_ref, vmax=vmax_ref,
                      interpolation="nearest")
im1 = axes[1].imshow(masked_cr, cmap="jet", vmin=vmin_cr, vmax=vmax_cr,
                      interpolation="nearest")

axes[0].set_title("Ref state (all rods out)")
axes[1].set_title("Single RE1 CR")
for ax in axes:
    ax.set_xticks([]); ax.set_yticks([])

cmap = plt.get_cmap("jet")
den_ref = vmax_ref - vmin_ref or 1.0
den_cr  = vmax_cr  - vmin_cr  or 1.0

for i in range(mat_ref.shape[0]):
    for j in range(mat_ref.shape[1]):
        v = mat_ref[i, j]
        if np.isfinite(v):
            c = cmap((v - vmin_ref) / den_ref)
            lum = 0.2126*c[0] + 0.7152*c[1] + 0.0722*c[2]
            axes[0].text(j, i, f"{v:.3f}", ha="center", va="center",
                         fontsize=9, color="black" if lum > 0.6 else "white")

for i in range(mat_cr.shape[0]):
    for j in range(mat_cr.shape[1]):
        v = mat_cr[i, j]
        if np.isfinite(v):
            c = cmap((v - vmin_cr) / den_cr)
            lum = 0.2126*c[0] + 0.7152*c[1] + 0.0722*c[2]
            axes[1].text(j, i, f"{v:.3f}", ha="center", va="center",
                         fontsize=9, color="black" if lum > 0.6 else "white")

fig.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)
fig.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)
fig.savefig(out_png, dpi=200); plt.close(fig)
print(out_png)


# ──────────────────────────── fig10: pow_ax ─────────────────────────────────
out_png   = os.path.join(_BASENAME, "./figs/fig10-pow_ax.png")

df = pd.read_excel(xlsx_path, sheet_name="pow_ax")

lower  = pd.to_numeric(df["Lower boundary, cm"], errors="coerce")
upper  = pd.to_numeric(df["Upper boundary, cm"], errors="coerce")
power  = pd.to_numeric(df["Power, MW"], errors="coerce")

data = pd.DataFrame({"lower": lower, "upper": upper, "power": power}).dropna()
data = data.sort_values(["lower", "upper"]).reset_index(drop=True)
print(data)

x, y = [], []
for _, r in data.iterrows():
    x.extend([float(r["lower"]), float(r["upper"])])
    y.extend([float(r["power"]),  float(r["power"])])

y_max = float(data["power"].max()) if data["power"].notna().any() else 1.0
y_min = 0.0
y_pad = 0.5

fig = plt.figure(figsize=(12, 6))
plt.plot(x, y, color="blue", linewidth=2.0)

x_grid = [14.92, 19.365, 65.974, 70.419,
           117.028, 121.473, 168.082, 172.527]
plt.vlines(x_grid, ymin=y_min, ymax=y_max + y_pad,
           colors="red", linestyles=(0, (6, 4)),
           linewidth=1.5, label="Spacer grid")

plt.xlabel("Height (cm)")
plt.ylabel("Power (MW)")
plt.xlim(float(data["lower"].min()), float(data["upper"].max()))
plt.ylim(y_min, y_max + y_pad)
plt.grid(True, alpha=0.5)
plt.legend(loc="upper right")
fig.savefig(out_png, dpi=200); plt.close(fig)
print(out_png)


# ──────────────────────────── fig11: pin-power ──────────────────────────────
out_png   = os.path.join(_BASENAME, "./figs/fig11-pinpower-ref.png")

df_ref = pd.read_excel(xlsx_path, sheet_name="pin_pow_ref",
                        header=None, usecols="B:DP", nrows=119)
df_CR  = pd.read_excel(xlsx_path, sheet_name="pin_pow_CR",
                        header=None, usecols="B:DP", nrows=119)

mat_ref = df_ref.to_numpy(dtype=float)
mat_cr  = df_CR.to_numpy(dtype=float)

masked_ref = np.ma.masked_invalid(mat_ref)
masked_cr  = np.ma.masked_invalid(mat_cr)

vmin_ref = float(np.nanmin(mat_ref));  vmax_ref = float(np.nanmax(mat_ref))
vmin_cr  = float(np.nanmin(mat_cr));   vmax_cr  = float(np.nanmax(mat_cr))

fig, axes = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)

im0 = axes[0].imshow(masked_ref, cmap="jet", vmin=vmin_ref, vmax=vmax_ref,
                      interpolation="nearest")
im1 = axes[1].imshow(masked_cr, cmap="jet", vmin=vmin_cr, vmax=vmax_cr,
                      interpolation="nearest")

for ax in axes:
    ax.set_xticks([]); ax.set_yticks([]); ax.set_aspect("equal")

axes[0].set_title("Reference state (all rods out)",       y=-0.08)
axes[1].set_title("Asymmetric insertion of a single RE1 CR at D5", y=-0.08)

cb0 = fig.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)
fmt0 = ScalarFormatter(useMathText=True); fmt0.set_powerlimits((4, 4))
cb0.formatter = fmt0; cb0.update_ticks()

cb1 = fig.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)
fmt1 = ScalarFormatter(useMathText=True); fmt1.set_powerlimits((4, 4))
cb1.formatter = fmt1; cb1.update_ticks()

fig.savefig(out_png, dpi=200); plt.close(fig)
print(out_png)