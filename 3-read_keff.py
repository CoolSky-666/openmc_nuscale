import openmc
import re
import os
import csv
from pathlib import Path
import pandas as pd

_BASENAME = os.path.dirname(os.path.abspath(__file__))

ref_xlsx = os.path.join(_BASENAME, "ref", "02-Reference_Solution_v3.xlsx")
df_ref = pd.read_excel(ref_xlsx, sheet_name="k-eff + CRW")
df_ref = df_ref[["Unnamed: 0", "k-eff", "STD"]].dropna(subset=["k-eff"])
ref_map = {}
for _, r in df_ref.iterrows():
    key = str(r["Unnamed: 0"])
    ref_map[key] = {
        "keff": float(r["k-eff"]),
        "std":  float(r["STD"]) if pd.notna(r["STD"]) else None,
    }

run_dirs = [
    Path(_BASENAME) / "data" / "All rods out (ARO)",
    Path(_BASENAME) / "data" / "RE1 in",
    Path(_BASENAME) / "data" / "RE2 in",
    Path(_BASENAME) / "data" / "SH3 in",
    Path(_BASENAME) / "data" / "SH4 in",
    Path(_BASENAME) / "data" / "All rods in (ARI)",
    Path(_BASENAME) / "data" / "RE1 at D5 in",
]

# 删除 statepoint 列
headers = ["case", "k-eff", "k-eff STD",
           "ref_k-eff", "ref STD", "rel_err(%)"]
rows = []

for d in run_dirs:
    case_label = d.name  # 直接用文件夹名

    files = list(d.glob("statepoint.*.h5"))
    if not files:
        rows.append([case_label, "N/A", "N/A", "N/A", "N/A", "N/A"])
        continue

    parsed = []
    for p in files:
        m = re.match(r"statepoint\.(\d+)\.h5$", p.name)
        if m:
            parsed.append((int(m.group(1)), p))

    if parsed:
        sp_path = max(parsed, key=lambda x: x[0])[1]
    else:
        sp_path = max(files, key=lambda p: p.stat().st_mtime)

    ref_entry = ref_map.get(case_label, {})

    with openmc.StatePoint(str(sp_path)) as sp:
        k    = float(sp.keff.n)
        std  = float(sp.keff.s)

    ref_keff = ref_entry.get("keff")
    ref_std  = ref_entry.get("std")

    if ref_keff is None or ref_keff == 0:
        rel_err = None
    else:
        rel_err = (k - ref_keff) / ref_keff * 100.0

    k_str    = f"{k:.5f}"
    std_str  = f"{std:.5f}"
    ref_str  = f"{ref_keff:.5f}" if ref_keff is not None else "N/A"
    ref_std_str = f"{ref_std:.5f}" if ref_std is not None else "N/A"
    err_str  = f"{rel_err:.5f}" if rel_err is not None else "N/A"

    rows.append([case_label, k_str, std_str, ref_str, ref_std_str, err_str])

# 终端打印表格
widths = [max(len(h), *(len(r[i]) for r in rows)) for i, h in enumerate(headers)]
fmt = "  ".join([f"{{:<{w}}}" for w in widths])
print(fmt.format(*headers))
print(fmt.format(*["-" * w for w in widths]))
for r in rows:
    print(fmt.format(*r))

# 写入 figs 文件夹下的自定义 csv 文件
out_dir = Path(_BASENAME) / "figs"
out_dir.mkdir(parents=True, exist_ok=True)
out_csv = out_dir / "keff_summary.csv"   # 自定义文件名，按需修改

with open(out_csv, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

print(f"\nCSV 已写入: {out_csv}")