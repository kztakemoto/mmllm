library(ggplot2)
library(ggrepel)

# load data
data <- read.csv("./data/summary_overall_preferences.csv", check.names=F)

## figure 2a (bar plot) #########################

# function for computing the distance 
euclidean_distance <- function(col1, col2) {
  return(sqrt(sum((col1 - col2)^2)))
}

# compute the distance between Human and LLM
distances <- data.frame(Model = character(), Distance = numeric())
for (colname in names(data)[-1]) {  # 最初の列(Label)と最後の列(Human)を除外
  if (colname != "Human") {
    distance <- euclidean_distance(data$Human, data[[colname]])
    distances <- rbind(distances, data.frame(Model = colname, Distance = distance))
  }
}

# plot the result
gg <- ggplot(distances, aes(x=Model, y=Distance)) + 
    geom_bar(stat="identity", width=0.5) + 
    labs(y="Distance from Human Preferences") +
    theme(
        axis.text.x = element_text(angle = 45, hjust = 1),
        aspect.ratio = 1,
        axis.title = element_text(size = 22, color="black"),
        axis.text = element_text(size = 20, color="black"),
    ) +
    ylim(0, max(distances$Distance) + 0.1)  # Set y-axis limits

ggsave("figure2a.png", plot = gg, width = 6, height = 6)

## figure 2b (PCA) #############################
# preprocessing
data_t <- t(data[-1])
colnames(data_t) <- data$Label

# run PCA
pca_result <- prcomp(data_t, center=T, scale.=F)

explained_variance_ratio <- pca_result$sdev^2 / sum(pca_result$sdev^2)
print(explained_variance_ratio)

# plot
df_pca <- as.data.frame(pca_result$x)
gg <- ggplot(df_pca, aes(x=PC1, y=PC2)) +
    geom_point(size=5) +
    geom_label_repel(aes(label=rownames(df_pca)), box.padding = 0.5, point.padding = 0.5, size=8) +
    labs(x = paste("PC1 (", round(explained_variance_ratio[1]*100, 1), "%)", sep=""),
        y = paste("PC2 (", round(explained_variance_ratio[2]*100, 1), "%)", sep="")) +
    theme(
        legend.position = "none",
        aspect.ratio = 1,
        axis.title = element_text(size = 22, color="black"),
        axis.text = element_text(size = 20, color="black"),
    )

ggsave("figure2b.png", plot = gg, width = 6, height = 6)