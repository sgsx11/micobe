import pandas as pd
import os
import traceback
import argparse

def modify_type(table, Type,P):
    count = 0
    # 求第level级分类数量
    x = table.copy()
    for i in range(len(table['taxonomy'])):
        if table['type'][i] == Type:
            x.loc[i, "new_score"] = table.loc[i, "score"] / P
            count += x.loc[i, "new_score"]
        # break
    tmp = 0
    for i in range(len(table['taxonomy'])):
        if table['type'][i] == Type:
            x.loc[i, "new_score_normalized"] = x.loc[i, "new_score"] / count * 100
            tmp += x.loc[i, "new_score_normalized"]
    print(tmp)
    # x.loc["new_score_normalized"] = (x.loc["new_score_normalized"]/count) * 100
    # print(x.loc[:"new_score_normalized"].sum(axis=1))
    return x

def modify(file, P, output_file):
    # print(output_file)
    table = pd.read_table((file))
    table['new_score'] = 0
    table['new_score_normalized'] = 0
    table['flagstat'] = P
    # print(table)
    table = modify_type(table, 'genus',P)
    table = modify_type(table, 'species',P)
    # print(table)
    table.to_csv(output_file, sep='\t')
    # save
def pathseq_norm(data_dir,flag_dir,output_dir):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    pathseq_files = os.listdir(flag_dir)
    #print(pathseq_files)
    for file in pathseq_files:
        print(file)
        #读取in total
        stat_file = flag_dir+ '\\' + file
        try:
            with open(stat_file,'r') as f:
                contexts = f.readlines()
                P = int(contexts[0].split(' ')[0])
                print(P)
                modify(data_dir+"\\"+file.split("_")[0]+"_rna_output.pathseq.txt",P,output_dir+"\\"+file[:-4]+'.normalized.txt')
        except:
            traceback.print_exc()
        print('\n')

#参数
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="Normalize the output result files of PathSeq.\n")

Required_Arguments = parser.add_argument_group('Required_Arguments')

Required_Arguments.add_argument("-in1","--input_dir1", help="Directory where pathseq files are located.")

Required_Arguments.add_argument("-in2","--input_dir2", help="Directory where flagstat files are located.")

Required_Arguments.add_argument("-o","--output_dir", help="Directory where output files are located.")

# Optional_Arguments = parser.add_argument_group('Optional_Arguments')
#
# Optional_Arguments.add_argument("-test",help="测试")

args = parser.parse_args()

print(args)

pathseq_norm(args.input_dir1,args.input_dir2,args.output_dir)
