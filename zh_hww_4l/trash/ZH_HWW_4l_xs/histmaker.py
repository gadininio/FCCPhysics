
# flavor = "mumu"
# flavor = "ee"

# list of processes (mandatory)
processList_mumu = {
    # 'p8_ee_ZZ_ecm240':{'fraction': 1},
    # 'p8_ee_WW_ecm240':{'fraction': 1}, 
    'wzp6_ee_mumuH_HWW_ecm240':{'fraction': 1},
}

processList_ee = {
    # 'p8_ee_ZZ_ecm240':{'fraction': 1},
    # 'p8_ee_WW_ecm240':{'fraction': 1}, 
    'wzp6_ee_eeH_HWW_ecm240':{'fraction': 1},
}

processList = processList_mumu | processList_ee

# # Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
# prodTag     = "FCCee/winter2023/IDEA/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json"

# additional/custom C++ functions, defined in header files (optional)
includePaths = ["../functions.h"]

# Define the input dir (optional)
inputDir = f"outputs/ntuples/"
#inputDir = "localSamples/"

#Optional: output directory, default is local running directory
outputDir   = f"outputs/hists/"


# optional: ncpus, default is 4, -1 uses all cores available
nCPUS       = -1

# scale the histograms with the cross-section and integrated luminosity
doScale = True
intLumi = 10800000.0 # 10.8 /ab for 240 GeV


# define some binning for various histograms
bins_p_mu = (250, 0, 250) # 100 MeV bins
bins_m_ll = (250, 0, 250) # 100 MeV bins
bins_p_ll = (250, 0, 250) # 100 MeV bins
bins_recoil = (250, 0, 250) # 1 GeV bins
bins_cosThetaMiss = (10000, 0, 1)

bins_theta = (500, -5, 5)
bins_eta = (600, -3, 3)
bins_phi = (500, -5, 5)

bins_count = (50, 0, 50)
bins_charge = (10, -5, 5)
bins_iso = (500, 0, 5)

bins_recoil_final = (200, 120, 140) # 100 MeV bins

bins_bool = (2, 0, 2) # boolean

# build_graph function that contains the analysis logic, cuts and histograms (mandatory)
def build_graph(df, dataset):

    results = []
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")

    results.append(df.Histo1D(("missingEnergy", "", *bins_p_mu), "missingEnergy"))

    # muons hists
    results.append(df.Histo1D(("muons_p", "", *bins_p_mu), "muons_p"))
    results.append(df.Histo1D(("muons_theta", "", *bins_theta), "muons_theta"))
    results.append(df.Histo1D(("muons_phi", "", *bins_phi), "muons_phi"))
    results.append(df.Histo1D(("muons_q", "", *bins_charge), "muons_q"))
    results.append(df.Histo1D(("muons_no", "", *bins_count), "muons_no"))
    results.append(df.Histo1D(("muons_iso", "", *bins_bool), "muons_is_iso"))

    # electrons hists
    results.append(df.Histo1D(("electrons_p", "", *bins_p_mu), "electrons_p"))
    results.append(df.Histo1D(("electrons_theta", "", *bins_theta), "electrons_theta"))
    results.append(df.Histo1D(("electrons_phi", "", *bins_phi), "electrons_phi"))
    results.append(df.Histo1D(("electrons_q", "", *bins_charge), "electrons_q"))
    results.append(df.Histo1D(("electrons_no", "", *bins_count), "electrons_no"))
    results.append(df.Histo1D(("electrons_iso", "", *bins_bool), "electrons_is_iso"))

    return results, weightsum

