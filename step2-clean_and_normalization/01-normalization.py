import pandas as pd
import os
import traceback
import argparse

def read_data(old_df,file,Type):
    df = pd.read_csv(file,sep='\t')
    new_df = df[["type","name","kingdom","new_score_normalized"]]
    new_df = new_df[new_df["type"] == Type]
    new_df = new_df.rename(columns={'new_score_normalized':'_'.join(file.split('/')[-1].split('_')[:2])})
    if old_df.empty:
        return new_df
    else:
        return pd.merge(old_df, new_df,on=["type","name","kingdom"],how='outer')

def get_matrix(data_dir,output_dir,type,sample_type):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    files = os.listdir(data_dir)
    old_df = pd.DataFrame()
    for file in files:
        old_df = read_data(old_df, data_dir +"/"+ file, type)
    old_df = old_df.fillna(0)
    old_df.sort_values(by="name", inplace=True, ascending=True)
    #print(old_df)
    # break
    old_df.to_csv(output_dir+"/"+sample_type+"_"+type+'_matrix.txt', sep='\t', index=None)

def modify_type(table,Type,P):#标准化并且求表达矩阵
    count = 0
    # 求第level级分类数量
    x = table.copy()
    for i in range(len(table['taxonomy'])):
        if table['type'][i] == Type:
            x.loc[i, "new_score"] = table.loc[i, "score"] / P
            count += x.loc[i, "new_score"]
        # break
    #tmp = 0
    for i in range(len(table['taxonomy'])):
        if table['type'][i] == Type:
            x.loc[i, "new_score_normalized"] = x.loc[i, "new_score"] / count * 100
            #tmp += x.loc[i, "new_score_normalized"]
    #print(tmp)
    return x

def modify(file, P, output_file):
    table = pd.read_table(file)
    table['new_score'] = 0
    table['new_score_normalized'] = 0
    table['flagstat'] = P
    table = modify_type(table, 'genus',P)
    table = modify_type(table, 'species',P)
    table.to_csv(output_file, sep='\t')
def pathseq_norm(data_dir,flag_dir,output_dir):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    pathseq_files = os.listdir(flag_dir)
    for file in pathseq_files:
        print(file)
        #读取in total
        stat_file = flag_dir+ '/' + file
        try:
            with open(stat_file,'r') as f:
                contexts = f.readlines()
                P = int(contexts[0].split(' ')[0])
                print(P)
                modify(data_dir+"/"+file.split("_")[0]+"_rna_output.pathseq.txt",P,output_dir+"\\"+file[:-4]+'.normalized.txt')
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

Required_Arguments.add_argument("-o","--norm_output_dir", help="Directory where output files are located.")

Required_Arguments.add_argument("-m","--martix_output_dir", help="Directory where output files are located.")

Required_Arguments.add_argument("-st","--sample_type")

# Optional_Arguments = parser.add_argument_group('Optional_Arguments')
#
# Optional_Arguments.add_argument("-test",help="测试")

args = parser.parse_args()

print(args)

pathseq_norm(args.input_dir1,args.input_dir2,args.norm_output_dir)

get_matrix(args.norm_output_dir,args.martix_output_dir,"genus",args.sample_type)

get_matrix(args.norm_output_dir,args.martix_output_dir,"species",args.sample_type)


