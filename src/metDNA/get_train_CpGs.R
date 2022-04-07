library(KnowSeq)
library("readr")
library("data.table")
library(rhdf5)

setwd("~/Google Drive/Mi unidad/Research/miRNA-RNASeq-LC/DNA-Methylation")

all_cpgs <- fread('CpGs_450_matrix_nonans.csv')

for (i in seq(0,10)){
  cat(i)
  name <- paste('train_degs/CpGs_DE_train',i,'_p0-001_cov2.csv',sep='')
  train <- fread(name)
  
  train <- t(train)
  
  colnames(train) <- train[1,]
  train <- train[2:nrow(train),]
  
  labels_train <- train[,ncol(train)]
  train <- train[,1:ncol(train)-1]
  
  # Feature selection process with mRMR and RF
  mrmrRanking <-featureSelection(train,labels_train,colnames(train), mode = "mrmr")
  #mrmrDEGs <- expressionMatrixall[names(mrmrRanking[1:40]),]
  
  file_name = paste('mrmrCpGs/mrmrCpGs_LC_DNA_3classes_split', i, '.txt', sep='')
  write.table(names(mrmrRanking[1:40]), file_name, row.names = FALSE)
  
}