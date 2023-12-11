# micobe
## step4-classification
### 01-method1.py
```shell
 python ./01-method1.py `
 -tm ./data/Tumor_genus_matrix_cleaned.txt `
 -o ./results/ `
 -k Bacteria `
 -cb Prevotella
```
```shell
low_sample: ['P368T', 'P229T', 'P160T']
high_sample: ['P223T', 'P198T', 'P156T']
classification_results has already been saved in ./results//method1/classification_results.json
```

### 02-method2.py
```shell
 python ./02-method2.py `
 -cbm ./data/cb_matrix.txt `
 -o ./results/ `
 -n 5
```