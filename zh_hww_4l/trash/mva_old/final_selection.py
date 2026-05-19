

is_loose = True

#Input directory where the files produced at the pre-selection level are
inputDir = f'../../../outputs/higgs/zh_hww_4l/mva{"_loose" if is_loose else ""}/preselection_with_bdt/full/'

#Input directory where the files produced at the pre-selection level are
#Optional: output directory, default is local running directory
outputDir = f'../../../outputs/higgs/zh_hww_4l/mva{"_loose" if is_loose else ""}/final_selection/full/'

# if no processList or empty dictionary provided, run over all ROOT files in the input directory
processList = {}

#Link to the dictonary that contains all the cross section informations etc...
procDict = "FCCee_procDict_winter2023_IDEA.json"

#Number of CPUs to use
nCPUS = -1

#produces ROOT TTrees, default is False
doTree = False


# scale the histograms with the cross-section and integrated luminosity
doScale = True
intLumi = 10800000.0 # 10.8 /ab for 240 GeV

saveTabular = True

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
    "sel0": "1==1",
    "sel1": "mva_score > 0.5",
}


#Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    "mva_score":{"cols": ["mva_score"], "title": "MVA score", "bins": [(100,0,1)]},
    "zll_m":{"cols": ["zll_m"], "title": "m_{Z} (GeV)", "bins": [(250,0,250)]},
    "zll_p":{"cols": ["zll_p"], "title": "p_{Z} (GeV)", "bins": [(250,0,250)]},
    "zll_recoil_m":{"cols": ["zll_recoil_m"], "title": "Recoil (GeV)", "bins": [(250,0,250)]},
    "zll_recoil_m_final":{"cols": ["zll_recoil_m"], "title": "Recoil (GeV)", "bins": [(200,120,140)]},
}
