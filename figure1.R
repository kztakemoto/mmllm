# This R script is adapted from the supplementary code 
# provided in 'The Moral Machine Experiment',
# which can be accessed at https://goo.gl/JXRrBP.

library(ggplot2)
library(reshape2)
library(dplyr)
library(tidyr)
library(AER)
library(sandwich)
library(multiwayvcov)
library(data.table)

source("chatbot_MMFunctionsShared.R")

# Loading data as a data.table
# e.g., GPT-3.5
profiles <- fread(input="./data/shared_responses_gpt-3.5-turbo-0613.csv")
profiles <- PreprocessProfiles(profiles)

# Compute ACME values
Coeffs.main <- GetMainEffectSizes(profiles,T,9)
plotdata.main <- GetPlotData(Coeffs.main,T,9)

# Compute additional ACME values
Coeffs.util <- GetMainEffectSizes.Util(profiles)
plotdata.util <- GetPlotData.Util(Coeffs.util)

## plot and save
PlotAndSave(plotdata.main, T, "MainChangePr", plotdata.util)

