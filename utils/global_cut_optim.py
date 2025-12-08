#!/usr/bin/env python3
"""
Global rectangular-cut optimiser for FCC-ee analyses.

Requirements:
  pip install uproot numpy scipy

Adapt:
  - signal_files / bkg_files: list of root files (can include multiple per class)
  - tree_name: name of TTree inside the files (e.g. "events")
  - variables: list of (varname, lower_bound, upper_bound) search bounds
  - vars_to_read: list of variable names to read from TTree (must include "weight")
"""

import uproot
import numpy as np
from scipy.optimize import differential_evolution
import math
import os
import sys

# -------------------------
# User settings - adapt me
# -------------------------
signal_files = ["signal.root"]                      # list of signal files
bkg_files    = ["bkg1.root", "bkg2.root"]           # list of background files
tree_name    = "events"                             # TTree name inside files
luminosity   = 10000.0   # pb^-1 (example)             # use whatever units match your weights
eps_b        = 0.10       # fractional background syst (10%); set 0.0 to ignore

# Variables to optimise: (name, search_min, search_max)
# We will search for windows [a,b] for each var (a<b). DE will optimize 2*len(vars) parameters in order:
# [a0, b0, a1, b1, ...]
variables = [
    ("m_ll",  80.0, 100.0),
    ("MET",   0.0, 100.0),
    ("pT1",   0.0, 200.0),
    ("pT2",   0.0, 200.0),
    ("mT_WW", 0.0, 300.0),
]

# Name of weight column in the TTree (if per-event weights exist). If you don't have weights, set to None and events count is used.
weight_name = "weight"  # or None

# Optional: if your ROOT files are large, you may prefer to precompute arrays and save them in numpy format first.
# -------------------------

# Build list of variable names to read
vars_to_read = [v[0] for v in variables]
if weight_name is not None:
    vars_to_read.append(weight_name)

def read_chain(files, tree_name, vars_to_read):
    """Read variables from a list of ROOT files and return a dict of numpy arrays and total raw entries."""
    arrays = {k: [] for k in vars_to_read}
    total_entries = 0
    for fname in files:
        if not os.path.exists(fname):
            raise FileNotFoundError(f"File not found: {fname}")
        with uproot.open(fname) as f:
            t = f[tree_name]
            # read in chunks if required, but here we read all
            data = t.arrays(vars_to_read, library="np")
            total_entries += len(data[vars_to_read[0]])
            for k in vars_to_read:
                arrays[k].append(data[k])
    # concatenate
    for k in vars_to_read:
        arrays[k] = np.concatenate(arrays[k]) if len(arrays[k])>0 else np.array([])
    return arrays, total_entries

print("Reading signal files...")
sig_arr, sig_entries = read_chain(signal_files, tree_name, vars_to_read)
print("Reading background files...")
bkg_arr, bkg_entries = read_chain(bkg_files, tree_name, vars_to_read)

# Extract arrays for convenience
sig_weights = sig_arr[weight_name] if weight_name else np.ones(len(next(iter(sig_arr.values()))))
bkg_weights = bkg_arr[weight_name] if weight_name else np.ones(len(next(iter(bkg_arr.values()))))

# Make 2D mask function to apply cuts given parameter vector x
nvars = len(variables)

def make_mask(arr, cuts):
    """
    arr: dict of arrays for a sample
    cuts: list/array of length 2*nvars: [a0,b0,a1,b1,...]
    returns boolean mask
    """
    mask = np.ones(len(next(iter(arr.values()))), dtype=bool)
    for iv in range(nvars):
        name = variables[iv][0]
        a = cuts[2*iv]
        b = cuts[2*iv+1]
        # enforce a <= b and clip to variable bounds
        if a > b:
            return np.zeros_like(mask)   # invalid -> mask none
        mask &= (arr[name] >= a) & (arr[name] <= b)
    return mask

def asimov_z(S, B, eps_b_frac=0.0):
    """
    Asimov significance without profiling nuisance (approx):
    - if eps_b_frac==0 : use standard Cowan formula Z_A = sqrt(2[(S+B) ln(1+S/B) - S])
    - if eps_b_frac>0 : use simple approximation Z = S / sqrt(B + (eps_b_frac * B)^2)
    (For exact profiling with nuisance see Cowan et al. - can be added if you want)
    """
    if S <= 0:
        return 0.0
    if B <= 0:
        # If no background, define Z = sqrt(2*S) (simple Poisson limit) OR S/sqrt(S) -> sqrt(S)
        return math.sqrt(2*S)
    if eps_b_frac > 0.0:
        denom = math.sqrt(B + (eps_b_frac * B)**2)
        return float(S / denom) if denom>0 else 0.0
    # standard Asimov
    try:
        val = 2.0 * ((S + B) * math.log(1.0 + S / B) - S)
        return math.sqrt(val) if val>0 else 0.0
    except Exception:
        return 0.0

def objective(x):
    """
    Objective to maximise: return negative Asimov Z (because scipy minimizes).
    x: array of length 2*nvars = [a0,b0,a1,b1,...]
    """
    # quick invalid check
    for i in range(nvars):
        a = x[2*i]; b = x[2*i+1]
        if a >= b:
            return 1e6  # heavily penalize invalid windows

    # signal
    s_mask = make_mask(sig_arr, x)
    S = float(np.sum(sig_weights[s_mask]))

    # background
    b_mask = make_mask(bkg_arr, x)
    B = float(np.sum(bkg_weights[b_mask]))

    Z = asimov_z(S, B, eps_b_frac=eps_b)
    # negative because we minimize
    return -Z

# Build bounds for optimizer: each variable has two parameters a,b, each constrained to provided var bounds
bounds = []
for (name, lo, hi) in variables:
    bounds.append((lo, hi))  # for a
    bounds.append((lo, hi))  # for b

# Differential evolution settings - you can tune population, maxiter for speed/precision tradeoff
print("Starting global optimisation with differential evolution...")
result = differential_evolution(objective, bounds, strategy='best1bin',
                                maxiter=60, popsize=15, tol=1e-3, polish=True, seed=42, workers=1)

best_x = result.x
best_Z = -result.fun

# Report results
print("\n=== Optimisation finished ===")
print(f"Best Asimov Z = {best_Z:.4f}")
for iv in range(nvars):
    name = variables[iv][0]
    a = best_x[2*iv]; b = best_x[2*iv+1]
    print(f"  {name} in [{a:.4f}, {b:.4f}]")

# compute final S and B for the best cut
s_mask = make_mask(sig_arr, best_x)
b_mask = make_mask(bkg_arr, best_x)
S = float(np.sum(sig_weights[s_mask]))
B = float(np.sum(bkg_weights[b_mask]))
print(f"Final S = {S:.3f},  B = {B:.3f}")

# Optionally save best cut to disk
import json
out = {"best_Z": float(best_Z), "S": S, "B": B,
       "cuts": { variables[i][0]: [float(best_x[2*i]), float(best_x[2*i+1])] for i in range(nvars) } }
with open("best_rect_cuts.json", "w") as fo:
    json.dump(out, fo, indent=2)
print("Saved best cuts to best_rect_cuts.json")