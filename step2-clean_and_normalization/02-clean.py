import pandas as pd
import os
import traceback
import argparse

def get_matrix(normal_files,tumor_files,control_files):
    normal_matrix = pd.read_csv(normal_files, sep='\t')
    normal_matrix.set_index('name', inplace=True)
    tumor_matrix = pd.read_csv(tumor_files,sep='\t')
    tumor_matrix.set_index('name', inplace=True)
    control_matrix = pd.read_csv(control_files,sep='\t')
    control_matrix['mean'] = control_matrix.iloc[:, 3:].mean(axis=1)
    control_matrix = control_matrix.sort_values(by="mean", ascending=False)
    return normal_matrix,tumor_matrix,control_matrix

def clean_by_threshold1(normal_matrix,tumor_matrix,control_matrix,threshold):
    mic_list = control_matrix[control_matrix['mean'] > float(threshold)]['name'].tolist()#存储在control中占比超过threshold的微生物
    normal_matrix,tumor_matrix = clean_by_list(normal_matrix, tumor_matrix, mic_list)
    #求取微生物占比均值
    return normal_matrix,tumor_matrix

def clean_by_threshold2(normal_matrix,tumor_matrix,control_matrix,threshold):
    #获取control_matrix包含的微生物
    mic_names = control_matrix["name"].tolist()
    #control中存在的微生物在normal中占比超过threshold(范围0-100)，将该样本删除.
    normal_matrix = clean_by_threshold2_utils(normal_matrix, mic_names, threshold,"normal")
    #control中存在的微生物在tumor中占比超过threshold(范围0-100)，将该样本删除.
    tumor_matrix = clean_by_threshold2_utils(tumor_matrix, mic_names, threshold,"tumor")
    return normal_matrix,tumor_matrix,

def clean_by_threshold2_utils(matrix,mic_names,threshold,sample_type):
    #筛选出在mic_names中出现的微生物构成的矩阵small_matrix
    mask = matrix.index.isin(mic_names)
    small_matrix = matrix[mask]
    #获取样本列名
    col_names = small_matrix.columns.tolist()[2:]
    #按列求取均值
    column_sum = small_matrix[col_names].sum()
    #筛选出均值大于threshold的列
    column_sum = column_sum[column_sum > float(threshold)]
    Samples_to_be_discarded = column_sum.index.tolist()
    #在df中去除特定的多列
    size = matrix.shape
    matrix = matrix.drop(columns=Samples_to_be_discarded)
    new_size = matrix.shape
    print("The size of the {}_matrix has been changed from {} to {}.".format(sample_type,size, new_size))
    print("The following samples have been removed from the {}_matrix:{}".format(sample_type,Samples_to_be_discarded))
    return matrix

def clean_by_list(normal_matrix,tumor_matrix,mic_list):
    #把name列作为索引，先判断mic_list中哪些在names中出现，删除在mic_list出现的行
    normal_matrix = clean_by_list_utils(normal_matrix, mic_list,"normal")
    tumor_matrix = clean_by_list_utils(tumor_matrix, mic_list,"tumor")
    return normal_matrix,tumor_matrix

def clean_by_list_utils(matrix,mic_list,sample_type):
    mask = matrix.index.isin(mic_list)
    size = matrix.shape
    matrix = matrix[~mask]
    new_size = matrix.shape
    print("The size of the {}_matrix has been changed from {} to {}.".format(sample_type,size, new_size))
    print("The following microorganisms have been removed from the {}_matrix:{}".format(sample_type,mic_list))
    return matrix

def save(matrix,file_name,output_dir):
    #print(matrix,file_name,output_dir)
    file = output_dir + "/" + file_name[:-4] + '_cleaned.txt'
    matrix.to_csv(file, sep='\t')
    print("matrix has been saved in {}".format(file))


#参数
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="data clean.\n")

Required_Arguments = parser.add_argument_group('Required_Arguments')

Required_Arguments.add_argument("-in1","--normal_files", help="normal matrix files.")

Required_Arguments.add_argument("-in2","--tumor_files", help="tumor matrix files.")

Required_Arguments.add_argument("-in3","--control_files", help="control matrix files.")

Required_Arguments.add_argument("-o","--output_dir", help="Directory where output files are located.")

Optional_Arguments = parser.add_argument_group('Optional_Arguments')

Optional_Arguments.add_argument("-t1","--threshold1", help="将在control中占比达到threshold1(范围0-100)的微生物从normal和tumor中删除.")

Optional_Arguments.add_argument("-t2","--threshold2", help="control中存在的微生物在normal和tumor中占比超过threshold2(范围0-100)，将该样本删除.")

Optional_Arguments.add_argument("-l","--list", help="特定的微生物列表。将列表中的微生物从normal和tumor中删除.")

args = parser.parse_args()

print(args)

normal_matrix,tumor_matrix,control_matrix = get_matrix(args.normal_files,args.tumor_files,args.control_files)

if not args.threshold1 is None:
    print("\nclean_by_threshold1")
    normal_matrix,tumor_matrix = clean_by_threshold1(normal_matrix,tumor_matrix,control_matrix,args.threshold1)

if not args.threshold2 is None:
    print("\nclean_by_threshold2")
    normal_matrix, tumor_matrix = clean_by_threshold2(normal_matrix, tumor_matrix, control_matrix, args.threshold2)

if not args.list is None:
    print("\nclean_by_list")
    normal_matrix,tumor_matrix = clean_by_list(normal_matrix,tumor_matrix,args.list.split(','))

#save
print("\nsave")
save(normal_matrix,args.normal_files.split('/')[-1],args.output_dir)
save(tumor_matrix,args.tumor_files.split('/')[-1],args.output_dir)
#save(normal_matrix,args.normal_files,args.output_dir)
