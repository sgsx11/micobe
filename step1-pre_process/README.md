# micobe
## step1-pre_process

### Alignment with Grch38 and T2T reference genomes, discard reads that can match the human genome
#### Alignment


#### Discard reads


### How to get flagstat files
#### Commands:
```shell
samtools flagstat -@ 10 P156N_rna_hg38_unmap_t2t_align.bam
```
#### output:
```shell
68210 + 0 in total (QC-passed reads + QC-failed reads)
0 + 0 secondary
0 + 0 supplementary
0 + 0 duplicates
0 + 0 mapped (0.00% : N/A)
68210 + 0 paired in sequencing
34105 + 0 read1
34105 + 0 read2
0 + 0 properly paired (0.00% : N/A)
0 + 0 with itself and mate mapped
0 + 0 singletons (0.00% : N/A)
0 + 0 with mate mapped to a different chr
0 + 0 with mate mapped to a different chr (mapQ>=5)
```


### Gene expression in the host





### Genetic mutations in the host



### Tumor mutation burden(TMB)
Here is an example code using maftools to calculate tumor mutation burden (TMB):
```R
# Load required packages
library(maftools)

# Load MAF file
mafFile <- "path_to_maf_file.maf"
maf <- read.maf(mafFile)

# Calculate TMB
result <- tmb(maf)
```
In the code above, make sure to replace "path_to_maf_file.maf" with the actual path to your MAF file. The tmb function calculates TMB based on the specified mutation types and filtering criteria. 
Note that you may need to install the maftools package using install.packages("maftools") before running the code.

Below is an example of the result obtained from the tmb function:

| Tumor_Sample_Barcode | total | total_perMB | total_perMB_log |
| :-----: |:-------:|:-----:|:--------:|
|P394T | 12029 | 240.58 | 2.38125952054885 |


### Tumor microenvironment(TME)
To perform deconvolution using CIBERSORT, you need to follow these steps:

Install the CIBERSORT package: First, you need to download and install the CIBERSORT package from the CIBERSORT website (https://cibersort.stanford.edu/). Follow the instructions provided on the website to install the package.

Prepare input data: You need to prepare your input data in a specific format for CIBERSORT. The input data should be a matrix where each row represents a gene and each column represents a sample. Make sure to normalize and preprocess your data appropriately before running CIBERSORT.

Run CIBERSORT: Once you have installed the CIBERSORT package and prepared your input data, you can run CIBERSORT using the following command in R:

```shell
CIBERSORT(input_data, signature_matrix, output_file)
```

input_data is your input gene expression matrix.
signature_matrix is the signature matrix provided by CIBERSORT, which contains the gene expression profiles of the cell types you want to deconvolve.
output_file is the path where you want to save the deconvolution results.
Interpret the results: The output of CIBERSORT will be a matrix with the estimated proportions of each cell type in each sample. You can use these results for downstream analysis or visualization.
Please note that the CIBERSORT algorithm assumes that the input gene expression profiles accurately represent the mixture of cell types in the samples. It is important to validate and interpret the results carefully based on the context and quality of your data.