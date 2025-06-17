import argparse
from pathlib import Path
import subprocess
import shutil

def concatenate_fastqs(barcode_folder: Path, combined_output_dir: Path) -> Path:
    """
    Concatenate all .fastq.gz files in a barcode folder into one combined file.
    Returns the path to the combined file.
    """
    combined_output_dir.mkdir(parents=True, exist_ok=True)
    combined_file = combined_output_dir / f"{barcode_folder.name}_combined.fastq.gz"

    with open(combined_file, "wb") as wfp:
        for fq_file in sorted(barcode_folder.glob("*.fastq.gz")):
            with open(fq_file, "rb") as rfp:
                shutil.copyfileobj(rfp, wfp)

    return combined_file

def run_workflow(input_path, workflow_path, output_path):
    input_path = Path(input_path)
    workflow_path = Path(workflow_path)
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    #The idea is to have a two-step glob where you get the directories in a subdirectory, then the files in those directories.
    subdirectories = [barcode_directory for barcode_directory in input_path.iterdir() if barcode_directory.is_dir()]
   
    for barcode_folder in subdirectories:
        print(f"Running workflow on barcode directory: {barcode_folder.name}")

        combined_path = output_path / "combined_files"
        combined_fastq = concatenate_fastqs(barcode_folder, combined_path)

        barcode_output_dir = output_path / barcode_folder.name
        barcode_output_dir.mkdir(parents=True, exist_ok=True)
            
        command = [
            "geneious",
            "-w", str(workflow_path),
            "-i", str(combined_fastq),
            "-o", str(barcode_output_dir / f"{barcode_folder.name}_results.csv")
        ]
        subprocess.run(command, check=True)


def main():
    parser = argparse.ArgumentParser(prog="Script to run a Geneious workflow on all barcodes in a dataset")
    parser.add_argument("-i", "--input_path",required=True, help="Path to dataset") #to a directory or a file
    parser.add_argument("-w","--workflow_path",required=True, help="Path to the workflow file")
    parser.add_argument("-o","--output_path", required=True, help="Path to the output directory")
    args = parser.parse_args()

    run_workflow(args.input_path, args.workflow_path, args.output_path)

    print(f"Input Path: {args.input_path}")
    print(f"Workflow Path: {args.workflow_path}")
    print(f"Output Path: {args.output_path}")

if __name__ == '__main__':
    main()
