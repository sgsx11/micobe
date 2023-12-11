import os
import pandas as pd
import argparse
import json



def t_stage(cr,si):

    pass

def start(cr,tmb,si,output_dir):
    #01-t_stage

    pass


#参数
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="Classify samples based on the clustering results of the characteristic bacterial abundance matrix.\n")

Required_Arguments = parser.add_argument_group('Required_Arguments')

Required_Arguments.add_argument("-cr","--classification_results", help="characteristic_bacteria_matrix.")

Required_Arguments.add_argument("-tmb","--tmb_file", help="Result file of tumor mutation load.")

Required_Arguments.add_argument("-si","--sample_info", help="Result file of tumor mutation load.")

Required_Arguments.add_argument("-o","--output_dir", help="Directory where output files are located.")

Optional_Arguments = parser.add_argument_group('Optional_Arguments')

#Optional_Arguments.add_argument("-n","--n_clusters", help="Number of categories for clustering samples. Default 3")

args = parser.parse_args()

start(args.classification_results, args.tmb_file, args.sample_info, args.output_dir)





