/**
 * Run with:
 *  root -l -q 'PrintEntries.C("data_files", "myTree", "myBranch")'
 */

#include <TSystem.h>
#include <TSystemDirectory.h>
#include <TList.h>
#include <TSystemFile.h>
#include <TString.h>
#include <TFile.h>
#include <TTree.h>
#include <TBranch.h>
#include <iostream>

// --- Helper Function: Processes a single ROOT file ---
void ProcessSingleFile(const char* filePath, const char* treeName, const char* branchName) {
    TFile *f = TFile::Open(filePath, "READ");
    if (!f || f->IsZombie()) {
        std::cerr << "[FAIL] " << filePath << ": Could not open file." << std::endl;
        return;
    }

    TTree *tree = nullptr;
    f->GetObject(treeName, tree);
    if (!tree) {
        std::cerr << "[FAIL] " << filePath << ": Tree '" << treeName << "' not found." << std::endl;
        f->Close();
        return;
    }

    TBranch *branch = tree->GetBranch(branchName);
    if (!branch) {
        std::cerr << "[FAIL] " << filePath << ": Branch '" << branchName << "' not found." << std::endl;
        f->Close();
        return;
    }

    Long64_t entries = branch->GetEntries();
    std::cout << filePath << ": " << entries << " entries" << std::endl;

    f->Close();
}


// --- Main Function: Determines if path is a file or directory ---
void PrintEntries(const char* targetPath, const char* treeName="events", const char* branchName="miss_energy") {
    FileStat_t pathInfo;
    
    // 1. Check if the path exists
    if (gSystem->GetPathInfo(targetPath, pathInfo) != 0) {
        std::cerr << "Error: The path '" << targetPath << "' does not exist." << std::endl;
        return;
    }

    // 2. If the path is a DIRECTORY
    if (R_ISDIR(pathInfo.fMode)) {
        std::cout << "Scanning directory: " << targetPath << std::endl;
        std::cout << "--------------------------------------------------" << std::endl;
        
        TSystemDirectory dir(targetPath, targetPath);
        TList *files = dir.GetListOfFiles();
        
        if (!files) return;

        TSystemFile *file;
        TString fname;
        TIter next(files);

        while ((file = (TSystemFile*)next())) {
            fname = file->GetName();
            
            // Only process files ending in .root
            if (!file->IsDirectory() && fname.EndsWith(".root")) {
                TString fullPath = TString::Format("%s/%s", targetPath, fname.Data());
                ProcessSingleFile(fullPath.Data(), treeName, branchName);
            }
        }
    } 
    // 3. If the path is a REGULAR FILE
    else if (R_ISREG(pathInfo.fMode)) {
        TString fname = targetPath;
        
        if (fname.EndsWith(".root")) {
            std::cout << "Processing single file: " << targetPath << std::endl;
            std::cout << "--------------------------------------------------" << std::endl;
            ProcessSingleFile(targetPath, treeName, branchName);
        } else {
            std::cerr << "Error: The file '" << targetPath << "' is not a .root file." << std::endl;
        }
    }
}