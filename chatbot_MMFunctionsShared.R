# This R script is adapted from the supplementary code 
# provided in 'The Moral Machine Experiment',
# which can be accessed at https://goo.gl/JXRrBP.

# Set up
library(tidyverse)
library(reshape2)
library(AER)
library(sandwich)
library(multiwayvcov)
library(data.table)
library(hrbrthemes)
library(extrafont)
# font_import()
# y
fonts()
#loadfonts()
library(ggthemes)

PreprocessProfiles <- function(profiles){
  profiles[,Saved := as.numeric(Saved)]
  profiles[,ScenarioType := as.factor(ScenarioType)]
  profiles[,AttributeLevel := factor(AttributeLevel, 
                                    levels=c("Rand",
                                             "Male","Female",
                                             "Fat","Fit",
                                             "Low","High",
                                             "Old","Young",
                                             "Less","More",
                                             "Pets","Hoomans"))]
  profiles[,Barrier := factor(Barrier, levels=c(1,0))]
  profiles[,CrossingSignal := factor(CrossingSignal, levels=c(0,2,1))]
  profiles[,ScenarioType := as.factor(ScenarioType)]
  profiles[,ScenarioTypeStrict := as.factor(ScenarioTypeStrict)]
  return(profiles)
}



calcWeightsActual <- function(Tr, X){
  T10 <- ifelse(Tr==levels(factor(Tr))[2],1,0)
  d <- as.numeric(ave(X, X, T10, FUN = length))
  w <- max(d)/d
  return(w)
}

calcWeightsTheoretical <- function(profiles){
  p <- apply(profiles,1,CalcTheoreticalInt)
  return(1/p)
}

CalcTheoreticalInt <- function(X){
  if (X["Intervention"]==0){
    if (X["Barrier"]==0){
      if (X["PedPed"] == 1) p <- 0.48
      else p <- 0.32
      
      if (X["CrossingSignal"]==0) p <- p*0.48
      else if (X["CrossingSignal"]==1) p <- p*0.2
      else p <- p * 0.32
    }
    else p <- 0.2
  }
  else {
    if (X["Barrier"]==0){
      if (X["PedPed"] == 1) {
        p <- 0.48
        if (X["CrossingSignal"]==0) p <- p*0.48
        else if (X["CrossingSignal"]==1) p <- p*0.32
        else p <- p * 0.2
      }
      else {
        p <- 0.2
        if (X["CrossingSignal"]==0) p <- p*0.48
        else if (X["CrossingSignal"]==1) p <- p*0.2
        else p <- p * 0.32
      }
    }
    else p <- 0.32
  }
  return(p)
}


########################################
############ Main Effects ##############
########################################
# Main effect sizes
GetMainEffectSizes <- function(profiles,savedata,r){
  Coeffs <- matrix(NA,r,2)
  AttLevels <- levels(profiles$AttributeLevel)
  lev <- levels(profiles$ScenarioType)
  if (levels(profiles$ScenarioType)[1]=="") lev <- levels(profiles$ScenarioType)[2:8]
  #lev <- lev[c(3,2,4,1,6,5)]
  lev <- c("Gender", "Fitness", "Social Value", "Age", "Utilitarian", "Species")
  #gender fitness social age uti spec
  # Six factors (gender, fitness, Social Status, age, utilitarianism, age, and species)
  
  # For intervention
  profiles$BC.weights <- calcWeightsTheoretical(profiles)
  lm.Int <- lm(Saved ~as.factor(Intervention), data=profiles, weights = BC.weights)
  summary.lm.Int <- summary(lm.Int)
  Coeffs[1,1] <- lm.Int$coefficients[[2]]
  Coeffs[1,2] <- summary.lm.Int$coefficients[2, "Std. Error"]
  
  # For relationship to vehicle 
  ## Consider only 'no legality' (CrossingSignal==0) and 'passengers vs. pedestrians' (PedPed==0)
  profile.Relation <- profiles[which(profiles$CrossingSignal==0 & profiles$PedPed==0),]
  profile.Relation$BC.weights <- calcWeightsTheoretical(profile.Relation)
  lm.Rel <- lm(Saved ~as.factor(Barrier), data=profile.Relation, weights = BC.weights)
  summary.lm.Rel <- summary(lm.Rel)
  Coeffs[2,1] <- lm.Rel$coefficients[[2]]
  Coeffs[2,2] <- summary.lm.Rel$coefficients[2, "Std. Error"]
  
  # Legality 
  ## Exclude 'no legality' (CrossingSignal!=0) and consider only 'pedestrians vs. pedestrians' (PedPed==1)
  profile.Legality <- profiles[which(profiles$CrossingSignal!=0 & profiles$PedPed==1),]
  profile.Legality$CrossingSignal <- factor(profile.Legality$CrossingSignal, levels=levels(profiles$CrossingSignal)[2:3])
  profile.Legality$BC.weights <- calcWeightsTheoretical(profile.Legality)
  lm.Leg <- lm(Saved ~as.factor(CrossingSignal), data=profile.Legality, weights = BC.weights)
  summary.lm.Leg <- summary(lm.Leg)
  Coeffs[3,1] <- lm.Leg$coefficients[[2]]
  Coeffs[3,2] <- summary.lm.Leg$coefficients[2, "Std. Error"]
  
  # Six factors (gender, fitness, Social Status, age, utilitarianism, age, and species)
  ## Extract data subsets and run regression for each
  for(i in 1:6){
    Temp <- profiles[which(profiles$ScenarioType==lev[i] & profiles$ScenarioTypeStrict==lev[i]),]
    Temp$AttributeLevel <- factor(Temp$AttributeLevel, levels=AttLevels[(i*2):(i*2+1)])
    Temp$BC.weights <- calcWeightsTheoretical(Temp)    
    lm.Temp <- lm(Saved ~ as.factor(AttributeLevel), data=Temp, weights = BC.weights)
    summary.lm.Temp <- summary(lm.Temp)
    #print(summary.lm.Temp)
    Coeffs[i+3,1] <- lm.Temp$coefficients[[2]]
    Coeffs[i+3,2] <- summary.lm.Temp$coefficients[2, "Std. Error"]
    
    # Save to a data frame
    if(savedata){
      var.name <- paste("profile",gsub(" ","",lev[i]),sep=".")
      assign(var.name,Temp)
    }
  }
  return(Coeffs)
}

# Prepare plotted dataset
GetPlotData <- function(Coeffs,isMainFig,r){
  # Convert to dataframe and add labels
  plotdata <- as.data.frame(Coeffs)
  colnames(plotdata)=c("Estimates","se")
  plotdata$Label <- c("Preference for action -> \n Preference for inaction",
                      "Sparing Passengers -> \n Sparing Pedestrians",
                      "Sparing the Unlawful -> \n Sparing the Lawful",
                      "Sparing Males -> \n Sparing Females",
                      "Sparing the Large -> \n Sparing the Fit",
                      "Sparing Lower Status -> \n Sparing Higher Status",
                      "Sparing the Elderly -> \n Sparing the Young",
                      "Sparing Fewer Characters -> \n Sparing More Characters",
                      "Sparing Pets -> \n Sparing Humans") 
  if(isMainFig)
    plotdata$Label <- c("Intervention",
                        "Relation to AV",
                        "Law",
                        "Gender",
                        "Fitness",
                        "Social Status",
                        "Age",
                        "No. Characters",
                        "Species") 
  
  
  plotdata$Label <- factor(plotdata$Label,as.ordered(plotdata$Label[match(sort(plotdata$Estimates[1:r]),plotdata$Estimates[1:r])]))
  plotdata$Label <- factor(plotdata$Label,levels = rev(levels(plotdata$Label)))
  
  plotdata$Estimates <- as.numeric(as.character(plotdata$Estimates))
  plotdata$se <- as.numeric(as.character(plotdata$se))
  
  return(plotdata)
}

# Effect of difference in number of characters within Utilitarian dimension
## Subclass by diff in number of characters
GetMainEffectSizes.Util <- function(profiles){
  Coeffs <- matrix(NA,4,2)
  AttLevels <- levels(profiles$AttributeLevel)
  for(i in 1:4){
    Temp <- profiles[which(profiles$ScenarioType== "Utilitarian" & profiles$ScenarioTypeStrict== "Utilitarian" & profiles$DiffNumberOFCharacters==i),]
    Temp$AttributeLevel <- factor(Temp$AttributeLevel, levels=AttLevels[10:11])
    Temp$BC.weights <- calcWeightsTheoretical(Temp)
    lm.Signed.NoC.Util <- lm(Saved ~as.factor(AttributeLevel), data=Temp, weights = BC.weights)
    summary.lm.Signed.NoC.Util <- summary(lm.Signed.NoC.Util)
    Coeffs[i,1] <- lm.Signed.NoC.Util$coefficients[[2]]
    Coeffs[i,2] <- summary.lm.Signed.NoC.Util$coefficients[2, "Std. Error"]
  }
  return(Coeffs)
}

GetPlotData.Util <- function(Coeffs){
  plotdata <- as.data.frame(Coeffs)
  colnames(plotdata)=c("Estimates","se")
  plotdata$Variant <- c(1:4)
  plotdata$Variant <- factor(plotdata$Variant,levels=rev(plotdata$Variant))
  plotdata$Label <- as.factor(rep("No. Characters",4))
  return(plotdata)
}

PlotAndSave <- function(plotdata.main,isMainFig,filename,plotdata.util){
  #label_order <- c("Intervention", "Relation to AV", "Gender", "Fitness", "Social Status", "Law", "Age", "No. Character", "Species")
  #plotdata.bars$Label <- factor(plotdata.bars$Label, levels = label_order)
  #plotdata.points$Label <- factor(plotdata.points$Label, levels = label_order)
  #plotdata.util$Label <- factor(plotdata.util$Label, levels = label_order)

  plotdata.main.human <- data.frame(
    Estimates = c(0.061, 0.097, 0.353, 0.119, 0.160, 0.345, 0.497, 0.651, 0.585),
    Label = c("Intervention", "Relation to AV", "Law", "Gender", "Fitness", "Social Status", "Age", "No. Characters", "Species")
  )

  plotdata.bars <- plotdata.main[plotdata.main$Label != "No. Characters", ]
  plotdata.points <- plotdata.main[plotdata.main$Label == "No. Characters", ]

  gg <- ggplot() +
    geom_col(data = plotdata.bars, aes(x=Label, y=Estimates), width=0.5, fill = "gray", color = "black") +
    geom_errorbar(data = plotdata.bars, aes(x=Label, ymin=Estimates-se, ymax=Estimates+se), width = 0.2) +
    geom_col(data = plotdata.util[abs(plotdata.util$Estimates) == max(abs(plotdata.util$Estimates)),], aes(x = Label, y = Estimates), fill = "gray", color = "black", width = 0.5) +
    geom_errorbar(data = plotdata.points, aes(x=Label, ymin=Estimates-se, ymax=Estimates+se), width= 0.2) +
    geom_point(data = plotdata.points, aes(x=Label, y=Estimates), color = "black", size = 6) +
    geom_errorbar(data = plotdata.util, aes(x = Label, ymin = Estimates - se, ymax = Estimates + se), width = 0.2) +
    geom_point(data = plotdata.util, aes(x = Label, y = Estimates), size = 6, color = "black", fill = "white", shape=21) +
    geom_text(data = plotdata.util, aes(x = Label, y = Estimates, label = Variant), hjust = 0.5, vjust = 0.5, size = 4, color = "black") +
    geom_hline(yintercept = 0, linetype="solid", color = "black", size=0.4) +
    geom_point(data = plotdata.main.human, aes(x = Label, y = Estimates), color = "red", size = 6, shape = '|') +
    scale_y_continuous(limits = c(-0.5, 1.2)) +
    xlab("") +
    ylab(expression(paste("\n",Delta,"P"))) +
    coord_flip() +
    annotate("text", x = "Intervention", y = -0.5, label = "Action", hjust = "left", vjust = "center", color = "black", size = 4) +
    annotate("text", x = "Intervention", y = 1.2, label = "Inaction", hjust = "right", vjust = "center", color = "black", size = 4) +
    annotate("text", x = "Relation to AV", y = -0.5, label = "Passengers", hjust = "left", vjust = "center", color = "black", size = 4) +
    annotate("text", x = "Relation to AV", y = 1.2, label = "Pedestrians", hjust = "right", vjust = "center", color = "black", size = 4) +
    annotate("text", x = "Law", y = -0.5, label = "Unlawful", hjust = "left", vjust = "center", color = "black", size = 4) +
    annotate("text", x = "Law", y = 1.2, label = "Lawful", hjust = "right", vjust = "center", color = "black", size = 4) +
    annotate("text", x = "Gender", y = -0.5, label = "Males", hjust = "left", vjust = "center", color = "black", size = 4) +
    annotate("text", x = "Gender", y = 1.2, label = "Females", hjust = "right", vjust = "center", color = "black", size = 4) +
    annotate("text", x = "Fitness", y = -0.5, label = "Large", hjust = "left", vjust = "center", color = "black", size = 4) +
    annotate("text", x = "Fitness", y = 1.2, label = "Fit", hjust = "right", vjust = "center", color = "black", size = 4) +
    annotate("text", x = "Social Status", y = -0.5, label = "Low status", hjust = "left", vjust = "center", color = "black", size = 4) +
    annotate("text", x = "Social Status", y = 1.2, label = "High status", hjust = "right", vjust = "center", color = "black", size = 4) +
    annotate("text", x = "Age", y = -0.5, label = "Old", hjust = "left", vjust = "center", color = "black", size = 4) +
    annotate("text", x = "Age", y = 1.2, label = "Young", hjust = "right", vjust = "center", color = "black", size = 4) +
    annotate("text", x = "No. Characters", y = -0.5, label = "Few", hjust = "left", vjust = "center", color = "black", size = 4) +
    annotate("text", x = "No. Characters", y = 1.2, label = "More", hjust = "right", vjust = "center", color = "black", size = 4) +
    annotate("text", x = "Species", y = -0.5, label = "Pets", hjust = "left", vjust = "center", color = "black", size = 4) +
    annotate("text", x = "Species", y = 1.2, label = "Humans", hjust = "right", vjust = "center", color = "black", size = 4) +
    theme_bw() + 
    theme(
      axis.text.y = element_text(angle = 45, hjust = 1),
      aspect.ratio = 0.5,
      axis.title = element_text(size = 14, color="black"),
      axis.text = element_text(size = 12, color="black"),
    )

  ggsave(paste0(filename, ".png"), plot = gg, width = 9, height = 6)
}


