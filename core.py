import openmc
import numpy as np
import matplotlib.pyplot as plt

import constants as c
from materials import build_mats
from lat import build_assemblies
from pins import s_bot_Z, s_top_Z

core_lat_template = [
    ['dummy',   'dummy',    'C1',       'B2 RE2',   'C1',       'dummy',    'dummy' ],
    ['dummy',   'C2',       'B1 SH4',   'A1',       'B1 SH3',   'C2',       'dummy' ],
    ['C1',      'B1 SH3',   'A2',       'A1 RE1',   'A2',       'B1 SH4',   'C1'    ],
    ['B2 RE2',  'A1',       'A1 RE1',   'C3',       'A1 RE1',   'A1',       'B2 RE2'],
    ['C1',      'B1 SH4',   'A2',       'A1 RE1',   'A2',       'B1 SH3',   'C1'    ],    
    ['dummy',   'C2',       'B1 SH3',   'A1',       'B1 SH4',   'C2',       'dummy' ], 
    ['dummy',   'dummy',    'C1',       'B2 RE2',   'C1',       'dummy',    'dummy' ]
]


s_barrel_IR = openmc.ZCylinder(r=c.barrel_IR, name='barrel_IR')
s_barrel_OR = openmc.ZCylinder(r=c.barrel_OR, name='barrel_OR',boundary_type='vacuum')

def build_core(mats={}, dict_cr={"RE1":0.00,"RE2":0.00,"SH3":0.00,"SH4":0.00}):
    
    c_outer_heavy_reflector = openmc.Cell(fill=mats['Heavy reflector'])
    u_outer_heavy_reflector = openmc.Universe(cells=[c_outer_heavy_reflector])

    dict_assemblies = build_assemblies(mats=mats, dict_cr=dict_cr)
    core_lattice = openmc.RectLattice(name = "NuScale Core")
    core_lattice.lower_left = (-c.lat_Pitch*3.5, -c.lat_Pitch*3.5)
    core_lattice.pitch = (c.lat_Pitch, c.lat_Pitch)
    core_lst = []
    for i in range(7):
        core_row_lst = []
        for j in range(7):
            core_row_lst.append(dict_assemblies[core_lat_template[i][j]])
        core_lst.append(core_row_lst)
    core_lattice.universes = core_lst
    core_lattice.outer = u_outer_heavy_reflector

    c_core_lattice = openmc.Cell(fill=core_lattice, region=-s_barrel_IR & -s_top_Z & +s_bot_Z)

    c_barrel = openmc.Cell(fill=mats['304L SS'], region=+s_barrel_IR & -s_barrel_OR & -s_top_Z & +s_bot_Z)

    core = openmc.Universe(name='core lattice')
    core.add_cell(c_core_lattice)
    core.add_cell(c_barrel)
    return core

def build_core_single_RE1(mats={}):

    c_outer_heavy_reflector = openmc.Cell(fill=mats['Heavy reflector'])
    u_outer_heavy_reflector = openmc.Universe(cells=[c_outer_heavy_reflector])

    dict_assemblies = build_assemblies(mats=mats, dict_cr={"RE1":1.00,"RE2":1.00,"SH3":1.00,"SH4":1.00})
    core_lattice = openmc.RectLattice(name = "NuScale Core")
    core_lattice.lower_left = (-c.lat_Pitch*3.5, -c.lat_Pitch*3.5)
    core_lattice.pitch = (c.lat_Pitch, c.lat_Pitch)
    core_lst = []
    for i in range(7):
        core_row_lst = []
        for j in range(7):
            core_row_lst.append(dict_assemblies[core_lat_template[i][j]])
        core_lst.append(core_row_lst)
    # single RE1 in
    RE1_in = build_assemblies(mats=mats, dict_cr={"RE1":0.00,"RE2":1.00,"SH3":1.00,"SH4":1.00})["A1 RE1"]
    core_lst[4][3] = RE1_in
    core_lattice.universes = core_lst
    core_lattice.outer = u_outer_heavy_reflector

    c_core_lattice = openmc.Cell(fill=core_lattice, region=-s_barrel_IR & -s_top_Z & +s_bot_Z)

    c_barrel = openmc.Cell(fill=mats['304L SS'], region=+s_barrel_IR & -s_barrel_OR & -s_top_Z & +s_bot_Z)

    core = openmc.Universe(name='core lattice')
    core.add_cell(c_core_lattice)
    core.add_cell(c_barrel)
    return core


if __name__ == '__main__':
    mats = build_mats()
    core = build_core(mats=mats,dict_cr={"RE1":1.00,"RE2":0.00,"SH3":0.00,"SH4":0.00})
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

    core.plot(
        width=(200.0, 200.0),
        origin=(0.0, 0.0, 120.0),
        basis='xy',
        pixels=(2000, 2000),
        color_by='material',
        colors=color_dict
        )
    plt.gca().set_aspect('auto')
    plt.gca().axis('off')
    plt.savefig(f"nuscale_core_xy.png", bbox_inches='tight', dpi=300)
    plt.close()

    core.plot(
        width=(200.0, 245.0),
        origin=(0.0, 0.0, 122.5),
        basis='xz',
        pixels=(2000, 2450),
        color_by='material',
        colors=color_dict
        )
    plt.gca().set_aspect('auto')
    plt.gca().axis('off')
    plt.savefig(f"nuscale_core_xz.png", bbox_inches='tight', dpi=300)
    plt.close()