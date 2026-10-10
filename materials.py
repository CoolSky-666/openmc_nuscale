import openmc
import constants as c

def build_mats():
    # create dict to store materials
    mats = {}

    mats['Zr-4'] = openmc.Material(name="Zr-4")
    mats['Zr-4'].add_nuclide('Cr50', 3.29620E-06, 'ao')
    mats['Zr-4'].add_nuclide('Cr52', 6.35640E-05, 'ao')
    mats['Zr-4'].add_nuclide('Cr53', 7.20760E-06, 'ao')
    mats['Zr-4'].add_nuclide('Cr54', 1.79410E-06, 'ao')
    mats['Zr-4'].add_nuclide('Fe54', 8.66980E-06, 'ao')
    mats['Zr-4'].add_nuclide('Fe56', 1.36100E-04, 'ao')
    mats['Zr-4'].add_nuclide('Fe57', 3.14310E-06, 'ao')
    mats['Zr-4'].add_nuclide('Fe58', 4.18290E-07, 'ao')
    mats['Zr-4'].add_nuclide('O16', 3.07440E-04, 'ao')
    mats['Zr-4'].add_nuclide('O17', 1.16800E-07, 'ao')
    mats['Zr-4'].add_nuclide('Sn112', 4.67350E-06, 'ao')
    mats['Zr-4'].add_nuclide('Sn114', 3.17990E-06, 'ao')
    mats['Zr-4'].add_nuclide('Sn115', 1.63810E-06, 'ao')
    mats['Zr-4'].add_nuclide('Sn116', 7.00550E-05, 'ao')
    mats['Zr-4'].add_nuclide('Sn117', 3.70030E-05, 'ao')
    mats['Zr-4'].add_nuclide('Sn118', 1.16690E-04, 'ao')
    mats['Zr-4'].add_nuclide('Sn119', 4.13870E-05, 'ao')
    mats['Zr-4'].add_nuclide('Sn120', 1.56970E-04, 'ao')
    mats['Zr-4'].add_nuclide('Sn122', 2.23080E-05, 'ao')
    mats['Zr-4'].add_nuclide('Sn124', 2.78970E-05, 'ao')
    mats['Zr-4'].add_nuclide('Zr90', 2.18280E-02, 'ao')
    mats['Zr-4'].add_nuclide('Zr91', 4.76010E-03, 'ao')
    mats['Zr-4'].add_nuclide('Zr92', 7.27590E-03, 'ao')
    mats['Zr-4'].add_nuclide('Zr94', 7.37340E-03, 'ao')
    mats['Zr-4'].add_nuclide('Zr96', 1.18790E-03, 'ao')
    # mats['Zr-4'].set_density('atom/b-cm', 4.343885E-02)

    # Inconel
    mats['Inconel'] = openmc.Material(name="Inconel")
    mats['Inconel'].add_nuclide('Cr50', 7.82390E-04, 'ao')
    mats['Inconel'].add_nuclide('Cr52', 1.50880E-02, 'ao')
    mats['Inconel'].add_nuclide('Cr53', 1.71080E-03, 'ao')
    mats['Inconel'].add_nuclide('Cr54', 4.25860E-04, 'ao')
    mats['Inconel'].add_nuclide('Fe54', 1.47970E-03, 'ao')
    mats['Inconel'].add_nuclide('Fe56', 2.32290E-02, 'ao')
    mats['Inconel'].add_nuclide('Fe57', 5.36450E-04, 'ao')
    mats['Inconel'].add_nuclide('Fe58', 7.13920E-05, 'ao')
    mats['Inconel'].add_nuclide('Mn55', 7.82010E-04, 'ao')
    mats['Inconel'].add_nuclide('Ni58', 2.93200E-02, 'ao')
    mats['Inconel'].add_nuclide('Ni60', 1.12940E-02, 'ao')
    mats['Inconel'].add_nuclide('Ni61', 4.90940E-04, 'ao')
    mats['Inconel'].add_nuclide('Ni62', 1.56530E-03, 'ao')
    mats['Inconel'].add_nuclide('Ni64', 3.98640E-04, 'ao')
    mats['Inconel'].add_nuclide('Si28', 5.67570E-04, 'ao')
    mats['Inconel'].add_nuclide('Si29', 2.88200E-05, 'ao')
    mats['Inconel'].add_nuclide('Si30', 1.89980E-05, 'ao')
    # mats['Inconel'].set_density('atom/b-cm', 8.778987E-02)

    # 304L SS
    mats['304L SS'] = openmc.Material(name="304L SS")
    mats['304L SS'].add_nuclide('Cr50', 7.67780E-04, 'ao')
    mats['304L SS'].add_nuclide('Cr52', 1.48060E-02, 'ao')
    mats['304L SS'].add_nuclide('Cr53', 1.67890E-03, 'ao')
    mats['304L SS'].add_nuclide('Cr54', 4.17910E-04, 'ao')
    mats['304L SS'].add_nuclide('Fe54', 3.46200E-03, 'ao')
    mats['304L SS'].add_nuclide('Fe56', 5.43450E-02, 'ao')
    mats['304L SS'].add_nuclide('Fe57', 1.25510E-03, 'ao')
    mats['304L SS'].add_nuclide('Fe58', 1.67030E-04, 'ao')
    mats['304L SS'].add_nuclide('Mn55', 1.76040E-03, 'ao')
    mats['304L SS'].add_nuclide('Ni58', 5.60890E-03, 'ao')
    mats['304L SS'].add_nuclide('Ni60', 2.16050E-03, 'ao')
    mats['304L SS'].add_nuclide('Ni61', 9.39170E-05, 'ao')
    mats['304L SS'].add_nuclide('Ni62', 2.99450E-04, 'ao')
    mats['304L SS'].add_nuclide('Ni64', 7.62610E-05, 'ao')
    mats['304L SS'].add_nuclide('Si28', 9.52810E-04, 'ao')
    mats['304L SS'].add_nuclide('Si29', 4.83810E-05, 'ao')
    mats['304L SS'].add_nuclide('Si30', 3.18930E-05, 'ao')
    # mats['304L SS'].set_density('atom/b-cm', 8.793223E-02)

    mats['uo2 A1'] = openmc.Material(name="uo2 A1")
    mats['uo2 A1'].add_nuclide('U235', 3.56456E-04, 'ao')
    mats['uo2 A1'].add_nuclide('U238', 2.31116E-02, 'ao')
    mats['uo2 A1'].add_nuclide('O16', 4.69361E-02, 'ao')
    # mats['uo2 A1'].set_density('atom/b-cm', 7.040416E-02)
    
    mats['uo2 A2'] = openmc.Material(name="uo2 A2")
    mats['uo2 A2'].add_nuclide('U235', 3.80219E-04, 'ao')
    mats['uo2 A2'].add_nuclide('U238', 2.30881E-02, 'ao')
    mats['uo2 A2'].add_nuclide('O16', 4.69367E-02, 'ao')
    # mats['uo2 A2'].set_density('atom/b-cm', 7.040502E-02)

    # uo2_B1
    mats['uo2 B1'] = openmc.Material(name="uo2 B1")
    mats['uo2 B1'].add_nuclide('U235', 5.94084E-04, 'ao')
    mats['uo2 B1'].add_nuclide('U238', 2.28766E-02, 'ao')
    mats['uo2 B1'].add_nuclide('O16', 4.69414E-02, 'ao')
    # mats['uo2 B1'].set_density('atom/b-cm', 7.041208E-02)

    mats['uo2 B2 C3'] = openmc.Material(name="uo2 B2 C3")
    mats['uo2 B2 C3'].add_nuclide('U235', 6.17846E-04, 'ao')
    mats['uo2 B2 C3'].add_nuclide('U238', 2.28531E-02, 'ao')
    mats['uo2 B2 C3'].add_nuclide('O16', 4.69419E-02, 'ao')
    # mats['uo2 B2 C3'].set_density('atom/b-cm', 7.041285E-02)

    # uo2_C1
    mats['uo2 C1'] = openmc.Material(name="uo2 C1")
    mats['uo2 C1'].add_nuclide('U235', 9.62391E-04, 'ao')
    mats['uo2 C1'].add_nuclide('U238', 2.25123E-02, 'ao')
    mats['uo2 C1'].add_nuclide('O16', 4.69495E-02, 'ao')
    # mats['uo2 C1'].set_density('atom/b-cm', 7.042419E-02)

    # uo2_C2
    mats['uo2 C2'] = openmc.Material(name="uo2 C2")
    mats['uo2 C2'].add_nuclide('U235', 1.08120E-03, 'ao')
    mats['uo2 C2'].add_nuclide('U238', 2.23948E-02, 'ao')
    mats['uo2 C2'].add_nuclide('O16', 4.69521E-02, 'ao')
    # mats['uo2 C2'].set_density('atom/b-cm', 7.042810E-02)
    
    # uo2_C2_with_Gd2O3
    mats['uo2 C2 Gd2O3'] = openmc.Material(name="uo2 C2 Gd2O3")
    mats['uo2 C2 Gd2O3'].add_nuclide('U235', 9.61347E-04, 'ao')
    mats['uo2 C2 Gd2O3'].add_nuclide('U238', 1.99124E-02, 'ao')
    mats['uo2 C2 Gd2O3'].add_nuclide('O16', 4.58016E-02, 'ao')
    mats['uo2 C2 Gd2O3'].add_nuclide('Gd152', 5.40541E-06, 'ao')
    mats['uo2 C2 Gd2O3'].add_nuclide('Gd154', 5.89189E-05, 'ao')
    mats['uo2 C2 Gd2O3'].add_nuclide('Gd155', 4.00000E-04, 'ao')
    mats['uo2 C2 Gd2O3'].add_nuclide('Gd156', 5.53243E-04, 'ao')
    mats['uo2 C2 Gd2O3'].add_nuclide('Gd157', 4.22973E-04, 'ao')
    mats['uo2 C2 Gd2O3'].add_nuclide('Gd158', 6.71352E-04, 'ao')
    mats['uo2 C2 Gd2O3'].add_nuclide('Gd160', 5.90811E-04, 'ao')
    # mats['uo2 C2 Gd2O3'].set_density('atom/b-cm', 6.937805E-02)

    # AIC (80-15-5)
    mats["AIC"] = openmc.Material(name="AIC")
    mats["AIC"].add_nuclide('Ag107', 2.35230E-02, 'ao')
    mats["AIC"].add_nuclide('Ag109', 2.18540E-02, 'ao')
    mats["AIC"].add_nuclide('Cd106', 3.38820E-05, 'ao')
    mats["AIC"].add_nuclide('Cd108', 2.41660E-05, 'ao')
    mats["AIC"].add_nuclide('Cd110', 3.39360E-04, 'ao')
    mats["AIC"].add_nuclide('Cd111', 3.48210E-04, 'ao')
    mats["AIC"].add_nuclide('Cd112', 6.56110E-04, 'ao')
    mats["AIC"].add_nuclide('Cd113', 3.32750E-04, 'ao')
    mats["AIC"].add_nuclide('Cd114', 7.82520E-04, 'ao')
    mats["AIC"].add_nuclide('Cd116', 2.04430E-04, 'ao')
    mats["AIC"].add_nuclide('In113', 3.42190E-04, 'ao')
    mats["AIC"].add_nuclide('In115', 7.65110E-03, 'ao')
    # mats["AIC"].set_density('atom/b-cm', 5.609172E-02)

    mats["B4C"] = openmc.Material(name="B4C")
    mats["B4C"].add_nuclide('B10', 1.52060E-02, 'ao')
    mats["B4C"].add_nuclide('B11', 6.15140E-02, 'ao')
    # mats["B4C"].add_nuclide('C12', 1.89720E-02, 'ao')
    # mats["B4C"].add_nuclide('C13', 2.12520E-04, 'ao')
    # mats["B4C"].add_nuclide('C0', 1.89720E-02+2.12520E-04, 'ao')
    mats["B4C"].add_element('C', 1.918452E-02, 'ao')
    # mats["B4C"].set_density('atom/b-cm', 9.590452E-02)

    # H2O + 1000 ppm boron
    mats["H2O + 1000 ppm boron"] = openmc.Material(name="H2O + 1000 ppm boron")
    mats["H2O + 1000 ppm boron"].add_nuclide('B10', 8.33778E-06, 'ao')
    mats["H2O + 1000 ppm boron"].add_nuclide('B11', 3.35608E-05, 'ao')
    mats["H2O + 1000 ppm boron"].add_nuclide('O16', 2.51573E-02, 'ao')
    mats["H2O + 1000 ppm boron"].add_nuclide('H1', 5.02932E-02, 'ao')
    mats["H2O + 1000 ppm boron"].add_s_alpha_beta('c_H_in_H2O') # thermal scattering law to H in coolant
    # mats["H2O + 1000 ppm boron"].set_density('atom/b-cm', 7.549240E-02)

    # helium 
    mats['Helium'] = openmc.Material(name = "Helium")
    mats['Helium'].add_nuclide('He3', 4.80890E-10, 'ao')
    mats['Helium'].add_nuclide('He4',2.40440E-04, 'ao')
    # mats['Helium'].set_density('atom/b-cm', 2.404405E-04)

    coolant = openmc.Material(name="H2O + 1000 ppm boron")
    coolant.add_nuclide('B10', 8.33778E-06, 'ao')
    coolant.add_nuclide('B11', 3.35608E-05, 'ao')
    coolant.add_nuclide('O16', 2.51573E-02, 'ao')
    coolant.add_nuclide('H1', 5.02932E-02, 'ao')
    # coolant.set_density('atom/b-cm', 7.549240E-02)

    # homogeneous materials
    mats["Heavy reflector"] = openmc.Material.mix_materials([mats['304L SS'], coolant], [0.956, 0.044], 'vo')
    # mats["Heavy reflector"].add_s_alpha_beta('c_H_in_H2O')
    mats["Bottom nozzle"] = openmc.Material.mix_materials([mats['304L SS'], coolant], [0.172, 0.828], 'vo')
    # mats["Bottom nozzle"].add_s_alpha_beta('c_H_in_H2O')
    mats["Top nozzle"] = openmc.Material.mix_materials([mats['304L SS'], coolant], [0.177, 0.823], 'vo')
    # mats["Top nozzle"].add_s_alpha_beta('c_H_in_H2O')

    for mat in mats.values():
        if mat.name == "H2O + 1000 ppm boron":
            mat.temperature = c.coolant_temperature
        elif mat.name[:3] == "uo2":
            mat.temperature = c.fuel_temperature 
        else:
            mat.temperature = c.structure_temperature # structure mats
    return mats

if __name__ == '__main__':
    mats = build_mats()
    print(mats)