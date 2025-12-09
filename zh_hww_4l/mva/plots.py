import ROOT

is_loose = True

# global parameters
intLumi        = 1.
intLumiLabel   = "L = 10.8 ab^{-1}"
ana_tex        = 'e^{+}e^{-}#rightarrow Z(l^{+}l^{-}) H#left[W(l#nu)W(l#nu)#right]'
delphesVersion = '3.4.2'
energy         = 240.0
collider       = 'FCC-ee'
inputDir       = f'../../../outputs/higgs/zh_hww_4l/mva{"_loose" if is_loose else ""}/final_selection/full/'
formats        = ['pdf']
outdir         = f'../../../outputs/higgs/zh_hww_4l/mva{"_loose" if is_loose else ""}/plots/'
yaxis          = ['lin','log']
stacksig       = ['nostack']
plotStatUnc    = True




variables = ['zll_recoil_m', 'zll_recoil_m_final', 'zll_m', 'zll_p', 'mva_score']
rebin = [1, 1] # uniform rebin per variable (optional)

###Dictonnary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['ZH']   = ["sel0", "sel1"]

extralabel = {}
extralabel['sel0'] = "Basic selection"
extralabel['sel1'] = "MVA > 0.5"

colors = {}
colors['ZH'] = ROOT.kRed
colors['WW'] = ROOT.kBlue+1
colors['ZZ'] = ROOT.kGreen+2


plots = {}
plots['ZH'] = {'signal':{'ZH':['wzp6_ee_eeH_HWW_ecm240', 'wzp6_ee_mumuH_HWW_ecm240']},
               'backgrounds':{'WW':['p8_ee_WW_ecm240'], 'ZZ':['p8_ee_ZZ_ecm240']}
           }

legend = {}
legend['ZH'] = 'ZH'
legend['WW'] = 'WW'
legend['ZZ'] = 'ZZ'
