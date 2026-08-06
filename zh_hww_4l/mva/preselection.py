
'''
This script applies a set of cuts. The cuts are applied sequentially, and can be toggled on/off using the apply_preselections (4 leptons and 2 OF SF pairs) and apply_selections (all other cuts) flags. The looser cuts (set with the is_loose flag) are designed to reduce the background while keeping a high signal efficiency to maintain enough stat for training and fit. The output of this script is ntuples containing the preselected events in which can be used for training a BDT (using is_training flag) or for making histograms.

Run with:

    Debug:
        run=debug ecm=365 training=True sel_type=medium fccanalysis run preselection.py

    Full, medium selections, training samples:
        run=full ecm=365 training=True  sel_type=medium chi2=1.0 iso=3.0 fccanalysis run preselection.py

    Full, medium selections, analysis samples:
        run=full ecm=365 training=False sel_type=medium chi2=1.0 iso=3.0 fccanalysis run preselection.py

    Local, medium selections, analysis samples:
        run=local ecm=365 training=False sel_type=medium chi2=1.0 fccanalysis run preselection.py


Then, add the parameters to the output root files for the analysis samples:

    python3 ../../utils/add_parameters_to_root.py \
        -f ../../../outputs/higgs/zh_hww_4l/mva/ecm365/<scheme>/preselection \
        -n dataset sel_type chi2 lepton_iso \
        -t string string float float \
        -v winter2023_IDEA medium 1.0 3

and for the training samples:

    python3 ../../utils/add_parameters_to_root.py \
        -f ../../../outputs/higgs/zh_hww_4l/mva/ecm365/<scheme>/preselection/training \
        -n dataset sel_type chi2 lepton_iso \
        -t string string float float \
        -v winter2023_training_IDEA medium 1.0 3

with e.g., scheme = "medium_full_chi2-1.0_iso-3.0".

'''


from addons.TMVAHelper.TMVAHelper import TMVAHelperXGB
import os

run = os.environ.get("run", "full")  # 'local', 'debug', 'full', 'full+condor'
ecm = os.environ.get("ecm", "240")  # '240' or '365'
is_training = os.environ.get("training", "False").lower() in ("true", "1")
sel_type = os.environ.get("sel_type", 'loose')  # presel, loose, medium, tight
chi2_coeff_default = 0.4
chi2_coeff = float(os.environ.get("chi2", chi2_coeff_default))
lepton_iso = float(os.environ.get("iso", -999))  # default isolation cut for firm selection

print(f"Run type: {run}, ECM: {ecm} GeV, Training mode: {is_training}, selections type: {sel_type}, chi2 coefficient: {chi2_coeff}, lepton isolation cut: {lepton_iso}")

if run == 'debug':  # debug run
    print("Running in debug mode: only 0.5% of bkg, 100% of signal data, 1 chunk")
    fraction = 0.005
    nchunks = 1
    condorize = False
    debug = True
    fullrun = False
elif run == 'full':  # full run
    print("Running in full mode: 100% of the data, 1 chunk")
    fraction = 1
    nchunks = 1
    condorize = False
    debug = False
    fullrun = True
elif run == 'full+condor':  # full run with condor
    print("Running in full mode: 100% of the data, 50 chunks, submitting to condor...")
    fraction = 1
    nchunks = 50
    condorize = True
    debug = False
    fullrun = True
else:  # local run
    print("Running in local mode: only 20% of bkg and 100% of signal data, 1 chunk")
    fraction = 0.2
    nchunks = 1
    condorize = False
    debug = False
    fullrun = False


# list of processes (mandatory)
if is_training:
    processList = {
        f'p8_ee_ZZ_llX_ecm{ecm}':{'fraction': fraction, 'chunks': nchunks},
        f'p8_ee_ZZ_tautauX_ecm{ecm}':{'fraction': fraction, 'chunks': nchunks},
        f'p8_ee_ZZ_ecm{ecm}':{'fraction': fraction, 'chunks': nchunks},
        f'p8_ee_WW_ee_ecm{ecm}':{'fraction': fraction, 'chunks': nchunks},
        f'p8_ee_WW_mumu_ecm{ecm}':{'fraction': fraction, 'chunks': nchunks},
        f'p8_ee_WW_ecm{ecm}':{'fraction': fraction, 'chunks': nchunks},
        f'wzp6_ee_eeH_HWW_{"llnunu_" if ecm=="240" else ""}ecm{ecm}':{'fraction': 1},
        f'wzp6_ee_mumuH_HWW_{"llnunu_" if ecm=="240" else ""}ecm{ecm}':{'fraction': 1},  #
    }
    
else:
    processList = {
        f'p8_ee_ZZ_ecm{ecm}':{'fraction': fraction, 'chunks': nchunks},
        f'p8_ee_WW_ee_ecm{ecm}':{'fraction': fraction, 'chunks': nchunks},
        f'p8_ee_WW_mumu_ecm{ecm}':{'fraction': fraction, 'chunks': nchunks},
        f'p8_ee_WW_ecm{ecm}':{'fraction': fraction, 'chunks': nchunks},
        f'wzp6_ee_eeH_HWW_{"llnunu_" if ecm=="240" else ""}ecm{ecm}':{'fraction': 1},
        f'wzp6_ee_mumuH_HWW_{"llnunu_" if ecm=="240" else ""}ecm{ecm}':{'fraction': 1},
    }
    
    if ecm == '365':
        processList['p8_ee_tt_ecm365'] = {'fraction': fraction, 'chunks': nchunks}

processList = {f'wzp6_ee_mumuH_HWW_{"llnunu_" if ecm=="240" else ""}ecm{ecm}':{'fraction': 0.2}} if debug else processList

# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
prodTag = "FCCee/winter2023/IDEA/" if not is_training else "FCCee/winter2023_training/IDEA/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json" if not is_training else "FCCee_procDict_winter2023_training_IDEA.json"

# Additional/custom C++ functions, defined in header files
includePaths = ["../functions.h"]

# Output directory
output_fix = sel_type
if debug: output_fix += "_debug"
if fullrun: output_fix += "_full"
if chi2_coeff != chi2_coeff_default: output_fix += f"_chi2-{chi2_coeff}"
if lepton_iso != -999: output_fix += f"_iso-{lepton_iso}"

# get time stamp for the output directory
from datetime import datetime
now = datetime.now()
dt_string = now.strftime("%Y%m%d_%H%M%S")
output_fix += f"_{dt_string}"

outputDir   = f"../../../outputs/higgs/zh_hww_4l/mva/ecm{ecm}/{output_fix}/preselection/{'training/' if is_training else ''}"


# Multithreading: -1 means using all cores
nCPUS       = -1

# Batch settings
runBatch    = condorize
batchQueue  = "longlunch"
compGroup = "group_u_FCC.local_gen"

# After training the BDT model, set to True to run inference and add the MVA score to the output ROOT files
bdt_model_path = f"../../../outputs/higgs/zh_hww_4l/mva/ecm{ecm}/{output_fix}/bdt_model.root"
doInference = False


class RDFanalysis():

    # encapsulate analysis logic, definitions and filters in the dataframe
    def analysers(df):

        df = df.Alias("Particle0", "Particle#0.index")
        df = df.Alias("Particle1", "Particle#1.index")
        df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
        df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

        # For signal events, keep only fully-leptonic WW decays (truth-level selection)
        df = df.Define("ww_leptonic", "FCCAnalyses::ZHfunctions::is_ww_leptonic(Particle, Particle1)")
        # df = df.Filter("ww_leptonic")

        ## define muons
        df = df.Alias("Muon0", "Muon#0.index")
        df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)")
        # df = df.Define("muons_all_p", "FCCAnalyses::ReconstructedParticle::get_p(muons_all)")
        
        df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::sel_p(5)(muons_all)")
        # df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
        # df = df.Define("muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons)")
        # df = df.Define("muons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(muons)")
        df = df.Define("muons_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")
        df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")

        if lepton_iso != -999:
            # compute the muon isolation and store muons with an isolation cut of 0.25 in a separate column muons_sel_iso
            df = df.Define("muons_iso", "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(muons, ReconstructedParticles)")
            df = df.Define("muons_sel_iso", f"FCCAnalyses::ZHfunctions::sel_iso({lepton_iso})(muons, muons_iso)")

        ## define electrons
        df = df.Alias("Electron0", "Electron#0.index")
        df = df.Define("electrons_all", "FCCAnalyses::ReconstructedParticle::get(Electron0, ReconstructedParticles)")
        # df = df.Define("electrons_all_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons_all)")
        
        df = df.Define("electrons", "FCCAnalyses::ReconstructedParticle::sel_p(5)(electrons_all)")
        # df = df.Define("electrons_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons)")
        # df = df.Define("electrons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(electrons)")
        # df = df.Define("electrons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(electrons)")
        df = df.Define("electrons_q", "FCCAnalyses::ReconstructedParticle::get_charge(electrons)")
        df = df.Define("electrons_no", "FCCAnalyses::ReconstructedParticle::get_n(electrons)")

        if lepton_iso != -999:
            # compute the muon isolation and store muons with an isolation cut of 0.25 in a separate column muons_sel_iso
            df = df.Define("electrons_iso", "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(electrons, ReconstructedParticles)")
            df = df.Define("electrons_sel_iso", f"FCCAnalyses::ZHfunctions::sel_iso({lepton_iso})(electrons, electrons_iso)")


        #########
        ### CUT 1: require exactly 4 leptons
        #########
        df = df.Define("n_leptons", "muons_no + electrons_no")            
        df = df.Filter("n_leptons == 4")
        
        # If lepton_iso is specified, require exactly 4 isolated leptons
        if lepton_iso != -999:
            df = df.Define("n_leptons_iso", "muons_sel_iso.size() + electrons_sel_iso.size()")
            df = df.Filter("n_leptons_iso == 4")


        #########
        ### CUT 2: at least 2 opposite-sign (OS) leptons
        #########
        # df = df.Filter(f"{leps}_no >= 2 && abs(Sum({leps}_q)) < {leps}_q.size()")
        # df = df.Filter(f"abs(Sum({leps}_q)) <= {leps}_q.size() - 4")
        df = df.Filter(f"abs(Sum(muons_q) + Sum(electrons_q)) <= muons_q.size() + electrons_q.size() - 4")


        #########
        ### CUT 3: at least one same-flavor (SF) lepton pair
        #########
        df = df.Filter("(muons_no >= 2) || (electrons_no >= 2)")


        #########
        ### CUT 4: leptons pT: leading muon pT [25, 80] GeV, subleading muon pT [15, 80] GeV, third muon pT [10,80] GeV, fourth muon pT [10,75] GeV
        #########
        df = df.Define("leptons0", "FCCAnalyses::ReconstructedParticle::merge(muons, electrons)")
        df = df.Define("leptons", "FCCAnalyses::ZHfunctions::sortByPt(leptons0)")
        df = df.Define("leptons_p", "FCCAnalyses::ReconstructedParticle::get_p(leptons)")

        df = df.Define("lep0_p", "leptons_p[0]")
        df = df.Define("lep1_p", "leptons_p[1]")
        df = df.Define("lep2_p", "leptons_p[2]")
        df = df.Define("lep3_p", "leptons_p[3]")
        
        if ecm == '240':
            if sel_type == 'loose':
                df = df.Filter("lep0_p > 20 && lep0_p < 85")
                df = df.Filter("lep1_p > 10 && lep1_p < 80")
                df = df.Filter("lep2_p > 10 && lep2_p < 80")
                df = df.Filter("lep3_p > 10 && lep3_p < 75")
            elif sel_type == 'tight':
                df = df.Filter("lep0_p > 25 && lep0_p < 80")
                df = df.Filter("lep1_p > 15 && lep1_p < 80")
                df = df.Filter("lep2_p > 10 && lep2_p < 80")
                df = df.Filter("lep3_p > 10 && lep3_p < 75")
        elif ecm == '365':
            if sel_type == 'loose' or sel_type == 'medium':
                df = df.Filter("lep0_p > 20 && lep0_p < 165")
                df = df.Filter("lep1_p > 10 && lep1_p < 160")
                df = df.Filter("lep2_p > 5 && lep2_p < 150")
                df = df.Filter("lep3_p > 5 && lep3_p < 150")
            elif sel_type == 'tight':
                df = df.Filter("lep0_p > 70 && lep0_p < 155")
                df = df.Filter("lep1_p > 25 && lep1_p < 105")
                df = df.Filter("lep2_p > 15 && lep2_p < 80")
                df = df.Filter("lep3_p > 5 && lep3_p < 65")


        #########
        ### Reconstruct the Z->ll candidate
        #########
        # Now we build the Z resonance based on the available leptons.
        # The function resonanceBuilder_mass_recoil_advanced returns the best lepton pair compatible with the Z mass (91.2 GeV) and recoil at 125 GeV, out of the 4 leptons, and the two remaining leptons coming from the W's.
        # The argument 0.4 gives a weight to the Z mass and the recoil mass in the chi2 minimization.
        # Technically, it returns a ReconstructedParticleData object with index 0 the Z->ll di-lepton system, index 1 and 2 the leptons of the pair, and index 3 and 4 the other two leptons.
        # If no pair is found, the returned vector is empty.
        # We then require that at least one pair was found (size>=5) to keep the event.
        df = df.Define("zbuilder_result", f"FCCAnalyses::ZHfunctions::resonanceBuilder_mass_recoil_advanced(91.2, 125, {chi2_coeff}, {ecm}, false)(muons, electrons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
        df = df.Filter("zbuilder_result.size() >= 5") # make sure at least one pair was found (and additional two leptons)
        
        df = df.Define("zll", "Vec_rp{zbuilder_result[0]}") # the Z
        df = df.Define("zll_tlv", "FCCAnalyses::ReconstructedParticle::get_tlv(zll, 0)")
        df = df.Define("zll_m", "FCCAnalyses::ReconstructedParticle::get_mass(zll)[0]") # Z mass
        df = df.Define("zll_p", "FCCAnalyses::ReconstructedParticle::get_p(zll)[0]") # momentum of the Z
        df = df.Define("zll_theta", "FCCAnalyses::ReconstructedParticle::get_theta(zll)[0]") # momentum of the Z
        df = df.Define("zll_phi", "FCCAnalyses::ReconstructedParticle::get_phi(zll)[0]") # momentum of the Z
    
        ## Recoil mass
        df = df.Define("zll_recoil", f"FCCAnalyses::ReconstructedParticle::recoilBuilder({ecm})(zll)") # compute the recoil based on the reconstructed Z
        df = df.Define("zll_recoil_m", "FCCAnalyses::ReconstructedParticle::get_mass(zll_recoil)[0]") # recoil mass
        
        ## Study the Z-lepton candidates
        df = df.Define("zll_leps", "Vec_rp{zbuilder_result[1],zbuilder_result[2]}") # the leptons 
        df = df.Define("zll_leps_p", "FCCAnalyses::ReconstructedParticle::get_p(zll_leps)") # get the momentum of the 2 leptons from the Z resonance
        df = df.Define("zll_leps_theta", "FCCAnalyses::ReconstructedParticle::get_theta(zll_leps)") # get the theta of these 2 leptons
        df = df.Define("zll_leps_phi", "FCCAnalyses::ReconstructedParticle::get_phi(zll_leps)") # get the phi of these 2 leptons
        df = df.Define("zll_leps_q", "FCCAnalyses::ReconstructedParticle::get_charge(zll_leps)")

        df = df.Define("zll_lep0_p", "zll_leps_p[0]")
        df = df.Define("zll_lep0_theta", "zll_leps_theta[0]")
        df = df.Define("zll_lep0_phi", "zll_leps_phi[0]")
        df = df.Define("zll_lep1_p", "zll_leps_p[1]")
        df = df.Define("zll_lep1_theta", "zll_leps_theta[1]")
        df = df.Define("zll_lep1_phi", "zll_leps_phi[1]")

        df = df.Define("zll_lep0_tlv", "FCCAnalyses::ReconstructedParticle::get_tlv(zll_leps, 0)")
        df = df.Define("zll_lep1_tlv", "FCCAnalyses::ReconstructedParticle::get_tlv(zll_leps, 1)")
        df = df.Define("zll_leps_dR", "zll_lep0_tlv.DeltaR(zll_lep1_tlv)")
        
        df = df.Define("zll_leps_category", "FCCAnalyses::ZHfunctions::getDileptonCategory(zll_leps)")
        df = df.Define("zll_lep0_p_index", "FCCAnalyses::ZHfunctions::findIndex(zll_lep0_p, {lep0_p, lep1_p, lep2_p, lep3_p})")
        df = df.Define("zll_lep1_p_index", "FCCAnalyses::ZHfunctions::findIndex(zll_lep1_p, {lep0_p, lep1_p, lep2_p, lep3_p})")

        ## Study the WW-lepton candidates
        df = df.Define("WW_leps", "Vec_rp{zbuilder_result[3],zbuilder_result[4]}") # the leptons 
        df = df.Define("WW_leps_p", "FCCAnalyses::ReconstructedParticle::get_p(WW_leps)")
        df = df.Define("WW_leps_theta", "FCCAnalyses::ReconstructedParticle::get_theta(WW_leps)")
        df = df.Define("WW_leps_phi", "FCCAnalyses::ReconstructedParticle::get_phi(WW_leps)")
        df = df.Define("WW_leps_q", "FCCAnalyses::ReconstructedParticle::get_charge(WW_leps)")
        
        df = df.Define("WW_lep0_p", "WW_leps_p[0]")
        df = df.Define("WW_lep0_theta", "WW_leps_theta[0]")
        df = df.Define("WW_lep0_phi", "WW_leps_phi[0]")
        df = df.Define("WW_lep1_p", "WW_leps_p[1]")
        df = df.Define("WW_lep1_theta", "WW_leps_theta[1]")
        df = df.Define("WW_lep1_phi", "WW_leps_phi[1]")
        
        df = df.Define("WW_leps_tlv0", "FCCAnalyses::ReconstructedParticle::get_tlv(WW_leps, 0)")
        df = df.Define("WW_leps_tlv1", "FCCAnalyses::ReconstructedParticle::get_tlv(WW_leps, 1)")
        df = df.Define("WW_leps_dR", "WW_leps_tlv0.DeltaR(WW_leps_tlv1)")

        df = df.Define("WW_leps_category", "FCCAnalyses::ZHfunctions::getDileptonCategory(WW_leps)")
        df = df.Define("WW_lep0_p_index", "FCCAnalyses::ZHfunctions::findIndex(WW_lep0_p, {lep0_p, lep1_p, lep2_p, lep3_p})")
        df = df.Define("WW_lep1_p_index", "FCCAnalyses::ZHfunctions::findIndex(WW_lep1_p, {lep0_p, lep1_p, lep2_p, lep3_p})")
                
        ## Build the WW system using the two leptons not coming from the Z and the missing energy vector
        df = df.Define("missingEnergy_vec", f"FCCAnalyses::ZHfunctions::missingEnergy({ecm}, ReconstructedParticles)")
        df = df.Define("missingEnergy_tlv", "FCCAnalyses::ReconstructedParticle::get_tlv(missingEnergy_vec, 0)")
        df = df.Define("WW_tlv", "missingEnergy_tlv + WW_leps_tlv0 + WW_leps_tlv1")
        df = df.Define("WW_mass", "WW_tlv.M()")
        df = df.Define("WW_p", "WW_tlv.P()")
        df = df.Define("WW_theta", "WW_tlv.Theta()")
        df = df.Define("WW_phi", "WW_tlv.Phi()")

        ## dR(Z, WW)
        df = df.Define("zll_WW_dR", "WW_tlv.DeltaR(zll_tlv)")
        
        
        #########
        ### CUT 5: Z mass window
        #########
        if ecm == '240':
            df = df.Filter("zll_m > 76 && zll_m < 106")
        elif ecm == '365':
            if sel_type == 'loose':
                df = df.Filter("zll_m > 30 && zll_m < 200")
            if sel_type == 'medium':
                # df = df.Filter("zll_m > 71 && zll_m < 111")
                df = df.Filter("zll_m > 61 && zll_m < 121")
            elif sel_type == 'tight':
                df = df.Filter("zll_m > 76 && zll_m < 106")


        #########
        ### CUT 6: Z momentum
        #########
        if ecm == '240':
            df = df.Filter("zll_p > 20 && zll_p < 70")
        elif ecm == '365':
            if sel_type == 'loose' or sel_type == 'medium':
                df = df.Filter("zll_p > 35 && zll_p < 155")
            elif sel_type == 'tight':
                df = df.Filter("zll_p > 60 && zll_p < 155")


        #########
        ### CUT 7: recoil mass window (reconstructed Higgs mass using the recoil method)
        #########
        if ecm == '240':
            if sel_type == 'loose':
                df = df.Filter("zll_recoil_m < 145 && zll_recoil_m > 120")
            elif sel_type == 'tight':
                df = df.Filter("zll_recoil_m < 140 && zll_recoil_m > 120")
        elif ecm == '365':
            if sel_type == 'loose' or sel_type == 'medium':
                df = df.Filter("zll_recoil_m < 230 && zll_recoil_m > 115")
            elif sel_type == 'tight':
                df = df.Filter("zll_recoil_m < 200 && zll_recoil_m > 115")


        #########
        ### CUT 8: cosThetaMiss
        #########  
        df = df.Define("miss_cosTheta", "FCCAnalyses::ZHfunctions::get_cosTheta_miss(missingEnergy_vec)")
        df = df.Define("miss_energy", "FCCAnalyses::ZHfunctions::get_missing_energy(missingEnergy_vec)")
        df = df.Filter("miss_cosTheta < 0.98")


        #########
        ### CUT 9: missingEnergy
        #########  
        if ecm == '240':
            if sel_type == 'loose':
                df = df.Filter("miss_energy > 20 && miss_energy < 120")
            elif sel_type == 'tight':
                df = df.Filter("miss_energy > 30 && miss_energy < 110")
        elif ecm == '365':
            if sel_type == 'loose' or sel_type == 'medium':
                df = df.Filter("miss_energy > 20 && miss_energy < 180")
            elif sel_type == 'tight':
                df = df.Filter("miss_energy > 30 && miss_energy < 160")


        #########
        ### CUT 10: WW system mass window
        #########
        if ecm == '240':
            if sel_type == 'loose':
                df = df.Filter("WW_mass > 60 && WW_mass < 135")
            elif sel_type == 'tight':
                df = df.Filter("WW_mass > 80 && WW_mass < 135")
        elif ecm == '365':
            if sel_type == 'loose' or sel_type == 'medium':
                df = df.Filter("WW_mass > 50")
            elif sel_type == 'tight':
                df = df.Filter("WW_mass > 70")


        #########
        ### CUT 11: dR(l_WW, l_WW)
        #########  
        if ecm == '240':
            df = df.Filter("WW_leps_dR > 0.25")
        elif ecm == '365':
            if sel_type == 'loose' or sel_type == 'medium':
                df = df.Filter("WW_leps_dR > 0.1 && WW_leps_dR < 4.0")
            elif sel_type == 'tight':
                df = df.Filter("WW_leps_dR > 0.1")


        #########
        ### CUT 12: dR(Z->ll, WW*)
        #########  
        if ecm == '365':
            if sel_type == 'medium':
                df = df.Filter("zll_WW_dR > 3.0")
            

        #########
        ### CUT 13: dR(l1, l2)
        #########  
        if ecm == '365':
            if sel_type == 'medium':
                df = df.Filter("zll_leps_dR < 3.0")

        
        if doInference:
            tmva_helper = TMVAHelperXGB(bdt_model_path, "bdt_model") # read the XGBoost training
            df = tmva_helper.run_inference(df, col_name="mva_score") # by default, makes a new column mva_score

        return df


    # define output branches to be saved
    def output():
        
        branchList = [
            # leptons
            "lep0_p",
            "lep1_p",
            "lep2_p",
            "lep3_p",
            "muons_no",
            "muons_q",
            "electrons_no",
            "electrons_q",
            "n_leptons",
            
            # Z->ll system
            "zll_m",
            "zll_p",
            "zll_theta",
            "zll_phi",
            "zll_recoil_m",
            
            # Z->ll leptons 
            "zll_lep0_p",
            "zll_lep0_theta",
            "zll_lep0_phi",
            "zll_lep1_p",
            "zll_lep1_theta",
            "zll_lep1_phi",
            
            "zll_leps_dR",
            "zll_leps_category",
            "zll_lep0_p_index",
            "zll_lep1_p_index",
            
            # WW leptons
            "WW_lep0_p",
            "WW_lep0_theta",
            "WW_lep0_phi",
            "WW_lep1_p",
            "WW_lep1_theta",
            "WW_lep1_phi",

            "WW_leps_dR",
            "WW_leps_category",
            "WW_lep0_p_index",
            "WW_lep1_p_index",
            
            # WW system
            "WW_mass",
            "WW_p",
            "WW_theta",
            "WW_phi",

            # dR(Z, WW)
            "zll_WW_dR",
            
            # missing energy
            "miss_cosTheta",
            "miss_energy",
            
            "ww_leptonic",
        ]
        
        if lepton_iso != -999:
            branchList += [
                "muons_iso",
                "electrons_iso",
                "n_leptons_iso",
            ]


        if doInference:
            branchList.append("mva_score")
            
        return branchList
