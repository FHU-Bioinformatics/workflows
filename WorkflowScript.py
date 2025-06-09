import argparse
from pathlib import Path
import subprocess


def run_workflow(input_path, workflow_path, output_path):
    input_path = Path(input_path)
    workflow_path = Path(workflow_path)
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    #The idea is to have a two-step glob where you get the directories in a subdirectory, then the files in those directories.
    subdirectories = [barcode_directory for barcode_directory in input_path.iterdir() if barcode_directory.is_dir()]

    for barcode_dir in subdirectories:
        fastq_files = list(barcode_dir.glob("*.fastq.gz"))
        for fastq_file in fastq_files:
            print(f"Running workflow on barcode directory: {barcode_dir.name}")

            command = [
                "geneious",
                "-w", str(workflow_path),
                "-i", str(fastq_file),
                "-o", str(output_path / f"{barcode_dir.name}.csv")
            ]
            subprocess.run(command, check=True)


def main():
    parser = argparse.ArgumentParser(prog="Script to run a Geneious workflow on all barcodes in a dataset")
    parser.add_argument("-i", "--input_path",required=True, help="Path to dataset")
    parser.add_argument("-w","--workflow_path",required=True, help="Path to the workflow file")
    parser.add_argument("-o","--output_path", required=True, help="Path to the output directory")
    args = parser.parse_args()

    run_workflow(args.input_path, args.workflow_path, args.output_path)

    print(f"Input Path: {args.input_path}")
    print(f"Workflow Path: {args.workflow_path}")
    print(f"Output Path: {args.output_path}")

if __name__ == '__main__':
    main()
