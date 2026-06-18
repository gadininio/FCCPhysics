/**
 * Run with:
 *  root -l -q 'PrintEntriesInFile.C("my_data.root", "myTree", "myBranch")'
 */

#include <TFile.h>
#include <TTree.h>
#include <TBranch.h>
#include <iostream>

// Function takes the file name, tree name, and branch name as arguments
void PrintEntriesInFile(const char* fileName, const char* treeName="events", const char* branchName="miss_energy") {
    // 1. Open the ROOT file
    TFile *file = TFile::Open(fileName, "READ");
    if (!file || file->IsZombie()) {
        std::cerr << "Error: Could not open file '" << fileName << "'." << std::endl;
        return;
    }

    // 2. Get the tree from the file
    TTree *tree = nullptr;
    file->GetObject(treeName, tree);
    if (!tree) {
        std::cerr << "Error: Could not find tree '" << treeName << "' in the file." << std::endl;
        file->Close();
        return;
    }

    // 3. Get the specific branch from the tree
    TBranch *branch = tree->GetBranch(branchName);
    if (!branch) {
        std::cerr << "Error: Could not find branch '" << branchName << "' in the tree." << std::endl;
        file->Close();
        return;
    }

    // 4. Get and print the number of entries
    Long64_t entries = branch->GetEntries();
    std::cout << "Total entries in file" << fileName << ": " << tree->GetEntries() << std::endl;

    // 5. Clean up by closing the file
    file->Close();
}