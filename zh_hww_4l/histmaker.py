
flavor = "ee" # mumu, ee
# flavor = "mumu" # mumu, ee

# list of processes (mandatory)
processList_mumu = {
    'p8_ee_ZZ_ecm240':{'fraction': 1},
    'p8_ee_WW_ecm240':{'fraction': 1}, 
    'wzp6_ee_mumuH_HWW_ecm240':{'fraction': 1},
}

processList_ee = {
    'p8_ee_ZZ_ecm240':{'fraction': 1},
    'p8_ee_WW_ecm240':{'fraction': 1}, 
    'wzp6_ee_eeH_HWW_ecm240':{'fraction': 1},
}

if flavor == "mumu":
    processList = processList_mumu
    leps = 'muons'
else:
    processList = processList_ee
    leps = 'electrons'

# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
prodTag     = "FCCee/winter2023/IDEA/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json"

# additional/custom C++ functions, defined in header files (optional)
includePaths = ["../functions.h"]

# Define the input dir (optional)
#inputDir    = "outputs/FCCee/higgs/mH-recoil/mumu/stage1"
#inputDir    = "localSamples/"

#Optional: output directory, default is local running directory
outputDir   = f"outputs/hists/{flavor}/"


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


# build_graph function that contains the analysis logic, cuts and histograms (mandatory)
def build_graph(df, dataset):

    results = []
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")


    # define collections
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")


    # For signal events, keep only fully-leptonic WW decays (truth-level selection)
    if "wzp6_ee_eeH_HWW_ecm240" in dataset or "wzp6_ee_mumuH_HWW_ecm240" in dataset:
        df = df.Define("ww_leptonic", "FCCAnalyses::ZHfunctions::is_ww_leptonic(Particle, Particle1)")
        df = df.Filter("ww_leptonic")


    # define muons
    df = df.Alias("Muon0", "Muon#0.index")
    df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)")
    df = df.Define("muons_all_p", "FCCAnalyses::ReconstructedParticle::get_p(muons_all)")
    
    df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::sel_p(10)(muons_all)")
    df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
    df = df.Define("muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons)")
    df = df.Define("muons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(muons)")
    df = df.Define("muons_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")
    df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")

    # compute the muon isolation and store muons with an isolation cut of 0.25 in a separate column muons_sel_iso
    df = df.Define("muons_iso", "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(muons, ReconstructedParticles)")
    df = df.Define("muons_sel_iso", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(muons, muons_iso)")


    # define electrons
    df = df.Alias("Electron0", "Electron#0.index")
    df = df.Define("electrons_all", "FCCAnalyses::ReconstructedParticle::get(Electron0, ReconstructedParticles)")
    df = df.Define("electrons_all_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons_all)")
    
    df = df.Define("electrons", "FCCAnalyses::ReconstructedParticle::sel_p(10)(electrons_all)")
    df = df.Define("electrons_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons)")
    df = df.Define("electrons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(electrons)")
    df = df.Define("electrons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(electrons)")
    df = df.Define("electrons_q", "FCCAnalyses::ReconstructedParticle::get_charge(electrons)")
    df = df.Define("electrons_no", "FCCAnalyses::ReconstructedParticle::get_n(electrons)")

    # compute the muon isolation and store muons with an isolation cut of 0.25 in a separate column muons_sel_iso
    df = df.Define("electrons_iso", "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(electrons, ReconstructedParticles)")
    df = df.Define("electrons_sel_iso", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(electrons, electrons_iso)")


    # baseline histograms, before any selection cuts (store with _cut0)
    results.append(df.Histo1D(("muons_all_p_cut0", "", *bins_p_mu), "muons_all_p"))
    results.append(df.Histo1D(("muons_p_cut0", "", *bins_p_mu), "muons_p"))
    results.append(df.Histo1D(("muons_theta_cut0", "", *bins_theta), "muons_theta"))
    results.append(df.Histo1D(("muons_phi_cut0", "", *bins_phi), "muons_phi"))
    results.append(df.Histo1D(("muons_q_cut0", "", *bins_charge), "muons_q"))
    results.append(df.Histo1D(("muons_no_cut0", "", *bins_count), "muons_no"))
    results.append(df.Histo1D(("muons_iso_cut0", "", *bins_iso), "muons_iso"))

    results.append(df.Histo1D(("electrons_all_p_cut0", "", *bins_p_mu), "electrons_all_p"))
    results.append(df.Histo1D(("electrons_p_cut0", "", *bins_p_mu), "electrons_p"))
    results.append(df.Histo1D(("electrons_theta_cut0", "", *bins_theta), "electrons_theta"))
    results.append(df.Histo1D(("electrons_phi_cut0", "", *bins_phi), "electrons_phi"))
    results.append(df.Histo1D(("electrons_q_cut0", "", *bins_charge), "electrons_q"))
    results.append(df.Histo1D(("electrons_no_cut0", "", *bins_count), "electrons_no"))
    results.append(df.Histo1D(("electrons_iso_cut0", "", *bins_iso), "electrons_iso"))


    #########
    ### CUT 0: all events
    #########
    df = df.Define("cut0", "0")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut0"))


    #########
    ### CUT 1: at least 1 muon with at least one isolated one
    #########
    df = df.Filter(f"{leps}_no >= 1 && {leps}_sel_iso.size() > 0")
    df = df.Define("cut1", "1")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut1"))


    #########
    ### CUT 2: at least 2 opposite-sign (OS) leptons
    #########
    df = df.Filter(f"{leps}_no >= 2 && abs(Sum({leps}_q)) < {leps}_q.size()")
    df = df.Define("cut2", "2")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut2"))

    # now we build the Z resonance based on the available leptons.
    # the function resonanceBuilder_mass_recoil returns the best lepton pair compatible with the Z mass (91.2 GeV) and recoil at 125 GeV
    # the argument 0.4 gives a weight to the Z mass and the recoil mass in the chi2 minimization
    # technically, it returns a ReconstructedParticleData object with index 0 the di-lepton system, index 1 and 2 the leptons of the pair
    df = df.Define("zbuilder_result", f"FCCAnalyses::ZHfunctions::resonanceBuilder_mass_recoil(91.2, 125, 0.4, 240, false)({leps}, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    df = df.Define("zll", "Vec_rp{zbuilder_result[0]}") # the Z
    df = df.Define("zll_leps", "Vec_rp{zbuilder_result[1],zbuilder_result[2]}") # the leptons 
    df = df.Define("zll_m", "FCCAnalyses::ReconstructedParticle::get_mass(zll)[0]") # Z mass
    df = df.Define("zll_p", "FCCAnalyses::ReconstructedParticle::get_p(zll)[0]") # momentum of the Z
    df = df.Define("zll_recoil", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zll)") # compute the recoil based on the reconstructed Z
    df = df.Define("zll_recoil_m", "FCCAnalyses::ReconstructedParticle::get_mass(zll_recoil)[0]") # recoil mass
    df = df.Define("zll_leps_p", "FCCAnalyses::ReconstructedParticle::get_p(zll_leps)") # get the momentum of the 2 leptons from the Z resonance

df = df.Define("leps_WW", "FCCAnasyss::RecoPartice::remove(zll_leps, muons)")
df = df.Define("leps_WW", "FCCAnasyss::RecoPartice::remove(zll_leps, electrons)")
'''
1. calculate signal eff
2. compute S/sqrt(B) = (S1+S2)/sqrt(B1+B2)
3. Compare with different selections

'''

    #########
    ### CUT 3: Z mass window
    #########
    results.append(df.Histo1D(("zll_m_cut2", "", *bins_m_ll), "zll_m"))
    df = df.Filter("zll_m > 86 && zll_m < 96")
    df = df.Define("cut3", "3")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut3"))


    #########
    ### CUT 4: Z momentum
    #########
    results.append(df.Histo1D(("zll_p_cut3", "", *bins_p_ll), "zll_p"))
    df = df.Filter("zll_p > 20 && zll_p < 70")
    df = df.Define("cut4", "4")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut4"))


    #########
    ### CUT 5: cosThetaMiss
    #########  
    df = df.Define("missingEnergy", "FCCAnalyses::ZHfunctions::missingEnergy(240., ReconstructedParticles)")
    df = df.Define("cosTheta_miss", "FCCAnalyses::ZHfunctions::get_cosTheta_miss(missingEnergy)")
    results.append(df.Histo1D(("cosThetaMiss_cut4", "", *bins_cosThetaMiss), "cosTheta_miss")) # plot it before the cut

    df = df.Filter("cosTheta_miss < 0.98")
    df = df.Define("cut5", "5")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut5"))


    #########
    ### CUT 6: recoil mass window
    #########
    results.append(df.Histo1D(("zll_recoil_m", "", *bins_recoil), "zll_recoil_m")) # plot it before the cut
    df = df.Filter("zll_recoil_m < 140 && zll_recoil_m > 120")
    df = df.Define("cut6", "6")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut6"))


    #########
    ### CUT 7: at least 4 leptons (to further suppress WW->lvlv)
    #########
    df = df.Define("leptons_no", "muons_no + electrons_no")
    results.append(df.Histo1D(("leptons_no", "", *bins_count), "leptons_no"))
    df = df.Filter("leptons_no >= 4")
    df = df.Define("cut7", "7")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut7"))


    #########
    ### CUT 8: at least 4 isolated leptons (to further suppress WW->lvlv)
    #########
    df = df.Filter("muons_sel_iso.size() + electrons_sel_iso.size() >= 4")
    df = df.Define("cut8", "8")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut8"))


    #########
    ### CUT 9: at least 2 pairs of 2 opposite-sign (OS) leptons
    #########
    df = df.Filter("abs(Sum(muons_q)) + abs(Sum(electrons_q)) <= muons_q.size() + electrons_q.size() -4")
    df = df.Define("cut9", "9")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut9"))


    ########################
    # Final histograms
    ########################
    results.append(df.Histo1D(("zll_m_final", "", *bins_m_ll), "zll_m"))
    results.append(df.Histo1D(("zll_recoil_m_final", "", *bins_recoil_final), "zll_recoil_m"))
    results.append(df.Histo1D(("zll_p_final", "", *bins_p_ll), "zll_p"))
    results.append(df.Histo1D(("zll_leps_p_final", "", *bins_p_mu), "zll_leps_p"))


    return results, weightsum

