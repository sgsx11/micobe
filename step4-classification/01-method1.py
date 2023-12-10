import os
import pandas as pd
import argparse
import json

def clssification1(tumor_matrix,cb,output_dir,kingdom,percent=50):
    matrix_T = pd.read_csv(tumor_matrix, sep='\t')
    matrix_T = matrix_T[matrix_T['kingdom'] == kingdom]
    matrix_T = matrix_T.drop(columns=['type', 'kingdom'])
    #选取Propionibacterium高表达的样本和低表达的T样本
    col_names = list(matrix_T.columns)[1:]
    values = matrix_T[matrix_T['name'] == cb].values.tolist()[0][1:]
    temp_zip = list(zip(col_names,values))
    sorted_list = sorted(temp_zip, key=lambda elem: elem[1])
    lenth = int(len(sorted_list)*percent/100)
    low_sample = [s[0].split('_')[0] for s in sorted_list[:lenth]]
    high_sample = [s[0].split('_')[0] for s in sorted_list[len(sorted_list)-lenth:]]
    print("low_sample:",low_sample)
    print("high_sample:",high_sample)
    # 存储
    save_dict = {'low_sample':low_sample,"high_sample":high_sample}
    json_str = json.dumps(save_dict)
    if not os.path.exists(output_dir+'/method1/'):
        os.mkdir(output_dir+'/method1/')
    with open(output_dir+'/method1/' + "classification_results.json", "w") as json_file:
        json.dump(json_str, json_file)
    print("classification_results has already been saved in {}".format(output_dir+'/method1/' + "classification_results.json"))

#参数
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="Classify samples based on the abundance of characteristic bacteria.\n")

Required_Arguments = parser.add_argument_group('Required_Arguments')

Required_Arguments.add_argument("-tm","--tumor_matrix", help="cleaned tumor sample expression matrix.")

Required_Arguments.add_argument("-o","--output_dir", help="Directory where output files are located.")

Required_Arguments.add_argument("-k","--kingdom", help="The kingdom types include bacteria, archaea, fungi , Eukaryota , etc.")


Optional_Arguments = parser.add_argument_group('Optional_Arguments')

Optional_Arguments.add_argument("-cb","--characteristic_bacteria", help="Characteristic bacteria for sample classification.")

Optional_Arguments.add_argument("-p","--percent", help="Taking the top p percentage of feature bacterial abundance as high samples, and the bottom p percentage as low samples, with p ranging from 0 to 100. Default 50.")

Optional_Arguments.add_argument("-cbc","--characteristic_bacteria_combination", help="Characteristic combination for sample classification.")

args = parser.parse_args()

print(args)

if not args.characteristic_bacteria is None:
    #基于特征菌的丰度将样本分为high和low两类
    if not args.percent is None:
        clssification1(args.tumor_matrix,args.characteristic_bacteria,args.output_dir,args.kingdom,int(args.percent))
    else:
        clssification1(args.tumor_matrix, args.characteristic_bacteria, args.output_dir,args.kingdom)

if not args.characteristic_bacteria_combination is None:
    # 基于特征菌的丰度将样本分为high和low两类
    #clssification(args.tumor_matrix, args.threshold, args.output_dir, args.kingdom)
    pass