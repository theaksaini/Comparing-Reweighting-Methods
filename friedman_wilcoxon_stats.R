library(dplyr)
library(purrr)

rm(list = ls())
cat("\014")

setwd('~/Desktop/Comparing-Reweighting-Methods-arxiv/Results')
#testing <- read.csv('hv_acc_dpd/hv_test.csv', header = TRUE, stringsAsFactors = FALSE)
#testing <- read.csv('hv_acc_sfn/hv_test.csv', header = TRUE, stringsAsFactors = FALSE)
#testing <- read.csv('hv_roc_dpd/hv_test.csv', header = TRUE, stringsAsFactors = FALSE)
testing <- read.csv('hv_roc_sfn/hv_test.csv', header = TRUE, stringsAsFactors = FALSE)

testing$exp <- gsub('Evolved Weights', 'Evolved', testing$ex)
testing$exp <- gsub('Deterministic Weights', 'Deterministic', testing$ex)
testing$exp <- gsub('Equal Weights', 'Equal', testing$ex)

# List of datasets
dataset_list <- c('heart_disease', 'student_math', 'student_por', 'creditg', 'titanic', 'us_crime', 'compas_violent', 'nlsy', 'compas', 'pmad_rus_phq', 'pmad_rus_epds')

for (d in dataset_list) {
  
  data <- filter(testing, dataset == d)
  
  # Using Friedman Test instead of Kruskal-Wallis
  pf <- friedman.test(hv ~ exp | rep, data = data)
  
  testing$exp <- factor(testing$exp, levels=c('Deterministic','Equal', 'Evolved'))
  
  pw <- pairwise.wilcox.test(x = data$hv, g = data$exp, p.adjust.method = "bonferroni",
                    paired = TRUE, conf.int = FALSE, alternative = 'g')
  
  # Build one line and cat it
  line <- sprintf("%s\t%.6g\t%.6g\t%.6g",
                  gsub("_"," ", d),
                  pf$p.value,
                  pw$p.value["Evolved","Deterministic"],
                  pw$p.value["Evolved","Equal"])
  cat(line, "\n")
}

