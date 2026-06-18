
07/06/2026

# Loose

## Numbers

[gino@lxplus942 utils]$ root -l -q 'PrintEntries.C("../../outputs/higgs/zh_hww_4l/mva/ecm365/loose_full/preselection/training")'

sig:
        training/wzp6_ee_eeH_HWW_ecm365_inc.root: 56231 entries
        training/wzp6_ee_mumuH_HWW_ecm365_inc.root: 62779 entries
        training/wzp6_ee_eeH_HWW_ecm365.root: 40796 entries
        training/wzp6_ee_mumuH_HWW_ecm365.root: 45892 entries

bkg:
        training/p8_ee_ZZ_llX_ecm365.root: 98328 entries
        training/p8_ee_ZZ_tautauX_ecm365.root: 118145 entries
        training/p8_ee_WW_ee_ecm365.root: 11972 entries
        training/p8_ee_WW_mumu_ecm365.root: 5562 entries
        training/p8_ee_WW_ecm365.root: 142 entries


[gino@lxplus942 utils]$ root -l -q 'PrintEntries.C("../../outputs/higgs/zh_hww_4l/mva/ecm365/loose_full/preselection")'

sig:
        wzp6_ee_eeH_HWW_ecm365_inc.root: 51719 entries
        wzp6_ee_mumuH_HWW_ecm365_inc.root: 57224 entries
        wzp6_ee_eeH_HWW_ecm365.root: 37400 entries
        wzp6_ee_mumuH_HWW_ecm365.root: 41717 entries

bkg:
        p8_ee_ZZ_ecm365.root: 13699 entries
        p8_ee_WW_ee_ecm365.root: 2316 entries
        p8_ee_WW_mumu_ecm365.root: 1113 entries
        p8_ee_WW_ecm365.root: 1391 entries
        p8_ee_tt_ecm365.root: 323 entries

## Cutflows

Cutflow for 365 GeV - Loose Selection
=====================================

/#         Cut                             Significance    Z(ll)H                Z(ee)H                Z(mumu)H              ZZ                    WW                    WW_ll                 tt                   
---------- ------------------------------- --------------- --------------------- --------------------- --------------------- --------------------- --------------------- --------------------- ---------------------
Cut 0      All events                      0.057           3.4625e+02 (100.0%)   2.2116e+02 (100.0%)   1.2509e+02 (100.0%)   1.9284e+06 (100.0%)   3.2150e+07 (100.0%)   1.0710e+06 (100.0%)   2.4000e+06 (100.0%)  
Cut 1      4 leptons                       1.429           3.0108e+02 (87.0%)    1.8824e+02 (85.1%)    1.1284e+02 (90.2%)    1.8999e+04 (1.0%)     3.6249e+03 (0.0%)     1.0107e+03 (0.1%)     2.0475e+04 (0.9%)    
Cut 2      2 OS pairs                      1.605           3.0108e+02 (100.0%)   1.8824e+02 (100.0%)   1.1284e+02 (100.0%)   1.7639e+04 (92.8%)    3.3545e+03 (92.5%)    1.0103e+03 (100.0%)   1.2892e+04 (63.0%)   
Cut 3      ≥1 SF pair                      1.605           3.0108e+02 (100.0%)   1.8824e+02 (100.0%)   1.1284e+02 (100.0%)   1.7639e+04 (100.0%)   3.3545e+03 (100.0%)   1.0103e+03 (100.0%)   1.2892e+04 (100.0%)  
Cut 4      p_l_1,p_l_2,p_l_3,p_l_4         1.737           3.0100e+02 (100.0%)   1.8818e+02 (100.0%)   1.1282e+02 (100.0%)   1.4963e+04 (84.8%)    2.7545e+03 (82.1%)    9.5753e+02 (94.8%)    1.1038e+04 (85.6%)   
Cut 5      30 < m_ll < 200                 1.924           2.9439e+02 (97.8%)    1.8189e+02 (96.7%)    1.1250e+02 (99.7%)    1.3657e+04 (91.3%)    1.7952e+03 (65.2%)    7.7862e+02 (81.3%)    6.8773e+03 (62.3%)   
Cut 6      35 < p_ll < 155                 2.277           2.9168e+02 (99.1%)    1.7980e+02 (98.9%)    1.1188e+02 (99.5%)    8.3487e+03 (61.1%)    1.6230e+03 (90.4%)    7.1516e+02 (91.9%)    5.4338e+03 (79.0%)   
Cut 7      115 < m_rec < 230               3.002           2.7694e+02 (94.9%)    1.6979e+02 (94.4%)    1.0716e+02 (95.8%)    6.0461e+03 (72.4%)    1.0809e+03 (66.6%)    5.6195e+02 (78.6%)    5.4489e+02 (10.0%)   
Cut 8      |cosθ_miss| < 0.98              3.477           2.7153e+02 (98.0%)    1.6634e+02 (98.0%)    1.0519e+02 (98.2%)    3.7049e+03 (61.3%)    1.0483e+03 (97.0%)    5.4166e+02 (96.4%)    5.3333e+02 (97.9%)   
Cut 9      20 < E_miss < 180               4.782           2.6960e+02 (99.3%)    1.6536e+02 (99.4%)    1.0423e+02 (99.1%)    9.0163e+02 (24.3%)    9.8482e+02 (93.9%)    4.9063e+02 (90.6%)    5.3156e+02 (99.7%)   
Cut 10     m_WW* > 50                      5.635           2.6766e+02 (99.3%)    1.6428e+02 (99.3%)    1.0338e+02 (99.2%)    4.6122e+02 (51.2%)    7.8767e+02 (80.0%)    4.3140e+02 (87.9%)    3.0844e+02 (58.0%)   
Cut 11     0.2<ΔR(l_WW*,1,l_WW*,2)<4.0     6.607           2.6466e+02 (98.9%)    1.6218e+02 (98.7%)    1.0248e+02 (99.1%)    4.2975e+02 (93.2%)    4.3949e+02 (55.8%)    1.8362e+02 (42.6%)    2.8711e+02 (93.1%)   

Total eff                                                  76.4341%              73.3319%              81.9185%              0.0223%               0.0014%               0.0171%               0.0120%              
Entries                                                    79117                 37400                 41717                 13699                 1391                  3429                  323                  


Cutflow for 365 GeV - Loose Selection - Training Dataset
========================================================

/#         Cut                             Significance    Z(ll)H                Z(ee)H                Z(mumu)H              ZZ_ll                 WW                    WW_ll                
---------- ------------------------------- --------------- --------------------- --------------------- --------------------- --------------------- --------------------- ---------------------
Cut 0      All events                      0.060           3.4664e+02 (100.0%)   2.2078e+02 (100.0%)   1.2586e+02 (100.0%)   4.9410e+05 (100.0%)   3.2149e+07 (100.0%)   1.0710e+06 (100.0%)  
Cut 1      4 leptons                       0.576           3.0217e+02 (87.2%)    1.8824e+02 (85.3%)    1.1393e+02 (90.5%)    2.7017e+05 (54.7%)    3.3916e+03 (0.0%)     9.9438e+02 (0.1%)    
Cut 2      2 OS pairs                      0.577           3.0217e+02 (100.0%)   1.8824e+02 (100.0%)   1.1393e+02 (100.0%)   2.7004e+05 (99.9%)    3.1431e+03 (92.7%)    9.9403e+02 (100.0%)  
Cut 3      ≥1 SF pair                      0.577           3.0217e+02 (100.0%)   1.8824e+02 (100.0%)   1.1393e+02 (100.0%)   2.7004e+05 (100.0%)   3.1431e+03 (100.0%)   9.9403e+02 (100.0%)  
Cut 4      p_l_1,p_l_2,p_l_3,p_l_4         0.625           3.0208e+02 (100.0%)   1.8817e+02 (100.0%)   1.1391e+02 (100.0%)   2.2944e+05 (85.0%)    2.6397e+03 (84.0%)    9.4203e+02 (94.8%)   
Cut 5      30 < m_ll < 200                 0.621           2.9542e+02 (97.8%)    1.8182e+02 (96.6%)    1.1360e+02 (99.7%)    2.2370e+05 (97.5%)    1.6780e+03 (63.6%)    7.6523e+02 (81.2%)   
Cut 6      35 < p_ll < 155                 0.801           2.9255e+02 (99.0%)    1.7962e+02 (98.8%)    1.1293e+02 (99.4%)    1.3077e+05 (58.5%)    1.5361e+03 (91.5%)    7.0407e+02 (92.0%)   
Cut 7      115 < m_rec < 230               0.920           2.7827e+02 (95.1%)    1.6994e+02 (94.6%)    1.0832e+02 (95.9%)    8.9619e+04 (68.5%)    1.0649e+03 (69.3%)    5.5570e+02 (78.9%)   
Cut 8      |cosθ_miss| < 0.98              1.293           2.7264e+02 (98.0%)    1.6644e+02 (97.9%)    1.0620e+02 (98.0%)    4.2594e+04 (47.5%)    1.0391e+03 (97.6%)    5.3604e+02 (96.5%)   
Cut 9      20 < E_miss < 180               5.699           2.7088e+02 (99.4%)    1.6558e+02 (99.5%)    1.0531e+02 (99.2%)    5.1837e+02 (1.2%)     9.8424e+02 (94.7%)    4.8546e+02 (90.6%)   
Cut 10     m_WW* > 50                      6.094           2.6878e+02 (99.2%)    1.6437e+02 (99.3%)    1.0442e+02 (99.2%)    4.4214e+02 (85.3%)    8.0675e+02 (82.0%)    4.2752e+02 (88.1%)   
Cut 11     0.2<ΔR(l_WW*,1,l_WW*,2)<4.0     7.237           2.6550e+02 (98.8%)    1.6216e+02 (98.7%)    1.0334e+02 (99.0%)    4.3429e+02 (98.2%)    4.5824e+02 (56.8%)    1.8791e+02 (44.0%)   

Total eff                                                  76.5931%              73.4507%              82.1054%              0.0879%               0.0014%               0.0175%              
Entries                                                    86688                 40796                 45892                 216473                142                   17534                


## Fit results:

Minuit2Minimizer : Valid minimum - status = 0
FVAL  = 0
Edm   = 2.10671033108341428e-14
Nfcn  = 26
bkg_norm	  = 0	 +/-  0.969617
r	  = 1	 +/-  0.0658628	(limited)
Minimization finished with status=0
Minimization success! status=0
Minimized in 0.040481 seconds (0.020000 CPU time)
FINAL NLL - NLL0 VALUE = 1.937430372e-08


 --- MultiDimFit ---
best fit parameter values: 
   r :    +1.000
Done in 0.00 min (cpu), 0.00 min (real)
6 log messages saved to combine_logger.out

==> 6.6% uncertainty


## tests

how to reduce ttbar contribution without impacting signal acceptance

### zll_recoil_m

[gino@lxplus942 utils]$ python3 simple_cut_optim.py --path '../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full' --ecm 365 --variables zll_recoil_m_final -xmin 115 -xmax 200
Found histograms: ['zll_recoil_m_final']
Optimizing cuts for histogram: zll_recoil_m_final
  For fixed window [115.0, 200.0] (bins [1151, 2001]), Z = 8.6720 with S=245.129 and B=553.886

  Signal yields:
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/wzp6_ee_mumuH_HWW_ecm365.root: 96.912 (eff=94.571%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/wzp6_ee_eeH_HWW_ecm365.root: 148.217 (eff=91.390%)
  Background yields:
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/p8_ee_ZZ_ecm365.root: 353.205 (eff=82.188%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/p8_ee_WW_ee_ecm365.root: 94.891 (eff=76.511%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/p8_ee_WW_mumu_ecm365.root: 47.124 (eff=79.066%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/p8_ee_tt_ecm365.root: 58.667 (eff=20.433%)



[gino@lxplus942 utils]$ python3 simple_cut_optim.py --path '../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full' --ecm 365 --variables zll_recoil_m_final -xmin 115 -xmax 210
Found histograms: ['zll_recoil_m_final']
Optimizing cuts for histogram: zll_recoil_m_final
  For fixed window [115.0, 210.0] (bins [1151, 2101]), Z = 8.4431 with S=253.134 and B=645.732

  Signal yields:
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/wzp6_ee_mumuH_HWW_ecm365.root: 99.150 (eff=96.754%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/wzp6_ee_eeH_HWW_ecm365.root: 153.984 (eff=94.947%)
  Background yields:
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/p8_ee_ZZ_ecm365.root: 383.792 (eff=89.306%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/p8_ee_WW_ee_ecm365.root: 106.243 (eff=85.665%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/p8_ee_WW_mumu_ecm365.root: 52.586 (eff=88.230%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/p8_ee_tt_ecm365.root: 103.111 (eff=35.913%)


### zll_WW_dR

[gino@lxplus942 utils]$ python3 simple_cut_optim.py --path '../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full' --ecm 365 --variables zll_WW_dR_final  -xmin 0 -xmax 10
Found histograms: ['zll_WW_dR_final']
Optimizing cuts for histogram: zll_WW_dR_final
  For fixed window [0.0, 10.0] (bins [501, 1001]), Z = 7.7534 with S=264.656 and B=900.484

  Signal yields:
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/wzp6_ee_mumuH_HWW_ecm365.root: 102.476 (eff=100.000%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/wzp6_ee_eeH_HWW_ecm365.root: 162.180 (eff=100.000%)
  Background yields:
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/p8_ee_ZZ_ecm365.root: 429.750 (eff=100.000%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/p8_ee_WW_ee_ecm365.root: 124.022 (eff=100.000%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/p8_ee_WW_mumu_ecm365.root: 59.601 (eff=100.000%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/p8_ee_tt_ecm365.root: 287.111 (eff=100.000%)

============================
 OPTIMAL DOUBLE-WINDOW CUTS 
============================

Histogram: zll_WW_dR_final
  Best significance Z = 7.7534
  Cut window in bins = (501, 1001)
  Cut window in x    = [0.0000, 10.0200]
  S = 264.656,  B = 900.484

Significance forula used: S/sqrt(S+B)
Cut optimization completed.

====

[gino@lxplus942 utils]$ python3 simple_cut_optim.py --path '../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full' --ecm 365 --variables zll_WW_dR_final  -xmin 2.5 -xmax 10
Found histograms: ['zll_WW_dR_final']
Optimizing cuts for histogram: zll_WW_dR_final
  For fixed window [2.5, 10.0] (bins [626, 1001]), Z = 8.0300 with S=263.837 and B=815.697

  Signal yields:
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/wzp6_ee_mumuH_HWW_ecm365.root: 102.243 (eff=99.772%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/wzp6_ee_eeH_HWW_ecm365.root: 161.595 (eff=99.639%)
  Background yields:
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/p8_ee_ZZ_ecm365.root: 415.100 (eff=96.591%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/p8_ee_WW_ee_ecm365.root: 123.593 (eff=99.655%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/p8_ee_WW_mumu_ecm365.root: 59.226 (eff=99.371%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/p8_ee_tt_ecm365.root: 217.778 (eff=75.851%)

============================
 OPTIMAL DOUBLE-WINDOW CUTS 
============================

Histogram: zll_WW_dR_final
  Best significance Z = 8.0300
  Cut window in bins = (626, 1001)
  Cut window in x    = [2.5000, 10.0200]
  S = 263.837,  B = 815.697

Significance forula used: S/sqrt(S+B)
Cut optimization completed.

===

[gino@lxplus942 utils]$ python3 simple_cut_optim.py --path '../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full' --ecm 365 --variables zll_WW_dR_final  -xmin 3 -xmax 10
Found histograms: ['zll_WW_dR_final']
Optimizing cuts for histogram: zll_WW_dR_final
  For fixed window [3.0, 10.0] (bins [651, 1001]), Z = 8.5210 with S=259.801 and B=669.818

  Signal yields:
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/wzp6_ee_mumuH_HWW_ecm365.root: 100.864 (eff=98.427%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/wzp6_ee_eeH_HWW_ecm365.root: 158.936 (eff=98.000%)
  Background yields:
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/p8_ee_ZZ_ecm365.root: 385.141 (eff=89.620%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/p8_ee_WW_ee_ecm365.root: 121.987 (eff=98.359%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/p8_ee_WW_mumu_ecm365.root: 58.691 (eff=98.473%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/loose_full/p8_ee_tt_ecm365.root: 104.000 (eff=36.223%)

============================
 OPTIMAL DOUBLE-WINDOW CUTS 
============================

Histogram: zll_WW_dR_final
  Best significance Z = 8.5210
  Cut window in bins = (651, 1001)
  Cut window in x    = [3.0000, 10.0200]
  S = 259.801,  B = 669.818

Significance forula used: S/sqrt(S+B)
Cut optimization completed.


==> zll_WW_dR > 3: ttbar 36%, sig 98%


# medium (with dR(Z->ll, WW*) cut)

## cutflows

Cutflow for 365 GeV - Medium Selection
======================================

/#         Cut                             Significance    Z(ll)H                Z(ee)H                Z(mumu)H              ZZ                    WW                    WW_ll                 tt                   
---------- ------------------------------- --------------- --------------------- --------------------- --------------------- --------------------- --------------------- --------------------- ---------------------
Cut 0      All events                      0.057           3.4625e+02 (100.0%)   2.2116e+02 (100.0%)   1.2509e+02 (100.0%)   1.9284e+06 (100.0%)   3.2150e+07 (100.0%)   1.0710e+06 (100.0%)   2.4000e+06 (100.0%)  
Cut 1      4 leptons                       1.429           3.0108e+02 (87.0%)    1.8824e+02 (85.1%)    1.1284e+02 (90.2%)    1.8999e+04 (1.0%)     3.6249e+03 (0.0%)     1.0107e+03 (0.1%)     2.0475e+04 (0.9%)    
Cut 2      2 OS pairs                      1.605           3.0108e+02 (100.0%)   1.8824e+02 (100.0%)   1.1284e+02 (100.0%)   1.7639e+04 (92.8%)    3.3545e+03 (92.5%)    1.0103e+03 (100.0%)   1.2892e+04 (63.0%)   
Cut 3      ≥1 SF pair                      1.605           3.0108e+02 (100.0%)   1.8824e+02 (100.0%)   1.1284e+02 (100.0%)   1.7639e+04 (100.0%)   3.3545e+03 (100.0%)   1.0103e+03 (100.0%)   1.2892e+04 (100.0%)  
Cut 4      p_l_1,p_l_2,p_l_3,p_l_4         1.737           3.0100e+02 (100.0%)   1.8818e+02 (100.0%)   1.1282e+02 (100.0%)   1.4963e+04 (84.8%)    2.7545e+03 (82.1%)    9.5753e+02 (94.8%)    1.1038e+04 (85.6%)   
Cut 5      30 < m_ll < 200                 1.924           2.9439e+02 (97.8%)    1.8189e+02 (96.7%)    1.1250e+02 (99.7%)    1.3657e+04 (91.3%)    1.7952e+03 (65.2%)    7.7862e+02 (81.3%)    6.8773e+03 (62.3%)   
Cut 6      35 < p_ll < 155                 2.277           2.9168e+02 (99.1%)    1.7980e+02 (98.9%)    1.1188e+02 (99.5%)    8.3487e+03 (61.1%)    1.6230e+03 (90.4%)    7.1516e+02 (91.9%)    5.4338e+03 (79.0%)   
Cut 7      115 < m_rec < 230               3.002           2.7694e+02 (94.9%)    1.6979e+02 (94.4%)    1.0716e+02 (95.8%)    6.0461e+03 (72.4%)    1.0809e+03 (66.6%)    5.6195e+02 (78.6%)    5.4489e+02 (10.0%)   
Cut 8      |cosθ_miss| < 0.98              3.477           2.7153e+02 (98.0%)    1.6634e+02 (98.0%)    1.0519e+02 (98.2%)    3.7049e+03 (61.3%)    1.0483e+03 (97.0%)    5.4166e+02 (96.4%)    5.3333e+02 (97.9%)   
Cut 9      20 < E_miss < 180               4.782           2.6960e+02 (99.3%)    1.6536e+02 (99.4%)    1.0423e+02 (99.1%)    9.0163e+02 (24.3%)    9.8482e+02 (93.9%)    4.9063e+02 (90.6%)    5.3156e+02 (99.7%)   
Cut 10     m_WW* > 50                      5.635           2.6766e+02 (99.3%)    1.6428e+02 (99.3%)    1.0338e+02 (99.2%)    4.6122e+02 (51.2%)    7.8767e+02 (80.0%)    4.3140e+02 (87.9%)    3.0844e+02 (58.0%)   
Cut 11     0.2<ΔR(l_WW*,1,l_WW*,2)<4.0     6.607           2.6466e+02 (98.9%)    1.6218e+02 (98.7%)    1.0248e+02 (99.1%)    4.2975e+02 (93.2%)    4.3949e+02 (55.8%)    1.8362e+02 (42.6%)    2.8711e+02 (93.1%)   
Cut 12     ΔR(Z→ll, WW*) > 3.0             7.137           2.5980e+02 (98.2%)    1.5894e+02 (98.0%)    1.0086e+02 (98.4%)    3.8514e+02 (89.6%)    3.9557e+02 (90.0%)    1.8068e+02 (98.4%)    1.0400e+02 (36.2%)   

Total eff                                                  75.0319%              71.8653%              80.6303%              0.0200%               0.0012%               0.0169%               0.0043%              
Entries                                                    77713                 36652                 41061                 12277                 1252                  3374                  117                  


Cutflow for 365 GeV - Medium Selection - Training Dataset
=========================================================

/#         Cut                             Significance    Z(ll)H                Z(ee)H                Z(mumu)H              ZZ_ll                 WW                    WW_ll                
---------- ------------------------------- --------------- --------------------- --------------------- --------------------- --------------------- --------------------- ---------------------
Cut 0      All events                      0.060           3.4664e+02 (100.0%)   2.2078e+02 (100.0%)   1.2586e+02 (100.0%)   4.9410e+05 (100.0%)   3.2149e+07 (100.0%)   1.0710e+06 (100.0%)  
Cut 1      4 leptons                       0.576           3.0217e+02 (87.2%)    1.8824e+02 (85.3%)    1.1393e+02 (90.5%)    2.7017e+05 (54.7%)    3.3916e+03 (0.0%)     9.9438e+02 (0.1%)    
Cut 2      2 OS pairs                      0.577           3.0217e+02 (100.0%)   1.8824e+02 (100.0%)   1.1393e+02 (100.0%)   2.7004e+05 (99.9%)    3.1431e+03 (92.7%)    9.9403e+02 (100.0%)  
Cut 3      ≥1 SF pair                      0.577           3.0217e+02 (100.0%)   1.8824e+02 (100.0%)   1.1393e+02 (100.0%)   2.7004e+05 (100.0%)   3.1431e+03 (100.0%)   9.9403e+02 (100.0%)  
Cut 4      p_l_1,p_l_2,p_l_3,p_l_4         0.625           3.0208e+02 (100.0%)   1.8817e+02 (100.0%)   1.1391e+02 (100.0%)   2.2944e+05 (85.0%)    2.6397e+03 (84.0%)    9.4203e+02 (94.8%)   
Cut 5      30 < m_ll < 200                 0.621           2.9542e+02 (97.8%)    1.8182e+02 (96.6%)    1.1360e+02 (99.7%)    2.2370e+05 (97.5%)    1.6780e+03 (63.6%)    7.6523e+02 (81.2%)   
Cut 6      35 < p_ll < 155                 0.801           2.9255e+02 (99.0%)    1.7962e+02 (98.8%)    1.1293e+02 (99.4%)    1.3077e+05 (58.5%)    1.5361e+03 (91.5%)    7.0407e+02 (92.0%)   
Cut 7      115 < m_rec < 230               0.920           2.7827e+02 (95.1%)    1.6994e+02 (94.6%)    1.0832e+02 (95.9%)    8.9619e+04 (68.5%)    1.0649e+03 (69.3%)    5.5570e+02 (78.9%)   
Cut 8      |cosθ_miss| < 0.98              1.293           2.7264e+02 (98.0%)    1.6644e+02 (97.9%)    1.0620e+02 (98.0%)    4.2594e+04 (47.5%)    1.0391e+03 (97.6%)    5.3604e+02 (96.5%)   
Cut 9      20 < E_miss < 180               5.699           2.7088e+02 (99.4%)    1.6558e+02 (99.5%)    1.0531e+02 (99.2%)    5.1837e+02 (1.2%)     9.8424e+02 (94.7%)    4.8546e+02 (90.6%)   
Cut 10     m_WW* > 50                      6.094           2.6878e+02 (99.2%)    1.6437e+02 (99.3%)    1.0442e+02 (99.2%)    4.4214e+02 (85.3%)    8.0675e+02 (82.0%)    4.2752e+02 (88.1%)   
Cut 11     0.2<ΔR(l_WW*,1,l_WW*,2)<4.0     7.237           2.6550e+02 (98.8%)    1.6216e+02 (98.7%)    1.0334e+02 (99.0%)    4.3429e+02 (98.2%)    4.5824e+02 (56.8%)    1.8791e+02 (44.0%)   
Cut 12     ΔR(Z→ll, WW*) > 3.0             7.264           2.6033e+02 (98.1%)    1.5874e+02 (97.9%)    1.0159e+02 (98.3%)    4.2266e+02 (97.3%)    4.1628e+02 (90.8%)    1.8498e+02 (98.4%)   

Total eff                                                  75.0999%              71.8987%              80.7153%              0.0855%               0.0013%               0.0173%              
Entries                                                    85049                 39934                 45115                 210738                129                   17261                


WW_ll is used for both training and analysis.


## fit results

Minuit2Minimizer : Valid minimum - status = 0
FVAL  = 0
Edm   = 7.79410117501053883e-14
Nfcn  = 24
bkg_norm	  = 0	 +/-  0.974914
r	  = 1	 +/-  0.0647676	(limited)
Minimization finished with status=0
Minimization success! status=0
Minimized in 0.038046 seconds (0.030000 CPU time)
FINAL NLL - NLL0 VALUE = 9.950966568e-09


 --- MultiDimFit ---
best fit parameter values: 
   r :    +1.000
Done in 0.00 min (cpu), 0.00 min (real)
6 log messages saved to combine_logger.out

==> 6.47% uncertainty


# medium + inclusive WW used in the fit

## cutflow

Cutflow for 365 GeV - Medium Selection - Inclusive WW in Fit
============================================================

/#         Cut                             Significance    Z(ll)H                Z(ee)H                Z(mumu)H              ZZ                    WW                    tt                   
---------- ------------------------------- --------------- --------------------- --------------------- --------------------- --------------------- --------------------- ---------------------
Cut 0      All events                      0.057           3.4625e+02 (100.0%)   2.2116e+02 (100.0%)   1.2509e+02 (100.0%)   1.9284e+06 (100.0%)   3.2150e+07 (100.0%)   2.4000e+06 (100.0%)  
Cut 1      4 leptons                       1.445           3.0108e+02 (87.0%)    1.8824e+02 (85.1%)    1.1284e+02 (90.2%)    1.8999e+04 (1.0%)     3.6249e+03 (0.0%)     2.0475e+04 (0.9%)    
Cut 2      2 OS pairs                      1.628           3.0108e+02 (100.0%)   1.8824e+02 (100.0%)   1.1284e+02 (100.0%)   1.7639e+04 (92.8%)    3.3545e+03 (92.5%)    1.2892e+04 (63.0%)   
Cut 3      ≥1 SF pair                      1.628           3.0108e+02 (100.0%)   1.8824e+02 (100.0%)   1.1284e+02 (100.0%)   1.7639e+04 (100.0%)   3.3545e+03 (100.0%)   1.2892e+04 (100.0%)  
Cut 4      p_l_1,p_l_2,p_l_3,p_l_4         1.766           3.0100e+02 (100.0%)   1.8818e+02 (100.0%)   1.1282e+02 (100.0%)   1.4963e+04 (84.8%)    2.7545e+03 (82.1%)    1.1038e+04 (85.6%)   
Cut 5      30 < m_ll < 200                 1.957           2.9439e+02 (97.8%)    1.8189e+02 (96.7%)    1.1250e+02 (99.7%)    1.3657e+04 (91.3%)    1.7952e+03 (65.2%)    6.8773e+03 (62.3%)   
Cut 6      35 < p_ll < 155                 2.328           2.9168e+02 (99.1%)    1.7980e+02 (98.9%)    1.1188e+02 (99.5%)    8.3487e+03 (61.1%)    1.6230e+03 (90.4%)    5.4338e+03 (79.0%)   
Cut 7      115 < m_rec < 230               3.106           2.7694e+02 (94.9%)    1.6979e+02 (94.4%)    1.0716e+02 (95.8%)    6.0461e+03 (72.4%)    1.0809e+03 (66.6%)    5.4489e+02 (10.0%)   
Cut 8      |cosθ_miss| < 0.98              3.642           2.7153e+02 (98.0%)    1.6634e+02 (98.0%)    1.0519e+02 (98.2%)    3.7049e+03 (61.3%)    1.0483e+03 (97.0%)    5.3333e+02 (97.9%)   
Cut 9      20 < E_miss < 180               5.200           2.6960e+02 (99.3%)    1.6536e+02 (99.4%)    1.0423e+02 (99.1%)    9.0163e+02 (24.3%)    9.8482e+02 (93.9%)    5.3156e+02 (99.7%)   
Cut 10     m_WW* > 50                      6.265           2.6766e+02 (99.3%)    1.6428e+02 (99.3%)    1.0338e+02 (99.2%)    4.6122e+02 (51.2%)    7.8767e+02 (80.0%)    3.0844e+02 (58.0%)   
Cut 11     0.2<ΔR(l_WW*,1,l_WW*,2)<4.0     7.021           2.6466e+02 (98.9%)    1.6218e+02 (98.7%)    1.0248e+02 (99.1%)    4.2975e+02 (93.2%)    4.3949e+02 (55.8%)    2.8711e+02 (93.1%)   
Cut 12     ΔR(Z→ll, WW*) > 3.0             7.679           2.5980e+02 (98.2%)    1.5894e+02 (98.0%)    1.0086e+02 (98.4%)    3.8514e+02 (89.6%)    3.9557e+02 (90.0%)    1.0400e+02 (36.2%)   

Total eff                                                  75.0319%              71.8653%              80.6303%              0.0200%               0.0012%               0.0043%              
Entries                                                    77713                 36652                 41061                 12277                 1252                  117                  


training is the same as "medium".


## fit results

Minuit2Minimizer : Valid minimum - status = 0
FVAL  = -6.66232487112420749e-13
Edm   = 3.05008664920756697e-16
Nfcn  = 31
bkg_norm	  = -1.30648e-07	 +/-  0.969622
r	  = 1	 +/-  0.0668733	(limited)
Minimization finished with status=0
Minimization success! status=0
Minimized in 0.039198 seconds (0.020000 CPU time)
FINAL NLL - NLL0 VALUE = 8.527464185e-09


 --- MultiDimFit ---
best fit parameter values: 
   r :    +1.000
Done in 0.00 min (cpu), 0.00 min (real)
6 log messages saved to combine_logger.out

==> 6.7% uncertainty


# tight + inclusive WW used in the fit + medium training

Use the same training as the `medium`, but tighter selections for the analysis.



# lepton iso

[gino@lxplus910 utils]$ python simple_cut_optim.py         --path '../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso/'         --ecm 365         --variables lep0_iso_final -xmin 0 -xmax 0.25
Found histograms: ['lep0_iso_final']
Optimizing cuts for histogram: lep0_iso_final
  For fixed window [0.0, 0.25] (bins [1, 251]), Z = 8.4245 with S=252.391 and B=645.161

  Signal yields:
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso//wzp6_ee_mumuH_HWW_ecm365.root: 98.381 (eff=97.538%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso//wzp6_ee_eeH_HWW_ecm365.root: 154.010 (eff=96.901%)
  Background yields:
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso//p8_ee_ZZ_ecm365.root: 380.195 (eff=95.948%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso//p8_ee_WW_ee_ecm365.root: 116.204 (eff=92.735%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso//p8_ee_WW_mumu_ecm365.root: 56.763 (eff=91.775%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso//p8_ee_tt_ecm365.root: 92.000 (eff=92.000%)


[gino@lxplus910 utils]$ python simple_cut_optim.py         --path '../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso/'         --ecm 365         --variables lep1_iso_final -xmin 0 -xmax 0.25
Found histograms: ['lep1_iso_final']
Optimizing cuts for histogram: lep1_iso_final
  For fixed window [0.0, 0.25] (bins [1, 251]), Z = 8.1578 with S=232.055 and B=577.114

  Signal yields:
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso//wzp6_ee_mumuH_HWW_ecm365.root: 89.948 (eff=89.177%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso//wzp6_ee_eeH_HWW_ecm365.root: 142.107 (eff=89.411%)
  Background yields:
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso//p8_ee_ZZ_ecm365.root: 339.977 (eff=85.799%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso//p8_ee_WW_ee_ecm365.root: 101.477 (eff=80.983%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso//p8_ee_WW_mumu_ecm365.root: 47.659 (eff=77.056%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso//p8_ee_tt_ecm365.root: 88.000 (eff=88.000%)


[gino@lxplus910 utils]$ python simple_cut_optim.py         --path '../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso/'         --ecm 365         --variables lep2_iso_final -xmin 0 -xmax 0.25
Found histograms: ['lep2_iso_final']
Optimizing cuts for histogram: lep2_iso_final
  For fixed window [0.0, 0.25] (bins [1, 251]), Z = 9.2954 with S=228.882 and B=377.419

  Signal yields:
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso//wzp6_ee_mumuH_HWW_ecm365.root: 89.147 (eff=88.383%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso//wzp6_ee_eeH_HWW_ecm365.root: 139.735 (eff=87.919%)
  Background yields:
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso//p8_ee_ZZ_ecm365.root: 277.313 (eff=69.984%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso//p8_ee_WW_ee_ecm365.root: 66.402 (eff=52.991%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso//p8_ee_WW_mumu_ecm365.root: 25.704 (eff=41.558%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso//p8_ee_tt_ecm365.root: 8.000 (eff=8.000%)


[gino@lxplus910 utils]$ python simple_cut_optim.py         --path '../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso/'         --ecm 365         --variables lep3_iso_final -xmin 0 -xmax 0.25
Found histograms: ['lep3_iso_final']
Optimizing cuts for histogram: lep3_iso_final
  For fixed window [0.0, 0.25] (bins [1, 251]), Z = 9.3488 with S=219.904 and B=333.386

  Signal yields:
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso//wzp6_ee_mumuH_HWW_ecm365.root: 85.359 (eff=84.628%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso//wzp6_ee_eeH_HWW_ecm365.root: 134.544 (eff=84.653%)
  Background yields:
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso//p8_ee_ZZ_ecm365.root: 264.842 (eff=66.837%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso//p8_ee_WW_ee_ecm365.root: 57.298 (eff=45.726%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso//p8_ee_WW_mumu_ecm365.root: 11.245 (eff=18.182%)
    ../../outputs/higgs/zh_hww_4l/histmaker/ecm365/hists/medium_inclWWInFit_iso//p8_ee_tt_ecm365.root: 0.000 (eff=0.000%)

# lepton pairing efficiency

Added the following to `histmaker.py` in `medium`:

```
    df = df.Define("pairing_info", "FCCAnalyses::ZHfunctions::check_pairing_efficiency_via_HWW(zbuilder_result, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    df = df.Define("is_correct_pairing", "pairing_info[0]")
    df = df.Define("true_Z_p",           "pairing_info[1]")
    df = df.Define("true_Z_mass",        "pairing_info[2]")
    df = df.Define("true_lepton1_p",     "pairing_info[3]")
    df = df.Define("true_lepton2_p",     "pairing_info[4]")
    df = df.Define("truth_lepton_dR",    "pairing_info[5]")
```

python3 plot_pairing_eff.py

# chi2 optimization

ecm=365 sel_type=5 chi2=0.0 fccanalysis run histmaker.py
ecm=365 sel_type=5 chi2=0.1 fccanalysis run histmaker.py
ecm=365 sel_type=5 chi2=0.2 fccanalysis run histmaker.py
ecm=365 sel_type=5 chi2=0.3 fccanalysis run histmaker.py
ecm=365 sel_type=5 chi2=0.4 fccanalysis run histmaker.py
ecm=365 sel_type=5 chi2=0.5 fccanalysis run histmaker.py
ecm=365 sel_type=5 chi2=0.6 fccanalysis run histmaker.py
ecm=365 sel_type=5 chi2=0.7 fccanalysis run histmaker.py
ecm=365 sel_type=5 chi2=0.8 fccanalysis run histmaker.py
ecm=365 sel_type=5 chi2=0.9 fccanalysis run histmaker.py
ecm=365 sel_type=5 chi2=1.0 fccanalysis run histmaker.py

python3 plot_chi2_opt.py