
# cutflow: full_loose_20260126_112336

/#         Cut                             Significance    Z(ll)H                Z(ee)H                Z(mumu)H              WW                    ZZ                   
---------- ------------------------------- --------------- --------------------- --------------------- --------------------- --------------------- ---------------------
Cut 0      All events                      0.110           1.5277e+03 (100.0%)   7.8624e+02 (100.0%)   7.4141e+02 (100.0%)   1.7754e+08 (100.0%)   1.4677e+07 (100.0%)  
Cut 1      4 leptons                       3.511           1.3583e+03 (88.9%)    6.9694e+02 (88.6%)    6.6132e+02 (89.2%)    9.1056e+03 (0.0%)     1.3918e+05 (0.9%)    
Cut 2      2 OS pairs                      3.605           1.3583e+03 (100.0%)   6.9694e+02 (100.0%)   6.6132e+02 (100.0%)   8.6924e+03 (95.5%)    1.3187e+05 (94.8%)   
Cut 3      ≥1 SF pair                      3.605           1.3583e+03 (100.0%)   6.9694e+02 (100.0%)   6.6132e+02 (100.0%)   8.6924e+03 (100.0%)   1.3187e+05 (100.0%)  
Cut 4      p_l_1,p_l_2,p_l_3,p_l_4         5.971           1.2519e+03 (92.2%)    6.4042e+02 (91.9%)    6.1148e+02 (92.5%)    1.8425e+03 (21.2%)    4.0868e+04 (31.0%)   
Cut 5      76 < m_ll < 106                 6.360           1.1603e+03 (92.7%)    5.8126e+02 (90.8%)    5.7903e+02 (94.7%)    4.0226e+02 (21.8%)    3.1725e+04 (77.6%)   
Cut 6      20 < p_ll < 70                  8.009           1.1497e+03 (99.1%)    5.7540e+02 (99.0%)    5.7431e+02 (99.2%)    3.7183e+02 (92.4%)    1.9087e+04 (60.2%)   
Cut 7      120 < m_rec < 145               10.193          1.1249e+03 (97.8%)    5.6049e+02 (97.4%)    5.6438e+02 (98.3%)    2.3917e+02 (64.3%)    1.0815e+04 (56.7%)   
Cut 8      |cosθ_miss| < 0.98              12.996          1.1025e+03 (98.0%)    5.4945e+02 (98.0%)    5.5302e+02 (98.0%)    2.3489e+02 (98.2%)    5.8591e+03 (54.2%)   
Cut 9      20 < E_miss < 120               24.305          1.1024e+03 (100.0%)   5.4944e+02 (100.0%)   5.5300e+02 (100.0%)   2.3299e+02 (99.2%)    7.2207e+02 (12.3%)   
Cut 10     60 < m_WW* < 135                26.117          1.0981e+03 (99.6%)    5.4713e+02 (99.6%)    5.5093e+02 (99.6%)    1.8924e+02 (81.2%)    4.8033e+02 (66.5%)   
Cut 11     ΔR(l_WW*,1, l_WW*,2)>0.25       26.898          1.0777e+03 (98.1%)    5.3706e+02 (98.2%)    5.4067e+02 (98.1%)    5.2304e+01 (27.6%)    4.7537e+02 (99.0%)   

Total                                                      70.5478%              68.3073%              72.9238%              0.0000%               0.0032%              


# number of entries (stat for training)

[gino@lxplus944 utils]$ root -l -q 'PrintEntries.C("../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_trainedWithoutWW/preselection/")'
[SUCCESS] ../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_trainedWithoutWW/preselection//p8_ee_ZZ_ecm240.root: 1843 entries
[SUCCESS] ../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_trainedWithoutWW/preselection//p8_ee_WW_ecm240.root: 110 entries
[SUCCESS] ../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_trainedWithoutWW/preselection//wzp6_ee_eeH_HWW_ecm240_inc.root: 14654 entries
[SUCCESS] ../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_trainedWithoutWW/preselection//wzp6_ee_eeH_HWW_ecm240.root: 12613 entries
[SUCCESS] ../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_trainedWithoutWW/preselection//wzp6_ee_eeH_HWW_llnunu_ecm240_inc.root: 173896 entries
[SUCCESS] ../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_trainedWithoutWW/preselection//wzp6_ee_eeH_HWW_llnunu_ecm240.root: 173896 entries
[SUCCESS] ../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_trainedWithoutWW/preselection//wzp6_ee_mumuH_HWW_ecm240_inc.root: 15642 entries
[SUCCESS] ../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_trainedWithoutWW/preselection//wzp6_ee_mumuH_HWW_ecm240.root: 13494 entries
[SUCCESS] ../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_trainedWithoutWW/preselection//wzp6_ee_mumuH_HWW_llnunu_ecm240_inc.root: 185741 entries
[SUCCESS] ../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_trainedWithoutWW/preselection//wzp6_ee_mumuH_HWW_llnunu_ecm240.root: 185741 entries

[gino@lxplus944 utils]$ root -l -q 'PrintEntries.C("../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_trainedWithoutWW/preselection/training")'
[SUCCESS] ../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_trainedWithoutWW/preselection/training/p8_ee_ZZ_llX_ecm240.root: 30197 entries
[SUCCESS] ../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_trainedWithoutWW/preselection/training/p8_ee_ZZ_tautauX_ecm240.root: 26910 entries
[FAIL] ../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_trainedWithoutWW/preselection/training/p8_ee_WW_ecm240.root: 0 entries
[SUCCESS] ../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_trainedWithoutWW/preselection/training/p8_ee_WW_ee_ecm240.root: 346 entries
[SUCCESS] ../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_trainedWithoutWW/preselection/training/p8_ee_WW_mumu_ecm240.root: 175 entries
[SUCCESS] ../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_trainedWithoutWW/preselection/training/wzp6_ee_eeH_HWW_llnunu_ecm240.root: 152564 entries
[SUCCESS] ../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_trainedWithoutWW/preselection/training/wzp6_ee_mumuH_HWW_llnunu_ecm240_inc.root: 185829 entries
[SUCCESS] ../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_trainedWithoutWW/preselection/training/wzp6_ee_eeH_HWW_llnunu_ecm240_inc.root: 174037 entries
[SUCCESS] ../../../outputs/higgs/zh_hww_4l/mva/ecm240/loose_full_trainedWithoutWW/preselection/training/wzp6_ee_mumuH_HWW_llnunu_ecm240.root: 162660 entries


==> train without WW, but use WW training samples (346+175=521 entries) as analysis samples (currently only 110 entries) for the fit.

# cutflow

  python3 detailed_cutflow.py \
    -cfg ../zh_hww_4l/cutflow_cng/config_240_loose_allbkg.json \
    -i ../../../outputs/higgs/zh_hww_4l/histmaker/ecm240/hists/full_loose_20260126_112336/ \
    -o ../../../outputs/higgs/zh_hww_4l/histmaker/ecm240/plots/full_loose_20260126_112336/ll/

  python3 detailed_cutflow.py \
    -cfg ../zh_hww_4l/cutflow_cng/config_240_loose.json \
    -i ../../../outputs/higgs/zh_hww_4l/histmaker/ecm240/hists/full_loose_20260126_112336/ \
    -o ../../../outputs/higgs/zh_hww_4l/histmaker/ecm240/plots/full_loose_20260126_112336/ll/
