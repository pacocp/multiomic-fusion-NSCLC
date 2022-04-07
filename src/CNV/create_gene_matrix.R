library(GenomicRanges)

path_files <- read.csv('files_path.csv')

# Initializes the progress bar
pb <- txtProgressBar(min = 1,      # Minimum value of the progress bar
                     max = nrow(path_files), # Maximum value of the progress bar
                     style = 3,    # Progress bar style (also available style = 1 and style = 2)
                     width = 50,   # Progress bar width. Defaults to getOption("width")
                     char = "=")   # Character used to create the bar

# for-loop over rows
for(i in 1:nrow(path_files)) { 
  row = path_files[i, ]
  copy.number.file <- row$Copy.Number
  gene.level.file <- row$Gene.Level
  
  df1 <- read.csv(gene.level.file, sep='\t')
  
  # Gene range template 
  Genes <- GRanges(df1$chromosome,
                   IRanges(df1$start, df1$end), genes=df1$gene_id)
  
  snps0 <- read.table(copy.number.file, head=TRUE)

  # the chromosomes names need to match, so I need to change things in file
  snps0['Chromosome'] <- lapply(snps0['Chromosome'], function(x) paste('chr',x,sep=""))
  # Here we read the segments of the sample ID and find the overlaps
  snps  <- GRanges(snps0$Chromosome, IRanges(snps0$Start, snps0$End),
                   Segment_Mean=snps0$Segment_Mean)
  # Overlaps
  olaps <- findOverlaps(query=snps, subject=Genes)
  
  # Dataframe with the overlaps
  olaps2 <- as.data.frame(olaps)
  df1$Row <- rownames(df1)
  NewDF <- merge(df1,olaps2,by.x="Row",by.y="subjectHits",all=T,sort=F)
  snps0$Row <- rownames(snps0)
  NewDF2 <- merge(NewDF,snps0,by.x="queryHits",by.y="Row",all.x=T,sort=F)[,c(-1,-2)]

  save_dir <- paste('cnv-segments/',row$Sample.IDs,"/gene_level_combination.csv",sep = "")

  write.csv(NewDF2,file=save_dir, row.names=FALSE)
  # Sets the progress bar to the current state
  setTxtProgressBar(pb, i)
}

close(pb) # Close the connection
