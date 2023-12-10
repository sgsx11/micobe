# micobe
## 01-nromalization

```shell
 python ./01-normalization.py `
 -in1 ./data/pathseq_files/Control/ `
 -in2 ../step1-pre_process/data/16s_rna_flag/Control/ `
 -o ./results/pathseq_files_normalized/Control/ `
 -m ./results/matrix/ `
 -st Control
```

## 02-clean

```shell
python ./02-clean.py `
-in1 ./results/matrix/Normal_genus_matrix.txt `
-in2 ./results/matrix/Tumor_genus_matrix.txt `
-in3 ./results/matrix/Control_genus_matrix.txt `
-o ./results/clean/ `
-t1 10
-t2 5
-l Abiotrophia,Acaricomes,Acetivibrio
```
```
Namespace(normal_files='./results/matrix/Normal_genus_matrix.txt', tumor_files='./results/matrix/Tumor_genus_matrix.txt', control_files='./results/matrix/Control_ge
clean_by_threshold1
The size of the normal_matrix has been changed from (771, 16) to (767, 16).
The following microorganisms have been removed from the normal_matrix:['Streptococcus', 'Rothia', 'Paracoccus', 'Bradyrhizobium']
The size of the tumor_matrix has been changed from (749, 16) to (745, 16).
The following microorganisms have been removed from the tumor_matrix:['Streptococcus', 'Rothia', 'Paracoccus', 'Bradyrhizobium']

clean_by_threshold2
The size of the normal_matrix has been changed from (767, 16) to (767, 15).
The following samples have been removed from the normal_matrix:['P223N_rna']
The size of the tumor_matrix has been changed from (745, 16) to (745, 13).
The following samples have been removed from the tumor_matrix:['P207T_rna', 'P326T_rna', 'P394T_rna']

clean_by_list
The size of the normal_matrix has been changed from (767, 15) to (764, 15).
The following microorganisms have been removed from the normal_matrix:['Abiotrophia', 'Acaricomes', 'Acetivibrio']
The size of the tumor_matrix has been changed from (745, 13) to (742, 13).
The following microorganisms have been removed from the tumor_matrix:['Abiotrophia', 'Acaricomes', 'Acetivibrio']
```