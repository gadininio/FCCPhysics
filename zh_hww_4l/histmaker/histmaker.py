
'''
Run this script with the command:
    ecm=365 sel=false fccanalysis run histmaker.py
    ecm=365 sel=true loose=true fccanalysis run histmaker.py
    ecm=365 sel=true loose=false fccanalysis run histmaker.py

Full run:
    ecm=365 sel=true loose=false fullrun=true fccanalysis run histmaker.py
    
'''


# fraction = 0.2
# nchunks = 1
# debug = False
# fullrun = False
# apply_selections = True
# is_loose = True 

import os
fraction = float(os.environ.get("fraction", 0.2))
nchunks = int(os.environ.get("nchunks", 1))
debug = os.environ.get("debug", "False").lower() in ("true", "1")
fullrun = os.environ.get("fullrun", "False").lower() in ("true", "1")
apply_selections = os.environ.get("sel", "True").lower() in ("true", "1")
is_loose = os.environ.get("loose", "True").lower() in ("true", "1")
ecm = os.environ.get("ecm", "240")

print(f"Running with ecm={ecm} GeV, apply_selections={apply_selections}, is_loose={is_loose}, debug={debug}, fullrun={fullrun}")

if fullrun and not debug:
    fraction = 1
    nchunks = 50

# list of processes (mandatory)
if ecm == '240':
    processList_mumu = {
        'p8_ee_ZZ_ecm240':{'fraction': fraction, 'chunks': nchunks},
        'p8_ee_WW_ecm240':{'fraction': fraction, 'chunks': nchunks},
        # 'wzp6_ee_mumu_ecm240':{'fraction': fraction, 'chunks': nchunks},
        # 'wzp6_ee_tautau_ecm240':{'fraction': fraction, 'chunks': nchunks},
        'wzp6_ee_mumuH_HWW_llnunu_ecm240':{'fraction': 1},
    }

    processList_ee = {
        'p8_ee_ZZ_ecm240':{'fraction': fraction, 'chunks': nchunks},
        'p8_ee_WW_ecm240':{'fraction': fraction, 'chunks': nchunks},
        # 'wzp6_ee_ee_Mee_30_150_ecm240':{'fraction': fraction, 'chunks': nchunks},
        # 'wzp6_ee_tautau_ecm240':{'fraction': fraction, 'chunks': nchunks},
        'wzp6_ee_eeH_HWW_llnunu_ecm240':{'fraction': 1},
    }

elif ecm == '365':
    processList_mumu = {
        'p8_ee_tt_ecm365':{'fraction': fraction, 'chunks': nchunks},
        'p8_ee_ZZ_ecm365':{'fraction': fraction, 'chunks': nchunks},
        # 'p8_ee_WW_ee_ecm365':{'fraction': fraction, 'chunks': nchunks},
        # 'p8_ee_WW_mumu_ecm365':{'fraction': fraction, 'chunks': nchunks},
        'p8_ee_WW_ecm365':{'fraction': fraction, 'chunks': nchunks},
        # 'wzp6_ee_mumu_ecm365':{'fraction': fraction, 'chunks': nchunks},
        # 'wzp6_ee_tautau_ecm365':{'fraction': fraction, 'chunks': nchunks},
        'wzp6_ee_mumuH_HWW_ecm365':{'fraction': 1},
    }

    processList_ee = {
        'p8_ee_tt_ecm365':{'fraction': fraction, 'chunks': nchunks},
        'p8_ee_ZZ_ecm365':{'fraction': fraction, 'chunks': nchunks},
        # 'p8_ee_WW_ee_ecm365':{'fraction': fraction, 'chunks': nchunks},
        # 'p8_ee_WW_mumu_ecm365':{'fraction': fraction, 'chunks': nchunks},
        'p8_ee_WW_ecm365':{'fraction': fraction, 'chunks': nchunks},
        # 'wzp6_ee_ee_Mee_30_150_ecm365':{'fraction': fraction, 'chunks': nchunks},
        # 'wzp6_ee_tautau_ecm365':{'fraction': fraction, 'chunks': nchunks},
        'wzp6_ee_eeH_HWW_ecm365':{'fraction': 1},
    }

processList = {f'wzp6_ee_mumuH_HWW_ecm{ecm}':{'fraction': 0.2}} if debug else processList_mumu | processList_ee


# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
prodTag     = "FCCee/winter2023/IDEA/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json"

# additional/custom C++ functions, defined in header files (optional)
includePaths = ["../../functions.h"]

# Define the input dir (optional)
#inputDir    = "outputs/FCCee/higgs/mH-recoil/mumu/stage1"
#inputDir    = "localSamples/"

#Optional: output directory, default is local running directory
output_fix = ""
if debug: output_fix = "debug/"
else:
    # add date-time stamp to output folder
    from datetime import datetime
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d_%H%M%S")
    dt_string = ''
    output_fix = f"{'full_' if fullrun else ''}{'nosel_' if not apply_selections else ('loose_' if is_loose else 'tight_')}{dt_string}/"
    # if last charachter is '_', remove it
    if output_fix.endswith('_'):
        output_fix = output_fix[:-1]
outputDir   = f"../../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/hists/{output_fix}/"


# optional: ncpus, default is 4, -1 uses all cores available
nCPUS       = -1

# scale the histograms with the cross-section and integrated luminosity
doScale = True
intLumi = 10.8e6 if ecm == '240' else 3e6  # 10.8 /ab for 240 GeV, 3 /ab for 365 GeV

n_bins = int(ecm) + 10

# define some binning for various histograms
bins_p_mu = (n_bins, 0, n_bins) # 100 MeV bins
bins_m_ll = (n_bins, 0, n_bins) # 100 MeV bins
bins_m_ll_large = (n_bins*2, 0, n_bins*2) # 100 MeV bins
bins_p_ll = (n_bins, 0, n_bins) # 100 MeV bins
bins_recoil = (n_bins, 0, n_bins) # 1 GeV bins
bins_cosThetaMiss = (10000, 0, 1)

bins_theta = (500, -5, 5)
bins_eta = (600, -3, 3)
bins_phi = (500, -5, 5)
bins_dR = (1000, -10, 10)

bins_count = (50, 0, 50)
bins_charge = (10, -5, 5)
bins_iso = (500, 0, 5)

# bins_recoil_final = (200, 120, 140) # 100 MeV bins
bins_recoil_final = (n_bins*10, 0, n_bins) # 0.1 GeV bins



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
    # if "wzp6_ee_eeH_HWW_ecm240" in dataset or "wzp6_ee_mumuH_HWW_ecm240" in dataset:
    if f"wzp6_ee_eeH_HWW" in dataset or f"wzp6_ee_mumuH_HWW" in dataset:
        print(f"Applying truth-level fully-leptonic WW decays cut on {dataset}")
        df = df.Define("ww_leptonic", "FCCAnalyses::ZHfunctions::is_ww_leptonic(Particle, Particle1)")
        df = df.Filter("ww_leptonic")


    # define muons
    df = df.Alias("Muon0", "Muon#0.index")
    df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)")
    df = df.Define("muons_all_p", "FCCAnalyses::ReconstructedParticle::get_p(muons_all)")
    
    df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::sel_p(5)(muons_all)")
    df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
    df = df.Define("muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons)")
    df = df.Define("muons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(muons)")
    df = df.Define("muons_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")
    df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")

    # # compute the muon isolation and store muons with an isolation cut of 0.25 in a separate column muons_sel_iso
    # df = df.Define("muons_iso", "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(muons, ReconstructedParticles)")
    # df = df.Define("muons_sel_iso", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(muons, muons_iso)")


    # define electrons
    df = df.Alias("Electron0", "Electron#0.index")
    df = df.Define("electrons_all", "FCCAnalyses::ReconstructedParticle::get(Electron0, ReconstructedParticles)")
    df = df.Define("electrons_all_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons_all)")
    
    df = df.Define("electrons", "FCCAnalyses::ReconstructedParticle::sel_p(5)(electrons_all)")
    df = df.Define("electrons_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons)")
    df = df.Define("electrons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(electrons)")
    df = df.Define("electrons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(electrons)")
    df = df.Define("electrons_q", "FCCAnalyses::ReconstructedParticle::get_charge(electrons)")
    df = df.Define("electrons_no", "FCCAnalyses::ReconstructedParticle::get_n(electrons)")

    # # compute the muon isolation and store muons with an isolation cut of 0.25 in a separate column muons_sel_iso
    # df = df.Define("electrons_iso", "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(electrons, ReconstructedParticles)")
    # df = df.Define("electrons_sel_iso", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(electrons, electrons_iso)")


    # baseline histograms, before any selection cuts (store with _cut0)
    results.append(df.Histo1D(("muons_all_p_cut0", "", *bins_p_mu), "muons_all_p"))
    results.append(df.Histo1D(("muons_p_cut0", "", *bins_p_mu), "muons_p"))
    results.append(df.Histo1D(("muons_theta_cut0", "", *bins_theta), "muons_theta"))
    results.append(df.Histo1D(("muons_phi_cut0", "", *bins_phi), "muons_phi"))
    results.append(df.Histo1D(("muons_q_cut0", "", *bins_charge), "muons_q"))
    results.append(df.Histo1D(("muons_no_cut0", "", *bins_count), "muons_no"))
    # results.append(df.Histo1D(("muons_iso_cut0", "", *bins_iso), "muons_iso"))

    results.append(df.Histo1D(("electrons_all_p_cut0", "", *bins_p_mu), "electrons_all_p"))
    results.append(df.Histo1D(("electrons_p_cut0", "", *bins_p_mu), "electrons_p"))
    results.append(df.Histo1D(("electrons_theta_cut0", "", *bins_theta), "electrons_theta"))
    results.append(df.Histo1D(("electrons_phi_cut0", "", *bins_phi), "electrons_phi"))
    results.append(df.Histo1D(("electrons_q_cut0", "", *bins_charge), "electrons_q"))
    results.append(df.Histo1D(("electrons_no_cut0", "", *bins_count), "electrons_no"))
    # results.append(df.Histo1D(("electrons_iso_cut0", "", *bins_iso), "electrons_iso"))



    #########
    ### CUT 0: all events
    #########
    df = df.Define("cut0", "0")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut0"))


    #########
    ### CUT 1: exactly 4 leptons (add isolation later)
    #########
    # df = df.Filter(f"{leps}_no >= 1 && {leps}_sel_iso.size() > 0")
    # df = df.Filter(f"{leps}_no == 4")
    
    df = df.Define("n_leptons", "muons_no + electrons_no")
    results.append(df.Histo1D(("n_leptons_cut0", "", *bins_count), "n_leptons"))
    
    df = df.Filter("n_leptons == 4")
    df = df.Define("cut1", "1")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut1"))


    #########
    ### CUT 2: at least 2 opposite-sign (OS) lepton pairs
    #########
    # df = df.Filter(f"{leps}_no >= 2 && abs(Sum({leps}_q)) < {leps}_q.size()")
    # df = df.Filter(f"abs(Sum({leps}_q)) <= {leps}_q.size() - 4")
    df = df.Filter(f"abs(Sum(muons_q) + Sum(electrons_q)) <= muons_q.size() + electrons_q.size() - 4")
    df = df.Define("cut2", "2")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut2"))


    #########
    ### CUT 3: at least one same-flavor (SF) lepton pair
    #########
    df = df.Filter("(muons_no >= 2) || (electrons_no >= 2)")
    df = df.Define("cut3", "3")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut3"))


    #########
    ### CUT 4: leptons p: leading muon p [25, 80] GeV, subleading muon p [15, 80] GeV, third muon p [10,80] GeV, fourth muon p [10,75] GeV
    #########
    df = df.Define("leptons0", "FCCAnalyses::ReconstructedParticle::merge(muons, electrons)")
    df = df.Define("leptons", "FCCAnalyses::ZHfunctions::sortByPt(leptons0)")
    df = df.Define("leptons_p", "FCCAnalyses::ReconstructedParticle::get_p(leptons)")

    df = df.Define("lep0_p", "leptons_p[0]")
    df = df.Define("lep1_p", "leptons_p[1]")
    df = df.Define("lep2_p", "leptons_p[2]")
    df = df.Define("lep3_p", "leptons_p[3]")
    
    results.append(df.Histo1D(("lep0_p_cut2", "", *bins_p_mu), "lep0_p"))
    results.append(df.Histo1D(("lep1_p_cut2", "", *bins_p_mu), "lep1_p"))
    results.append(df.Histo1D(("lep2_p_cut2", "", *bins_p_mu), "lep2_p"))
    results.append(df.Histo1D(("lep3_p_cut2", "", *bins_p_mu), "lep3_p"))
    
    if apply_selections:
        if ecm == '240':
            if is_loose:
                df = df.Filter("lep0_p > 20 && lep0_p < 85")
                df = df.Filter("lep1_p > 10 && lep1_p < 80")
                df = df.Filter("lep2_p > 10 && lep2_p < 80")
                df = df.Filter("lep3_p > 10 && lep3_p < 75")
            else:
                df = df.Filter("lep0_p > 25 && lep0_p < 80")
                df = df.Filter("lep1_p > 15 && lep1_p < 80")
                df = df.Filter("lep2_p > 10 && lep2_p < 80")
                df = df.Filter("lep3_p > 10 && lep3_p < 75")
        elif ecm == '365':
            if is_loose:
                results.append(df.Histo1D(("lep0_p_cut2a", "", *bins_p_mu), "lep0_p"))
                df = df.Filter("lep0_p > 70 && lep0_p < 155")
                results.append(df.Histo1D(("lep1_p_cut2b", "", *bins_p_mu), "lep1_p"))
                df = df.Filter("lep1_p > 25 && lep1_p < 105")
                results.append(df.Histo1D(("lep2_p_cut2c", "", *bins_p_mu), "lep2_p"))
                df = df.Filter("lep2_p > 15 && lep2_p < 80")
                results.append(df.Histo1D(("lep3_p_cut2d", "", *bins_p_mu), "lep3_p"))
                df = df.Filter("lep3_p > 5 && lep3_p < 65")
            else:
                results.append(df.Histo1D(("lep0_p_cut2a", "", *bins_p_mu), "lep0_p"))
                df = df.Filter("lep0_p > 70 && lep0_p < 155")
                results.append(df.Histo1D(("lep1_p_cut2b", "", *bins_p_mu), "lep1_p"))
                df = df.Filter("lep1_p > 25 && lep1_p < 105")
                results.append(df.Histo1D(("lep2_p_cut2c", "", *bins_p_mu), "lep2_p"))
                df = df.Filter("lep2_p > 15 && lep2_p < 80")
                results.append(df.Histo1D(("lep3_p_cut2d", "", *bins_p_mu), "lep3_p"))
                df = df.Filter("lep3_p > 5 && lep3_p < 65")
    df = df.Define("cut4", "4")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut4"))


    #########
    ### Reconstruct the Z->ll candidate
    #########
    # if debug:
    #     df = df.Define("test", "FCCAnalyses::ZHfunctions::test()")
        # df.Display(["test"]).Print()

    # Now we build the Z resonance based on the available leptons.
    # The function resonanceBuilder_mass_recoil_advanced returns the best lepton pair compatible with the Z mass (91.2 GeV) and recoil at 125 GeV, out of the 4 leptons, and the two remaining leptons coming from the W's.
    # The argument 0.4 gives a weight to the Z mass and the recoil mass in the chi2 minimization.
    # Technically, it returns a ReconstructedParticleData object with index 0 the Z->ll di-lepton system, index 1 and 2 the leptons of the pair, and index 3 and 4 the other two leptons.
    # If no pair is found, the returned vector is empty.
    # We then require that at least one pair was found (size>=5) to keep the event.
    df = df.Define("zbuilder_result", f"FCCAnalyses::ZHfunctions::resonanceBuilder_mass_recoil_advanced(91.2, 125, 0.4, {ecm}, false)(muons, electrons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    df = df.Filter("zbuilder_result.size() >= 5") # make sure at least one pair was found (and additional two leptons)

    df = df.Define("zll", "Vec_rp{zbuilder_result[0]}") # the Z
    df = df.Define("zll_tlv", "FCCAnalyses::ReconstructedParticle::get_tlv(zll, 0)")
    df = df.Define("zll_m", "FCCAnalyses::ReconstructedParticle::get_mass(zll)[0]") # Z mass
    df = df.Define("zll_p", "FCCAnalyses::ReconstructedParticle::get_p(zll)[0]") # momentum of the Z
    df = df.Define("zll_theta", "FCCAnalyses::ReconstructedParticle::get_theta(zll)[0]") # momentum of the Z
    df = df.Define("zll_phi", "FCCAnalyses::ReconstructedParticle::get_phi(zll)[0]") # momentum of the Z

    # results.append(df.Histo1D(("zll_m_cut4", "", *bins_m_ll), "zll_m"))
    results.append(df.Histo1D(("zll_p_cut4", "", *bins_p_ll), "zll_p"))
    results.append(df.Histo1D(("zll_theta_cut4", "", *bins_theta), "zll_theta"))
    results.append(df.Histo1D(("zll_phi_cut4", "", *bins_phi), "zll_phi"))

    ## Recoil mass
    df = df.Define("zll_recoil", f"FCCAnalyses::ReconstructedParticle::recoilBuilder({ecm})(zll)") # compute the recoil based on the reconstructed Z
    df = df.Define("zll_recoil_m", "FCCAnalyses::ReconstructedParticle::get_mass(zll_recoil)[0]") # recoil mass
    results.append(df.Histo1D(("zll_recoil_m_cut4", "", *bins_recoil), "zll_recoil_m")) # plot it before the cut

    ## Study the Z-lepton candidates
    df = df.Define("zll_leps", "Vec_rp{zbuilder_result[1],zbuilder_result[2]}") # Z-lepton candidates
    df = df.Define("zll_leps_p", "FCCAnalyses::ReconstructedParticle::get_p(zll_leps)") # get the momentum of these 2 leptons
    df = df.Define("zll_leps_theta", "FCCAnalyses::ReconstructedParticle::get_theta(zll_leps)") # get the theta of these 2 leptons
    df = df.Define("zll_leps_phi", "FCCAnalyses::ReconstructedParticle::get_phi(zll_leps)") # get the phi of these 2 leptons
    
    df = df.Define("zll_lep0_p", "zll_leps_p[0]")
    df = df.Define("zll_lep0_theta", "zll_leps_theta[0]")
    df = df.Define("zll_lep0_phi", "zll_leps_phi[0]")
    df = df.Define("zll_lep1_p", "zll_leps_p[1]")
    df = df.Define("zll_lep1_theta", "zll_leps_theta[1]")
    df = df.Define("zll_lep1_phi", "zll_leps_phi[1]")
    results.append(df.Histo1D(("zll_lep0_p_cut4", "", *bins_p_mu), "zll_lep0_p"))
    results.append(df.Histo1D(("zll_lep0_theta_cut4", "", *bins_theta), "zll_lep0_theta"))
    results.append(df.Histo1D(("zll_lep0_phi_cut4", "", *bins_phi), "zll_lep0_phi"))
    results.append(df.Histo1D(("zll_lep1_p_cut4", "", *bins_p_mu), "zll_lep1_p"))
    results.append(df.Histo1D(("zll_lep1_theta_cut4", "", *bins_theta), "zll_lep1_theta"))
    results.append(df.Histo1D(("zll_lep1_phi_cut4", "", *bins_phi), "zll_lep1_phi"))

    df = df.Define("zll_lep0_tlv", "FCCAnalyses::ReconstructedParticle::get_tlv(zll_leps, 0)")
    df = df.Define("zll_lep1_tlv", "FCCAnalyses::ReconstructedParticle::get_tlv(zll_leps, 1)")
    df = df.Define("zll_leps_dR", "zll_lep0_tlv.DeltaR(zll_lep1_tlv)")
    results.append(df.Histo1D(("zll_leps_dR_cut4", "", *bins_dR), "zll_leps_dR"))

    df = df.Define("zll_leps_category", "FCCAnalyses::ZHfunctions::getDileptonCategory(zll_leps)")
    results.append(df.Histo1D(("zll_leps_category_cut4", "", 4, -1, 3), "zll_leps_category"))

    df = df.Define("zll_lep0_p_index", "FCCAnalyses::ZHfunctions::findIndex(zll_lep0_p, {lep0_p, lep1_p, lep2_p, lep3_p})")
    df = df.Define("zll_lep1_p_index", "FCCAnalyses::ZHfunctions::findIndex(zll_lep1_p, {lep0_p, lep1_p, lep2_p, lep3_p})")
    results.append(df.Histo1D(("zll_lep0_p_index_cut4", "", 5, -1, 4), "zll_lep0_p_index"))  # Which lepton is zll_lep0_p?
    results.append(df.Histo1D(("zll_lep1_p_index_cut4", "", 5, -1, 4), "zll_lep1_p_index"))  # Which lepton is zll_lep1_p?
    
    ## Study the WW-lepton candidates
    df = df.Define("WW_leps", "Vec_rp{zbuilder_result[3],zbuilder_result[4]}") # the leptons 
    df = df.Define("WW_leps_p", "FCCAnalyses::ReconstructedParticle::get_p(WW_leps)")
    df = df.Define("WW_leps_theta", "FCCAnalyses::ReconstructedParticle::get_theta(WW_leps)")
    df = df.Define("WW_leps_phi", "FCCAnalyses::ReconstructedParticle::get_phi(WW_leps)")

    df = df.Define("WW_lep0_p", "WW_leps_p[0]")
    df = df.Define("WW_lep0_theta", "WW_leps_theta[0]")
    df = df.Define("WW_lep0_phi", "WW_leps_phi[0]")
    df = df.Define("WW_lep1_p", "WW_leps_p[1]")
    df = df.Define("WW_lep1_theta", "WW_leps_theta[1]")
    df = df.Define("WW_lep1_phi", "WW_leps_phi[1]")
    results.append(df.Histo1D(("WW_lep0_p_cut4", "", *bins_p_mu), "WW_lep0_p"))
    results.append(df.Histo1D(("WW_lep0_theta_cut4", "", *bins_theta), "WW_lep0_theta"))
    results.append(df.Histo1D(("WW_lep0_phi_cut4", "", *bins_phi), "WW_lep0_phi"))
    results.append(df.Histo1D(("WW_lep1_p_cut4", "", *bins_p_mu), "WW_lep1_p"))
    results.append(df.Histo1D(("WW_lep1_theta_cut4", "", *bins_theta), "WW_lep1_theta"))
    results.append(df.Histo1D(("WW_lep1_phi_cut4", "", *bins_phi), "WW_lep1_phi"))
    
    df = df.Define("WW_lep0_tlv", "FCCAnalyses::ReconstructedParticle::get_tlv(WW_leps, 0)")
    df = df.Define("WW_lep1_tlv", "FCCAnalyses::ReconstructedParticle::get_tlv(WW_leps, 1)")
    df = df.Define("WW_leps_dR", "WW_lep0_tlv.DeltaR(WW_lep1_tlv)")
    results.append(df.Histo1D(("WW_leps_dR_cut4", "", *bins_dR), "WW_leps_dR"))

    df = df.Define("WW_leps_category", "FCCAnalyses::ZHfunctions::getDileptonCategory(WW_leps)")
    results.append(df.Histo1D(("WW_leps_category_cut4", "", 4, -1, 3), "WW_leps_category"))
    
    df = df.Define("WW_lep0_p_index", "FCCAnalyses::ZHfunctions::findIndex(WW_lep0_p, {lep0_p, lep1_p, lep2_p, lep3_p})")
    df = df.Define("WW_lep1_p_index", "FCCAnalyses::ZHfunctions::findIndex(WW_lep1_p, {lep0_p, lep1_p, lep2_p, lep3_p})")
    results.append(df.Histo1D(("WW_lep0_p_index_cut4", "", 5, -1, 4), "WW_lep0_p_index"))  # Which lepton is WW_lep0_p?
    results.append(df.Histo1D(("WW_lep1_p_index_cut4", "", 5, -1, 4), "WW_lep1_p_index"))  # Which lepton is WW_lep1_p?    
    
    ## Build the WW system using the two leptons not coming from the Z and the missing energy vector
    df = df.Define("missingEnergy_vec", f"FCCAnalyses::ZHfunctions::missingEnergy({ecm}, ReconstructedParticles)")
    df = df.Define("missingEnergy_tlv", "FCCAnalyses::ReconstructedParticle::get_tlv(missingEnergy_vec, 0)")
    df = df.Define("WW_tlv", "missingEnergy_tlv + WW_lep0_tlv + WW_lep1_tlv")
    df = df.Define("WW_p", "WW_tlv.P()")
    df = df.Define("WW_theta", "WW_tlv.Theta()")
    df = df.Define("WW_phi", "WW_tlv.Phi()")
    df = df.Define("WW_mass", "WW_tlv.M()")
    results.append(df.Histo1D(("WW_mass_cut4", "", *bins_m_ll_large), "WW_mass"))
    results.append(df.Histo1D(("WW_p_cut4", "", *bins_p_mu), "WW_p"))
    results.append(df.Histo1D(("WW_theta_cut4", "", *bins_theta), "WW_theta"))
    results.append(df.Histo1D(("WW_phi_cut4", "", *bins_phi), "WW_phi"))

    ## dR(Z, WW)
    df = df.Define("zll_WW_dR", "WW_tlv.DeltaR(zll_tlv)")
    results.append(df.Histo1D(("zll_WW_dR_cut4", "", *bins_dR), "zll_WW_dR"))


    #########
    ### CUT 5: Z mass window
    #########
    results.append(df.Histo1D(("zll_m_cut4", "", *bins_m_ll), "zll_m"))  # already done above
    if apply_selections:
        if ecm == '240':
            # df = df.Filter("zll_m > 86 && zll_m < 96")  # tighter cut - smaller significance
            df = df.Filter("zll_m > 76 && zll_m < 106")
        elif ecm == '365':
            df = df.Filter("zll_m > 76 && zll_m < 106")
    df = df.Define("cut5", "5")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut5"))


    #########
    ### CUT 6: Z momentum
    #########
    results.append(df.Histo1D(("zll_p_cut5", "", *bins_p_ll), "zll_p"))
    if apply_selections:
        if ecm == '240':
            df = df.Filter("zll_p > 20 && zll_p < 70")
        elif ecm == '365':
            if is_loose:
                df = df.Filter("zll_p > 35 && zll_p < 155")
            else:
                df = df.Filter("zll_p > 140 && zll_p < 150")
    df = df.Define("cut6", "6")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut6"))


    #########
    ### CUT *: recoil mass window (reconstructed Higgs mass using the recoil method)
    #########
    results.append(df.Histo1D(("zll_recoil_m_cut6", "", *bins_recoil), "zll_recoil_m")) # plot it before the cut
    if apply_selections:
        if ecm == '240':
            if is_loose:
                df = df.Filter("zll_recoil_m < 145 && zll_recoil_m > 120")
            else:
                df = df.Filter("zll_recoil_m < 140 && zll_recoil_m > 120")
        elif ecm == '365':
            if is_loose:
                df = df.Filter("zll_recoil_m < 145 && zll_recoil_m > 120")
            else:
                # pass  # don't apply recoil mass cut for 365 GeV tight selection, as this variable will be used for the fit.
                df = df.Filter("zll_recoil_m < 140 && zll_recoil_m > 120")
    df = df.Define("cut7", "7")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut7"))


    #########
    ### CUT 7: cosThetaMiss
    #########  
    df = df.Define("cosTheta_miss", "FCCAnalyses::ZHfunctions::get_cosTheta_miss(missingEnergy_vec)")
    results.append(df.Histo1D(("cosThetaMiss_cut7", "", *bins_cosThetaMiss), "cosTheta_miss")) # plot it before the cut
    if apply_selections:
        df = df.Filter("cosTheta_miss < 0.98")
    df = df.Define("cut8", "8")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut8"))


    #########
    ### CUT 8: missingEnergy
    #########  
    df = df.Define("missingEnergy", "FCCAnalyses::ZHfunctions::get_missing_energy(missingEnergy_vec)")
    results.append(df.Histo1D(("missingEnergy_cut8", "", *bins_p_mu), "missingEnergy")) # plot it before the cut
    if apply_selections:
        if ecm == '240':
            if is_loose:
                df = df.Filter("missingEnergy > 20 && missingEnergy < 120")
            else:
                df = df.Filter("missingEnergy > 30 && missingEnergy < 110")
        elif ecm == '365':
            if is_loose:
                df = df.Filter("missingEnergy > 20 && missingEnergy < 170")
            else:
                df = df.Filter("missingEnergy > 30 && missingEnergy < 160")
    df = df.Define("cut9", "9")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut9"))


    #########
    ### CUT 9: WW system mass window
    #########  
    results.append(df.Histo1D(("WW_mass_cut9", "", *bins_m_ll_large), "WW_mass"))
    if apply_selections:
        if ecm == '240':
            if is_loose:
                df = df.Filter("WW_mass > 60 && WW_mass < 135")
            else:
                df = df.Filter("WW_mass > 80 && WW_mass < 135")
        elif ecm == '365':
            if is_loose:
                df = df.Filter("WW_mass > 50")
            else:
                df = df.Filter("WW_mass > 80 && WW_mass < 130")
    df = df.Define("cut10", "10")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut10"))


    #########
    ### CUT *: WW system momentum
    #########  
    results.append(df.Histo1D(("WW_p_cut10", "", *bins_p_ll), "WW_p"))
    if apply_selections:
        if ecm == '365':
            if is_loose:
                df = df.Filter("WW_p > 100 && WW_p < 150")
            else:
                df = df.Filter("WW_p > 120 && WW_p < 150")
            df = df.Define("cut11", "11")
            results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut11"))
    
    
    #########
    ### CUT 10: dR(l_WW, l_WW)
    #########  
    results.append(df.Histo1D(("WW_leps_dR_cut9", "", *bins_dR), "WW_leps_dR"))
    if apply_selections:
        if ecm == '240':
            df = df.Filter("WW_leps_dR > 0.25")
            df = df.Define("cut11", "11")
            results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut11"))
        elif ecm == '365':
            if is_loose:
                df = df.Filter("WW_leps_dR > 0.1 && WW_leps_dR < 4.0")
            else:
                df = df.Filter("WW_leps_dR > 0.1")
            df = df.Define("cut12", "12")
            results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut12"))

    
    # #########
    # ### CUT 11: dR(WW, ZZ)>0.25
    # #########  
    # results.append(df.Histo1D(("zll_WW_dR_cut10", "", *bins_dR), "zll_WW_dR"))
    # if apply_selections:
    #     if ecm == '365':
    #         df = df.Filter("zll_WW_dR > 3.0 && zll_WW_dR < 4.0")
    #         df = df.Define("cut13", "13")
    #         results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut13"))


    ########################
    # Final histograms
    ########################
    
    # Leptons
    results.append(df.Histo1D(("lep0_p_final", "", *bins_p_mu), "lep0_p"))
    results.append(df.Histo1D(("lep1_p_final", "", *bins_p_mu), "lep1_p"))
    results.append(df.Histo1D(("lep2_p_final", "", *bins_p_mu), "lep2_p"))
    results.append(df.Histo1D(("lep3_p_final", "", *bins_p_mu), "lep3_p"))
    results.append(df.Histo1D(("n_leptons_final", "", *bins_count), "n_leptons"))
    
    # zll system
    results.append(df.Histo1D(("zll_m_final", "", *bins_m_ll), "zll_m"))
    results.append(df.Histo1D(("zll_recoil_m_final", "", *bins_recoil_final), "zll_recoil_m"))
    results.append(df.Histo1D(("zll_p_final", "", *bins_p_ll), "zll_p"))
    results.append(df.Histo1D(("zll_theta_final", "", *bins_theta), "zll_theta"))
    results.append(df.Histo1D(("zll_phi_final", "", *bins_phi), "zll_phi"))

    # zll leptons
    results.append(df.Histo1D(("zll_lep0_p_final", "", *bins_p_mu), "zll_lep0_p"))
    results.append(df.Histo1D(("zll_lep0_theta_final", "", *bins_theta), "zll_lep0_theta"))
    results.append(df.Histo1D(("zll_lep0_phi_final", "", *bins_phi), "zll_lep0_phi"))
    results.append(df.Histo1D(("zll_lep0_p_index_final", "", 5, -1, 4), "zll_lep0_p_index"))  # Which muon is zll_lep0_p?
    results.append(df.Histo1D(("zll_lep1_p_final", "", *bins_p_mu), "zll_lep1_p"))
    results.append(df.Histo1D(("zll_lep1_theta_final", "", *bins_theta), "zll_lep1_theta"))
    results.append(df.Histo1D(("zll_lep1_phi_final", "", *bins_phi), "zll_lep1_phi"))
    results.append(df.Histo1D(("zll_lep1_p_index_final", "", 5, -1, 4), "zll_lep1_p_index"))  # Which muon is zll_lep1_p?
    
    results.append(df.Histo1D(("zll_leps_dR_final", "", *bins_dR), "zll_leps_dR"))
    results.append(df.Histo1D(("zll_leps_category_final", "", 4, -1, 3), "zll_leps_category"))

    # WW system
    results.append(df.Histo1D(("WW_mass_final", "", *bins_m_ll_large), "WW_mass"))
    results.append(df.Histo1D(("WW_p_final", "", *bins_p_ll), "WW_p"))
    results.append(df.Histo1D(("WW_theta_final", "", *bins_theta), "WW_theta"))
    results.append(df.Histo1D(("WW_phi_final", "", *bins_phi), "WW_phi"))

    # WW leptons
    results.append(df.Histo1D(("WW_lep0_p_final", "", *bins_p_mu), "WW_lep0_p"))
    results.append(df.Histo1D(("WW_lep0_theta_final", "", *bins_theta), "WW_lep0_theta"))
    results.append(df.Histo1D(("WW_lep0_phi_final", "", *bins_phi), "WW_lep0_phi"))
    results.append(df.Histo1D(("WW_lep0_p_index_final", "", 5, -1, 4), "WW_lep0_p_index"))  # Which muon is zll_lep0_p?
    results.append(df.Histo1D(("WW_lep1_p_final", "", *bins_p_mu), "WW_lep1_p"))
    results.append(df.Histo1D(("WW_lep1_theta_final", "", *bins_theta), "WW_lep1_theta"))
    results.append(df.Histo1D(("WW_lep1_phi_final", "", *bins_phi), "WW_lep1_phi"))
    results.append(df.Histo1D(("WW_lep1_p_index_final", "", 5, -1, 4), "WW_lep1_p_index"))  # Which muon is zll_lep1_p?

    results.append(df.Histo1D(("WW_leps_dR_final", "", *bins_dR), "WW_leps_dR"))
    results.append(df.Histo1D(("WW_leps_category_final", "", 4, -1, 3), "WW_leps_category"))
    
    # dR(Z, WW)
    results.append(df.Histo1D(("zll_WW_dR_final", "", *bins_dR), "zll_WW_dR"))

    # missing energy
    results.append(df.Histo1D(("cosThetaMiss_final", "", *bins_cosThetaMiss), "cosTheta_miss"))
    results.append(df.Histo1D(("missingEnergy_final", "", *bins_p_mu), "missingEnergy"))
    
    return results, weightsum

