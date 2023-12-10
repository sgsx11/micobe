# micobe
## step3-select_high_abundance_and_characteristics_micorbiome
### 01-abundance
```shell
python ./01-abundance.py `
-nm ./data/Normal_genus_matrix_cleaned.txt `
-tm ./data/Tumor_genus_matrix_cleaned.txt `
-o ./results/abundance/ `
-t 0.5 `
-k Bacteria
```
```shell
0         N      Prevotella  13.481003
1         N     Veillonella   4.939090
2         N   Fusobacterium   2.981523
3         N       Neisseria   2.300763
4         N     Haemophilus   2.791491
..      ...             ...        ...
67        T   Mycobacterium   0.463137
68        T  Granulicatella   0.668897
69        T   Campylobacter   0.641153
70        T  Paraprevotella   0.482820
71        T           Other  37.241925

[72 rows x 3 columns]

```


### 02-characteristics_micorbiome.py
```shell
python ./02-characteristics_micorbiome.py `
-nm ./data/Normal_genus_matrix_cleaned.txt `
-tm ./data/Tumor_genus_matrix_cleaned.txt `
-o ./results/characteristics_micorbiome/ `
-n 10 `
-k Bacteria
```
```shell
Namespace(normal_matrix='./data/Normal_genus_matrix_cleaned.txt', tumor_matrix='./data/Tumor_genus_matrix_cleaned.txt', nums='10', output_dir='./results/characteris
tics_micorbiome/', kingdom='Bacteria')

Samples paired as N/T.
['P156N_rna', 'P160N_rna', 'P180N_rna', 'P193N_rna', 'P198N_rna', 'P229N_rna', 'P268N_rna', 'P270N_rna', 'P303N_rna', 'P368N_rna']
['P156T_rna', 'P160T_rna', 'P180T_rna', 'P193T_rna', 'P198T_rna', 'P229T_rna', 'P268T_rna', 'P270T_rna', 'P303T_rna', 'P368T_rna']

Characteristic_bacteria: ['Prevotella', 'Fusobacterium', 'Veillonella', 'Neisseria', 'Haemophilus', 'Gemella', 'Porphyromonas', 'Sphingobacterium', 'Moraxella', 'Ac
inetobacter']

ratio_matrix
               name       P156      P160      P180       P193      P198      P229       P268      P270      P303       P368
0        Prevotella   6.160950  1.087030  0.379706   5.354326  0.835737  1.506701   0.578588  2.445876  0.399993   0.075386
1     Fusobacterium   0.013548  0.690933  1.085779   2.244264  1.805566  1.201844   0.543800  9.672227  1.088812  27.597004
2       Veillonella   0.000000  1.057606  0.453420  33.729323  3.041625  1.090604   0.298058  8.259587  3.058526  11.434202
3         Neisseria   0.000000  0.905492  0.882298   3.800990  0.797509  6.310193   3.758501  3.329545  2.341980  34.699791
4       Haemophilus   0.796541  1.478308  1.739129   2.231366  2.133965  3.153393   1.277571  4.548381  1.247488   2.481406
5           Gemella   0.001249  1.254441  0.755695   1.992999  1.248007  1.832294   0.510085  1.474721  0.889120        inf
6     Porphyromonas   1.606586  0.992234  0.687701   1.677378  0.839875  4.268358   1.044543  1.642441  2.461946   0.192865
7  Sphingobacterium  13.598701  2.358909  6.700933   0.649066  0.228801  0.664031  23.441014  1.814501  0.061910   1.388994
8         Moraxella   0.000000  0.691290  0.908266   0.316021  0.832005  1.147494   3.406437  0.432526  0.304055        inf
9     Acinetobacter   0.002621  2.046292  1.346317   1.267563  1.212257  0.725553   3.623032  4.721297  0.506602        inf

labels: ['Neisseria', 'Veillonella', 'Haemophilus', 'Sphingobacterium', 'Fusobacterium', 'Porphyromonas', 'Prevotella', 'Acinetobacter', 'Moraxella', 'Gemella']    

data: [[-0.14322656038931017, -0.18066193244461398, 1.9263752176287852, -0.3264270964474375, 2.657684105335375, 1.9101574161797634, 1.7353250563449105, 1.2277287562
792432, 5.116855050387721], [0.08080201832054176, -1.1410799502777478, 5.075931477571701, 1.604842205256092, 0.12512685071189592, -1.7463367824101057, 3.04606971777
85514, 1.6128367409925979, 3.515283784170643], [-0.32817992345357294, 0.563947105284282, 0.7983646850587723, 1.1579273861549257, 1.093536848859574, 1.65690497060699
5, 0.35340356222190467, 2.1853532061350958, 0.3190254831849053, 1.3111577144685975], [3.7653968909645084, 1.2381197796364372, 2.7443620617361533, -0.623561987414685

samples: [['P160', 'P180', 'P193', 'P198', 'P229', 'P268', 'P270', 'P303', 'P368'], ['P160', 'P180', 'P193', 'P198', 'P229', 'P268', 'P270', 'P303', 'P368'], ['P156
', 'P160', 'P180', 'P193', 'P198', 'P229', 'P268', 'P270', 'P303', 'P368'], ['P156', 'P160', 'P180', 'P193', 'P198', 'P229', 'P268', 'P270', 'P303', 'P368'], ['P156
', 'P160', 'P180', 'P193', 'P198', 'P229', 'P268', 'P270', 'P303', 'P368'], ['P156', 'P160', 'P180', 'P193', 'P198', 'P229', 'P268', 'P270', 'P303', 'P368'], ['P156
', 'P160', 'P180', 'P193', 'P198', 'P229', 'P268', 'P270', 'P303', 'P368'], ['P156', 'P160', 'P180', 'P193', 'P198', 'P229', 'P268', 'P270', 'P303'], ['P160', 'P180
', 'P193', 'P198', 'P229', 'P268', 'P270', 'P303'], ['P156', 'P160', 'P180', 'P193', 'P198', 'P229', 'P268', 'P270', 'P303']]

labels.pkl,data.pkl and samples.pkl has been saved in ./results/characteristics_micorbiome/
```
