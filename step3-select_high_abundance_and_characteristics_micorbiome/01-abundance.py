import os
import pandas as pd
import argparse

def group_and_save(new_df,output_dir):
    lenth = len(new_df.values)
    category = ['N'] * lenth + ['T'] * lenth  #N/T
    subcategory = new_df['name'].values.tolist() * 2 #微生物名称
    value = new_df['N'].values.tolist() + new_df['T'].values.tolist()
    r_df = pd.DataFrame()
    r_df['category'] = category
    r_df['subcategory'] = subcategory
    r_df['value'] = value
    print("Data used for drawing the next step.")
    print(r_df)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    r_df.to_csv(output_dir + "stack_plot.txt", sep="\t",index = None)

def abundance(normal_matrix,tumor_matrix,threshold,output_dir,kingdom):
    matrix_N = pd.read_csv(normal_matrix, sep='\t')
    matrix_T = pd.read_csv(tumor_matrix, sep='\t')
    matrix_N = matrix_N[matrix_N['kingdom'] == kingdom]
    matrix_T = matrix_T[matrix_T['kingdom'] == kingdom]
    matrix_N = matrix_N.drop(columns=['type','kingdom'])
    matrix_T = matrix_T.drop(columns=['type', 'kingdom'])
    #合并N_T矩阵
    matrix = pd.merge(matrix_N, matrix_T, on="name", how='outer')
    matrix = matrix.fillna(0)
    # print(genus_matrix)
    col_names_N = list(matrix_N.columns)
    col_names_T = list(matrix_T.columns)
    # 除name列之外的所有列求行均值,然后和name列合并为新的DataFrame
    # wgs_N = wgs_N_matrix.iloc[:,1:].mean(axis=1)
    # wgs_T = wgs_T_matrix.iloc[:,1:].mean(axis=1)
    mean_N = matrix[col_names_N[1:]].mean(axis=1)
    mean_T = matrix[col_names_T[1:]].mean(axis=1)
    matrix_mean = pd.DataFrame({'name': matrix['name'], 'N': mean_N, 'T': mean_T})
    matrix_mean['mean'] = matrix_mean.iloc[:, 1:].mean(axis=1) #计算用于排序的均值
    matrix_mean = matrix_mean.sort_values(by="mean", ascending=False)
    finall_df = matrix_mean[matrix_mean['mean'] > float(threshold)].reset_index(drop=True)
    finall_df.loc[len(finall_df.index)] = ['Other', 100 - finall_df.sum()['N'], 100 - finall_df.sum()['T'],100 - finall_df.sum()['mean']]
    group_and_save(finall_df,output_dir + '/')

#参数
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="Differences in microbial abundance between normal and tumor samples.\n")

Required_Arguments = parser.add_argument_group('Required_Arguments')

Required_Arguments.add_argument("-nm","--normal_matrix", help="cleaned normal sample expression matrix.")

Required_Arguments.add_argument("-tm","--tumor_matrix", help="cleaned tumor sample expression matrix.")

Required_Arguments.add_argument("-t","--threshold", help="Microbes with abundance greater than the threshold value are defined as major microbes.The range is from 0 to 100.")

Required_Arguments.add_argument("-o","--output_dir", help="Directory where output files are located.")

Required_Arguments.add_argument("-k","--kingdom", help="The kingdom types include bacteria, archaea, fungi , Eukaryota , etc.")

args = parser.parse_args()

print(args)

abundance(args.normal_matrix,args.tumor_matrix,args.threshold,args.output_dir,args.kingdom)