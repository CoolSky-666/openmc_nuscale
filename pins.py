import openmc
import constants as c
from materials import build_mats
import matplotlib.pyplot as plt

# ============================================================
# Pin radius surfaces
# ============================================================

s_fuel_OR = openmc.ZCylinder(r=c.fuel_OR, name='fuel_OR')
s_fuel_clad_IR = openmc.ZCylinder(r=c.fuel_clad_IR, name='fuel_clad_IR')
s_fuel_clad_OR = openmc.ZCylinder(r=c.fuel_clad_OR, name='fuel_clad_OR')
s_spring_OR = openmc.ZCylinder(r=c.spring_OR, name='spring_OR')

s_grid = openmc.model.RectangularPrism(width=c.grid_Pitch,height=c.grid_Pitch,axis='z')
s_pin = openmc.model.RectangularPrism(width=c.pin_Pitch,height=c.pin_Pitch,axis='z')

s_bot_Z = openmc.ZPlane(z0=c.bot_Z, name='bot_Z', boundary_type='vacuum')
s_bot_nozzle_top_Z = openmc.ZPlane(z0=c.bot_nozzle_top_Z, name='bot_nozzle_top_Z')
s_bot_endcap_top_Z = openmc.ZPlane(z0=c.bot_endcap_top_Z, name='bot_endcap_top_Z')
s_cr_endplug_bot_Z = openmc.ZPlane(z0=c.cr_endplug_bot_Z, name='cr_endplug_bot_Z')
s_cr_endplug_top_Z = openmc.ZPlane(z0=c.cr_endplug_top_Z, name='cr_endplug_top_Z')
s_cr_aic_top_Z = openmc.ZPlane(z0=c.cr_aic_top_Z, name='cr_aic_top_Z')
s_cr_endplug_up_Z = openmc.ZPlane(z0=c.cr_endplug_up_Z, name='cr_endplug_up_Z')
s_fuel_top_Z = openmc.ZPlane(z0=c.fuel_top_Z, name='fuel_top_Z') # 211.365
s_spring_top_Z = openmc.ZPlane(z0=c.spring_top_Z, name='spring_top_Z')
s_top_endcap_top_Z = openmc.ZPlane(z0=c.top_endcap_top_Z, name='top_endcap_top_Z')
s_top_nozzle_bot_Z = openmc.ZPlane(z0=c.top_nozzle_bot_Z, name='top_nozzle_bot_Z')
s_top_Z = openmc.ZPlane(z0=c.top_Z, name='top_Z', boundary_type='vacuum')

s_grid1_bot_Z = openmc.ZPlane(z0=c.grid1_bot_Z, name='grid1_bot_Z')
s_grid1_top_Z = openmc.ZPlane(z0=c.grid1_top_Z, name='grid1_top_Z')

s_grid2_bot_Z = openmc.ZPlane(z0=c.grid2_bot_Z, name='grid2_bot_Z')
s_grid2_top_Z = openmc.ZPlane(z0=c.grid2_top_Z, name='grid2_top_Z')

s_grid3_bot_Z = openmc.ZPlane(z0=c.grid3_bot_Z, name='grid3_bot_Z')
s_grid3_top_Z = openmc.ZPlane(z0=c.grid3_top_Z, name='grid3_top_Z')

s_grid4_bot_Z = openmc.ZPlane(z0=c.grid4_bot_Z, name='grid4_bot_Z')
s_grid4_top_Z = openmc.ZPlane(z0=c.grid4_top_Z, name='grid4_top_Z')

s_grid5_bot_Z = openmc.ZPlane(z0=c.grid5_bot_Z, name='grid5_bot_Z')
s_grid5_top_Z = openmc.ZPlane(z0=c.grid5_top_Z, name='grid5_top_Z')

def build_fuel_pin(fuel_name="uo2 A1",mats={}):
    u_fuel = openmc.Universe(name=f'fuel_active_{fuel_name}')
    c_f1 = openmc.Cell(fill=mats[fuel_name],    region=-s_fuel_OR)
    c_f2 = openmc.Cell(fill=mats['Helium'],     region=+s_fuel_OR & -s_fuel_clad_IR)
    c_f3 = openmc.Cell(fill=mats['Zr-4'],       region=+s_fuel_clad_IR & -s_fuel_clad_OR)
    u_fuel.add_cells([c_f1, c_f2, c_f3])

    u_fuel_endcap = openmc.Universe(name=f'fuel_endcap_{fuel_name}')
    c_f4 = openmc.Cell(fill=mats['Zr-4'],       region=-s_fuel_clad_OR)
    u_fuel_endcap.add_cells([c_f4])

    u_fuel_spring = openmc.Universe(name=f'fuel_spring_{fuel_name}')
    c_f5 = openmc.Cell(fill=mats['Inconel'],    region=-s_spring_OR)
    c_f6 = openmc.Cell(fill=mats['Helium'],     region=+s_spring_OR & -s_fuel_clad_IR)
    c_f7 = openmc.Cell(fill=mats['Zr-4'],       region=+s_fuel_clad_IR & -s_fuel_clad_OR)
    u_fuel_spring.add_cells([c_f5, c_f6, c_f7])

    u_fuel_grid_htp = openmc.Universe(name='fuel_outer_grid_htp')
    c_fg1 = openmc.Cell(fill=mats["H2O + 1000 ppm boron"], region=+s_fuel_clad_OR & -s_grid)
    c_fg2 = openmc.Cell(fill=mats["Zr-4"],   region=+s_grid & -s_pin)
    u_fuel_grid_htp.add_cells([c_fg1, c_fg2])

    u_fuel_grid_hmp = openmc.Universe(name='fuel_outer_grid_hmp')
    c_fg3 = openmc.Cell(fill=mats["H2O + 1000 ppm boron"], region=+s_fuel_clad_OR & -s_grid)
    c_fg4 = openmc.Cell(fill=mats["Inconel"],   region=+s_grid & -s_pin)
    u_fuel_grid_hmp.add_cells([c_fg3, c_fg4])

    fuel_axial_segments = [
        # Bottom nozzle (0-10.160)
        (s_bot_Z,      s_bot_nozzle_top_Z,          mats['Bottom nozzle'],     mats['Bottom nozzle']),
        # Bottom endcap (10.160-11.365)
        (s_bot_nozzle_top_Z,  s_bot_endcap_top_Z,   u_fuel_endcap,             mats["H2O + 1000 ppm boron"]),
        
        # Active fuel (11.365-211.365)
        (s_bot_endcap_top_Z,  s_grid1_bot_Z,         u_fuel,             mats["H2O + 1000 ppm boron"]),
        # Grid 1
        (s_grid1_bot_Z,  s_grid1_top_Z,         u_fuel,             u_fuel_grid_hmp),
        (s_grid1_top_Z,  s_grid2_bot_Z,         u_fuel,             mats["H2O + 1000 ppm boron"]),
        # Grid 2
        (s_grid2_bot_Z,  s_grid2_top_Z,         u_fuel,             u_fuel_grid_htp),
        (s_grid2_top_Z,  s_grid3_bot_Z,         u_fuel,             mats["H2O + 1000 ppm boron"]),
        # Grid 3
        (s_grid3_bot_Z,  s_grid3_top_Z,         u_fuel,             u_fuel_grid_htp),
        (s_grid3_top_Z,  s_grid4_bot_Z,         u_fuel,             mats["H2O + 1000 ppm boron"]),
        # Grid 4
        (s_grid4_bot_Z,  s_grid4_top_Z,         u_fuel,             u_fuel_grid_htp),
        (s_grid4_top_Z,  s_fuel_top_Z,          u_fuel,             mats["H2O + 1000 ppm boron"]),
        
        # Plenum spring (211.365-224.855)
        (s_fuel_top_Z,      s_grid5_bot_Z,    u_fuel_spring,        mats["H2O + 1000 ppm boron"]),
        # Grid 5
        (s_grid5_bot_Z,  s_grid5_top_Z,    u_fuel_spring,           u_fuel_grid_htp),
        (s_grid5_top_Z,  s_spring_top_Z,    u_fuel_spring,          mats["H2O + 1000 ppm boron"]),

        # Top endcap (224.855-226.06)
        (s_spring_top_Z,  s_top_endcap_top_Z,    u_fuel_endcap,             mats["H2O + 1000 ppm boron"]),
        # Coolant (226.060-234.541)
        (s_top_endcap_top_Z,  s_top_nozzle_bot_Z,    mats["H2O + 1000 ppm boron"],  mats["H2O + 1000 ppm boron"]),
        # Top nozzle (234.541-243.561)
        (s_top_nozzle_bot_Z,  s_top_Z,    mats['Top nozzle'],     mats['Top nozzle']),
    ]

    cells_fuel = []
    for i, (zbot, ztop, u_inner, u_outer) in enumerate(fuel_axial_segments):
        z_reg = -ztop & +zbot
        # Inner cell: everything inside the cladding outer radius
        if isinstance(u_inner, openmc.Material):
            c_in = openmc.Cell(fill=u_inner, region=(-s_fuel_clad_OR) & z_reg, name=f'fuel_seg{i}_inner_mat')
        else:
            c_in = openmc.Cell(fill=u_inner, region=(-s_fuel_clad_OR) & z_reg, name=f'fuel_seg{i}_inner_uni')
        # Outer cell: coolant + grid wrapper, bounded by rect_gridout (1.26 cm pitch)
        if isinstance(u_outer, openmc.Material):
            c_out = openmc.Cell(fill=u_outer, region=(+s_fuel_clad_OR) & z_reg & -s_pin, name=f'fuel_seg{i}_outer_mat')
        else:
            c_out = openmc.Cell(fill=u_outer, region=(+s_fuel_clad_OR) & z_reg & -s_pin, name=f'fuel_seg{i}_outer_uni')
        cells_fuel.append(c_in)
        cells_fuel.append(c_out)

    u_fuel_pin = openmc.Universe(name=f'full_fuel_pin_{fuel_name}')
    u_fuel_pin.add_cells(cells_fuel)
    return u_fuel_pin

s_gt_clad_IR = openmc.ZCylinder(r=c.gt_clad_IR, name='gt_clad_IR')
s_gt_clad_OR = openmc.ZCylinder(r=c.gt_clad_OR, name='gt_clad_OR')

def build_empty_gt_pin(mats):
    u_gt = openmc.Universe(name=f'empty_gt_pin')
    c_gt1 = openmc.Cell(fill=mats["H2O + 1000 ppm boron"],    region=-s_gt_clad_IR)
    c_gt2 = openmc.Cell(fill=mats['Zr-4'],       region=+s_gt_clad_IR & -s_gt_clad_OR)
    u_gt.add_cells([c_gt1, c_gt2])
    
    u_gt_grid_htp = openmc.Universe(name='gt_outer_grid_htp')
    c_gtg1 = openmc.Cell(fill=mats["H2O + 1000 ppm boron"], region=+s_gt_clad_OR & -s_grid)
    c_gtg2 = openmc.Cell(fill=mats["Zr-4"],   region=+s_grid & -s_pin)
    u_gt_grid_htp.add_cells([c_gtg1, c_gtg2])

    u_gt_grid_hmp = openmc.Universe(name='gt_outer_grid_hmp')
    c_gtg3 = openmc.Cell(fill=mats["H2O + 1000 ppm boron"], region=+s_gt_clad_OR & -s_grid)
    c_gtg4 = openmc.Cell(fill=mats["Inconel"],   region=+s_grid & -s_pin)
    u_gt_grid_hmp.add_cells([c_gtg3, c_gtg4])

    gt_axial_segments = [
        # Bottom nozzle (0-10.160)
        (s_bot_Z,      s_bot_nozzle_top_Z,          mats['Bottom nozzle'],     mats['Bottom nozzle']),
        # Empty guide tube (10.160-234.541)
        (s_bot_nozzle_top_Z, s_grid1_bot_Z,    u_gt,             mats["H2O + 1000 ppm boron"]),
        # Grid 1 (14.920-19.365)
        (s_grid1_bot_Z, s_grid1_top_Z,    u_gt,             u_gt_grid_hmp),
        (s_grid1_top_Z, s_grid2_bot_Z,    u_gt,             mats["H2O + 1000 ppm boron"]),
        # Grid 2 (65.974-70.419)
        (s_grid2_bot_Z, s_grid2_top_Z,    u_gt,             u_gt_grid_htp),
        (s_grid2_top_Z, s_grid3_bot_Z,    u_gt,             mats["H2O + 1000 ppm boron"]),
        # Grid 3 (117.028-121.473)
        (s_grid3_bot_Z, s_grid3_top_Z,    u_gt,             u_gt_grid_htp),
        (s_grid3_top_Z, s_grid4_bot_Z,    u_gt,             mats["H2O + 1000 ppm boron"]),
        # Grid 4 (168.082-172.527)
        (s_grid4_bot_Z, s_grid4_top_Z,    u_gt,             u_gt_grid_htp),
        (s_grid4_top_Z, s_grid5_bot_Z,    u_gt,             mats["H2O + 1000 ppm boron"]),
        # Grid 5 (219.136-223.581)
        (s_grid5_bot_Z, s_grid5_top_Z,    u_gt,             u_gt_grid_htp),
        (s_grid5_top_Z, s_top_nozzle_bot_Z,    u_gt,        mats["H2O + 1000 ppm boron"]),
        # Top nozzle (234.541-243.561)
        (s_top_nozzle_bot_Z,  s_top_Z,    mats['Top nozzle'],     mats['Top nozzle']),
    ]

    cells_gt = []
    for i, (zbot, ztop, u_inner, u_outer) in enumerate(gt_axial_segments):
        z_reg = -ztop & +zbot
        # Inner cell: everything inside the cladding outer radius
        if isinstance(u_inner, openmc.Material):
            c_in = openmc.Cell(fill=u_inner, region=(-s_gt_clad_OR) & z_reg, name=f'fuel_seg{i}_inner_mat')
        else:
            c_in = openmc.Cell(fill=u_inner, region=(-s_gt_clad_OR) & z_reg, name=f'fuel_seg{i}_inner_uni')
        # Outer cell: coolant + grid wrapper, bounded by rect_gridout (1.26 cm pitch)
        if isinstance(u_outer, openmc.Material):
            c_out = openmc.Cell(fill=u_outer, region=(+s_gt_clad_OR) & z_reg & -s_pin, name=f'fuel_seg{i}_outer_mat')
        else:
            c_out = openmc.Cell(fill=u_outer, region=(+s_gt_clad_OR) & z_reg & -s_pin, name=f'fuel_seg{i}_outer_uni')
        cells_gt.append(c_in)
        cells_gt.append(c_out)

    u_empty_gt_pin = openmc.Universe(name=f'full_empty_gt_pin')
    u_empty_gt_pin.add_cells(cells_gt)
    return u_empty_gt_pin

s_cr_aic_OR = openmc.ZCylinder(r=c.cr_aic_OR, name='cr_aic_OR')
s_cr_clad_IR = openmc.ZCylinder(r=c.cr_clad_IR, name='cr_clad_IR')
s_cr_clad_OR = openmc.ZCylinder(r=c.cr_clad_OR, name='cr_clad_OR')
s_cr_b4c_OR = openmc.ZCylinder(r=c.cr_b4c_OR, name='cr_b4c_OR')



def build_gtcr0_pin(mats={}):
    u_gt = openmc.Universe(name=f'empty_gt_pin')
    c_gt1 = openmc.Cell(fill=mats["H2O + 1000 ppm boron"],    region=-s_gt_clad_IR)
    c_gt2 = openmc.Cell(fill=mats['Zr-4'],       region=+s_gt_clad_IR & -s_gt_clad_OR)
    u_gt.add_cells([c_gt1, c_gt2])

    # u_inner
    # fig a. GT + CR AIC
    u_cr_aic_gt = openmc.Universe(name=f'cr_aic_gt')
    c_cr_aic_gt1 = openmc.Cell(fill=mats["AIC"],   region=-s_cr_aic_OR)
    c_cr_aic_gt2 = openmc.Cell(fill=mats['Helium'], region=+s_cr_aic_OR & -s_cr_clad_IR)
    c_cr_aic_gt3 = openmc.Cell(fill=mats['304L SS'],   region=+s_cr_clad_IR & -s_cr_clad_OR)
    c_cr_aic_gt4 = openmc.Cell(fill=mats["H2O + 1000 ppm boron"],    region=+s_cr_clad_OR & -s_gt_clad_IR)
    c_cr_aic_gt5 = openmc.Cell(fill=mats['Zr-4'],       region=+s_gt_clad_IR & -s_gt_clad_OR)
    u_cr_aic_gt.add_cells([c_cr_aic_gt1, c_cr_aic_gt2, c_cr_aic_gt3, c_cr_aic_gt4, c_cr_aic_gt5])

    # fig b. GT + CR B4C
    u_cr_b4c_gt = openmc.Universe(name=f'cr_b4c_gt')
    c_cr_b4c_gt1 = openmc.Cell(fill=mats["B4C"],    region=-s_cr_b4c_OR)
    c_cr_b4c_gt2 = openmc.Cell(fill=mats['Helium'], region=+s_cr_b4c_OR & -s_cr_clad_IR)
    c_cr_b4c_gt3 = openmc.Cell(fill=mats['304L SS'],   region=+s_cr_clad_IR & -s_cr_clad_OR)
    c_cr_b4c_gt4 = openmc.Cell(fill=mats["H2O + 1000 ppm boron"],    region=+s_cr_clad_OR & -s_gt_clad_IR)
    c_cr_b4c_gt5 = openmc.Cell(fill=mats['Zr-4'],       region=+s_gt_clad_IR & -s_gt_clad_OR)
    u_cr_b4c_gt.add_cells([c_cr_b4c_gt1, c_cr_b4c_gt2, c_cr_b4c_gt3, c_cr_b4c_gt4, c_cr_b4c_gt5])
     
    # fig c. GT + CR Plenum
    u_cr_plenum_gt = openmc.Universe(name=f'cr_plenum_gt')
    c_cr_plenum_gt1 = openmc.Cell(fill=mats['Helium'],  region=-s_cr_clad_IR)
    c_cr_plenum_gt2 = openmc.Cell(fill=mats['304L SS'], region=+s_cr_clad_IR & -s_cr_clad_OR)
    c_cr_plenum_gt3 = openmc.Cell(fill=mats["H2O + 1000 ppm boron"],    region=+s_cr_clad_OR & -s_gt_clad_IR)
    c_cr_plenum_gt4 = openmc.Cell(fill=mats['Zr-4'],       region=+s_gt_clad_IR & -s_gt_clad_OR)
    u_cr_plenum_gt.add_cells([c_cr_plenum_gt1, c_cr_plenum_gt2, c_cr_plenum_gt3, c_cr_plenum_gt4])
    
    # fig d. GT + CR end plug
    u_cr_endplug_gt = openmc.Universe(name=f'cr_endplug_gt')
    c_cr_endplug_gt1 = openmc.Cell(fill=mats['304L SS'],region= -s_cr_clad_OR)
    c_cr_endplug_gt2 = openmc.Cell(fill=mats["H2O + 1000 ppm boron"],    region=+s_cr_clad_OR & -s_gt_clad_IR)
    c_cr_endplug_gt3 = openmc.Cell(fill=mats['Zr-4'],       region=+s_gt_clad_IR & -s_gt_clad_OR)
    u_cr_endplug_gt.add_cells([c_cr_endplug_gt1, c_cr_endplug_gt2, c_cr_endplug_gt3])

    # u_outer
    u_gt_grid_htp = openmc.Universe(name='gt_outer_grid_htp')
    c_gtg1 = openmc.Cell(fill=mats["H2O + 1000 ppm boron"], region=+s_gt_clad_OR & -s_grid)
    c_gtg2 = openmc.Cell(fill=mats["Zr-4"],   region=+s_grid & -s_pin)
    u_gt_grid_htp.add_cells([c_gtg1, c_gtg2])

    u_gt_grid_hmp = openmc.Universe(name='gt_outer_grid_hmp')
    c_gtg3 = openmc.Cell(fill=mats["H2O + 1000 ppm boron"], region=+s_gt_clad_OR & -s_grid)
    c_gtg4 = openmc.Cell(fill=mats["Inconel"],   region=+s_grid & -s_pin)
    u_gt_grid_hmp.add_cells([c_gtg3, c_gtg4])

    cr_gt_axial_segments = [
        # Bottom nozzle (0-10.160)
        (s_bot_Z,      s_bot_nozzle_top_Z,          mats['Bottom nozzle'],     mats['Bottom nozzle']),
        
        # Empty Guide Tube (10.160-18.546)
        (s_bot_nozzle_top_Z, s_grid1_bot_Z,    u_gt,                      mats["H2O + 1000 ppm boron"]),
        # Grid 1 lower half
        (s_grid1_bot_Z, s_cr_endplug_bot_Z, u_gt, u_gt_grid_hmp),
        
        # End plug (18.546-23.405)
        # Grid 1 upper half
        (s_cr_endplug_bot_Z, s_grid1_top_Z,  u_cr_endplug_gt, u_gt_grid_hmp),
        (s_grid1_top_Z,s_cr_endplug_top_Z,     u_cr_endplug_gt ,mats["H2O + 1000 ppm boron"]),

        # AIC (23.405-53.885)
        (s_cr_endplug_top_Z,s_cr_aic_top_Z,         u_cr_aic_gt ,mats["H2O + 1000 ppm boron"]),

        # B4C (53.885-211.365)
        (s_cr_aic_top_Z,s_grid2_bot_Z, u_cr_b4c_gt, mats["H2O + 1000 ppm boron"]),
        (s_grid2_bot_Z, s_grid2_top_Z, u_cr_b4c_gt, u_gt_grid_htp),
        (s_grid2_top_Z, s_grid3_bot_Z, u_cr_b4c_gt, mats["H2O + 1000 ppm boron"]),
        (s_grid3_bot_Z, s_grid3_top_Z, u_cr_b4c_gt, u_gt_grid_htp),
        (s_grid3_top_Z, s_grid4_bot_Z, u_cr_b4c_gt, mats["H2O + 1000 ppm boron"]),
        (s_grid4_bot_Z, s_grid4_top_Z, u_cr_b4c_gt, u_gt_grid_htp),
        (s_grid4_top_Z, s_fuel_top_Z,  u_cr_b4c_gt, mats["H2O + 1000 ppm boron"]),

        # Upper plenum (211.365-234.541)
        (s_fuel_top_Z,s_grid5_bot_Z,           u_cr_plenum_gt ,mats["H2O + 1000 ppm boron"]),
        (s_grid5_bot_Z,s_grid5_top_Z,           u_cr_plenum_gt ,u_gt_grid_htp),
        (s_grid5_top_Z,s_top_nozzle_bot_Z,           u_cr_plenum_gt ,mats["H2O + 1000 ppm boron"]),
        # Top nozzle (234.541-243.561)
        (s_top_nozzle_bot_Z,  s_top_Z,              mats['Top nozzle'],     mats['Top nozzle']),
    ]

    cells_cr_gt = []
    for i, (zbot, ztop, u_inner, u_outer) in enumerate(cr_gt_axial_segments):
        z_reg = -ztop & +zbot
        # Inner cell: everything inside the cladding outer radius
        if isinstance(u_inner, openmc.Material):
            c_in = openmc.Cell(fill=u_inner, region=-s_gt_clad_OR & z_reg, name=f'fuel_seg{i}_inner_mat')
        else:
            c_in = openmc.Cell(fill=u_inner, region=-s_gt_clad_OR & z_reg, name=f'fuel_seg{i}_inner_uni')
        # Outer cell: coolant + grid wrapper, bounded by rect_gridout (1.26 cm pitch)
        if isinstance(u_outer, openmc.Material):
            c_out = openmc.Cell(fill=u_outer, region=(+s_gt_clad_OR) & z_reg & -s_pin, name=f'fuel_seg{i}_outer_mat')
        else:
            c_out = openmc.Cell(fill=u_outer, region=(+s_gt_clad_OR) & z_reg & -s_pin, name=f'fuel_seg{i}_outer_uni')
        cells_cr_gt.append(c_in)
        cells_cr_gt.append(c_out)

    u_cr_gt_pin = openmc.Universe(name=f'full_empty_cr_gt_pin')
    u_cr_gt_pin.add_cells(cells_cr_gt)
    return u_cr_gt_pin


def build_gtcr1_pin(mats={}):
    u_gt = openmc.Universe(name=f'empty_gt_pin')
    c_gt1 = openmc.Cell(fill=mats["H2O + 1000 ppm boron"],    region=-s_gt_clad_IR)
    c_gt2 = openmc.Cell(fill=mats['Zr-4'],       region=+s_gt_clad_IR & -s_gt_clad_OR)
    u_gt.add_cells([c_gt1, c_gt2])

    # u_inner
    # fig a. GT + CR AIC
    u_cr_aic_gt = openmc.Universe(name=f'cr_aic_gt')
    c_cr_aic_gt1 = openmc.Cell(fill=mats["AIC"],   region=-s_cr_aic_OR)
    c_cr_aic_gt2 = openmc.Cell(fill=mats['Helium'], region=+s_cr_aic_OR & -s_cr_clad_IR)
    c_cr_aic_gt3 = openmc.Cell(fill=mats['304L SS'],   region=+s_cr_clad_IR & -s_cr_clad_OR)
    c_cr_aic_gt4 = openmc.Cell(fill=mats["H2O + 1000 ppm boron"],    region=+s_cr_clad_OR & -s_gt_clad_IR)
    c_cr_aic_gt5 = openmc.Cell(fill=mats['Zr-4'],       region=+s_gt_clad_IR & -s_gt_clad_OR)
    u_cr_aic_gt.add_cells([c_cr_aic_gt1, c_cr_aic_gt2, c_cr_aic_gt3, c_cr_aic_gt4, c_cr_aic_gt5])
    
    # fig b. GT + CR B4C
    u_cr_b4c_gt = openmc.Universe(name=f'cr_b4c_gt')
    c_cr_b4c_gt1 = openmc.Cell(fill=mats["B4C"],    region=-s_cr_b4c_OR)
    c_cr_b4c_gt2 = openmc.Cell(fill=mats['Helium'], region=+s_cr_b4c_OR & -s_cr_clad_IR)
    c_cr_b4c_gt3 = openmc.Cell(fill=mats['304L SS'],   region=+s_cr_clad_IR & -s_cr_clad_OR)
    c_cr_b4c_gt4 = openmc.Cell(fill=mats["H2O + 1000 ppm boron"],    region=+s_cr_clad_OR & -s_gt_clad_IR)
    c_cr_b4c_gt5 = openmc.Cell(fill=mats['Zr-4'],       region=+s_gt_clad_IR & -s_gt_clad_OR)
    u_cr_b4c_gt.add_cells([c_cr_b4c_gt1, c_cr_b4c_gt2, c_cr_b4c_gt3, c_cr_b4c_gt4, c_cr_b4c_gt5])
    
    # fig d. GT + CR end plug
    u_cr_endplug_gt = openmc.Universe(name=f'cr_endplug_gt')
    c_cr_endplug_gt1 = openmc.Cell(fill=mats['304L SS'],region= -s_cr_clad_OR)
    c_cr_endplug_gt2 = openmc.Cell(fill=mats["H2O + 1000 ppm boron"],    region=+s_cr_clad_OR & -s_gt_clad_IR)
    c_cr_endplug_gt3 = openmc.Cell(fill=mats['Zr-4'],       region=+s_gt_clad_IR & -s_gt_clad_OR)
    u_cr_endplug_gt.add_cells([c_cr_endplug_gt1, c_cr_endplug_gt2, c_cr_endplug_gt3])

    # u_outer
    u_gt_grid_htp = openmc.Universe(name='gt_outer_grid_htp')
    c_gtg1 = openmc.Cell(fill=mats["H2O + 1000 ppm boron"], region=+s_gt_clad_OR & -s_grid)
    c_gtg2 = openmc.Cell(fill=mats["Zr-4"],   region=+s_grid & -s_pin)
    u_gt_grid_htp.add_cells([c_gtg1, c_gtg2])

    u_gt_grid_hmp = openmc.Universe(name='gt_outer_grid_hmp')
    c_gtg3 = openmc.Cell(fill=mats["H2O + 1000 ppm boron"], region=+s_gt_clad_OR & -s_grid)
    c_gtg4 = openmc.Cell(fill=mats["Inconel"],   region=+s_grid & -s_pin)
    u_gt_grid_hmp.add_cells([c_gtg3, c_gtg4])

    cr_gt_axial_segments = [
        # Bottom nozzle (0-10.160)
        (s_bot_Z,      s_bot_nozzle_top_Z,          mats['Bottom nozzle'],     mats['Bottom nozzle']),
        
        # Empty Guide Tube (10.160-206.506)
        (s_bot_nozzle_top_Z, s_grid1_bot_Z,    u_gt,                      mats["H2O + 1000 ppm boron"]),
        (s_grid1_bot_Z, s_grid1_top_Z,  u_gt, u_gt_grid_hmp),
        (s_grid1_top_Z,s_grid2_bot_Z, u_gt, mats["H2O + 1000 ppm boron"]),
        (s_grid2_bot_Z, s_grid2_top_Z, u_gt, u_gt_grid_htp),
        (s_grid2_top_Z, s_grid3_bot_Z, u_gt, mats["H2O + 1000 ppm boron"]),
        (s_grid3_bot_Z, s_grid3_top_Z, u_gt, u_gt_grid_htp),
        (s_grid3_top_Z, s_grid4_bot_Z, u_gt, mats["H2O + 1000 ppm boron"]),
        (s_grid4_bot_Z, s_grid4_top_Z, u_gt, u_gt_grid_htp),
        (s_grid4_top_Z, s_cr_endplug_up_Z,  u_gt, mats["H2O + 1000 ppm boron"]),

        # End plug (206.506-211.365)
        (s_cr_endplug_up_Z, s_fuel_top_Z, u_cr_endplug_gt ,mats["H2O + 1000 ppm boron"]),
        # AIC (211.365-226.060) + Grid 5
        (s_fuel_top_Z, s_grid5_bot_Z,           u_cr_aic_gt, mats["H2O + 1000 ppm boron"]),
        (s_grid5_bot_Z, s_grid5_top_Z,          u_cr_aic_gt, u_gt_grid_htp),
        (s_grid5_top_Z, s_top_endcap_top_Z,     u_cr_aic_gt, mats["H2O + 1000 ppm boron"]),
        # B4C (226.060-234.541)        
        (s_top_endcap_top_Z,s_top_nozzle_bot_Z,           u_cr_b4c_gt ,mats["H2O + 1000 ppm boron"]),
        # Top nozzle (234.541-243.561)
        (s_top_nozzle_bot_Z,  s_top_Z,              mats['Top nozzle'],     mats['Top nozzle']),
    ]

    cells_cr_gt = []
    for i, (zbot, ztop, u_inner, u_outer) in enumerate(cr_gt_axial_segments):
        z_reg = -ztop & +zbot
        # Inner cell: everything inside the cladding outer radius
        if isinstance(u_inner, openmc.Material):
            c_in = openmc.Cell(fill=u_inner, region=-s_gt_clad_OR & z_reg, name=f'fuel_seg{i}_inner_mat')
        else:
            c_in = openmc.Cell(fill=u_inner, region=-s_gt_clad_OR & z_reg, name=f'fuel_seg{i}_inner_uni')
        # Outer cell: coolant + grid wrapper, bounded by rect_gridout (1.26 cm pitch)
        if isinstance(u_outer, openmc.Material):
            c_out = openmc.Cell(fill=u_outer, region=(+s_gt_clad_OR) & z_reg & -s_pin, name=f'fuel_seg{i}_outer_mat')
        else:
            c_out = openmc.Cell(fill=u_outer, region=(+s_gt_clad_OR) & z_reg & -s_pin, name=f'fuel_seg{i}_outer_uni')
        cells_cr_gt.append(c_in)
        cells_cr_gt.append(c_out)

    u_cr_gt_pin = openmc.Universe(name=f'full_empty_cr_gt_pin')
    u_cr_gt_pin.add_cells(cells_cr_gt)
    return u_cr_gt_pin


def build_cr_gt_pin(withdrawn=1.0,mats={}):
    u_cr_gt = openmc.Universe(name=f'empty_gt_pin')
    c_cr_gt1 = openmc.Cell(fill=mats["H2O + 1000 ppm boron"],    region=+s_cr_clad_OR & -s_gt_clad_IR)
    c_cr_gt2 = openmc.Cell(fill=mats['Zr-4'],       region=+s_gt_clad_IR & -s_gt_clad_OR)
    u_cr_gt.add_cells([c_cr_gt1, c_cr_gt2])
    
    u_gt_grid_htp = openmc.Universe(name='gt_outer_grid_htp')
    c_gtg1 = openmc.Cell(fill=mats["H2O + 1000 ppm boron"], region=+s_gt_clad_OR & -s_grid)
    c_gtg2 = openmc.Cell(fill=mats["Zr-4"],   region=+s_grid & -s_pin)
    u_gt_grid_htp.add_cells([c_gtg1, c_gtg2])

    u_gt_grid_hmp = openmc.Universe(name='gt_outer_grid_hmp')
    c_gtg3 = openmc.Cell(fill=mats["H2O + 1000 ppm boron"], region=+s_gt_clad_OR & -s_grid)
    c_gtg4 = openmc.Cell(fill=mats["Inconel"],   region=+s_grid & -s_pin)
    u_gt_grid_hmp.add_cells([c_gtg3, c_gtg4])

    u_cr_b4c = openmc.Universe(name=f'cr_b4c')
    c_cr1 = openmc.Cell(fill=mats["B4C"],    region=-s_cr_b4c_OR)
    c_cr2 = openmc.Cell(fill=mats['Helium'], region=+s_cr_b4c_OR & -s_cr_clad_IR)
    c_cr3 = openmc.Cell(fill=mats['304L SS'],   region=+s_cr_clad_IR & -s_cr_clad_OR)
    u_cr_b4c.add_cells([c_cr1, c_cr2, c_cr3])

    u_cr_aic = openmc.Universe(name=f'cr_aic')
    c_cr4 = openmc.Cell(fill=mats["AIC"],   region=-s_cr_aic_OR)
    c_cr5 = openmc.Cell(fill=mats['Helium'], region=+s_cr_aic_OR & -s_cr_clad_IR)
    c_cr6 = openmc.Cell(fill=mats['304L SS'],   region=+s_cr_clad_IR & -s_cr_clad_OR)
    u_cr_aic.add_cells([c_cr4, c_cr5, c_cr6])

    u_cr_plenum = openmc.Universe(name=f'cr_plenum')
    c_cr_pl1 = openmc.Cell(fill=mats['Helium'], region=-s_cr_clad_IR)
    c_cr_pl2 = openmc.Cell(fill=mats['304L SS'],       region=+s_cr_clad_IR & -s_cr_clad_OR)
    u_cr_plenum.add_cells([c_cr_pl1, c_cr_pl2])

    u_cr_endplug = openmc.Universe(name=f'cr_endplug')
    c_cr_end1 = openmc.Cell(fill=mats['304L SS'],region= -s_cr_clad_OR)
    u_cr_endplug.add_cells([c_cr_end1])

    cr_gt_axial_segments = [
        # Bottom nozzle (0-10.160)
        (s_bot_Z,      s_bot_nozzle_top_Z,          mats['Bottom nozzle'],     mats['Bottom nozzle']),
        # Empty guide tube (10.160-234.541)
        (s_bot_nozzle_top_Z, s_grid1_bot_Z,    u_cr_gt,             mats["H2O + 1000 ppm boron"]),
        # Grid 1 (14.920-19.365)
        (s_grid1_bot_Z, s_grid1_top_Z,    u_cr_gt,             u_gt_grid_hmp),
        (s_grid1_top_Z, s_grid2_bot_Z,    u_cr_gt,             mats["H2O + 1000 ppm boron"]),
        # Grid 2 (65.974-70.419)
        (s_grid2_bot_Z, s_grid2_top_Z,    u_cr_gt,             u_gt_grid_htp),
        (s_grid2_top_Z, s_grid3_bot_Z,    u_cr_gt,             mats["H2O + 1000 ppm boron"]),
        # Grid 3 (117.028-121.473)
        (s_grid3_bot_Z, s_grid3_top_Z,    u_cr_gt,             u_gt_grid_htp),
        (s_grid3_top_Z, s_grid4_bot_Z,    u_cr_gt,             mats["H2O + 1000 ppm boron"]),
        # Grid 4 (168.082-172.527)
        (s_grid4_bot_Z, s_grid4_top_Z,    u_cr_gt,             u_gt_grid_htp),
        (s_grid4_top_Z, s_grid5_bot_Z,    u_cr_gt,             mats["H2O + 1000 ppm boron"]),
        # Grid 5 (219.136-223.581)
        (s_grid5_bot_Z, s_grid5_top_Z,    u_cr_gt,             u_gt_grid_htp),
        (s_grid5_top_Z, s_top_nozzle_bot_Z,    u_cr_gt,        mats["H2O + 1000 ppm boron"]),
        # Top nozzle (234.541-243.561)
        (s_top_nozzle_bot_Z,  s_top_Z,    mats['Top nozzle'],     mats['Top nozzle']),
    ]

    cells_cr_gt = []
    for i, (zbot, ztop, u_inner, u_outer) in enumerate(cr_gt_axial_segments):
        z_reg = -ztop & +zbot
        # Inner cell: everything inside the cladding outer radius
        if isinstance(u_inner, openmc.Material):
            c_in = openmc.Cell(fill=u_inner, region=+s_cr_clad_OR & (-s_gt_clad_OR) & z_reg, name=f'fuel_seg{i}_inner_mat')
        else:
            c_in = openmc.Cell(fill=u_inner, region=+s_cr_clad_OR & (-s_gt_clad_OR) & z_reg, name=f'fuel_seg{i}_inner_uni')
        # Outer cell: coolant + grid wrapper, bounded by rect_gridout (1.26 cm pitch)
        if isinstance(u_outer, openmc.Material):
            c_out = openmc.Cell(fill=u_outer, region=(+s_gt_clad_OR) & z_reg & -s_pin, name=f'fuel_seg{i}_outer_mat')
        else:
            c_out = openmc.Cell(fill=u_outer, region=(+s_gt_clad_OR) & z_reg & -s_pin, name=f'fuel_seg{i}_outer_uni')
        cells_cr_gt.append(c_in)
        cells_cr_gt.append(c_out)

    unmovable_cr_axial_segments = [
        # Bottom nozzle (0-10.160)
        (s_bot_Z,      s_bot_nozzle_top_Z,          mats['Bottom nozzle']),
        # Empty Guide Tube (10.160-18.546)
        (s_bot_nozzle_top_Z, s_cr_endplug_bot_Z,    mats["H2O + 1000 ppm boron"]),
        # movable part (18.546-234.541)
        # Top nozzle (234.541-243.561)
        (s_top_nozzle_bot_Z, s_top_Z,    mats["Top nozzle"]),
    ]

    for i, (zbot, ztop, u_inner) in enumerate(unmovable_cr_axial_segments):
        z_reg = -ztop & +zbot
        # Inner cell: everything inside the cladding outer radius
        if isinstance(u_inner, openmc.Material):
            c_in = openmc.Cell(fill=u_inner, region=-s_cr_clad_OR & z_reg, name=f'fuel_seg{i}_inner_mat')
        else:
            c_in = openmc.Cell(fill=u_inner, region=-s_cr_clad_OR & z_reg, name=f'fuel_seg{i}_inner_uni')
        cells_cr_gt.append(c_in)


    # movable control rod part
    movable_cr_axial_segments = [
        # End plug (18.546-23.405)
        (s_cr_endplug_bot_Z,s_cr_endplug_top_Z,u_cr_endplug),
        # AIC (23.405-53.885)
        (s_cr_endplug_top_Z,s_cr_aic_top_Z,u_cr_aic),
        # B4C (53.885-211.365)
        (s_cr_aic_top_Z,s_fuel_top_Z,u_cr_b4c),
        # Upper plenum (211.365-234.541)
        (s_fuel_top_Z,s_top_nozzle_bot_Z,u_cr_plenum),
    ]

    cells_movable_cr = []

    for i, (zbot, ztop, u_inner) in enumerate(movable_cr_axial_segments):
        z_reg = -ztop & +zbot
        # Inner cell: everything inside the cladding outer radius
        if isinstance(u_inner, openmc.Material):
            c_in = openmc.Cell(fill=u_inner, region=-s_cr_clad_OR & z_reg, name=f'fuel_seg{i}_inner_mat')
        else:
            c_in = openmc.Cell(fill=u_inner, region=-s_cr_clad_OR & z_reg, name=f'fuel_seg{i}_inner_uni')
        cells_movable_cr.append(c_in)
    
    c_cr_outer = openmc.Cell(fill=mats["H2O + 1000 ppm boron"], region= (-s_cr_clad_OR) | -s_cr_endplug_bot_Z)
    cells_movable_cr.append(c_cr_outer)

    u_movable_cr = openmc.Universe(name=f'movable_cr_pin')
    u_movable_cr.add_cells(cells_movable_cr)
    c_movable_cr = openmc.Cell(fill=u_movable_cr, region=-s_cr_clad_OR & +s_cr_endplug_bot_Z & -s_top_nozzle_bot_Z, name=f'movable_cr')
    c_movable_cr.translation = (0.0, 0.0, withdrawn*(c.top_nozzle_bot_Z-c.cr_endplug_bot_Z))

    cells_cr_gt.append(c_movable_cr)
    u_cr_gt_pin = openmc.Universe(name=f'full_empty_cr_gt_pin')
    u_cr_gt_pin.add_cells(cells_cr_gt)

    if withdrawn == 0.0:
        return build_gtcr0_pin(mats=mats)
    elif withdrawn == 1.0:
        return build_gtcr1_pin(mats=mats)
    else:
        return u_cr_gt_pin

def plot_pin(name,pin,color_dict,z_lst):
    # plot xz
    pin.plot(width=(2.0, 245.0),
               origin=(0.0, 0.0, 122.5),
               basis='xz',
               pixels=(1000, 8000),
               color_by='material',
               colors=color_dict
               )
    plt.gca().set_aspect('auto')
    plt.gca().axis('off')
    plt.savefig(f"nuscale_{name}_xz.png", bbox_inches='tight', dpi=300)
    plt.close()
    # plot xy
    for z in z_lst:
        pin.plot(width=(1.5, 1.5),
               origin=(0.0, 0.0, z),
               basis='xy',
               pixels=(1000, 1000),
               color_by='material',
               colors=color_dict
               )
        plt.gca().set_aspect('auto')
        plt.gca().axis('off')
        plt.savefig(f"nuscale_{name}_{z:.2f}.png", bbox_inches='tight', dpi=300)
        plt.close()

    return None

if __name__ == "__main__":
    mats = build_mats()
    color_dict = {
            mats['uo2 A1']: 'darkred',
            mats['uo2 A2']: 'firebrick',
            mats['uo2 B1']: 'red',
            mats['uo2 B2 C3']: 'orangered',
            mats['uo2 C1']: 'chocolate',
            mats['uo2 C2']: 'darkorange',
            mats['uo2 C2 Gd2O3']: 'gold',

            mats['Helium']: 'whitesmoke',
            mats["H2O + 1000 ppm boron"]: [198,226,255],
            mats['B4C']: 'lime',
            mats['AIC']: 'lightgreen',
            mats['304L SS']: 'black',
            mats['Zr-4']: 'grey',
            mats['Inconel']: 'silver',

            mats['Heavy reflector']: 'midnightblue',
            mats['Bottom nozzle']: 'steelblue',          # 原 mat_bn
            mats['Top nozzle']: 'cadetblue',             # 原 mat_tn
                }

    fuel_pin = build_fuel_pin(fuel_name="uo2 A1",mats=mats)
    z_lst_fuel = [2.0, 12.000, 15.000, 20.000, 68.000, 120.000, 170.000, 212.000, 220.000, 225.000,230.000,240.000]
    plot_pin("fuel_pin",fuel_pin,color_dict,z_lst_fuel)
    
    # empty_gt_pin = build_empty_gt_pin(mats=mats)
    # z_lst_empty_gt = [2.0, 15.000, 20.000, 68.000, 120.000, 170.000, 220.000, 240.000]
    # plot_pin("empty_gt_pin",empty_gt_pin,color_dict,z_lst_empty_gt)
    
    # cr_gt_pin = build_cr_gt_pin(withdrawn=1.0,mats=mats)
    # z_lst_cr_gt = [2.0, 15.000, 20.000, 40.000 ,68.000, 120.000, 170.000, 220.000, 240.000]
    # plot_pin("cr_gt_pin",cr_gt_pin,color_dict,z_lst_cr_gt)
    
    print("finish")
