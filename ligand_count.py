# Govinda KC
# The University of Texas at El Paso
# Computational Science Program
# Last modified: 09/14/2019

# A script to retrieve the number of ligands (ligand count) and other information using uniprot id from Pharos website
# Usage: python3 ligand_count.py P07948

# For many ligands at once, Use csv file containing containing the target information such as target gene (e.g., LYN) or Uniprot accession (e.g., P07948).

# next work: Try to get all the accession ids, symbols used from pharos website.

from urllib.error import HTTPError
import csv
import json
from tqdm import tqdm
from urllib.request import urlopen
import requests
import sys, re
import csv
pharos = "https://pharos.nih.gov/idg/api/v1/targets/"

def fetch_ligand(target):
    outfile = open('lig_counts.csv','w')
    try:
        req = urlopen(pharos + target)
        target_dict = json.loads(req.read())
        Gene=target_dict['gene']
        Group = target_dict['idgTDL']
        # Retrieve ligand links for this target
        print("Counting the ligands for target: ", target, end = ' --> ')
        req = urlopen(pharos + '{0}'.format(target_dict['id']) +"/links(kind=ix.idg.models.Ligand)")
        link = json.loads(req.read())
        print(len(link))
        ligand_count=str(len(link))
        # Writing the information to a csv file
        outfile.write('Gene - '+Gene+'\t'+'UniProt - '+target+'\t'+'Ligand_count - '+ligand_count+'\t'+'Group - '+Group+'\n')
     
    except Exception as e:
        print(e, end=' --> ')
        #print('Please wait, it may longer time')
        print('{} (could not be found on the server)'.format(target))
        outfile.write(target+','+'not found'+'\n')
        pass

    outfile.close()
if __name__ == "__main__":

    fetch_ligand(sys.argv[1])
#    # For many ligands information using uniprot ids 
#    _file = open('uniprots.txt','r').readlines()
#    
#    for uniprot in _file:
#        uniprot = uniprot.strip()
#        # This line below is added just to ignore if the file contains some hidden characters.
#        uniprot = re.sub("[^a-z0-9]+","", uniprot, flags=re.IGNORECASE)
#        fetch_ligand(uniprot)
