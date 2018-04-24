# PTS1_PTS2_predictor
------------------------------------------------------------------------------------------------------------------------------------------
This program will get the NCBI access number from your proteomics result in a Excel table, search for its protein sequence into the NCBI server, find the  glycosomal motifs PTS1, PTS2 and give you an output Excel table with the original data with new columns YES/NO for the PTS motifs and the encountered sequences.
------------------------------------------------------------------------------------------------------------------------------------------

Hi! My name is Jonas and *I'm not a bioinformatician*! A collegue of mine had a proteomics table with several and several proteins that she wanted to check whether they have putative PTS binding sites for glycosomal import and, instead of she searching one by one, I wrote this code to help her.

Feel free to used it, however, the code lacks statistical analysis of the encountered sequences! I'm interested in adding it to the code, so if you can help me with that I will appreciate!

NOTE: Read the instructions in the code. You'll need to rename your accession number column with 'Accession', and I used the NCBI server to look for protein sequences, so your accession numbers has to match the ones from the NCBI server.


REFERENCES

Fred R. Opperdoes and Jean-Pierre Szikora. In silico prediction of the glycosomal enzymes of Leishmania major and trypanosomes. Molecular & Biochemical Parasitology vol. 147, pp. 193–206, 2006.

Markus Kunze, Naila Malkani, Sebastian Maurer-Stroh, Christoph Wiesinger, Johannes A. Schmid, and Johannes Berger. Mechanistic Insights into PTS2-mediated Peroxisomal Protein Import. THE JOURNAL OF BIOLOGICAL CHEMISTRY VOL. 290, NO. 8, pp. 4928–4940, February 20, 2015.
