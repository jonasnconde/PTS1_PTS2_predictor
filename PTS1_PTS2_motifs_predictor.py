"""
----------------------- PTS1_PTS2_motifs_predictor.py -------------------------

This program will get the NCBI access number from your proteomics result in a 
Excel table, search for its protein sequence into the NCBI server, find the 
glycosomal motifs PTS1, PTS2 and give you an output Excel table with the 
original data with new columns YES/NO for the glycosomal motifs and the
encountered sequence.
-------------------------------------------------------------------------------
"""

import os, re
import pandas as pd
import numpy as np
from Bio import Entrez

# Add your folder directory.
os.chdir('C:\\Users\\jonas\\OneDrive\\proteomaAna\\goodscripts')

# Add the name of your Excel file and the name of its sheet you are going to
# use. IMPORTANT: your column for your accession numbers MUST be named
# 'Accession' or otherwise you have to change it in the code.
file = "table_1_tot-re_for_pandas.xlsx"
sheet = "Sheet1"

# Opening the Excel file and its sheet as a pandas dataframe.
table = pd.read_excel(file, sheetname = sheet)

# Remove the rows that contains NaN values for your 'Accession' column 
# and creating a subset.
table_subset = table.dropna(subset=['Accession'])

# In order to enter NCBI database you have to identify yourself (enter your
# email bellow).
Entrez.email = 'jonasconde@biof.ufrj.br'

# Creating a function for getting the protein sequences from NCBI and adding it
# to the dataframe.
seq = []
def return_ptn_NCBI(dataframe):
    countDown = (len(dataframe))
    for acode in dataframe['Accession']:
        countDown = countDown - 1
        print('Searching... ' + str(acode) + ' | Count Down: ' + str(countDown))
        handle = Entrez.efetch(db="protein", id=int(acode), retmode="xml")
        record = Entrez.read(handle)
        handle.close()
        sequence = record[0]['GBSeq_sequence']
        if sequence == '':
            seq.append(np.nan)
        else:
            seq.append(sequence)
    return seq

# calling the function.
return_ptn_NCBI(table_subset)

# Adding the 'Sequence' column to the subset dataframe.
table_subset['Sequence'] = seq

# Now we are going to search for glycosomal motifs. For that, we need to set
# the Regex for each one.
PTS1 = re.compile(r'''(
    (s|t|a|g|c|n){1}
    (r|k|h){1}
    (l|i|v|m|a|f|y){1}$
    )''', re.VERBOSE)

SSL = re.compile(r'''(
    (s){2}
    (l|i|f){1}$
    )''', re.VERBOSE)

PTS2 = re.compile(r'''(
    ^(m){1}
    (\w{0,20})
    (r|k){1}
    (l|v|i){1}
    (\w{5})
    (h|k|q|r){1}
    (l|a|i|f|v|y){1}
    )''', re.VERBOSE)

# Let's create lists that will save the results as YES/NO to PTS1/2 or SSL,
# and lists that will record the matched sequences for PTS1/2 or SSL.
PTS1_YN = []
PTS2_YN = []
SSL_YN = []

PTS1_seq = []
PTS2_seq = []
SSL_seq = []

# Ok, now let's create a function for finding the glycosomal motifs. The
# parameters will be the dataframe, the Regex, the YN list and the seq list.
def find_glycosomal_motifs(dataframe, glyco_re, glyco_YN_list, glyco_seq_list):
    for seq in dataframe['Sequence']:
        signal = glyco_re.findall(seq)
        if signal == []:
            glyco_YN_list.append('NO')
            glyco_seq_list.append(np.nan)
        else:
            glyco_YN_list.append('YES')
            if len(signal[0][0]) == 3:
                glyco_seq_list.append(signal[0][0].upper())
            else:
                glyco_seq_list.append(signal[0][2].upper() + signal[0][3].upper() +
                                      signal[0][4].upper() + signal[0][5].upper() +
                                            signal[0][6].upper())
    
# Let's call the function for each glycosomal motif (PTS1, PTS2, SSL)
find_glycosomal_motifs(table_subset, PTS1, PTS1_YN, PTS1_seq)
find_glycosomal_motifs(table_subset, PTS2, PTS2_YN, PTS2_seq)
find_glycosomal_motifs(table_subset, SSL, SSL_YN, SSL_seq) 

# Adding the new columns.
table_subset['PTS1'] = PTS1_YN
table_subset['PTS1_seq'] = PTS1_seq
table_subset['PTS2'] = PTS2_YN
table_subset['PTS2_seq'] = PTS2_seq
table_subset['SSL'] = SSL_YN
table_subset['SSL_seq'] = SSL_seq

# Let's create a subset filtering only the glycossomal proteins and that will
# serve as a new sheet into the Excel output file.
table_gly_subset = table_subset[(table_subset.PTS1 == 'YES') | (table_subset.PTS2 == 'YES') | 
                                (table_subset.SSL == 'YES')]

# Creating the Excel writer using XlsxWriter engine.    
writer = pd.ExcelWriter('PTS_proteins.xlsx', engine = 'xlsxwriter')

# Converting the dataframe to an XlsxWriter Excel object.
table_subset.to_excel(writer, sheet_name='Main_table')
table_gly_subset.to_excel(writer, sheet_name='Only_PTS_ptns')

# Closing the Pandas Excel writer and output the Excel file.
writer.save()
