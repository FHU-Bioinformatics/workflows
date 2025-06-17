# Workflows

Each workflow accomplishes a different task at hand

## FHU-Bioinfo

This is the current workflow that takes a barcode, trims sequences, runs De Novo Assembly, and then BLASTs each consensus, sequence, and sequences within the contigs. It then has an Assembly, Query, and Hits folder inside of the barcode in Geneious Prime. Assembly has information on the De Novo Assembly, Query has each sequence/consensus that met the requirements to be ran through BLAST, and Hits has every sequence/consensus from Query that returned a hit on an organism.

### -Filtered

Same as FHU-Bioinfo, but it does not run the sequences that make up contigs (less to BLAST)

## FHU-Bioinfo-DoubleBlast

This workflow is an older workflow that utilizes two remote database blast hits to organize the hits for the data