
No BDT:   loose selections - including a cut on the recoil mass. Fit is done using the BDT score.
With BDT: tight selections - no cut is applied on the recoil mass. Fit is done using the recoil mass.

# combine

cd /afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/histmaker/ecm365/combine/tight_

singularity exec /eos/project/f/fccsw-web/www/analysis/auxiliary/combine-standalone_v9.2.1.sif bash -c '/afs/cern.ch/work/g/gino/private/FCC-ee/outputs/higgs/zh_hww_4l/histmaker/ecm365/combine/tight_; text2workspace.py datacard.txt -o ws.root; combine -M MultiDimFit -v 10 --rMin 0.9 --rMax 1.1 --setParameters r=1 ws.root'

# results

## with stat unc

Minuit2Minimizer : Valid minimum - status = 0
FVAL  = -8.26064549664320517e-14
Edm   = 2.21709301041505395e-14
Nfcn  = 23
r	  = 1	 +/-  0.144847	(limited)
Minimization finished with status=0
Minimization success! status=0
Minimized in 0.040147 seconds (0.030000 CPU time)
FINAL NLL - NLL0 VALUE = 4.892631828e-11


 --- MultiDimFit ---
best fit parameter values: 
   r :    +1.000
Done in 0.00 min (cpu), 0.00 min (real)
6 log messages saved to combine_logger.out

==> 14.48% uncertainty!

## without stat unc

Minuit2Minimizer : Valid minimum - status = 0
FVAL  = -3.37237286808847719e-14
Edm   = 3.70452464955884861e-16
Nfcn  = 25
r	  = 1	 +/-  0.144721	(limited)
Minimization finished with status=0
Minimization success! status=0
Minimized in 0.041885 seconds (0.020000 CPU time)
FINAL NLL - NLL0 VALUE = -3.372372868e-14


 --- MultiDimFit ---
best fit parameter values: 
   r :    +1.000
Done in 0.00 min (cpu), 0.00 min (real)
6 log messages saved to combine_logger.out

==> 14.47% uncertainty!
