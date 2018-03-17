import csv
import numpy as np
import pandas as pd



def OpenMetaData():
    with open('/Users/jameskonda/Desktop/Genomics/EucBarcodeReader/metadata/EucMetadata.csv', mode='r') as infile:
        reader = csv.reader(infile)
        metadata = dict((rows[7],[rows[0],rows[1],rows[2],rows[3],rows[4],rows[5],rows[6]]) for rows in reader)
    return metadata

def CheckIfMetadata():#feildID, filename):
    # lookup metadata in CSV
    # CHECK if metadata:
        # if not, Move to Move to no-metadata
    with open('/Users/jameskonda/Desktop/Genomics/EucBarcodeReader/metadata/EucMetadata.csv', mode='r') as infile:
        reader = csv.reader(infile)
        mydict = dict((rows[7],[rows[0],rows[1],rows[2],rows[3],rows[4],rows[5],rows[6]]) for rows in reader)

    if "nah" not in mydict.keys():
        print("good work dickhead")




CheckIfMetadata()
