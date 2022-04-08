# Machine-Learning-Based Late Fusion on Multi-Omics and Multi-Scale Data for Non-Small-Cell Lung Cancer Diagnosis 

### *Francisco Carrillo-Perez, Juan Carlos Morales, Daniel Castillo-Secilla, Olivier Gevaert, Ignacio Rojas & Luis Javier Herrera*

Implementation of the Journal of Personalized Medicine paper [Machine-Learning-Based Late Fusion on Multi-Omics and Multi-Scale Data for Non-Small-Cell Lung Cancer Diagnosis](https://www.mdpi.com/2075-4426/12/4/601)

---
## Abstract

Differentiation between the various non-small-cell lung cancer subtypes is crucial for providing an effective treatment to the patient. For this purpose, machine learning techniques have been used in recent years over the available biological data from patients. However, in most cases this problem has been treated using a single-modality approach, not exploring the potential of the multi-scale and multi-omic nature of cancer data for the classification. In this work, we study the fusion of five multi-scale and multi-omic modalities (RNA-Seq, miRNA-Seq, whole-slide imaging, copy number variation, and DNA methylation) by using a late fusion strategy and machine learning techniques. We train an independent machine learning model for each modality and we explore the interactions and gains that can be obtained by fusing their outputs in an increasing manner, by using a novel optimization approach to compute the parameters of the late fusion. The final classification model, using all modalities, obtains an F1 score of 96.81±1.07, an AUC of 0.993±0.004, and an AUPRC of 0.980±0.016, improving those results that each independent model obtains and those presented in the literature for this problem. These obtained results show that leveraging the multi-scale and multi-omic nature of cancer data can enhance the performance of single-modality clinical decision support systems in personalized medicine, consequently improving the diagnosis of the patient.

---

## Implementation

Code can be found in the src folder:

- **[integration_late_fusion_all.ipynb]**: Code containing the late fusion of the different sources.
- **[plots-multiomics-paper.ipynb]**: Code for obtaining the plots on the manuscript.
- **[CNV/create_gene_matrix.R]**: Code for obtaining the gene matrix for the copy number variation data.
- **[CNV/create_mrmr_DEGs_CNV.ipynb]**: Code for obtaining the DEGs for the mRMR algorithm.
- **[CNV/preprocess_cnv.ipyn]**: Preprocessing the CNV data and training of the models.
- **[metDNA/create_mrmr_CpGs.ipynb]**: Obtaining differentiated CpGs.
- **[metDNA/get_methy_matrix.py]**: Obtaining the CpGs matrix.
- **[metDNA/get_train_CpGs.R]**: Obtaining the different CpGs for each training split.
- **[metDNA/preprocess_cpgs.ipynb]**: Code for training the models on DNA Methylation data.
- **[miRNA/miRNA_classification.ipynb]**: Code for training the models on miRNA data.
- **[miRNA/miRNA-create-dataset.py]**: Code for creating the dataset for the miRNA data.
- **[RNA/create_dataset-RNASeq.py]**: Code for creating the dataset for the RNA-Seq data.
- **[RNA/rna-seq-classification.ipynb]**: Code for training the models on RNA-Seq data.
- **[RNA/RNA-Seq-mRMR.R]**: Code for obtaining the mRMR genes.
- **[WSI/data_reader.py]**: Data reader for the WSI data
- **[WSI/dataset.py]**: Pytorch dataset for patches
- **[WSI/obtain_patches.py]**: Obtain the patches from the slide images.
- **[WSI/read_img.py]**: Reading the slide images
- **[WSI/train_pred.py]**: Functions to train the CNN model.
- **[WSI/utils.py]**: Utilities functions.
- **[WSI/wsi_train.py]**: Main file of train.
  
## Citation

If you find this research or code useful, please cite as follows:

```
Carrillo-Perez, F.; Morales, J.C.; Castillo-Secilla, D.; Gevaert, O.; Rojas, I.; Herrera, L.J. Machine-Learning-Based Late Fusion on Multi-Omics and Multi-Scale Data for Non-Small-Cell Lung Cancer Diagnosis. J. Pers. Med. 2022, 12, 601. https://doi.org/10.3390/jpm12040601 
```
```
@article{2022, title={Machine-Learning-Based Late Fusion on Multi-Omics and Multi-Scale Data for Non-Small-Cell Lung Cancer Diagnosis}, volume={12}, ISSN={2075-4426}, url={http://dx.doi.org/10.3390/jpm12040601}, DOI={10.3390/jpm12040601}, number={4}, journal={Journal of Personalized Medicine}, publisher={MDPI AG}, author={Carrillo-Perez, Francisco and Morales, Juan Carlos and Castillo-Secilla, Daniel and Gevaert, Olivier and Rojas, Ignacio and Herrera, Luis Javier}, year={2022}, month={Apr}, pages={601} }
```