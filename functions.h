#ifndef ZHfunctions_H
#define ZHfunctions_H

#include <cmath>
#include <vector>
#include <math.h>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/ParticleIDData.h"
#include "ReconstructedParticle2MC.h"


namespace FCCAnalyses { namespace ZHfunctions {


// build the Z resonance based on the available leptons. Returns the best lepton pair compatible with the Z mass and recoil at 125 GeV
// technically, it returns a ReconstructedParticleData object with index 0 the di-lepton system, index and 2 the leptons of the pair
struct resonanceBuilder_mass_recoil {
    float m_resonance_mass;
    float m_recoil_mass;
    float chi2_recoil_frac;
    float ecm;
    bool m_use_MC_Kinematics;
    resonanceBuilder_mass_recoil(float arg_resonance_mass, float arg_recoil_mass, float arg_chi2_recoil_frac, float arg_ecm, bool arg_use_MC_Kinematics);
    Vec_rp operator()(Vec_rp legs, Vec_i recind, Vec_i mcind, Vec_rp reco, Vec_mc mc, Vec_i parents, Vec_i daugthers) ;
};

resonanceBuilder_mass_recoil::resonanceBuilder_mass_recoil(float arg_resonance_mass, float arg_recoil_mass, float arg_chi2_recoil_frac, float arg_ecm, bool arg_use_MC_Kinematics) {m_resonance_mass = arg_resonance_mass, m_recoil_mass = arg_recoil_mass, chi2_recoil_frac = arg_chi2_recoil_frac, ecm = arg_ecm, m_use_MC_Kinematics = arg_use_MC_Kinematics;}

Vec_rp resonanceBuilder_mass_recoil::resonanceBuilder_mass_recoil::operator()(Vec_rp legs, Vec_i recind, Vec_i mcind, Vec_rp reco, Vec_mc mc, Vec_i parents, Vec_i daugthers) {

    Vec_rp result;
    result.reserve(3);
    std::vector<std::vector<int>> pairs; // for each permutation, add the indices of the muons
    int n = legs.size();
  
    if(n > 1) {
        ROOT::VecOps::RVec<bool> v(n);
        std::fill(v.end() - 2, v.end(), true); // helper variable for permutations
        do {
            std::vector<int> pair;
            rp reso;
            reso.charge = 0;
            TLorentzVector reso_lv; 
            for(int i = 0; i < n; ++i) {
                if(v[i]) {
                    pair.push_back(i);
                    reso.charge += legs[i].charge;
                    TLorentzVector leg_lv;

                    if(m_use_MC_Kinematics) { // MC kinematics
                        int track_index = legs[i].tracks_begin;   // index in the Track array
                        int mc_index = ReconstructedParticle2MC::getTrack2MC_index(track_index, recind, mcind, reco);
                        if (mc_index >= 0 && mc_index < mc.size()) {
                            leg_lv.SetXYZM(mc.at(mc_index).momentum.x, mc.at(mc_index).momentum.y, mc.at(mc_index).momentum.z, mc.at(mc_index).mass);
                        }
                    }
                    else { // reco kinematics
                         leg_lv.SetXYZM(legs[i].momentum.x, legs[i].momentum.y, legs[i].momentum.z, legs[i].mass);
                    }

                    reso_lv += leg_lv;
                }
            }

            if(reso.charge != 0) continue; // neglect non-zero charge pairs
            reso.momentum.x = reso_lv.Px();
            reso.momentum.y = reso_lv.Py();
            reso.momentum.z = reso_lv.Pz();
            reso.mass = reso_lv.M();
            result.emplace_back(reso);
            pairs.push_back(pair);

        } while(std::next_permutation(v.begin(), v.end()));
    }
    else {
        return Vec_rp(); // return empty list
        // std::cout << "ERROR: resonanceBuilder_mass_recoil, at least two leptons required." << std::endl;
        // exit(1);
    }

    if(result.size() > 1) {
        Vec_rp bestReso;

        int idx_min = -1;
        float d_min = 9e9;
        for (int i = 0; i < result.size(); ++i) {

            // calculate recoil
            auto recoil_p4 = TLorentzVector(0, 0, 0, ecm);
            TLorentzVector tv1;
            tv1.SetXYZM(result.at(i).momentum.x, result.at(i).momentum.y, result.at(i).momentum.z, result.at(i).mass);
            recoil_p4 -= tv1;

            auto recoil_fcc = edm4hep::ReconstructedParticleData();
            recoil_fcc.momentum.x = recoil_p4.Px();
            recoil_fcc.momentum.y = recoil_p4.Py();
            recoil_fcc.momentum.z = recoil_p4.Pz();
            recoil_fcc.mass = recoil_p4.M();

            TLorentzVector tg;
            tg.SetXYZM(result.at(i).momentum.x, result.at(i).momentum.y, result.at(i).momentum.z, result.at(i).mass);

            float boost = tg.P();
            float mass = std::pow(result.at(i).mass - m_resonance_mass, 2); // mass
            float rec = std::pow(recoil_fcc.mass - m_recoil_mass, 2); // recoil
            float d = (1.0-chi2_recoil_frac)*mass + chi2_recoil_frac*rec;

            if(d < d_min) {
                d_min = d;
                idx_min = i;
            }
        }
        if(idx_min > -1) { 
            bestReso.push_back(result.at(idx_min));
            auto & l1 = legs[pairs[idx_min][0]];
            auto & l2 = legs[pairs[idx_min][1]];
            bestReso.emplace_back(l1);
            bestReso.emplace_back(l2);
        }
        else {
            return Vec_rp(); // return empty list
            // std::cout << "ERROR: resonanceBuilder_mass_recoil, no mininum found." << std::endl;
            // exit(1);
        }
        return bestReso;
    }
    else {
        auto & l1 = legs[0];
        auto & l2 = legs[1];
        result.emplace_back(l1);
        result.emplace_back(l2);
        return result;
    }
}




// build the Z resonance based on the available leptons. Returns the best lepton pair compatible with the Z mass and recoil at 125 GeV
// technically, it returns a ReconstructedParticleData object with index 0 the di-lepton system, index and 2 the leptons of the pair
struct resonanceBuilder_mass_recoil_advanced {
    float m_resonance_mass;
    float m_recoil_mass;
    float chi2_recoil_frac;
    float ecm;
    bool m_use_MC_Kinematics;
    resonanceBuilder_mass_recoil_advanced(float arg_resonance_mass, float arg_recoil_mass, float arg_chi2_recoil_frac, float arg_ecm, bool arg_use_MC_Kinematics);
    Vec_rp operator()(Vec_rp muon_legs, Vec_rp electron_legs, Vec_i recind, Vec_i mcind, Vec_rp reco, Vec_mc mc, Vec_i parents, Vec_i daugthers) ;
    void buildResonances(const Vec_rp &legs, const Vec_i &recind, const Vec_i &mcind, const Vec_rp &reco, const Vec_mc &mc, Vec_rp &result, std::vector<std::vector<int>> &pairs);
};

resonanceBuilder_mass_recoil_advanced::resonanceBuilder_mass_recoil_advanced(float arg_resonance_mass, float arg_recoil_mass, float arg_chi2_recoil_frac, float arg_ecm, bool arg_use_MC_Kinematics) {
    m_resonance_mass = arg_resonance_mass, m_recoil_mass = arg_recoil_mass, chi2_recoil_frac = arg_chi2_recoil_frac, ecm = arg_ecm, m_use_MC_Kinematics = arg_use_MC_Kinematics;
}

// -----------------------------------------------
// Build all opposite-charge resonance candidates
void resonanceBuilder_mass_recoil_advanced::buildResonances(const Vec_rp &legs, const Vec_i &recind, const Vec_i &mcind, const Vec_rp &reco, const Vec_mc &mc, Vec_rp &result, std::vector<std::vector<int>> &pairs) {

    int n = legs.size();
    ROOT::VecOps::RVec<bool> v(n);
    std::fill(v.end() - 2, v.end(), true);

    do {
        std::vector<int> pair;
        rp reso;
        reso.charge = 0;
        reso.type = legs[0].type; // assume all legs are of the same type. From some reason, this doesn't work, hence the following line.
        TLorentzVector reso_lv;

        for (int i = 0; i < n; ++i) {
            if (v[i]) {
                pair.push_back(i);
                reso.charge += legs[i].charge;
                TLorentzVector leg_lv;

                if (m_use_MC_Kinematics) {
                    int track_index = legs[i].tracks_begin;
                    int mc_index = ReconstructedParticle2MC::getTrack2MC_index(track_index, recind, mcind, reco);
                    if (mc_index >= 0 && mc_index < mc.size()) {
                        leg_lv.SetXYZM(mc.at(mc_index).momentum.x, mc.at(mc_index).momentum.y, mc.at(mc_index).momentum.z, mc.at(mc_index).mass);
                    }
                }
                else {
                    leg_lv.SetXYZM(legs[i].momentum.x, legs[i].momentum.y, legs[i].momentum.z, legs[i].mass);
                }

                reso_lv += leg_lv;
            }
        }

        if (reso.charge != 0)
            continue;

        reso.momentum.x = reso_lv.Px();
        reso.momentum.y = reso_lv.Py();
        reso.momentum.z = reso_lv.Pz();
        reso.mass = reso_lv.M();

        result.emplace_back(reso);
        pairs.push_back(pair);

    } while (std::next_permutation(v.begin(), v.end()));
}

Vec_rp resonanceBuilder_mass_recoil_advanced::resonanceBuilder_mass_recoil_advanced::operator()(Vec_rp legs_muons, Vec_rp legs_electrons, Vec_i recind, Vec_i mcind, Vec_rp reco, Vec_mc mc, Vec_i parents, Vec_i daugthers) {
    Vec_rp result;
    std::vector<std::vector<int>> pairs; // for each permutation, add the indices of the muons
  
    // ensure legs have correct type
    for(auto & p : legs_muons) p.type = 13;
    for(auto & p : legs_electrons) p.type = 11;

    if(legs_muons.size() > 1) {
        // std::cout << "DEBUG: resonanceBuilder_mass_recoil_advanced: number of muon legs = " << legs_muons.size() << ", type = " << legs_muons[0].type << std::endl;
        buildResonances(legs_muons, recind, mcind, reco, mc, result, pairs);
        // std::cout << "DEBUG: resonanceBuilder_mass_recoil_advanced: number of resonance candidates after muons = " << result.size() << ", type = " << result[0].type << std::endl;
    }
    if(legs_electrons.size() > 1) {  // GADI: I thing the "else" here is a bug, because in cases with 2e+2mu, only the muons will be consdered
        // std::cout << "DEBUG: resonanceBuilder_mass_recoil_advanced: number of electrons legs = " << legs_electrons.size() << ", type = " << legs_electrons[0].type << std::endl;
        buildResonances(legs_electrons, recind, mcind, reco, mc, result, pairs);
        // std::cout << "DEBUG: resonanceBuilder_mass_recoil_advanced: number of resonance candidates after electrons = " << result.size() << ", type = " << result[0].type << std::endl;
    }
    // else {
    //     return Vec_rp(); // return empty list
    //     // std::cout << "ERROR: resonanceBuilder_mass_recoil_advanced, at least two leptons required." << std::endl;
    //     // exit(1);
    // }

    Vec_rp bestReso;
    bestReso.reserve(5);
    std::vector<int> selected_indices;

    if(result.size() == 0) {
        return Vec_rp(); // return empty list
        // std::cout << "ERROR: resonanceBuilder_mass_recoil_advanced, no opposite-charge lepton pair found." << std::endl;
        // exit(1);
    }
    else if(result.size() == 1) { // only one pair found
        bestReso.push_back(result.at(0));
        selected_indices = {0, 1};  // GADI: check if that means only 2 leptons exist
    }
    else { // more than one pair found, select the best one
        int idx_min = -1;
        float d_min = 9e9;
        for (int i = 0; i < result.size(); ++i) {

            // calculate recoil
            auto recoil_p4 = TLorentzVector(0, 0, 0, ecm);
            TLorentzVector tv1;
            tv1.SetXYZM(result.at(i).momentum.x, result.at(i).momentum.y, result.at(i).momentum.z, result.at(i).mass);
            recoil_p4 -= tv1;

            auto recoil_fcc = edm4hep::ReconstructedParticleData();
            recoil_fcc.momentum.x = recoil_p4.Px();
            recoil_fcc.momentum.y = recoil_p4.Py();
            recoil_fcc.momentum.z = recoil_p4.Pz();
            recoil_fcc.mass = recoil_p4.M();

            TLorentzVector tg;
            tg.SetXYZM(result.at(i).momentum.x, result.at(i).momentum.y, result.at(i).momentum.z, result.at(i).mass);

            float boost = tg.P();
            float mass = std::pow(result.at(i).mass - m_resonance_mass, 2); // mass
            float rec = std::pow(recoil_fcc.mass - m_recoil_mass, 2); // recoil
            float d = (1.0-chi2_recoil_frac)*mass + chi2_recoil_frac*rec;

            if(d < d_min) {
                d_min = d;
                idx_min = i;
            }
        }
        if(idx_min > -1) { // best pair candidate found
            bestReso.push_back(result.at(idx_min));
            selected_indices = pairs[idx_min];
        }
        else {
            std::cout << "ERROR: resonanceBuilder_mass_recoil_advanced, no mininum found." << std::endl;
            exit(1);
        }
    }

    // Add the two leptons of the selected pair to 'bestRepo' list that will be returned.
    rp l1, l2;
    int resonance_type = std::abs(bestReso.at(0).type);
    if(resonance_type == 13) {  // resonance is a muon pair
        l1 = legs_muons[selected_indices[0]];
        l2 = legs_muons[selected_indices[1]];
    }
    else if(resonance_type == 11) {  // resonance is an electron pair
        l1 = legs_electrons[selected_indices[0]];
        l2 = legs_electrons[selected_indices[1]];
    }
    else {
        std::cout << "ERROR: resonanceBuilder_mass_recoil_advanced, unknown resonance type." << std::endl;
        exit(1);
    }
    bestReso.emplace_back(l1);
    bestReso.emplace_back(l2);

    // Find the two other leptons not in the selected pair
    if (resonance_type == 13) {  // The resonance is a muon pair
        for (size_t i = 0; i < legs_muons.size(); ++i) {
            if (i != selected_indices[0] && i != selected_indices[1]) {  // add all muons not in the pair (should be no such muons, but just in case)
                bestReso.push_back(legs_muons[i]);
            }
        }
        for (size_t i = 0; i < legs_electrons.size(); ++i) {  // add all electrons
            bestReso.push_back(legs_electrons[i]);
        }
    }
    else {  // The resonance is an electron pair
        for (size_t i = 0; i < legs_muons.size(); ++i) {  // add all muons
            bestReso.push_back(legs_muons[i]);
        }
    }
    for (size_t i = 0; i < legs_electrons.size(); ++i) {  // add all electrons not in the pair (should be no such electrons, but just in case)
        if (i != selected_indices[0] && i != selected_indices[1]) {
            bestReso.push_back(legs_electrons[i]);
        }
    }

    // // print bestReso content for debugging
    // for(size_t i = 0; i < bestReso.size(); ++i) {
    //     std::cout << "bestReso[" << i << "] type: " << bestReso[i].type << " charge: " << bestReso[i].charge << " p: " << std::sqrt(bestReso[i].momentum.x*bestReso[i].momentum.x + bestReso[i].momentum.y*bestReso[i].momentum.y + bestReso[i].momentum.z*bestReso[i].momentum.z) << " mass: " << bestReso[i].mass << std::endl;
    // }
    
    return bestReso;
}


// Get dilepton vector, and return the dilepton category: -1: not leptonic, 0: e+e-, 1: mu+mu-, 2: e-mu or mu-e
int getDileptonCategory(Vec_rp in) {
    if(in.size() < 2) return -1;
    int n_e = 0;
    int n_mu = 0;
    for(auto & p : in) {
        // std::cout << "getWWleptonicCategory: particle type = " << p.type << std::endl;
        if(std::abs(p.type) == 11) n_e++;
        else if(std::abs(p.type) == 13) n_mu++;
    }
    if(n_e == 2 && n_mu == 0) return 0;
    else if(n_e == 0 && n_mu == 2) return 1;
    else if(n_e + n_mu == 2) return 2;
    return -1;
}


// Sort particles by descending pT
Vec_rp sortByPt(Vec_rp in) {
    std::sort(in.begin(), in.end(), [](const auto& a, const auto& b) {
        const float ptA = std::hypot(a.momentum.x, a.momentum.y);
        const float ptB = std::hypot(b.momentum.x, b.momentum.y);
        return ptA > ptB;
    });
    return in;
}


// Return the index (0..3) of the muon whose momentum matches lepton_p
int findIndex(float p, const std::vector<float>& p_list, float tol = 1e-3) {
    for (size_t i = 0; i < p_list.size(); ++i) {
        if (std::fabs(p_list[i] - p) < tol) {
            return static_cast<int>(i);
        }
    }
    return -1; // not found
}


struct sel_iso {
    sel_iso(float arg_max_iso);
    float m_max_iso = .25;
    Vec_rp operator() (Vec_rp in, Vec_f iso);
  };

sel_iso::sel_iso(float arg_max_iso) : m_max_iso(arg_max_iso) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  sel_iso::operator() (Vec_rp in, Vec_f iso) {
    Vec_rp result;
    result.reserve(in.size());
    for (size_t i = 0; i < in.size(); ++i) {
        auto & p = in[i];
        if (iso[i] < m_max_iso) {
            result.emplace_back(p);
        }
    }
    return result;
}

 
// compute the cone isolation for reco particles
struct coneIsolation {

    coneIsolation(float arg_dr_min, float arg_dr_max);
    double deltaR(double eta1, double phi1, double eta2, double phi2) { return TMath::Sqrt(TMath::Power(eta1-eta2, 2) + (TMath::Power(phi1-phi2, 2))); };

    float dr_min = 0;
    float dr_max = 0.4;
    Vec_f operator() (Vec_rp in, Vec_rp rps) ;
};

coneIsolation::coneIsolation(float arg_dr_min, float arg_dr_max) : dr_min(arg_dr_min), dr_max( arg_dr_max ) { };
Vec_f coneIsolation::coneIsolation::operator() (Vec_rp in, Vec_rp rps) {

    Vec_f result;
    result.reserve(in.size());

    std::vector<ROOT::Math::PxPyPzEVector> lv_reco;
    std::vector<ROOT::Math::PxPyPzEVector> lv_charged;
    std::vector<ROOT::Math::PxPyPzEVector> lv_neutral;

    for(size_t i = 0; i < rps.size(); ++i) {
        ROOT::Math::PxPyPzEVector tlv;
        tlv.SetPxPyPzE(rps.at(i).momentum.x, rps.at(i).momentum.y, rps.at(i).momentum.z, rps.at(i).energy);

        if(rps.at(i).charge == 0) lv_neutral.push_back(tlv);
        else lv_charged.push_back(tlv);
    }

    for(size_t i = 0; i < in.size(); ++i) {
        ROOT::Math::PxPyPzEVector tlv;
        tlv.SetPxPyPzE(in.at(i).momentum.x, in.at(i).momentum.y, in.at(i).momentum.z, in.at(i).energy);
        lv_reco.push_back(tlv);
    }

    // compute the isolation (see https://github.com/delphes/delphes/blob/master/modules/Isolation.cc#L154) 
    for (auto & lv_reco_ : lv_reco) {
        double sumNeutral = 0.0;
        double sumCharged = 0.0;
        // charged
        for (auto & lv_charged_ : lv_charged) {
            double dr = coneIsolation::deltaR(lv_reco_.Eta(), lv_reco_.Phi(), lv_charged_.Eta(), lv_charged_.Phi());
            if(dr > dr_min && dr < dr_max) sumCharged += lv_charged_.P();
        }

        // neutral
        for (auto & lv_neutral_ : lv_neutral) {
            double dr = coneIsolation::deltaR(lv_reco_.Eta(), lv_reco_.Phi(), lv_neutral_.Eta(), lv_neutral_.Phi());
            if(dr > dr_min && dr < dr_max) sumNeutral += lv_neutral_.P();
        }
        double sum = sumCharged + sumNeutral;
        double ratio= sum / lv_reco_.P();
        result.emplace_back(ratio);
    }
    return result;
}
 
Vec_i get_iso(Vec_f iso, float arg_max_iso) {
    Vec_i result;
    result.reserve(iso.size());
    for (size_t i = 0; i < iso.size(); ++i) {
        result.emplace_back(iso[i] < arg_max_iso ? 1 : 0);
    }
    return result;
}

// returns missing energy vector, based on reco particles
Vec_rp missingEnergy(float ecm, Vec_rp in, float p_cutoff = 0.0) {
    float px = 0, py = 0, pz = 0, e = 0;
    for(auto &p : in) {
        if (std::sqrt(p.momentum.x * p.momentum.x + p.momentum.y*p.momentum.y) < p_cutoff) continue;
        px += -p.momentum.x;
        py += -p.momentum.y;
        pz += -p.momentum.z;
        e += p.energy;
    }

    Vec_rp ret;
    rp res;
    res.momentum.x = px;
    res.momentum.y = py;
    res.momentum.z = pz;
    res.energy = ecm-e;
    ret.emplace_back(res);
    return ret;
}

// calculate the cosine(theta) of the missing energy vector
float get_cosTheta_miss(Vec_rp met){
    float costheta = 0.;
    if(met.size() > 0) {
        TLorentzVector lv_met;
        lv_met.SetPxPyPzE(met[0].momentum.x, met[0].momentum.y, met[0].momentum.z, met[0].energy);
        costheta = fabs(std::cos(lv_met.Theta()));
    }
    return costheta;
}

// returns the missing energy
float get_missing_energy(Vec_rp met){
    if(met.size() > 0) {
        return met[0].energy;
    }
    return 0.;
}

// checks if the WW system decays leptonically (e or mu)
bool is_ww_leptonic(Vec_mc mc, Vec_i ind) {
   int l1 = 0;
   int l2 = 0;
   //cout << "*********" << endl;
   for(size_t i = 0; i < mc.size(); ++i) {
        auto & p = mc[i];
        if(std::abs(p.PDG) == 24) {  // W decays
            int ds = p.daughters_begin;
            int de = p.daughters_end;
            for(int k=ds; k<de; k++) {
                int pdg = abs(mc[ind[k]].PDG);
                if(pdg == 24) continue;
                //std::cout << "W " << pdg << endl;
                if(pdg == 11 or pdg == 13) {  // e or mu
                    if(l1 == 0) l1 = pdg;
                    else l2 = pdg;
                }
            }
        }
        // else if(std::abs(p.PDG) == 15) { // tau decays
        //     int ds = p.daughters_begin;
        //     int de = p.daughters_end;
        //     for(int k=ds; k<de; k++) {
        //         int pdg = abs(mc[ind[k]].PDG);
        //         if(pdg == 15) continue;
        //         //std::cout << "T " << pdg << endl;
        //         if(pdg == 11 or pdg == 13) {
        //             if(l1 == 0) l1 = pdg;
        //             else l2 = pdg;
        //         }
        //     }
        // }
   }
//    if(l1 == l2 && (l1==13 || l1 == 11)) {
   if((l1==11 || l1==13) && (l2==11 || l2==13)) {
       //std::cout << "LEPTONIC-----------" << l1 << " " << l2 << endl;
       return true;
   }
   return false;
}


}}

#endif