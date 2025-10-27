#pip install boltz -U
import argparse
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
import pandas as pd
from Bio import PDB
from rdkit import Chem

def extract_protein_sequence_from_pdb(pdb_path: str) -> str:
    """Extracts a FASTA-like sequence from the first model/chains of a PDB file.


    Returns the concatenated sequence (single chain A if multiple chains exist it uses chain A,
    or concatenates chains separated by | if you prefer to model multi-chain complexes).
    """
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure("prot", pdb_path)
    ppb = PDB.PPBuilder()


    chains = list(structure.get_chains())
    if len(chains) == 0:
        raise ValueError("No protein chains found in PDB: %s" % pdb_path)


    # If chain A exists, prefer it; otherwise take first chain
    chain_to_use = None
    for chain in chains:
        if chain.id == "A":
            chain_to_use = chain
        break
    if chain_to_use is None:
        chain_to_use = chains[0]


    seq = "".join([str(pp.get_sequence()) for pp in ppb.build_peptides(chain_to_use)])
    if not seq:
        raise ValueError("Could not extract sequence from PDB chain %s" % chain_to_use.id)
    return seq

def canonicalize_smiles(smiles: str) -> str:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles}")
    # neutralize / sanitize by RDKit default
    Chem.SanitizeMol(mol)
    return Chem.MolToSmiles(mol, isomericSmiles=True)

def write_yaml_for_ligand(protein_seq: str, ligand_smiles: str, ligand_id: str, out_path: Path):
    """Write a Boltz-compatible YAML file for a single protein+ligand pair.


    Minimal schema (based on Boltz examples):
    version: 1
    sequences:
    - protein:
    id: A
    sequence: "..."
    - ligand:
    id: LIG
    smiles: "..."

    The file is saved as <ligand_id>.yaml in out_path.
    """
    yaml_content = {
        "version": 1,
        "sequences": [
        {"protein": {"id": "A", "sequence": protein_seq}},
        {"ligand": {"id": ligand_id, "smiles": ligand_smiles}},
        ],
        }
    out_file = out_path / f"{ligand_id}.yaml"
    # Write using simple JSON-to-YAML-ish representation to avoid adding pyyaml dependency here.
    # Boltz accepts standard YAML; writing a minimal representation is fine.
    # We'll write a small hand-constructed YAML to keep dependencies small.
    with out_file.open("w") as fh:
        fh.write("version: 1\n")
        fh.write("sequences:\n")
        fh.write(" - protein:\n")
        fh.write("   id: A\n")
        # ensure long sequence is folded properly
        fh.write(f" sequence: {protein_seq}\n") #>-
        # indent the sequence lines
        seq_lines = protein_seq
        #fh.write(" " + seq_lines + "\n")
        fh.write(" - ligand:\n")
        fh.write(f" id: {ligand_id}\n")
        fh.write(f" smiles: \"{ligand_smiles}\"\n")
    return out_file

def run_boltz_predict(input_dir: Path, out_dir: Path, use_msa_server: bool = True, extra_args: list = None):
    """Call the `boltz predict` CLI on the given input directory.


    This will run Boltz on all YAML files present in input_dir. It writes results into out_dir.
    """
    cmd = ["boltz", "predict", str(input_dir), "--out_dir", str(out_dir)]
    if use_msa_server:
        cmd.append("--use_msa_server")
    if extra_args:
        cmd += extra_args

    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    
def find_affinity_jsons(output_root: Path):
    """Search recursively for JSON files that look like Boltz affinity outputs.
    Returns list of pathlib.Path objects.
    """
    jsons = list(output_root.rglob("*affinity*.json"))
    # fallback: any json under predictions
    if not jsons:
        jsons = list(output_root.rglob("*.json"))
    return jsons

def parse_affinity_json(json_path: Path):
    with json_path.open() as fh:
        data = json.load(fh)
    # Boltz output structure can vary; attempt to extract the most useful fields
    # Typical keys: affinity_pred_value, affinity_probability_binary
    out = {}
    # flatten if predictions are nested
    if isinstance(data, dict):
        keys = list(data.keys())
    # attempt to locate affinity keys anywhere
    if "affinity_pred_value" in data:
        out["affinity_pred_value"] = data.get("affinity_pred_value")
    if "affinity_probability_binary" in data:
        out["affinity_probability_binary"] = data.get("affinity_probability_binary")
    # some outputs store predictions under `predictions` or `outputs`
    for candidate in ["predictions", "outputs", "affinity"]:
        if candidate in data and isinstance(data[candidate], dict):
            if "affinity_pred_value" in data[candidate]:
                out["affinity_pred_value"] = data[candidate]["affinity_pred_value"]
    if "affinity_probability_binary" in data[candidate]:
        out["affinity_probability_binary"] = data[candidate]["affinity_probability_binary"]
    return out

def main(args):
    print("\n Hello! Starting Boltz ligand affinity prediction pipeline.\n")
    # extract sequence
    protein_seq = extract_protein_sequence_from_pdb(str(args.pdb_file))
    print(f"Extracted protein sequence: {protein_seq} \n")
    print(f"Extracted protein sequence length: {len(protein_seq)} \n")

    # Create temp input dir with yaml files
    tmp_input_dir = Path(args.work_dir) if args.work_dir else Path(tempfile.mkdtemp(prefix="boltz_inputs_"))
    tmp_input_dir.mkdir(parents=True, exist_ok=True)

    #df load
    df = pd.read_csv(args.ligands_csv)
    print(f"Loaded {len(df)} ligands from {args.ligands_csv} \n")
    
    #output dir
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    created_yaml_files = []
    for idx, row in df.iterrows():
        smiles = row["SMILES_Prepared"]
        # prefer using index_ID for file names
        ligand_id = str(row.get("index_ID", idx))
        try:
            smiles_canon = canonicalize_smiles(smiles)
        except Exception as e:
            print(f"Skipping {ligand_id} due to invalid SMILES: {smiles} -> {e}")
            continue
        yfile = write_yaml_for_ligand(protein_seq, smiles_canon, ligand_id, tmp_input_dir)
        created_yaml_files.append((ligand_id, yfile))

    print(f"Wrote {len(created_yaml_files)} YAML files to {tmp_input_dir}")

    # run boltz predict once on the directory
    run_boltz_predict(tmp_input_dir, output_dir, use_msa_server=args.use_msa_server, extra_args=args.extra_args)

    # parse results
    jsons = find_affinity_jsons(output_dir)
    print(f"Found {len(jsons)} JSON output files to parse")

    records = []
    for j in jsons:
        try:
            parsed = parse_affinity_json(j)
            # derive ligand id from filename (basename without extension)
            ligand_id = j.stem
            rec = {"index_ID": ligand_id, "affinity_pred_value": parsed.get("affinity_pred_value"),
            "affinity_probability_binary": parsed.get("affinity_probability_binary"), "json_file": str(j)}
            records.append(rec)
        except Exception as e:
            print(f"Failed to parse {j}: {e}")

    out_df = pd.DataFrame(records)
    # merge with original smiles (if present)
    if "index_ID" in df.columns:
        merged = df.merge(out_df, how="left", left_on="index_ID", right_on="index_ID")
    else:
        # if index_ID was the DataFrame index
        df_indexed = df.reset_index().rename(columns={"index": "index_ID"})
        merged = df_indexed.merge(out_df, how="left", on="index_ID")

    # save
    merged.to_csv(output_dir / "boltz_affinity_results.csv", index=False)
    print(f"Saved results to {output_dir / 'boltz_affinity_results.csv'}")

    # cleanup temp dir if it was auto-created
    if not args.work_dir:
        try:
            shutil.rmtree(tmp_input_dir)
        except Exception:
            pass

    return merged

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ligands_csv", required=True, help="CSV file with columns SMILES_Prepared and index_ID")
    parser.add_argument("--pdb_file", required=True, help="Protein PDB file to use for predictions")
    parser.add_argument("--output_dir", required=True, help="Directory where Boltz outputs will be written")
    parser.add_argument("--work_dir", default=None, help="Optional directory to write Boltz YAML inputs (default: temp dir)")
    parser.add_argument("--use_msa_server", action="store_true", help="Add --use_msa_server to boltz call (recommended)")
    parser.add_argument("--extra_args", nargs="*", help="Extra arguments to append to boltz predict command", default=None)

    args = parser.parse_args()
    res = main(args)
    # print small summary
    print(res[ [c for c in res.columns if 'affinity' in c or c in ['index_ID','SMILES_Prepared'] ] ].head())