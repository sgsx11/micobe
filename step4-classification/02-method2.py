import os
import pandas as pd
import argparse
import json

def clssification(cbm,output_dir):
    cb_matrix = pd.read_csv(cbm, sep='\t')
    print(cb_matrix)
    pass

#参数
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="Classify samples based on the clustering results of the characteristic bacterial abundance matrix.\n")

Required_Arguments = parser.add_argument_group('Required_Arguments')

Required_Arguments.add_argument("-cbm","--characteristic_bacteria_matrix", help="characteristic_bacteria_matrix.")

Required_Arguments.add_argument("-o","--output_dir", help="Directory where output files are located.")

args = parser.parse_args()

print(args)


clssification(args.characteristic_bacteria_matrix,args.output_dir)

