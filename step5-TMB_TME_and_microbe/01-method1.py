import os
import pandas as pd
import argparse
import json

def t_stage(classification_result,sample_info,output_dir):
    print("\nt_stage")
    #读取step4的分类结果
    with open(classification_result,"r") as json_file:
        data = json.load(json_file)
    data = eval(data)
    print(data)
    low_samples =  data["low_sample"]
    high_samples = data["high_sample"]
    info = pd.read_excel(sample_info)
    print(info)
    period = {}
    files = info['文件'].values.tolist()
    t_stage = {"low_sample":[],"high_sample":[]}
    for name in low_samples:
        file_name = name.split('_')[0] + '_rna_output.pathseq.txt'
        if file_name in files:
            t = info[info['文件'] == file_name]['pT'].values[0]
            period[name] = t
            t_stage["low_sample"].append(t)
    for name in high_samples:
        file_name = name.split('_')[0] + '_rna_output.pathseq.txt'
        if file_name in files:
            t = info[info['文件'] == file_name]['pT'].values[0]
            period[name] = t
            t_stage["high_sample"].append(t)
    print("sample:t_stage ",period)
    print("t_stage:",t_stage)
    #保存
    json_str = json.dumps(t_stage)
    if not os.path.exists(output_dir + '/method1/'):
        os.mkdir(output_dir + '/method1/')
    with open(output_dir + '/method1/' + "t_stage.json", "w") as json_file:
        json.dump(json_str, json_file)
    print("t stage results has already been saved in {}".format(output_dir + '/method1/' + "t_stage.json"))


def TMB(classification_result,tmb_dir,output_dir):
    # 读取step4的分类结果
    with open(classification_result, "r") as json_file:
        data = json.load(json_file)
    data = eval(data)
    tmb = pd.read_csv(tmb_dir, sep="\t")
    tmb.set_index(tmb.columns[0], inplace=True)
    print("tmb_table:",tmb)
    sample_tmb = {"low_sample":[],"high_sample":[]}
    low_samples = data["low_sample"]
    high_samples = data["high_sample"]
    for sample in low_samples:
        sample_tmb["low_sample"].append(tmb.loc[sample]['total_perMB_log'])
    for sample in high_samples:
        sample_tmb["high_sample"].append(tmb.loc[sample]['total_perMB_log'])
    print("sample:tmb ",sample_tmb)
    #保存
    json_str = json.dumps(sample_tmb)
    if not os.path.exists(output_dir + '/method1/'):
        os.mkdir(output_dir + '/method1/')
    with open(output_dir + '/method1/' + "sample_tmb.json", "w") as json_file:
        json.dump(json_str, json_file)
    print("sample tmb results has already been saved in {}".format(output_dir + '/method1/' + "sample_tmb.json"))


def start(classification_result,tmb,sample_info,output_dir):
    #01-t_stage
    #t_stage(classification_result, sample_info,output_dir)
    #02-tmb
    TMB(classification_result,tmb,output_dir)
    #03-tme


    pass


#参数
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="Classify samples based on the clustering results of the characteristic bacterial abundance matrix.\n")

Required_Arguments = parser.add_argument_group('Required_Arguments')

Required_Arguments.add_argument("-cr","--classification_results", help="classification_results.")

Required_Arguments.add_argument("-tmb","--tmb_file", help="Result file of tumor mutation load.")

Required_Arguments.add_argument("-si","--sample_info", help="Result file of tumor mutation load.")

Required_Arguments.add_argument("-o","--output_dir", help="Directory where output files are located.")

Optional_Arguments = parser.add_argument_group('Optional_Arguments')

#Optional_Arguments.add_argument("-n","--n_clusters", help="Number of categories for clustering samples. Default 3")

args = parser.parse_args()

print(args)

start(args.classification_results, args.tmb_file, args.sample_info, args.output_dir)





