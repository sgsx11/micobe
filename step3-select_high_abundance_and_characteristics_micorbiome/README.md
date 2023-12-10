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
