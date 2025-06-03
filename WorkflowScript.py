import argparse
from pathlib import Path
import subprocess

def run_workflow(input_path, workflow_path, output_path):
    input_path = Path(input_path)
    workflow_path = Path(workflow_path)
    output_path = Path(output_path)

    for barcode_directory in input_path.iterdir():
        if barcode_directory.is_dir():
            print(f"Running workflow on {barcode_directory.name}")

            command = [
                "geneious",
                "--run-workflow", str(workflow_path),
                "--input", str(barcode_directory),
                "--output", f"{output_path}/{barcode_directory.name}",
                "--export-csv" 
            ]

            subprocess.run(command, check=True)


def main():
    parser = argparse.ArgumentParser(prog="Script to run a Geneious workflow on all barcodes in a dataset")
    parser.add_argument("input_path", help="Path to dataset")
    parser.add_argument("workflow_path", help="Path to the workflow file")
    parser.add_argument("output_path", help="Path to the output directory")
    args = parser.parse_args()

    run_workflow(args.input_path, args.workflow_path, args.output_path)

if __name__ == '__main__':
    main()
