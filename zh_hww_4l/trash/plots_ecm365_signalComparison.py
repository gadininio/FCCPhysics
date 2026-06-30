'''
Signal-only comparison plots for the 365 GeV ZH, H->WW histmaker output.

Run from this directory with, for example:
    scheme=medium2 flavor=ll fccanalysis plots plots_ecm365_signalComparison.py

This configuration intentionally leaves plots_ecm365.py untouched. It reuses
the histogram definitions from that file, but changes the process grouping so
both signal samples are drawn as overlaid line histograms.
'''

import importlib.util
import os
from pathlib import Path

import ROOT


_base_path = Path(__file__).with_name("plots_ecm365.py")
_base_spec = importlib.util.spec_from_file_location(
    "_plots_ecm365_base_for_signal_comparison", _base_path
)
_base = importlib.util.module_from_spec(_base_spec)
_base_spec.loader.exec_module(_base)


ecm = os.environ.get("ecm", "365")
flavor = os.environ.get("flavor", "ll")
scheme = os.environ.get("scheme", "presel")

lumi = "10.8" if ecm == "240" else "3"
intLumi = _base.intLumi
intLumiLabel = f"L = {lumi} ab^{{-1}}"
ana_tex = _base.ana_tex
delphesVersion = _base.delphesVersion
energy = _base.energy
collider = _base.collider
formats = list(_base.formats)
plotStatUnc = False

inputDir = _base.inputDir
outdir = (
    f"../../../outputs/higgs/zh_hww_4l/histmaker/ecm{ecm}/plots/"
    f"{scheme}/{flavor}_signalComparison/"
)


procs = {
    "signal": {
        "ZmumuH": ["wzp6_ee_mumuH_HWW_ecm365"],
        "ZeeH": ["wzp6_ee_eeH_HWW_ecm365"],
    },
    "backgrounds": {},
}

colors = {
    "ZmumuH": ROOT.kBlue + 1,
    "ZeeH": ROOT.kRed + 1,
}

legend = {
    "ZmumuH": "Z(#mu^{+}#mu^{-})H, H#rightarrow WW*",
    "ZeeH": "Z(e^{+}e^{-})H, H#rightarrow WW*",
}

legendCoord = [0.50, 0.78, 0.96, 0.88]
legendTextSize = 0.030


hists = {}
for hist_name, hist_cfg in _base.hists.items():
    cfg = dict(hist_cfg)
    cfg["stack"] = False
    cfg.pop("scaleSig", None)
    hists[hist_name] = cfg
