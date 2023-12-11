import os
import pandas as pd
import argparse
import json
from sklearn.cluster import KMeans
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.decomposition import PCA

def save_json(save_dict,output_dir):
    json_str = json.dumps(save_dict)
    if not os.path.exists(output_dir+'/method2/'):
        os.mkdir(output_dir+'/method2/')
    with open(output_dir+'/method2/' + "classification_results.json", "w") as json_file:
        json.dump(json_str, json_file)
    print("classification_results has already been saved in {}".format(output_dir+'/method2/' + "classification_results.json"))

def cluster(matrix,output_dir,n_clusters=3):
    #使用pca对特征微生物的矩阵进行降维
    #将matrix转化为np.array
    samples = matrix.columns.tolist()
    x = []
    for sample in samples:
        value = matrix[sample].values.tolist()
        x.append(value)
    x = np.array(x)
    print("\noriginal data:",x)
    pca = PCA(n_components=2) #将原始数据降成二维
    newX = pca.fit_transform(x)
    print("\nPCA dimensionality reduction data:", newX)
    #使用kmeans对降维后的数据进行聚类
    kmeans = KMeans(n_clusters=n_clusters,random_state=0)  # 假设您希望将数据聚为3个簇
    kmeans.fit(newX)
    labels = kmeans.labels_  # 获取每个样本的聚类标签
    #生成分类dict，转成json保存
    dict = {}
    for i in range(len(labels)):
        label = int(labels[i])
        sample = samples[i]
        if label not in dict.keys():
            dict[label] = []
        dict[label].append(sample)
    print("KMeans clustering results:",dict)
    save_json(dict,output_dir)


def clssification(cbm,output_dir,n_clusters):
    cb_matrix = pd.read_csv(cbm, sep='\t')
    #分出Tumor样本和normal样本
    columns = cb_matrix.columns.tolist()[1:]
    normal_sample = []
    tumor_sample = []
    for col in columns:
        if col.split("_")[0][-1] == "N":
            normal_sample.append(col)
        else:
            tumor_sample.append(col)
    print("normal_sample:",normal_sample)
    print("tumor_sample:",tumor_sample)
    matrix_t = cb_matrix[['name']+tumor_sample]
    matrix_t = matrix_t
    matrix_t.set_index('name', inplace=True)
    print("\nmatrix_t")
    print(matrix_t)
    cluster(matrix_t,output_dir,n_clusters)



#参数
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="Classify samples based on the clustering results of the characteristic bacterial abundance matrix.\n")

Required_Arguments = parser.add_argument_group('Required_Arguments')

Required_Arguments.add_argument("-cbm","--characteristic_bacteria_matrix", help="characteristic_bacteria_matrix.")

Required_Arguments.add_argument("-o","--output_dir", help="Directory where output files are located.")

Optional_Arguments = parser.add_argument_group('Optional_Arguments')

Optional_Arguments.add_argument("-n","--n_clusters", help="Number of categories for clustering samples. Default 3")

args = parser.parse_args()

print(args)


clssification(args.characteristic_bacteria_matrix,args.output_dir,int(args.n_clusters))



