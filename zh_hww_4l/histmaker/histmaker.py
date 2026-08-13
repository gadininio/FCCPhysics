
'''
Run with:
    ecm=240 sel_type=1 fccanalysis run histmaker.py
    ecm=365 sel_type=5 fccanalysis run histmaker.py
    ecm=365 sel_type=8 fccanalysis run histmaker.py

Use different chi2 coeff for the resonance builder:
    ecm=365 sel_type=5 chi2=1.0 fccanalysis run histmaker.py

Add lepton isolation cut:
    ecm=365 sel_type=5 chi2=1.0 iso=3 fccanalysis run histmaker.py

Full run:
    ecm=240 sel_type=1 fullrun=true fccanalysis run histmaker.py
    ecm=365 sel_type=5 chi2=1.0 fullrun=true fccanalysis run histmaker.py

Full run for training:
    ecm=365 sel_type=5 fullrun=true training=true fccanalysis run histmaker.py
        
Selection types (sel_type):
    0: preselections only
    1: loose selections
    5: medium selections (loose + dR(Z->ll, WW*) cut)
    8: medium optimized for chi2=1.0
    7: firm selections (medium + lepton isolation)
    6: tight selections
    2: tightest selections
    
    3: loose selections without m_rec cut
    4: tightest selections without m_rec cut
'''


import os
fraction = float(os.environ.get("fraction", 0.2))
nchunks = int(os.environ.get("nchunks", 1))
debug = os.environ.get("debug", "False").lower() in ("true", "1")
fullrun = os.environ.get("fullrun", "False").lower() in ("true", "1")
ecm = os.environ.get("ecm", "240")
sel_type = int(os.environ.get("sel_type", 0))  # 0: presel, 1: loose, 2: tightest, 3: loose without zll_recoil cut, 4: tightest without zll_recoil cut
is_training = os.environ.get("training", "False").lower() in ("true", "1")
chi2_coeff_default = 0.4
chi2_coeff = float(os.environ.get("chi2", chi2_coeff_default))
lepton_iso = float(os.environ.get("iso", -999))  # default isolation cut for firm selection

if sel_type == 8: chi2_coeff = 1.0  # el_type=8 is medium optimized for chi2=1.0

print(f"Running with fraction={fraction}, nchunks={nchunks}, debug={debug}, fullrun={fullrun}, ecm={ecm}, sel_type={sel_type}, training={is_training}, chi2_coeff={chi2_coeff}, lepton_iso={lepton_iso}")


if fullrun and not debug:
    fraction = 1
    nchunks = 50

# list of processes (mandatory)
if ecm == '240':
    processList = {
        'p8_ee_ZZ_ecm240':{'fraction': fraction, 'chunks': nchunks},
        'p8_ee_WW_ecm240':{'fraction': fraction, 'chunks': nchunks},
        # 'wzp6_ee_ee_Mee_30_150_ecm240':{'fraction': fraction, 'chunks': nchunks},
        # 'wzp6_ee_mumu_ecm240':{'fraction': fraction, 'chunks': nchunks},
        # 'wzp6_ee_tautau_ecm240':{'fraction': fraction, 'chunks': nchunks},
        'wzp6_ee_eeH_HWW_llnunu_ecm240':{'fraction': 1}, # note that l=e,mu,tau, so w_leptonic_filter should still be applied!
        'wzp6_ee_mumuH_HWW_llnunu_ecm240':{'fraction': 1},
    }
elif ecm == '365':
    if is_training:
        processList = {
            'p8_ee_ZZ_llX_ecm365':{'fraction': fraction, 'chunks': nchunks},
            'p8_ee_ZZ_tautauX_ecm365':{'fraction': fraction, 'chunks': nchunks},
            'p8_ee_WW_ee_ecm365':{'fraction': fraction, 'chunks': nchunks},
            'p8_ee_WW_mumu_ecm365':{'fraction': fraction, 'chunks': nchunks},
            'p8_ee_WW_ecm365':{'fraction': fraction, 'chunks': nchunks},
            'wzp6_ee_eeH_HWW_ecm365':{'fraction': 1},
            'wzp6_ee_mumuH_HWW_ecm365':{'fraction': 1},
        }
    else:
        processList = {
            'p8_ee_tt_ecm365':{'fraction': fraction, 'chunks': nchunks},
            'p8_ee_ZZ_ecm365':{'fraction': fraction, 'chunks': nchunks},
            'p8_ee_WW_ee_ecm365':{'fraction': fraction, 'chunks': nchunks},
            'p8_ee_WW_mumu_ecm365':{'fraction': fraction, 'chunks': nchunks},
            'p8_ee_WW_ecm365':{'fraction': fraction, 'chunks': nchunks},
            # 'wzp6_ee_ee_Mee_30_150_ecm365':{'fraction': fraction, 'chunks': nchunks},
            # 'wzp6_ee_mumu_ecm365':{'fraction': fraction, 'chunks': nchunks},
            # 'wzp6_ee_tautau_ecm365':{'fraction': fraction, 'chunks': nchunks},
            'wzp6_ee_eeH_HWW_ecm365':{'fraction': 1},
            'wzp6_ee_mumuH_HWW_ecm365':{'fraction': 1},
        }

processList = {f'wzp6_ee_mumuH_HWW_ecm{ecm}':{'fraction': 0.2}} if debug else processList


# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
prodTag     = "FCCee/winter2023/IDEA/" if not is_training else "FCCee/winter2023_training/IDEA/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json" if not is_training else "FCCee_procDict_winter2023_training_IDEA.json"

# additional/custom C++ functions, defined in header files (optional)
includePaths = ["../functions.h"]

# Define the input dir (optional)
#inputDir    = "outputs/FCCee/higgs/mH-recoil/mumu/stage1"
#inputDir    = "localSamples/"

#Optional: output directory, default is local running directory
if sel_type == 0:   output_fix = "presel"
elif sel_type == 1: output_fix = "loose"
elif sel_type == 5: output_fix = "medium3"
elif sel_type == 8: output_fix = "medium5"
elif sel_type == 7: output_fix = "firm"
elif sel_type == 6: output_fix = "tight"
elif sel_type == 2: output_fix = "tightest"

elif sel_type == 3: output_fix = "loose_norecoil"
elif sel_type == 4: output_fix = "tightest_norecoil"

if is_training: output_fix += "_training"

if debug: output_fix += "_debug"
elif fullrun: output_fix += "_full"

if chi2_coeff != chi2_coeff_default:
    output_fix += f"_chi2-{chi2_coeff}"

if lepton_iso != -999: output_fix += f"_iso-{lepton_iso}"
elif sel_type == 7: lepton_iso = 0.25  # default isolation cut for firm selection

# get time stamp for the output directory
from datetime import datetime
now = datetime.now()
dt_string = now.strftime("%Y%m%d_%H%M%S")
output_fix += f"_{dt_string}"

# output_fix = ""
# if debug: output_fix = "debug/"
# else:
#     # add date-time stamp to output folder
#     from datetime import datetime
#     now = datetime.now()
#     dt_string = now.strftime("%Y%m%d_%H%M%S")
#     dt_string = ''
#     output_fix = f"{'full_' if fullrun else ''}{'nosel_' if not apply_selections else ('loose_' if is_loose else 'tight_')}{dt_string}/"
#     # if last charachter is '_', remove it
#     if output_fix.endswith('_'):
#         output_fix = output_fix[:-1]
outputDir   = f"../../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/hists/{output_fix}/"


# optional: ncpus, default is 4, -1 uses all cores available
nCPUS       = -1

# scale the histograms with the cross-section and integrated luminosity
doScale = True
intLumi = 10.8e6 if ecm == '240' else 3e6  # 10.8 /ab for 240 GeV, 3 /ab for 365 GeV

if ecm == '240':
    n_bins = 250
elif ecm == '365':
    n_bins = 400

# define some binning for various histograms
bins_p_mu = (n_bins, 0, n_bins) # 100 MeV bins
bins_m_ll = (n_bins*10, 0, n_bins) # 100 MeV bins
bins_m_ll_large = (n_bins*20, 0, n_bins*2) # 100 MeV bins
bins_p_ll = (n_bins, 0, n_bins) # 100 MeV bins
bins_recoil = (n_bins, 0, n_bins) # 1 GeV bins
bins_cosThetaMiss = (10000, 0, 1)
bins_q2 = (150000, -150000, 0)

bins_theta = (500, -5, 5)
bins_eta = (600, -3, 3)
bins_phi = (500, -5, 5)
bins_dPhi = (320, 0, 3.2)
bins_dR = (1000, -10, 10)
bins_cosTheta = (2000, -1, 1)

bins_count = (50, 0, 50)
bins_charge = (10, -5, 5)
bins_iso = (10000, 0, 10)
bins_iso_log = (40000, -20, 20)

# bins_recoil_final = (200, 120, 140) # 100 MeV bins
bins_recoil_final = (n_bins*10, 0, n_bins) # 0.1 GeV bins



# build_graph function that contains the analysis logic, cuts and histograms (mandatory)
def build_graph(df, dataset):

    results = []
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")


    # define collections
    df = df.Alias("Particle0", "Particle#0.index")  # truth parents
    df = df.Alias("Particle1", "Particle#1.index")  # truth daughters 
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")  # recind - contains the indices of the reconstructed objects (specifically the tracks).
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")  # mcind - contains the corresponding indices of the generated MC particles.


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

    if sel_type == 7 or lepton_iso != -999:  # firm selection, apply lepton isolation
        # compute the muon isolation and store muons with an isolation cut of 0.25 in a separate column muons_sel_iso
        df = df.Define("muons_iso", "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(muons, ReconstructedParticles)")
        df = df.Define("muons_sel_iso", f"FCCAnalyses::ZHfunctions::sel_iso({lepton_iso})(muons, muons_iso)")


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

    if sel_type == 7 or lepton_iso != -999:  # firm selection, apply lepton isolation
        # compute the electron isolation and store electrons with an isolation cut of 0.25 in a separate column electrons_sel_iso
        df = df.Define("electrons_iso", "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(electrons, ReconstructedParticles)")
        df = df.Define("electrons_sel_iso", f"FCCAnalyses::ZHfunctions::sel_iso({lepton_iso})(electrons, electrons_iso)")


    # baseline histograms, before any selection cuts (store with _cut0)
    results.append(df.Histo1D(("muons_all_p_cut0", "", *bins_p_mu), "muons_all_p"))
    results.append(df.Histo1D(("muons_p_cut0", "", *bins_p_mu), "muons_p"))
    results.append(df.Histo1D(("muons_theta_cut0", "", *bins_theta), "muons_theta"))
    results.append(df.Histo1D(("muons_phi_cut0", "", *bins_phi), "muons_phi"))
    results.append(df.Histo1D(("muons_q_cut0", "", *bins_charge), "muons_q"))
    results.append(df.Histo1D(("muons_no_cut0", "", *bins_count), "muons_no"))
    if sel_type == 7 or lepton_iso != -999:
        results.append(df.Histo1D(("muons_iso_cut0", "", *bins_iso), "muons_iso"))

    results.append(df.Histo1D(("electrons_all_p_cut0", "", *bins_p_mu), "electrons_all_p"))
    results.append(df.Histo1D(("electrons_p_cut0", "", *bins_p_mu), "electrons_p"))
    results.append(df.Histo1D(("electrons_theta_cut0", "", *bins_theta), "electrons_theta"))
    results.append(df.Histo1D(("electrons_phi_cut0", "", *bins_phi), "electrons_phi"))
    results.append(df.Histo1D(("electrons_q_cut0", "", *bins_charge), "electrons_q"))
    results.append(df.Histo1D(("electrons_no_cut0", "", *bins_count), "electrons_no"))
    if sel_type == 7 or lepton_iso != -999:
        results.append(df.Histo1D(("electrons_iso_cut0", "", *bins_iso), "electrons_iso"))


    icut = 0  # cut counter, used for cutflow histogram

    #########
    ### CUT 0: all events
    #########
    df = df.Define(f"cut{icut}", str(icut))
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{icut}"))
    icut += 1

    #########
    ### CUT 1: exactly 4 leptons  # (and for `firm` selections, they are isolated)
    #########
    # df = df.Filter(f"{leps}_no >= 1 && {leps}_sel_iso.size() > 0")
    # df = df.Filter(f"{leps}_no == 4")
    
    df = df.Define("n_leptons", "muons_no + electrons_no")
    results.append(df.Histo1D(("n_leptons_cut0", "", *bins_count), "n_leptons"))
    
    if sel_type >= 0:
        # if sel_type == 7:  # firm selection, use isolated leptons
        #     df = df.Define("n_leptons_iso", "muons_sel_iso.size() + electrons_sel_iso.size()")
        #     df = df.Filter("n_leptons == 4 && n_leptons_iso == 4")
        # else:
        df = df.Filter("n_leptons == 4")
    df = df.Define(f"cut{icut}", str(icut))
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{icut}"))
    icut += 1


    #########
    ### CUT 1a: exactly 4 isolated leptons
    #########
    if sel_type == 7:  # firm selection, use isolated leptons
        df = df.Define("n_leptons_iso", "muons_sel_iso.size() + electrons_sel_iso.size()")
        df = df.Filter("n_leptons_iso > 1")
        df = df.Define(f"cut{icut}", str(icut))
        results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{icut}"))
        icut += 1

    if lepton_iso != -999:  # leptpn isolation is specified, apply isolation cut
        df = df.Define("n_leptons_iso", "muons_sel_iso.size() + electrons_sel_iso.size()")
        df = df.Filter("n_leptons_iso == 4")
        df = df.Define(f"cut{icut}", str(icut))
        results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{icut}"))
        icut += 1


    #########
    ### CUT 2: at least 2 opposite-sign (OS) lepton pairs
    #########
    # df = df.Filter(f"{leps}_no >= 2 && abs(Sum({leps}_q)) < {leps}_q.size()")
    # df = df.Filter(f"abs(Sum({leps}_q)) <= {leps}_q.size() - 4")
    if sel_type >= 0:
        df = df.Filter(f"abs(Sum(muons_q) + Sum(electrons_q)) <= muons_q.size() + electrons_q.size() - 4")
    df = df.Define(f"cut{icut}", str(icut))
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{icut}"))
    icut += 1


    #########
    ### CUT 3: at least one same-flavor (SF) lepton pair
    #########
    if sel_type >= 0:
        df = df.Filter("(muons_no >= 2) || (electrons_no >= 2)")
    df = df.Define(f"cut{icut}", str(icut))
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{icut}"))
    icut += 1


    #########
    ### CUT 4: leptons p: leading muon p [25, 80] GeV, subleading muon p [15, 80] GeV, third muon p [10,80] GeV, fourth muon p [10,75] GeV
    #########
    df = df.Define("leptons0", "FCCAnalyses::ReconstructedParticle::merge(muons, electrons)")
    df = df.Define("leptons", "FCCAnalyses::ZHfunctions::sortByPt(leptons0)")
    
    # leptons iso
    df = df.Define("leptons_iso", "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(leptons, ReconstructedParticles)")
    df = df.Define("lep0_iso", "leptons_iso[0]")
    df = df.Define("lep1_iso", "leptons_iso[1]")
    df = df.Define("lep2_iso", "leptons_iso[2]")
    df = df.Define("lep3_iso", "leptons_iso[3]")
    
    df = df.Define("lep0_iso_log", "log10(leptons_iso[0] + 1e-10)")
    df = df.Define("lep1_iso_log", "log10(leptons_iso[1] + 1e-10)")
    df = df.Define("lep2_iso_log", "log10(leptons_iso[2] + 1e-10)")
    df = df.Define("lep3_iso_log", "log10(leptons_iso[3] + 1e-10)") 
    
    results.append(df.Histo1D(("lep0_iso_log_cut2", "", *bins_iso_log), "lep0_iso_log"))
    results.append(df.Histo1D(("lep1_iso_log_cut2", "", *bins_iso_log), "lep1_iso_log"))
    results.append(df.Histo1D(("lep2_iso_log_cut2", "", *bins_iso_log), "lep2_iso_log"))
    results.append(df.Histo1D(("lep3_iso_log_cut2", "", *bins_iso_log), "lep3_iso_log"))    
    
    # leptons p
    df = df.Define("leptons_p", "FCCAnalyses::ReconstructedParticle::get_p(leptons)")
    df = df.Define("lep0_p", "leptons_p[0]")
    df = df.Define("lep1_p", "leptons_p[1]")
    df = df.Define("lep2_p", "leptons_p[2]")
    df = df.Define("lep3_p", "leptons_p[3]")
    
    results.append(df.Histo1D(("lep0_p_cut2", "", *bins_p_mu), "lep0_p"))
    results.append(df.Histo1D(("lep1_p_cut2", "", *bins_p_mu), "lep1_p"))
    results.append(df.Histo1D(("lep2_p_cut2", "", *bins_p_mu), "lep2_p"))
    results.append(df.Histo1D(("lep3_p_cut2", "", *bins_p_mu), "lep3_p"))
    
    if sel_type > 0:
        if ecm == '240':
            if sel_type == 1 or sel_type == 3:  # loose (with or without m_rec cut)
                df = df.Filter("lep0_p > 20 && lep0_p < 85")
                df = df.Filter("lep1_p > 10 && lep1_p < 80")
                df = df.Filter("lep2_p > 10 && lep2_p < 80")
                df = df.Filter("lep3_p > 5  && lep3_p < 75")
            elif sel_type == 2 or sel_type == 4:  # tight (with or without m_rec cut)
                df = df.Filter("lep0_p > 25 && lep0_p < 80")
                df = df.Filter("lep1_p > 15 && lep1_p < 80")
                df = df.Filter("lep2_p > 10 && lep2_p < 80")
                df = df.Filter("lep3_p > 10 && lep3_p < 75")
        elif ecm == '365':
            if sel_type == 1 or sel_type == 3 or sel_type == 5 or sel_type == 6 or sel_type == 7 or sel_type == 8:  # loose (with or without m_rec cut)
                results.append(df.Histo1D(("lep0_p_cut2a", "", *bins_p_mu), "lep0_p"))
                df = df.Filter("lep0_p > 20 && lep0_p < 165")
                results.append(df.Histo1D(("lep1_p_cut2b", "", *bins_p_mu), "lep1_p"))
                df = df.Filter("lep1_p > 10 && lep1_p < 160")
                results.append(df.Histo1D(("lep2_p_cut2c", "", *bins_p_mu), "lep2_p"))
                df = df.Filter("lep2_p > 5 && lep2_p < 150")
                results.append(df.Histo1D(("lep3_p_cut2d", "", *bins_p_mu), "lep3_p"))
                df = df.Filter("lep3_p > 5 && lep3_p < 150")
            elif sel_type == 2 or sel_type == 4:  # tight (with or without m_rec cut)
                results.append(df.Histo1D(("lep0_p_cut2a", "", *bins_p_mu), "lep0_p"))
                df = df.Filter("lep0_p > 70 && lep0_p < 155")
                results.append(df.Histo1D(("lep1_p_cut2b", "", *bins_p_mu), "lep1_p"))
                df = df.Filter("lep1_p > 25 && lep1_p < 105")
                results.append(df.Histo1D(("lep2_p_cut2c", "", *bins_p_mu), "lep2_p"))
                df = df.Filter("lep2_p > 15 && lep2_p < 80")
                results.append(df.Histo1D(("lep3_p_cut2d", "", *bins_p_mu), "lep3_p"))
                df = df.Filter("lep3_p > 5 && lep3_p < 65")
    df = df.Define(f"cut{icut}", str(icut))
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{icut}"))
    icut += 1
    

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
    df = df.Define("zbuilder_result", f"FCCAnalyses::ZHfunctions::resonanceBuilder_mass_recoil_advanced(91.2, 125, {chi2_coeff}, {ecm}, false)(muons, electrons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    df = df.Filter("zbuilder_result.size() >= 5") # make sure at least one pair was found (and additional two leptons)


    # ## Pairing efficiency study: we can check if the pairing was correct by matching the reconstructed leptons to the generated ones and checking if they come from the same Z boson.
    # df = df.Define("pairing_info", "FCCAnalyses::ZHfunctions::check_pairing_efficiency(zbuilder_result, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    # # df = df.Define("is_correct_pairing", "is_correct_pairing(bestReso, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    # df = df.Define("is_correct_pairing", "pairing_info.is_correct")
    # df = df.Define("true_Z_p",           "pairing_info.true_Z_p")
    # df = df.Define("true_Z_mass",        "pairing_info.true_Z_mass")
    # df = df.Define("true_lepton1_p",     "pairing_info.true_lepton1_p")
    # df = df.Define("true_lepton2_p",     "pairing_info.true_lepton2_p")
    # df = df.Define("truth_lepton_dR",    "pairing_info.truth_lepton_dR")

    df = df.Define("pairing_info", "FCCAnalyses::ZHfunctions::check_pairing_efficiency_via_HWW(zbuilder_result, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    df = df.Define("is_correct_pairing", "pairing_info[0]")
    df = df.Define("true_Z_p",           "pairing_info[1]")
    df = df.Define("true_Z_mass",        "pairing_info[2]")
    df = df.Define("true_lepton1_p",     "pairing_info[3]")
    df = df.Define("true_lepton2_p",     "pairing_info[4]")
    df = df.Define("truth_lepton_dR",    "pairing_info[5]")

    results.append(df.Histo1D(("eff_total_cut4", "Overall Pairing Efficiency; ; Efficiency", 2, -0.5, 1.5), "is_correct_pairing"))
    results.append(df.Histo1D(("true_Z_p_cut4", "True Z Momentum; p_{Z} [GeV]; Events", 100, 0, 250), "true_Z_p"))
    results.append(df.Histo1D(("true_Z_mass_cut4", "True Z Mass; m_{Z} [GeV]; Events", 100, 0, 200), "true_Z_mass"))
    results.append(df.Histo1D(("true_lepton1_p_cut4", "True Lepton 1 Momentum; p_{l1} [GeV]; Events", 100, 0, 250), "true_lepton1_p"))
    results.append(df.Histo1D(("true_lepton2_p_cut4", "True Lepton 2 Momentum; p_{l2} [GeV]; Events", 100, 0, 250), "true_lepton2_p"))
    results.append(df.Histo1D(("truth_lepton_dR_cut4", "dR between the two leptons from the Z decay; dR; Events", 50, 0, 5), "truth_lepton_dR"))
    
    df = df.Define("zll", "Vec_rp{zbuilder_result[0]}") # the Z
    df = df.Define("zll_tlv", "FCCAnalyses::ReconstructedParticle::get_tlv(zll, 0)")
    df = df.Define("zll_m", "FCCAnalyses::ReconstructedParticle::get_mass(zll)[0]") # Z mass
    df = df.Define("zll_p", "FCCAnalyses::ReconstructedParticle::get_p(zll)[0]") # momentum of the Z
    df = df.Define("zll_pt", "FCCAnalyses::ReconstructedParticle::get_pt(zll)[0]") # momentum of the Z
    df = df.Define("zll_theta", "FCCAnalyses::ReconstructedParticle::get_theta(zll)[0]") # momentum of the Z
    df = df.Define("zll_phi", "FCCAnalyses::ReconstructedParticle::get_phi(zll)[0]") # momentum of the Z

    # results.append(df.Histo1D(("zll_m_cut4", "", *bins_m_ll), "zll_m"))
    results.append(df.Histo1D(("zll_p_cut4", "", *bins_p_ll), "zll_p"))
    results.append(df.Histo1D(("zll_pt_cut4", "", *bins_p_ll), "zll_pt"))
    results.append(df.Histo1D(("zll_theta_cut4", "", *bins_theta), "zll_theta"))
    results.append(df.Histo1D(("zll_phi_cut4", "", *bins_phi), "zll_phi"))

    ## Recoil mass
    df = df.Define("zll_recoil", f"FCCAnalyses::ReconstructedParticle::recoilBuilder({ecm})(zll)") # compute the recoil based on the reconstructed Z
    df = df.Define("zll_recoil_m", "FCCAnalyses::ReconstructedParticle::get_mass(zll_recoil)[0]") # recoil mass
    results.append(df.Histo1D(("zll_recoil_m_cut4", "", *bins_recoil), "zll_recoil_m")) # plot it before the cut

    ## Study the Z-lepton candidates
    df = df.Define("zll_leps", "Vec_rp{zbuilder_result[1],zbuilder_result[2]}") # Z-lepton candidates
    df = df.Define("zll_leps_p", "FCCAnalyses::ReconstructedParticle::get_p(zll_leps)") # get the momentum of these 2 leptons
    df = df.Define("zll_leps_pt", "FCCAnalyses::ReconstructedParticle::get_pt(zll_leps)") # get the momentum of these 2 leptons
    df = df.Define("zll_leps_theta", "FCCAnalyses::ReconstructedParticle::get_theta(zll_leps)") # get the theta of these 2 leptons
    df = df.Define("zll_leps_phi", "FCCAnalyses::ReconstructedParticle::get_phi(zll_leps)") # get the phi of these 2 leptons
    
    df = df.Define("zll_lep0_p", "zll_leps_p[0]")
    df = df.Define("zll_lep0_pt", "zll_leps_pt[0]")
    df = df.Define("zll_lep0_theta", "zll_leps_theta[0]")
    df = df.Define("zll_lep0_phi", "zll_leps_phi[0]")
    df = df.Define("zll_lep1_p", "zll_leps_p[1]")
    df = df.Define("zll_lep1_pt", "zll_leps_pt[1]")
    df = df.Define("zll_lep1_theta", "zll_leps_theta[1]")
    df = df.Define("zll_lep1_phi", "zll_leps_phi[1]")
    results.append(df.Histo1D(("zll_lep0_p_cut4", "", *bins_p_mu), "zll_lep0_p"))
    results.append(df.Histo1D(("zll_lep0_pt_cut4", "", *bins_p_mu), "zll_lep0_pt"))
    results.append(df.Histo1D(("zll_lep0_theta_cut4", "", *bins_theta), "zll_lep0_theta"))
    results.append(df.Histo1D(("zll_lep0_phi_cut4", "", *bins_phi), "zll_lep0_phi"))
    results.append(df.Histo1D(("zll_lep1_p_cut4", "", *bins_p_mu), "zll_lep1_p"))
    results.append(df.Histo1D(("zll_lep1_pt_cut4", "", *bins_p_mu), "zll_lep1_pt"))
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
    
    df = df.Define("zll_acolinearity", "FCCAnalyses::ZHfunctions::acolinearity(zll_leps)")
    results.append(df.Histo1D(("zll_acolinearity_cut4", "", *bins_cosTheta), "zll_acolinearity"))
    
    # For the VBF componenet, the two "resonance" leptons Z->ll don't come from the Z, but they are the scattered electron and positron going in the forward direction. Compute q1^2 and q2^2 of the virtual radiated Z bosons using the 4-momenta of the scattered electrons and the beam electron and positron.
    df = df.Define("vbf_q2_values", f"FCCAnalyses::ZHfunctions::vbf_q2_builder({ecm})(zll_leps)")
    df = df.Define("vbf_q1_squared", "vbf_q2_values[0]")
    df = df.Define("vbf_q2_squared", "vbf_q2_values[1]")    
    results.append(df.Histo1D(("vbf_q1_squared_cut4", "", *bins_q2), "vbf_q1_squared"))
    results.append(df.Histo1D(("vbf_q2_squared_cut4", "", *bins_q2), "vbf_q2_squared"))
   
    
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
    df = df.Define("WW_leps_mass", "(WW_lep0_tlv + WW_lep1_tlv).M()")
    df = df.Define("WW_leps_dPhi", "std::abs(WW_lep0_tlv.DeltaPhi(WW_lep1_tlv))")
    df = df.Define("WW_leps_dR", "WW_lep0_tlv.DeltaR(WW_lep1_tlv)")
    results.append(df.Histo1D(("WW_leps_mass_cut4", "", *bins_m_ll), "WW_leps_mass"))
    results.append(df.Histo1D(("WW_leps_dPhi_cut4", "", *bins_dPhi), "WW_leps_dPhi"))
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

    ## Missing mass
    # df = df.Define("missingMass", "FCCAnalyses::ReconstructedParticle::get_mass(missingEnergy_vec)[0]")
    # df = df.Define("missingMass", "missingEnergy_tlv.M()")
    df = df.Define("missingMass", "FCCAnalyses::ZHfunctions::get_missing_mass(missingEnergy_vec)")
    results.append(df.Histo1D(("missingMass_cut4", "", *bins_m_ll_large), "missingMass"))


    #########
    ### CUT 5: Z mass window
    #########
    results.append(df.Histo1D(("zll_m_cut4", "", *bins_m_ll), "zll_m"))  # already done above
    if sel_type > 0:
        if ecm == '240':
            # df = df.Filter("zll_m > 86 && zll_m < 96")  # tighter cut - smaller significance
            df = df.Filter("zll_m > 76 && zll_m < 106")
        elif ecm == '365':
            if sel_type == 1:  # loose
                df = df.Filter("zll_m > 30 && zll_m < 200")
            if sel_type == 5 or sel_type == 7:  # medium or firm
                df = df.Filter("zll_m > 71 && zll_m < 111")
            elif sel_type == 8:  # medium (optimized for chi2=1.0)
                df = df.Filter("zll_m > 61 && zll_m < 121")
            elif sel_type == 6:  # tight
                df = df.Filter("zll_m > 50 && zll_m < 150")
            elif sel_type == 2:  # tightest
                df = df.Filter("zll_m > 76 && zll_m < 106")
    df = df.Define(f"cut{icut}", str(icut))
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{icut}"))
    icut += 1


    #########
    ### CUT 6: Z momentum
    #########
    results.append(df.Histo1D(("zll_p_cut5", "", *bins_p_ll), "zll_p"))
    if sel_type > 0:
        if ecm == '240':
            df = df.Filter("zll_p > 20 && zll_p < 70")
        elif ecm == '365':
            if sel_type == 1 or sel_type == 3 or sel_type == 5 or sel_type == 7 or sel_type == 8:  # loose (with or without m_rec cut)
                df = df.Filter("zll_p > 35 && zll_p < 155")
            elif sel_type == 6:  # tight
                df = df.Filter("zll_p > 60 && zll_p < 155")
            elif sel_type == 2 or sel_type == 4:  # tightest (with or without m_rec cut)
                df = df.Filter("zll_p > 140 && zll_p < 150")
    df = df.Define(f"cut{icut}", str(icut))
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{icut}"))
    icut += 1


    #########
    ### CUT *: recoil mass window (reconstructed Higgs mass using the recoil method)
    #########
    results.append(df.Histo1D(("zll_recoil_m_cut6", "", *bins_recoil), "zll_recoil_m")) # plot it before the cut
    if sel_type > 0:  # apply m_rec cut for loose and tight selections
        if ecm == '240':
            if sel_type == 1:  # loose (with m_rec cut)
                df = df.Filter("zll_recoil_m < 145 && zll_recoil_m > 120")
            elif sel_type == 2:  # tight (with m_rec cut)
                df = df.Filter("zll_recoil_m < 140 && zll_recoil_m > 120")
        elif ecm == '365':
            if sel_type == 1 or sel_type == 5 or sel_type == 7 or sel_type == 8:  # loose (with m_rec cut)
                df = df.Filter("zll_recoil_m < 230 && zll_recoil_m > 115")
            elif sel_type == 6:  # tight
                df = df.Filter("zll_recoil_m < 200 && zll_recoil_m > 115")
            elif sel_type == 2:  # tightest (with m_rec cut)
                # pass  # don't apply recoil mass cut for 365 GeV tight selection, as this variable will be used for the fit.
                df = df.Filter("zll_recoil_m < 140 && zll_recoil_m > 120")
    
    if sel_type != 3 and sel_type != 4:
        df = df.Define(f"cut{icut}", str(icut))
        results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{icut}"))
        icut += 1


    #########
    ### CUT 7: cosThetaMiss
    #########  
    df = df.Define("cosTheta_miss", "FCCAnalyses::ZHfunctions::get_cosTheta_miss(missingEnergy_vec)")
    results.append(df.Histo1D(("cosThetaMiss_cut7", "", *bins_cosThetaMiss), "cosTheta_miss")) # plot it before the cut
    if sel_type > 0:
        df = df.Filter("cosTheta_miss < 0.98")
    df = df.Define(f"cut{icut}", str(icut))
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{icut}"))
    icut += 1


    #########
    ### CUT 8: missingEnergy
    #########  
    df = df.Define("missingEnergy", "FCCAnalyses::ZHfunctions::get_missing_energy(missingEnergy_vec)")
    results.append(df.Histo1D(("missingEnergy_cut8", "", *bins_p_mu), "missingEnergy")) # plot it before the cut
    if sel_type > 0:
        if ecm == '240':
            if sel_type == 1 or sel_type == 3:  # loose (with or without m_rec cut)
                df = df.Filter("missingEnergy > 20 && missingEnergy < 120")
            elif sel_type == 2 or sel_type == 4:  # tight (with or without m_rec cut)
                df = df.Filter("missingEnergy > 30 && missingEnergy < 110")
        elif ecm == '365':
            if sel_type == 1 or sel_type == 3 or sel_type == 5 or sel_type == 6 or sel_type == 7 or sel_type == 8:  # loose (with or without m_rec cut)
                df = df.Filter("missingEnergy > 20 && missingEnergy < 180")
            elif sel_type == 2 or sel_type == 4:  # tightest (with or without m_rec cut)
                df = df.Filter("missingEnergy > 30 && missingEnergy < 160")
    df = df.Define(f"cut{icut}", str(icut))
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{icut}"))
    icut += 1


    #########
    ### CUT 9: WW system mass window
    #########  
    results.append(df.Histo1D(("WW_mass_cut9", "", *bins_m_ll_large), "WW_mass"))
    if sel_type > 0:
        if ecm == '240':
            if sel_type == 1 or sel_type == 3:  # loose (with or without m_rec cut)
                df = df.Filter("WW_mass > 60 && WW_mass < 135")
            elif sel_type == 2 or sel_type == 4:  # tight (with or without m_rec cut)
                df = df.Filter("WW_mass > 80 && WW_mass < 135")
        elif ecm == '365':
            if sel_type == 1 or sel_type == 3 or sel_type == 5 or sel_type == 7 or sel_type == 8:  # loose (with or without m_rec cut)
                df = df.Filter("WW_mass > 50")
            elif sel_type == 6:  # tight
                df = df.Filter("WW_mass > 70")
            elif sel_type == 2 or sel_type == 4:  # tightest (with or without m_rec cut)
                df = df.Filter("WW_mass > 80 && WW_mass < 130")
    df = df.Define(f"cut{icut}", str(icut))
    results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{icut}"))
    icut += 1


    # #########
    # ### CUT *: WW system momentum
    # #########  
    # results.append(df.Histo1D(("WW_p_cut10", "", *bins_p_ll), "WW_p"))
    # if sel_type > 0:
    #     if ecm == '365':
    #         if sel_type == 1 or sel_type == 3 or sel_type == 5 or sel_type == 7 or sel_type == 8:  # loose (with or without m_rec cut)
    #             df = df.Filter("WW_p > 100 && WW_p < 150")
    #         elif sel_type == 2 or sel_type == 4:  # tight (with or without m_rec cut)
    #             df = df.Filter("WW_p > 120 && WW_p < 150")
    #         df = df.Define("cut11", "11")
    #         results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut11"))
    
    
    #########
    ### CUT 10: dR(l_WW, l_WW)
    #########  
    results.append(df.Histo1D(("WW_leps_dR_cut9", "", *bins_dR), "WW_leps_dR"))
    if sel_type > 0:
        if ecm == '240':
            df = df.Filter("WW_leps_dR > 0.25")
        elif ecm == '365':
            if sel_type == 1 or sel_type == 3 or sel_type == 5 or sel_type == 6 or sel_type == 7 or sel_type == 8:  # loose (with or without m_rec cut)
                df = df.Filter("WW_leps_dR > 0.1 && WW_leps_dR < 4.0")
            elif sel_type == 2 or sel_type == 4:  # tight (with or without m_rec cut)
                df = df.Filter("WW_leps_dR > 0.1")
        df = df.Define(f"cut{icut}", str(icut))
        results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{icut}"))
        icut += 1
            
    
    #########
    ### CUT 11: dR(Z->ll, WW*)
    #########  
    results.append(df.Histo1D(("zll_WW_dR_cut11", "", *bins_dR), "zll_WW_dR"))
    if sel_type > 0:
        if ecm == '365':
            if sel_type == 5 or sel_type == 6 or sel_type == 7 or sel_type == 8:  # medium or tight
                df = df.Filter("zll_WW_dR > 3.0")
            df = df.Define(f"cut{icut}", str(icut))
            results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{icut}"))
            icut += 1


    #########
    ### CUT 12: dR(l1, l2)
    #########  
    results.append(df.Histo1D(("zll_leps_dR_cut12", "", *bins_dR), "zll_leps_dR"))
    if sel_type > 0:
        if ecm == '365':
            if sel_type == 5 or sel_type == 6 or sel_type == 7 or sel_type == 8:  # medium or tight
                df = df.Filter("zll_leps_dR < 3.0")
            df = df.Define(f"cut{icut}", str(icut))
            results.append(df.Histo1D(("cutFlow", "", *bins_count), f"cut{icut}"))
            icut += 1


    ########################
    # Final histograms
    ########################
    
    # Leptons
    results.append(df.Histo1D(("lep0_p_final", "", *bins_p_mu), "lep0_p"))
    results.append(df.Histo1D(("lep1_p_final", "", *bins_p_mu), "lep1_p"))
    results.append(df.Histo1D(("lep2_p_final", "", *bins_p_mu), "lep2_p"))
    results.append(df.Histo1D(("lep3_p_final", "", *bins_p_mu), "lep3_p"))
    results.append(df.Histo1D(("n_leptons_final", "", *bins_count), "n_leptons"))

    results.append(df.Histo1D(("lep0_iso_final", "", *bins_iso), "lep0_iso"))
    results.append(df.Histo1D(("lep1_iso_final", "", *bins_iso), "lep1_iso"))
    results.append(df.Histo1D(("lep2_iso_final", "", *bins_iso), "lep2_iso"))
    results.append(df.Histo1D(("lep3_iso_final", "", *bins_iso), "lep3_iso"))    
    
    results.append(df.Histo1D(("lep0_iso_log_final", "", *bins_iso_log), "lep0_iso_log"))
    results.append(df.Histo1D(("lep1_iso_log_final", "", *bins_iso_log), "lep1_iso_log"))
    results.append(df.Histo1D(("lep2_iso_log_final", "", *bins_iso_log), "lep2_iso_log"))
    results.append(df.Histo1D(("lep3_iso_log_final", "", *bins_iso_log), "lep3_iso_log"))        
    
    # zll system
    results.append(df.Histo1D(("zll_m_final", "", *bins_m_ll), "zll_m"))
    results.append(df.Histo1D(("zll_recoil_m_final", "", *bins_recoil_final), "zll_recoil_m"))
    results.append(df.Histo1D(("zll_p_final", "", *bins_p_ll), "zll_p"))
    results.append(df.Histo1D(("zll_pt_final", "", *bins_p_ll), "zll_pt"))
    results.append(df.Histo1D(("zll_theta_final", "", *bins_theta), "zll_theta"))
    results.append(df.Histo1D(("zll_phi_final", "", *bins_phi), "zll_phi"))

    # zll leptons
    results.append(df.Histo1D(("zll_lep0_p_final", "", *bins_p_mu), "zll_lep0_p"))
    results.append(df.Histo1D(("zll_lep0_pt_final", "", *bins_p_mu), "zll_lep0_pt"))
    results.append(df.Histo1D(("zll_lep0_theta_final", "", *bins_theta), "zll_lep0_theta"))
    results.append(df.Histo1D(("zll_lep0_phi_final", "", *bins_phi), "zll_lep0_phi"))
    results.append(df.Histo1D(("zll_lep0_p_index_final", "", 5, -1, 4), "zll_lep0_p_index"))  # Which muon is zll_lep0_p?
    results.append(df.Histo1D(("zll_lep1_p_final", "", *bins_p_mu), "zll_lep1_p"))
    results.append(df.Histo1D(("zll_lep1_pt_final", "", *bins_p_mu), "zll_lep1_pt"))
    results.append(df.Histo1D(("zll_lep1_theta_final", "", *bins_theta), "zll_lep1_theta"))
    results.append(df.Histo1D(("zll_lep1_phi_final", "", *bins_phi), "zll_lep1_phi"))
    results.append(df.Histo1D(("zll_lep1_p_index_final", "", 5, -1, 4), "zll_lep1_p_index"))  # Which muon is zll_lep1_p?
    
    results.append(df.Histo1D(("zll_leps_dR_final", "", *bins_dR), "zll_leps_dR"))
    results.append(df.Histo1D(("zll_leps_category_final", "", 4, -1, 3), "zll_leps_category"))
    results.append(df.Histo1D(("zll_acolinearity_final", "", *bins_cosTheta), "zll_acolinearity"))
    results.append(df.Histo1D(("vbf_q1_squared_final", "", *bins_q2), "vbf_q1_squared"))
    results.append(df.Histo1D(("vbf_q2_squared_final", "", *bins_q2), "vbf_q2_squared"))
   
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

    results.append(df.Histo1D(("WW_leps_mass_final", "", *bins_m_ll), "WW_leps_mass"))
    results.append(df.Histo1D(("WW_leps_dPhi_final", "", *bins_dPhi), "WW_leps_dPhi"))
    results.append(df.Histo1D(("WW_leps_dR_final", "", *bins_dR), "WW_leps_dR"))
    results.append(df.Histo1D(("WW_leps_category_final", "", 4, -1, 3), "WW_leps_category"))
    
    # dR(Z, WW)
    results.append(df.Histo1D(("zll_WW_dR_final", "", *bins_dR), "zll_WW_dR"))

    # missing energy
    results.append(df.Histo1D(("cosThetaMiss_final", "", *bins_cosThetaMiss), "cosTheta_miss"))
    results.append(df.Histo1D(("missingEnergy_final", "", *bins_p_mu), "missingEnergy"))
    results.append(df.Histo1D(("missingMass_final", "", *bins_m_ll_large), "missingMass"))
    
    # truth info used for pairing efficiency
    results.append(df.Histo1D(("true_Z_p_final", "True Z Momentum; p_{Z} [GeV]; Events", 100, 0, 250), "true_Z_p"))
    results.append(df.Histo1D(("true_Z_mass_final", "True Z Mass; m_{Z} [GeV]; Events", 100, 0, 200), "true_Z_mass"))
    results.append(df.Histo1D(("true_lepton1_p_final", "True Lepton 1 Momentum; p_{l1} [GeV]; Events", 100, 0, 250), "true_lepton1_p"))
    results.append(df.Histo1D(("true_lepton2_p_final", "True Lepton 2 Momentum; p_{l2} [GeV]; Events", 100, 0, 250), "true_lepton2_p"))
    results.append(df.Histo1D(("truth_lepton_dR_final", "dR between the two leptons from the Z decay; dR; Events", 50, 0, 5), "truth_lepton_dR"))

    results.append(df.Histo1D(("eff_total_final", "Overall Pairing Efficiency; ; Efficiency", 2, -0.5, 1.5), "is_correct_pairing"))
    
    # Profile histogram to plot Efficiency vs. True Z Momentum directly (y-axis is the mean of is_correct_pairing in each x-axis bin)
    # results.append(df.Profile1D(("eff_vs_Z_p", "Pairing Efficiency vs True Z Momentum; True p_{Z} [GeV]; Efficiency", 50, 0, 250), "true_Z_p", "is_correct_pairing"))
    # results.append(df.Profile1D(("eff_vs_Z_mass", "Pairing Efficiency vs True Z Mass; True m_{Z} [GeV]; Efficiency", 50, 0, 200), "true_Z_mass", "is_correct_pairing"))
    # results.append(df.Profile1D(("eff_vs_lepton1_p", "Pairing Efficiency vs True Lepton 1 Momentum; True p_{l1} [GeV]; Efficiency", 50, 0, 250), "true_lepton1_p", "is_correct_pairing"))
    # results.append(df.Profile1D(("eff_vs_lepton2_p", "Pairing Efficiency vs True Lepton 2 Momentum; True p_{l2} [GeV]; Efficiency", 50, 0, 250), "true_lepton2_p", "is_correct_pairing"))
    # results.append(df.Profile1D(("eff_vs_lepton_dR", "Pairing Efficiency vs dR between the two leptons from Z decay; True dR; Efficiency", 25, 0, 5), "truth_lepton_dR", "is_correct_pairing"))
    
    
    # select events with correct pairing for efficiency calculation
    df = df.Filter("is_correct_pairing == 1")
    
    # numerator for efficiency calculation
    results.append(df.Histo1D(("true_Z_p_selected_final", "True Z Momentum; p_{Z} [GeV]; Events", 100, 0, 250), "true_Z_p"))
    results.append(df.Histo1D(("true_Z_mass_selected_final", "True Z Mass; m_{Z} [GeV]; Events", 100, 0, 200), "true_Z_mass"))
    results.append(df.Histo1D(("true_lepton1_p_selected_final", "True Lepton 1 Momentum; p_{l1} [GeV]; Events", 100, 0, 250), "true_lepton1_p"))
    results.append(df.Histo1D(("true_lepton2_p_selected_final", "True Lepton 2 Momentum; p_{l2} [GeV]; Events", 100, 0, 250), "true_lepton2_p"))
    results.append(df.Histo1D(("truth_lepton_dR_selected_final", "dR between the two leptons from the Z decay; dR; Events", 50, 0, 5), "truth_lepton_dR"))

    
    return results, weightsum
