import os
import pandas as pd
import argparse
import json


def save(dict_file,file_name,output_dir):
    # 保存
    json_str = json.dumps(dict_file)
    if not os.path.exists(output_dir + '/method2/'):
        os.mkdir(output_dir + '/method2/')
    with open(output_dir + '/method2/' + file_name, "w") as json_file:
        json.dump(json_str, json_file)
    print("results has already been saved in {}".format(output_dir + '/method2/' + file_name))

def TMB(tmb_dir,output_dir,data):
    #读取tmb结果
    tmb = pd.read_csv(tmb_dir, sep="\t")
    tmb.set_index(tmb.columns[0], inplace=True)
    print("tmb_table:", tmb)
    tmb_result = {"label":[],"N":[],"T":[]}
    print(data.keys())
    keys = sorted(data.keys())
    tmb_result["label"] = keys
    for key in keys:
        N_tmp = []
        T_tmp = []
        for sample in data[key]:
            sample_T = sample.split("_")[0]
            sample_N = sample_T[:-1] + "N"
            N_tmp.append(tmb.loc[sample_N]['total_perMB_log'])
            T_tmp.append(tmb.loc[sample_T]['total_perMB_log'])
        tmb_result["N"].append(N_tmp)
        tmb_result["T"].append(T_tmp)
    print(tmb_result)
    #保存结果
    save(tmb_result,"multi_tmb_result",output_dir)
    pass

def TME(tme_dir,output_dir,data):
    #读取tme结果
    tme = pd.read_csv(tme_dir, sep="\t")
    print("tme_table:", tme)
    #提取每个免疫细胞在异质肿瘤样本中的丰度并与N样本比较
    keys = sorted(data.keys())
    colnames = list(tme.columns)[:22]
    tme_results = {}
    tme_results['label'] = keys
    for col in colnames:
        tme_results[col] = {"N":[],"T":[]}
        for key in keys:
            N_tmp = []
            T_tmp = []
            for sample in data[key]:
                sample_T = sample.split("_")[0]
                sample_N = sample_T[:-1] + "N"
                N_tmp.append(tme.loc[sample_N][col])
                T_tmp.append(tme.loc[sample_T][col])
            tme_results[col]["N"].append(N_tmp)
            tme_results[col]["T"].append(T_tmp)
    print(tme_results)
    save(tme_results, "multi_tme_result", output_dir)
    pass

def start(classification_result,tmb,tme,output_dir):
    #读取分类结果
    # 读取step4的分类结果
    with open(classification_result, "r") as json_file:
        data = json.load(json_file)
    data = eval(data)
    print(data)
    #02-tmb
    TMB(tmb,output_dir,data)
    #03-tme
    TME(tme,output_dir,data)
    pass


#参数
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="Classify samples based on the clustering results of the characteristic bacterial abundance matrix.\n")

Required_Arguments = parser.add_argument_group('Required_Arguments')

Required_Arguments.add_argument("-cr","--classification_results", help="classification_results.")

Required_Arguments.add_argument("-tmb","--tmb_file", help="Result file of tumor mutation load.")

Required_Arguments.add_argument("-tme","--tme_file", help="Result file of tumor mircroenvirment.")

Required_Arguments.add_argument("-o","--output_dir", help="Directory where output files are located.")

Optional_Arguments = parser.add_argument_group('Optional_Arguments')

#Optional_Arguments.add_argument("-n","--n_clusters", help="Number of categories for clustering samples. Default 3")

args = parser.parse_args()

print(args)

start(args.classification_results, args.tmb_file, args.tme_file, args.output_dir)
