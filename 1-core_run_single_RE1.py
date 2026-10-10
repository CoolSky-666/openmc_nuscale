import openmc
import numpy as np
import sys, os

import constants as c
from core import build_core_single_RE1
from materials import build_mats

# import os
# os.environ['OPENMC_CROSS_SECTIONS'] = '/home/cool/NuData/endfb-vii.1-hdf5/cross_sections.xml'

openmc.config['cross_sections'] = '/home/cool/NuData/endfb-vii.1-hdf5/cross_sections.xml'

_BASENAME = os.path.dirname(os.path.abspath(__file__))
_DATA_DIR = os.path.join(_BASENAME, "data")

def run_case(case_name, mats):
    """Build and run a single control-rod configuration.

    Parameters
    ----------
    case_name : str
        Case key in CASES, used as the run sub-directory name.
    mats : dict
        Materials dictionary returned by build_mats() (reused across cases).
    """
    case_dir = os.path.join(_DATA_DIR, case_name)
    os.makedirs(case_dir, exist_ok=True)
    print(f"\n{'='*60}")
    print(f"[INFO] Running case '{case_name}' in: {case_dir}")
    print(f"{'='*60}")

    # ============================================================
    # Geometry
    # ============================================================
    core = build_core_single_RE1(mats=mats)
    geometry = openmc.Geometry(core)
    
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
    run_case(case_name="RE1 at D5 in", mats=mats)