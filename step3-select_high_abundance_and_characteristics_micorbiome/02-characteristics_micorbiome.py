import os
import pandas as pd
import argparse
import numpy as np
import pickle

def save(labels,data,samples,output_dir):
    print("\nlabels:",labels)
    print("\ndata:", data)
    print("\nsamples:", samples)
    with open(output_dir + "/labels.pkl", "wb") as file:
        pickle.dump(labels, file)
    with open(output_dir + "/data.pkl", "wb") as file:
        pickle.dump(data, file)
    with open(output_dir + "/samples.pkl", "wb") as file:
        pickle.dump(samples, file)
    print("\nlabels.pkl,data.pkl and samples.pkl has been saved in {}".format(output_dir))

def get_plot_data(ratio_matrix):
    # 对ratio_matrix的数据进行筛选，去掉0或者inf的数据，其余数据转成list，便于后续的绘图
    names = list(ratio_matrix['name'])  # 提取特征菌名称
    Mic_names = []  # 存储[特征菌名称,丰度均值]的元素对
    Mic_dict = {}  # key: 特征菌名称 values:[丰度比值,样本名称]
    cols = ratio_matrix.columns[1:]
    for name in names:  # 遍历特征菌列表
        data = list(ratio_matrix[ratio_matrix['name'] == name].iloc[0].values[1:])  # data为该特征菌在各样本中的丰度列表
        abundance_ratio = []  # abundance_ratio为筛选后的data
        sample_name = []  # sample_name为筛选后的样本名称
        for d in data:
            if d != 0.0 and d != float("inf"):
                abundance_ratio.append(np.log2(d))  # 取对数
                sample_name.append(cols[data.index(d)])
        if len(abundance_ratio) > 0:
            mean = np.mean(abundance_ratio)
            Mic_names.append([name, mean])
            # print(mean)
            Mic_dict[name] = [abundance_ratio, sample_name]
    Mic_names = sorted(Mic_names, key=(lambda x: x[1]), reverse=True)  # 按照丰度均值排序
    # 做箱型图的输入数据预处理
    data = []
    labels = []
    samples = []
    for Mic_name in Mic_names:
        data.append(Mic_dict[Mic_name[0]][0])  # 取出abundance_ratio
        samples.append(Mic_dict[Mic_name[0]][1])
        labels.append(Mic_name[0])
    return labels,data,samples


def CB(normal_matrix,tumor_matrix,nums,output_dir,kingdom):
    matrix_N = pd.read_csv(normal_matrix, sep='\t')
    matrix_T = pd.read_csv(tumor_matrix, sep='\t')
    matrix_N = matrix_N[matrix_N['kingdom'] == kingdom]
    matrix_T = matrix_T[matrix_T['kingdom'] == kingdom]
    matrix_N = matrix_N.drop(columns=['type', 'kingdom'])
    matrix_T = matrix_T.drop(columns=['type', 'kingdom'])
    col_names_N = list(matrix_N.columns)
    col_names_T = list(matrix_T.columns)
    #获得N/T成对的样本
    names_N = []
    names_T = []
    for name in col_names_T:
        N_sample = name.split("_")[0][:-1] + "N_" + '_'.join(name.split("_")[1:])
        if N_sample in col_names_N:
            names_T.append(name)
            names_N.append(N_sample)
    print("\nSamples paired as N/T.")
    print(names_N)
    print(names_T)
    # 合并N_T矩阵
    matrix = pd.merge(matrix_N, matrix_T, on="name", how='outer')
    matrix = matrix.fillna(0)
    # 根据所有T样本中微生物丰度的均值进行排序，取前nums个作为特征菌
    T_matrix = matrix[col_names_T]
    ##删除name列外的数据列中全为0的行
    new_T_matrix = T_matrix[~(T_matrix.iloc[:, 1:] == 0).all(axis=1)]  # df.iloc[:,1:] 除name列外的所有列
    # 求微生物丰度均值
    new_T_matrix_copy = new_T_matrix.copy()
    new_T_matrix_copy['mean'] = new_T_matrix.iloc[:, 1:].mean(axis=1)
    new_T_matrix_copy = new_T_matrix_copy.sort_values(by="mean", ascending=False)
    # 求丰度均值前十的微生物
    Characteristic_bacteria = list(new_T_matrix_copy[:nums]['name'])
    print("\nCharacteristic_bacteria:",Characteristic_bacteria)
    # 从matrix中取出nums个特征菌对应的矩阵
    df = matrix[matrix['name'] == Characteristic_bacteria[0]]
    for bacteria in Characteristic_bacteria[1:]:
        df = pd.concat([df, matrix[matrix['name'] == bacteria]], ignore_index=True)
    cb_matrix = df
    # 求取特征菌在N/T对中的丰度比值矩阵
    new_col_names = ['name']
    for i in range(len(names_N)):
        new_col_name = names_N[i].split('_')[0][:-1]
        new_col_names.append(new_col_name)
        cb_matrix[new_col_name] = cb_matrix[names_T[i]] / cb_matrix[names_N[i]]
    ratio_matrix = cb_matrix[new_col_names]
    ratio_matrix = ratio_matrix.fillna(0)
    ratio_matrix = ratio_matrix[~(ratio_matrix.iloc[:, 1:] == 0).all(axis=1)]  # df.iloc[:,1:] 除name列外的所有列
    print("\nratio_matrix")
    print(ratio_matrix)
    #获得用于后续绘图的数据并保存
    labels,data,samples = get_plot_data(ratio_matrix)
    save(labels,data,samples,output_dir)

#参数
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="Differences in microbial abundance between normal and tumor samples.\n")

Required_Arguments = parser.add_argument_group('Required_Arguments')

Required_Arguments.add_argument("-nm","--normal_matrix", help="cleaned normal sample expression matrix.")

Required_Arguments.add_argument("-tm","--tumor_matrix", help="cleaned tumor sample expression matrix.")

Required_Arguments.add_argument("-n","--nums", help="Number of characteristic bacteria.")

Required_Arguments.add_argument("-o","--output_dir", help="Directory where output files are located.")

Required_Arguments.add_argument("-k","--kingdom", help="The kingdom types include bacteria, archaea, fungi , Eukaryota , etc.")

args = parser.parse_args()

print(args)

CB(args.normal_matrix,args.tumor_matrix,int(args.nums),args.output_dir,args.kingdom)