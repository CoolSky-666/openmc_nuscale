import openmc
import numpy as np
import sys, os

import constants as c
from core import build_core
from materials import build_mats
import matplotlib.pyplot as plt

# import os
# os.environ['OPENMC_CROSS_SECTIONS'] = '/home/cool/NuData/endfb-vii.1-hdf5/cross_sections.xml'

openmc.config['cross_sections'] = '/home/cool/NuData/endfb-vii.1-hdf5/cross_sections.xml'

# ============================================================
# Case selection (control rod configurations)
# withdrawn=0 -> rod INSERTED (in)
# withdrawn=1 -> rod WITHDRAWN (out)
# ============================================================
CASES = {
    "All rods out (ARO)":   {"RE1": 1.00, "RE2": 1.00, "SH3": 1.00, "SH4": 1.00},
    "RE1 in":               {"RE1": 0.00, "RE2": 1.00, "SH3": 1.00, "SH4": 1.00},
    "RE2 in":               {"RE1": 1.00, "RE2": 0.00, "SH3": 1.00, "SH4": 1.00},
    "SH3 in":               {"RE1": 1.00, "RE2": 1.00, "SH3": 0.00, "SH4": 1.00},
    "SH4 in":               {"RE1": 1.00, "RE2": 1.00, "SH3": 1.00, "SH4": 0.00},
    "All rods in (ARI)":    {"RE1": 0.00, "RE2": 0.00, "SH3": 0.00, "SH4": 0.00},
}

_BASENAME = os.path.dirname(os.path.abspath(__file__))
_DATA_DIR = os.path.join(_BASENAME, "data")

def run_case(case_name, dict_cr, mats):
    """Build and run a single control-rod configuration.

    Parameters
    ----------
    case_name : str
        Case key in CASES, used as the run sub-directory name.
    dict_cr : dict
        {"RE1":.., "RE2":.., "SH3":.., "SH4":..} withdrawn fractions.
    mats : dict
        Materials dictionary returned by build_mats() (reused across cases).
    """
    case_dir = os.path.join(_DATA_DIR, case_name)
    os.makedirs(case_dir, exist_ok=True)
    print(f"\n{'='*60}")
    print(f"[INFO] Running case '{case_name}' in: {case_dir}")
    print(f"[INFO] dict_cr = {dict_cr}")
    print(f"{'='*60}")
    

    # ============================================================
    # Geometry
    # ============================================================
    core = build_core(mats=mats, dict_cr=dict_cr)
    geometry = openmc.Geometry(core)

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

    geometry.plot(
        width=(200.0, 200.0),
        origin=(0.0, 0.0, 120.0),
        basis='xy',
        pixels=(2000, 2000),
        color_by='material',
        colors=color_dict
        )
    plt.gca().set_aspect('auto')
    plt.gca().axis('off')
    save_path_xy = os.path.join(case_dir, f"nuscale_core_{case_name}_xy.png")
    plt.savefig(save_path_xy, bbox_inches='tight', dpi=300)
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
    save_path_xz = os.path.join(case_dir, f"nuscale_core_{case_name}_xz.png")
    plt.savefig(save_path_xz, bbox_inches='tight', dpi=300)
    plt.close()
    
    # ============================================================
    # Tallies
    # ============================================================
    mesh1 = openmc.RegularMesh()
    mesh1.dimension = [7, 7]
    mesh1.lower_left = [-c.lat_Pitch*3.5, -c.lat_Pitch*3.5]
    mesh1.upper_right = [c.lat_Pitch*3.5, c.lat_Pitch*3.5]
    mesh_filter1 = openmc.MeshFilter(mesh1)
    t1 = openmc.Tally(name='as_pow')
    t1.filters = [mesh_filter1]
    t1.scores = ['heating']

    mesh2 = openmc.RegularMesh()
    mesh2.dimension = [7*17, 7*17]
    mesh2.lower_left = [-c.lat_Pitch*3.5, -c.lat_Pitch*3.5]
    mesh2.upper_right = [c.lat_Pitch*3.5, c.lat_Pitch*3.5]
    mesh_filter2 = openmc.MeshFilter(mesh2)
    t2 = openmc.Tally(name='pin_pow')
    t2.filters = [mesh_filter2]
    t2.scores = ['heating']

    mesh3 = openmc.RectilinearMesh()
    mesh3.x_grid = [-c.lat_Pitch*3.5, +c.lat_Pitch*3.5]
    mesh3.y_grid = [-c.lat_Pitch*3.5, +c.lat_Pitch*3.5]
    z_lst = [11.365,14.920,19.365,31.017,42.670,54.322,65.974,70.419,82.071,93.724,105.376,117.028,121.473,133.125,144.778,156.430,168.082,172.527,182.236,191.946,201.656,211.365]
    mesh3.z_grid = z_lst
    mesh_filter3 = openmc.MeshFilter(mesh3)
    t3 = openmc.Tally(name='pow_ax')
    t3.filters = [mesh_filter3]
    t3.scores = ['heating']
    tallies = openmc.Tallies([t1, t2, t3])

    # ============================================================
    # Settings
    # ============================================================
    r_dist   = openmc.stats.Uniform(0, c.barrel_OR)
    phi_dist = openmc.stats.Uniform(0, 2*np.pi)
    z_dist   = openmc.stats.Uniform(0, c.top_Z)
    spatial_dist = openmc.stats.CylindricalIndependent(r_dist, phi_dist, z_dist)
    source = openmc.IndependentSource(
        space=spatial_dist,
        constraints={'fissionable': True},
        angle=openmc.stats.Isotropic())
    temperature = {
        'default': 293.6,
        'method': 'interpolation',
        'multipole': False }

    settings = openmc.Settings()
    settings.batches = 300
    settings.inactive = 100
    settings.particles = 100000
    settings.temperature = temperature
    settings.source = source
    settings.ptables = True
    settings.resonance_scattering = {'enable': False}
    settings.photon_transport = False

    materials = openmc.Materials(geometry.get_all_materials().values())

    model = openmc.Model(geometry, materials, settings, tallies)
    model.tallies = tallies
    model.run(cwd=case_dir)


# ============================================================
# Build materials ONCE, then iterate all 6 cases sequentially
# ============================================================
if __name__ == '__main__':
    mats = build_mats()
    for case_name, dict_cr in CASES.items():
        run_case(case_name, dict_cr, mats)