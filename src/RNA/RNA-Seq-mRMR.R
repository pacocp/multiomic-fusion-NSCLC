suppressMessages(library(KnowSeq))
library(caret)

# Merging in one matrix all the count files indicated inside the CSV file
countsInformation <- countsToMatrix("LUAD-LUSC-dataset-other.csv", extension = '')

data <- read.csv('LUAD-LUSC-dataset.csv')
case_ids <- data$Run

# Exporting to independent variables the counts matrix and the labels

countsMatrix <- countsInformation$countsMatrix

labels <- countsInformation$labels

# Downloading human annotation
myAnnotation <- getGenesAnnotation(rownames(countsMatrix))

# Calculating gene expression values matrix using the counts matrix

expressionMatrix <- calculateGeneExpressionValues(countsMatrix,myAnnotation,
                                                  genesNames = TRUE)

expressionMatrix <- t(expressionMatrix)


# training
svaMod <- batchEffectRemoval(expressionMatrix, labels, method = "sva")

DEGsInformation <- DEGsExtraction(expressionMatrix, labels, lfc = 2,
                                       pvalue = 0.01, number = Inf, 
                                       svaCorrection = FALSE,
                                       cov = 2)

topTable <- DEGsInformation$Table
DEGsMatrix <- DEGsInformation$DEGsMatrix
DEGsMatrixML <- DEGsMatrix
#DEGsMatrixML <- DEGsMatrixML[, 1:dim(DEGsMatrixML)[2]-1]

DEGsMatrixML <- t(DEGsMatrixML)
# Feature selection process with mRMR and RF
mrmrRanking <-featureSelection(DEGsMatrixML,labels,colnames(DEGsMatrixML), mode = "mrmr")

save_df <- as.data.frame(DEGsMatrixML, row.names = case_ids) 
reorder_df <- save_df[, mrmrRanking]
reorder_df$Labels <- labels
write.csv(reorder_df, 'mRMR-LC-3classes-RNA.csv', row.names=TRUE)
