# Overview

Micobe is a tumor microbiome analysis pipeline that consists of the following seven parts: 
## Step 1: pre-process
By aligning against the Grch38 and T2T reference genomes, the reads that can be matched to the human genome are discarded. Then, the reads are aligned against the microbial community genomes provided by Pathseq to obtain the Pathseq result file.

To achieve this, it is necessary to upload the reference database, the mapping script, and configure the corresponding parameters for selection. In addition to the microbiome, host gene expression and mutations are also generated at this step for use in Step 5.

[Detailed operation](https://github.com/sgsx11/micobe/blob/main/step1-pre_process/README.md)
## Step 2: clean and normalization
The input file is the result file output by pathseq, which is first normalized and then cleaned.
The rule is: 
1) The inputted pathseq result file has three categories, namely Tumor, Normal, and Control; 
2) Remove microorganisms with a proportion above the threshold in Control from Tumor and Normal; 
3) If the proportion of microorganisms detected in the control in Tumor and Normal exceeds the threshold, the entire sample will be judged as severely contaminated and discarded; 
4) You can also provide a microbial list to filter specific microorganisms.
[Detailed operation](https://github.com/sgsx11/micobe/blob/main/step2-clean_and_normalization/README.md)
## Step 3: select high abundance and characteristics microbiome 
Set a high abundance threshold, select microorganisms whose abundance exceeds the threshold in T, and compare them with the abundance detected in N. Set a threshold (ratio), and determine microorganisms that exceed the threshold as characteristic microorganisms.
[Detailed operation](https://github.com/sgsx11/micobe/blob/main/step3-select_high_abundance_and_characteristics_micorbiome/README.md)
## Step 4: classification
Option 1: Based on the characteristic microorganisms, select specific characteristic microorganisms or combinations of characteristic microorganisms (such as ratios), classify the samples, set thresholds, and generate a matrix of microbial abundance.
Option 2: Using the characteristic microorganisms of step 3, perform cluster analysis directly and divide T into several categories.
[Detailed operation](https://github.com/sgsx11/micobe/blob/main/step4-classification/README.md)
## Step 5: TMB (Tumor Mutational Burden), TME (Tumor Microenvironment), and microbe
Option 1: Analyze the corresponding samples selected from Step 4 Option 1
Option 2: Analyze the corresponding samples selected from Step 4 Option 2
Option 1 evaluates the association between microorganisms and tumor progression, which means that an increase in microbial abundance leads to an increase in malignancy and is associated with T staging. Samples with high microbial abundance in T tend to have lower corresponding T stages.
Option 2 evaluates the heterogeneity of tumors, which means that based on the composition of microorganisms, patients can be divided into different subtypes, and samples from different subtypes can be compared with N.
Simply put, for T samples, Scheme 1 is binary classification and Scheme 2 is multi classification. Option one is a comparison between the two categories, while option two is a comparison with N separately.
TMB refers to simply counting the differences in TMB between different types of samples. TME is done using IBOR software.
[Detailed operation](https://github.com/sgsx11/micobe/blob/main/step5-TMB_TME_and_microbe/README.md)
## Step 6: prediction
Select characteristic bacteria as features, construct a model, and predict the classification of samples.
[Detailed operation](https://github.com/sgsx11/micobe/blob/main/step6-prediction/README.md)
## Step 7: plot
Concentrate on drawing images of the previous steps
[Detailed operation](https://github.com/sgsx11/micobe/blob/main/step7-plot/README.md)