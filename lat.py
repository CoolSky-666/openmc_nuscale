import openmc
import matplotlib.pyplot as plt
import numpy as np

import constants as c
from materials import build_mats
from pins import build_fuel_pin, build_empty_gt_pin, build_cr_gt_pin
from pins import s_top_Z, s_bot_Z, s_bot_nozzle_top_Z, s_top_nozzle_bot_Z

tube_x = np.array([5, 8, 11, 3, 13, 2, 5, 8, 11, 14, 2, 5, 8, 11, 14,
                       2, 5, 8, 11, 14, 3, 13, 5, 8, 11])
tube_y = np.array([2, 2, 2, 3, 3, 5, 5, 5, 5, 5, 8, 8, 8, 8, 8,
                    11, 11, 11, 11, 11, 13, 13, 14, 14, 14])

poison_x = np.array([2, 14, 7, 9, 6, 10, 3, 13, 3, 13, 6, 10, 7, 9, 2, 14])
poison_y = np.array([2, 2, 3, 3, 6, 6, 7, 7, 9, 9, 10, 10, 13, 13, 14, 14])

s_lat = openmc.model.RectangularPrism(width=c.lat_Pitch,
                                          height=c.lat_Pitch, axis='z')
lat_region = -s_lat & -s_top_Z & +s_bot_Z

def _make_assembly(mats={}, name='A1 RE1', dict_pin={}):
    c_outer_h2o = openmc.Cell(fill=mats['H2O + 1000 ppm boron'],region=-s_top_nozzle_bot_Z & +s_bot_nozzle_top_Z)
    c_outer_top = openmc.Cell(fill=mats['Top nozzle'],region=-s_top_Z & +s_top_nozzle_bot_Z)
    c_outer_bot = openmc.Cell(fill=mats['Bottom nozzle'],region=-s_bot_nozzle_top_Z & +s_bot_Z)
    u_outer_h2o = openmc.Universe(cells=[c_outer_h2o,c_outer_top,c_outer_bot])

    lat = openmc.RectLattice(name=f'Fuel Assembly {name}')
    lat.pitch      = (c.pin_Pitch, c.pin_Pitch)
    lat.lower_left = (-c.pin_Pitch * 17 / 2, -c.pin_Pitch * 17 / 2)
    lat.outer = u_outer_h2o
    lat.universes  = np.tile(dict_pin["f"], (17, 17))
    if ("cr" in dict_pin):
        lat.universes[tube_x, tube_y] = dict_pin["cr"]
        lat.universes[8, 8] = dict_pin["gt"]
    else:
        lat.universes[tube_x, tube_y] = dict_pin["gt"]

    if ("fp" in dict_pin):
        lat.universes[poison_x, poison_y] = dict_pin["fp"]

    u_lat = openmc.Universe(name=name)
    u_lat.add_cell(openmc.Cell(fill=lat, region=lat_region))
    return u_lat


def build_assemblies(mats={}, dict_cr={"RE1": 1.00, "RE2": 1.00, "SH3": 1.00, "SH4": 1.00}):
    
    gt      = build_empty_gt_pin(mats=mats)
    cr_re1  = build_cr_gt_pin(withdrawn=dict_cr["RE1"], mats=mats)
    cr_re2  = build_cr_gt_pin(withdrawn=dict_cr["RE2"], mats=mats)
    cr_sh3  = build_cr_gt_pin(withdrawn=dict_cr["SH3"], mats=mats)
    cr_sh4  = build_cr_gt_pin(withdrawn=dict_cr["SH4"], mats=mats)

    f_A1     = build_fuel_pin(fuel_name='uo2 A1',       mats=mats)
    f_A2     = build_fuel_pin(fuel_name='uo2 A2',       mats=mats)
    f_B1     = build_fuel_pin(fuel_name='uo2 B1',       mats=mats)
    f_B2_C3  = build_fuel_pin(fuel_name='uo2 B2 C3',    mats=mats)
    f_C1     = build_fuel_pin(fuel_name='uo2 C1',       mats=mats)
    f_C2     = build_fuel_pin(fuel_name='uo2 C2',       mats=mats)
    f_C2_Gd  = build_fuel_pin(fuel_name='uo2 C2 Gd2O3', mats=mats)

    specs = {
        "A1 RE1": {"f":f_A1,"cr":cr_re1,"gt":gt},
        "A1":     {"f":f_A1,"gt":gt},
        "A2":     {"f":f_A2,"gt":gt},
        "B1 SH3": {"f":f_B1,"cr":cr_sh3,"gt":gt},
        "B1 SH4": {"f":f_B1,"cr":cr_sh4,"gt":gt},
        "B2 RE2": {"f":f_B2_C3,"cr":cr_re2,"gt":gt},
        "C1":     {"f":f_C1,"gt":gt},
        "C2":     {"f":f_C2,"fp":f_C2_Gd,"gt":gt},
        "C3":     {"f":f_B2_C3,"gt":gt},
    }

    dict_assemblies = {}

    for name,pin_dict in specs.items():
        dict_assemblies[name] = _make_assembly(mats=mats, name=name, dict_pin=pin_dict)
    
    c_heavy_reflector = openmc.Cell(fill=mats['Heavy reflector'],region=lat_region)
    u_heavy_reflector = openmc.Universe(cells=[c_heavy_reflector])
    dict_assemblies['dummy'] = u_heavy_reflector
    
    return dict_assemblies


if __name__ == "__main__":
    mats = build_mats()
    dict_assemblies = build_assemblies(mats=mats, dict_cr={"RE1":0.00,"RE2":0.00,"SH3":0.00,"SH4":0.00})
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
            mats['Bottom nozzle']: 'steelblue',
            mats['Top nozzle']: 'cadetblue',
        }

    for as_name, u_as in dict_assemblies.items():
        u_as.plot(
            width=(22.0, 22.0),
            origin=(0.0, 0.0, 120.0),
            basis='xy',
            pixels=(2200, 2200),
            color_by='material',
            colors=color_dict
            )
        plt.gca().set_aspect('auto')
        plt.gca().axis('off')
        plt.savefig(f"nuscale_lat_{as_name}_xy.png", bbox_inches='tight', dpi=300)
        plt.close()

        u_as.plot(
            width=(22.0, 245.0),
            origin=(0.0, 0.0, 122.5),
            basis='xz',
            pixels=(1000, 2450),
            color_by='material',
            colors=color_dict
            )
        plt.gca().set_aspect('auto')
        plt.gca().axis('off')
        plt.savefig(f"nuscale_lat_{as_name}_xz.png", bbox_inches='tight', dpi=300)
        plt.close()