'''
This script appends TParameters to an existing ROOT file. It takes three lists as input: parameter names, types, and values. The script ensures that all three lists have the same length and then writes each parameter to the specified ROOT file.

Run with:
    python add_parameters.py \
        -f outputs/my_stage1_output.root \
        -n mva_threshold max_iterations use_gpu algorithm_name \
        -t double int bool string \
        -v 0.85 100 true xgboost
'''


import argparse
import sys
import os
import glob
import ROOT

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Append TParameters to multiple ROOT files.")
    parser.add_argument("-f", "--files", nargs='+', required=True, help="List of ROOT files, or directory paths containing ROOT files.")
    parser.add_argument("-n", "--names", nargs='+', required=True, help="List of parameter names.")
    parser.add_argument("-t", "--types", nargs='+', required=True, help="List of types (int, float, double, bool, string).")
    parser.add_argument("-v", "--values", nargs='+', required=True, help="List of parameter values.")
    
    args = parser.parse_args()
    
    # Ensure all lists have the exact same length
    if not (len(args.names) == len(args.types) == len(args.values)):
        print("Error: The number of names, types, and values provided must be equal.")
        sys.exit(1)
        
    # Resolve the target files
    target_files = []
    for path in args.files:
        if os.path.isdir(path):
            # If it is a directory, find all .root files inside it
            found_files = glob.glob(os.path.join(path, "*.root"))
            if not found_files:
                print(f"Warning: No .root files found in directory '{path}'.")
            target_files.extend(found_files)
        elif os.path.isfile(path) and path.endswith(".root"):
            # If it is a direct file path, add it to the list
            target_files.append(path)
        else:
            print(f"Warning: '{path}' is not a valid ROOT file or directory. Skipping.")
            
    # Remove any duplicate paths just in case
    target_files = list(set(target_files))
    
    if not target_files:
        print("Error: No valid ROOT files found to process.")
        sys.exit(1)
        
    print(f"Found {len(target_files)} file(s) to process. Applying parameters...")
    
    # Iterate through every valid file found
    for file_path in target_files:
        print(f" -> Updating: {file_path}")
        root_file = ROOT.TFile(file_path, "UPDATE")
        
        if root_file.IsZombie():
            print(f"    Error: Could not open {file_path}. Skipping.")
            continue
            
        # Write the parameters to the current file
        for name, ptype, val_str in zip(args.names, args.types, args.values):
            ptype = ptype.lower()
            
            try:
                if ptype == "int":
                    val = int(val_str)
                    param = ROOT.TParameter("int")(name, val)
                    param.Write()
                    
                elif ptype in ["float", "double"]:
                    val = float(val_str)
                    param = ROOT.TParameter("double")(name, val)
                    param.Write()
                    
                elif ptype == "bool":
                    val = val_str.lower() in ['true', '1', 'yes']
                    param = ROOT.TParameter("bool")(name, val)
                    param.Write()
                    
                elif ptype in ["string", "str"]:
                    param = ROOT.TNamed(name, val_str)
                    param.Write()
                    
                else:
                    print(f"    Warning: Type '{ptype}' for parameter '{name}' is not recognized.")
                    
            except ValueError:
                print(f"    Error: Failed to convert '{val_str}' into type '{ptype}' for parameter '{name}'.")
                
        # Close and save the current file
        root_file.Close()
        
    print("All files processed successfully.")

if __name__ == "__main__":
    main()