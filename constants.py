import math

# ============================================================
# 1. Materials and run parameters
# ============================================================

power = 160e6 # W
fuel_temperature = 900 # K
coolant_temperature = 600 # K
structure_temperature = 600 # K

# ============================================================
# 2. Pin radius parameters
# ============================================================
    
fuel_OR = 0.4058
fuel_clad_IR = 0.4140
fuel_clad_OR = 0.4750
spring_OR = 0.0646

gt_clad_IR = 0.5715
gt_clad_OR = 0.6121

cr_aic_OR = 0.4267
cr_clad_IR = 0.4369
cr_clad_OR = 0.4839
cr_b4c_OR = 0.4229

barrel_IR = 93.9800
barrel_OR = 99.0600

# ============================================================
# 3. Axial parameters
# ============================================================

bot_Z = 0.000
bot_nozzle_top_Z = 10.160
bot_endcap_top_Z = 11.365
cr_endplug_bot_Z = 18.546
cr_endplug_top_Z = 23.405
cr_aic_top_Z = 53.885
cr_endplug_up_Z = 206.506
fuel_top_Z = 211.365
spring_top_Z = 224.855
top_endcap_top_Z = 226.06
top_nozzle_bot_Z = 234.541
top_Z = 243.561

grid1_bot_Z = 14.920
grid1_top_Z = 19.365
grid2_bot_Z = 65.974
grid2_top_Z = 70.419
grid3_bot_Z = 117.028
grid3_top_Z = 121.473
grid4_bot_Z = 168.082
grid4_top_Z = 172.527
grid5_bot_Z = 219.136
grid5_top_Z = 223.581

# ============================================================
# 4. Lattice parameters
# ============================================================

pin_Pitch = 1.2598
grid_Pitch = 1.2242
lat_Pitch = 21.5036