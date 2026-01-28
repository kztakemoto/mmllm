library(ggplot2)
library(ggrepel)
library(dplyr)
library(tidyr)
library(reshape2)
library(RColorBrewer)
library(lubridate)
library(lme4)
library(lmerTest)

# ============================================================================
# Load and prepare data
# ============================================================================

# Load data
data <- read.csv("table_S1.csv")

# Function to group models by family
group_models <- function(model_name) {
  if (grepl("DeepSeek", model_name)) return("DeepSeek")
  if (grepl("Llama", model_name)) return("Llama")
  if (grepl("Gemma", model_name)) return("Gemma")
  if (grepl("Qwen", model_name)) return("Qwen")
  return("Other")
}

# Add group column
data$Group <- sapply(data$Model, group_models)
data_sub <- subset(data, is.na(data$Size) == F)

print(dim(data_sub))

# Add reasoning information
data_sub <- data_sub %>%
  mutate(
    Reasoning_binary = ifelse(!is.na(Reasoning) & 
                              tolower(trimws(Reasoning)) == "yes", 1, 0),
    Reasoning_label = ifelse(Reasoning_binary == 1, 
                            "Reasoning", "Standard")
  )

# ============================================================================
# ANALYSIS 1: Main power-law scaling relationship
# ============================================================================

cat("\n=== MAIN POWER-LAW ANALYSIS ===\n")

# Power-law fit (log-log linear regression)
log_model <- lm(log10(Distance) ~ log10(Size), data = data_sub)
print(summary(log_model))
alpha <- -coef(log_model)[2]  # power-law exponent
intercept <- coef(log_model)[1]

# Compare with alternative models
model_linear <- lm(Distance ~ Size, data = data_sub)
model_log <- lm(Distance ~ log10(Size), data = data_sub)
model_exp <- lm(log10(Distance) ~ Size, data = data_sub)

cat("\nR-squared comparison:\n")
cat(sprintf("Power-law (log-log): %.3f\n", summary(log_model)$r.squared))
cat(sprintf("Linear: %.3f\n", summary(model_linear)$r.squared))
cat(sprintf("Logarithmic: %.3f\n", summary(model_log)$r.squared))
cat(sprintf("Exponential: %.3f\n", summary(model_exp)$r.squared))

# Calculate fitted values for visualization
data_sub$fitted <- 10^predict(log_model)

# Correlation test
cor_result <- cor.test(data_sub$Size, data_sub$Distance, method = "spearman")
print(cor_result)

# Statistical summary
cat(sprintf("\nPower-law exponent: α = %.3f\n", alpha))
cat(sprintf("R-squared: %.3f\n", summary(log_model)$r.squared))

# ============================================================================
# FIGURE 1: Main scaling relationship (log-log plot)
# ============================================================================

fig1 <- ggplot(data_sub, aes(x = Size, y = Distance)) +
  geom_line(aes(y = fitted), color = "black", linetype = "dashed", linewidth = 1) +
  geom_point(aes(color = Group), size = 3) +
  geom_text_repel(aes(label = Model, color = Group), 
                  size = 3.5,
                  max.overlaps = 15,
                  force = 3,
                  segment.size = 0.3,
                  min.segment.length = 0.1) +
  labs(x = "Model Size (Billion Parameters)",
       y = "Distance from Human") +
  scale_x_log10(breaks = c(1, 3, 10, 30, 100, 300, 1000)) +
  scale_y_log10(breaks = c(0.5, 0.7, 1.0, 1.5, 2.0)) +
  theme_bw(base_size = 12) +
  theme(
    axis.title = element_text(size = 14),
    axis.text = element_text(size = 12),
    legend.position = c(0.98, 0.7),
    legend.justification = c("right", "bottom"),
    legend.title = element_blank(),
    legend.text = element_text(size = 11),
    legend.background = element_rect(fill = "white", color = "black", linewidth = 0.3),
    panel.grid.minor = element_blank()
  ) +
  scale_color_brewer(palette = "Set1")

ggsave("figure_logDlogS.pdf", plot = fig1, width = 8, height = 6, device = cairo_pdf)
ggsave("figure_logDlogS.eps", plot = fig1, width = 8, height = 6, device = "eps")
ggsave("figure_logDlogS.png", plot = fig1, width = 8, height = 6, dpi = 300)

# ============================================================================
# ANALYSIS 2: Family-specific scaling relationships
# ============================================================================

cat("\n=== FAMILY-SPECIFIC ANALYSIS ===\n")
cat("\n=== Family-specific correlations ===\n")

for (group in unique(data_sub$Group)) {
  group_data <- filter(data_sub, Group == group)
  if (nrow(group_data) >= 3) {
    cor_test <- cor.test(log10(group_data$Size), log10(group_data$Distance), 
                        method = "spearman")
    cat(sprintf("%s: n = %d, rho = %.3f, p = %.4f\n", 
                group, nrow(group_data), cor_test$estimate, cor_test$p.value))
  }
}

# ============================================================================
# FIGURE 2: Family-specific scaling relationships
# ============================================================================

fig2 <- ggplot(data_sub, aes(x = log10(Size), y = log10(Distance), 
                              color = Group, shape = Group)) +
  geom_point(alpha = 0.7, size = 3) +
  geom_smooth(method = "lm", se = TRUE, linewidth = 1) +
  scale_color_brewer(palette = "Set1") +
  scale_shape_manual(values = c(16, 17, 15, 18, 4)) +
  labs(x = expression(paste("Model Size (", log[10], " parameters)")),
       y = expression(paste("Distance from Human (", log[10], ")")),
       color = "Model Family",
       shape = "Model Family") +
  theme_bw(base_size = 12) +
  theme(
    legend.position = c(0.85, 0.8),
    legend.background = element_rect(fill = "white", color = "black"),
    axis.title = element_text(size = 14),
    axis.text = element_text(size = 12)
  )

ggsave("figure_family_scaling.pdf", plot = fig2, 
       width = 8, height = 6, device = cairo_pdf)
ggsave("figure_family_scaling.png", plot = fig2, 
       width = 8, height = 6, dpi = 300)

# ============================================================================
# ANALYSIS 3: Reasoning vs. Standard models
# ============================================================================

cat("\n=== REASONING VS. STANDARD MODELS ===\n")

standard_data <- filter(data_sub, Reasoning_binary == 0)
reasoning_data <- filter(data_sub, Reasoning_binary == 1)

cat(sprintf("Standard models: n = %d, mean distance = %.3f\n", 
            nrow(standard_data), mean(standard_data$Distance)))
cat(sprintf("Extended reasoning models: n = %d, mean distance = %.3f\n", 
            nrow(reasoning_data), mean(reasoning_data$Distance)))

if (nrow(standard_data) >= 3 && nrow(reasoning_data) >= 3) {
  cor_standard <- cor.test(log10(standard_data$Size), 
                          log10(standard_data$Distance), 
                          method = "spearman")
  cor_reasoning <- cor.test(log10(reasoning_data$Size), 
                           log10(reasoning_data$Distance), 
                           method = "spearman")
  
  cat(sprintf("Standard: rho = %.3f, p = %.4f\n", 
              cor_standard$estimate, cor_standard$p.value))
  cat(sprintf("Reasoning: rho = %.3f, p = %.4f\n", 
              cor_reasoning$estimate, cor_reasoning$p.value))
}

# ============================================================================
# FIGURE 3: Reasoning vs. Standard models
# ============================================================================

fig3 <- ggplot(data_sub, aes(x = log10(Size), y = log10(Distance), 
                              color = Reasoning_label, shape = Reasoning_label)) +
  geom_point(alpha = 0.7, size = 3) +
  geom_smooth(method = "lm", se = TRUE, linewidth = 1) +
  scale_color_manual(values = c("Standard" = "gray50", 
                                "Reasoning" = "#E41A1C"),
                    name = "Model Type") +
  scale_shape_manual(values = c("Standard" = 16, 
                               "Reasoning" = 17),
                    name = "Model Type") +
  labs(x = expression(paste("Model Size (", log[10], " parameters)")),
       y = expression(paste("Distance from Human (", log[10], ")"))) +
  theme_bw(base_size = 12) +
  theme(
    legend.position = c(0.85, 0.85),
    legend.background = element_rect(fill = "white", color = "black"),
    axis.title = element_text(size = 14),
    axis.text = element_text(size = 12)
  )

ggsave("figure_reasoning_effect.pdf", plot = fig3, 
       width = 8, height = 6, device = cairo_pdf)
ggsave("figure_reasoning_effect.png", plot = fig3, 
       width = 8, height = 6, dpi = 300)

# ============================================================================
# ANALYSIS 4: Temporal trends (release date effects)
# ============================================================================

cat("\n=== TEMPORAL TREND ANALYSIS ===\n")

# Prepare temporal data
data_temporal <- data_sub %>%
  filter(!is.na(Reasoning), !is.na(ReleaseDate)) %>%
  mutate(
    Reasoning = trimws(tolower(Reasoning)),
    Reasoning_binary = ifelse(Reasoning == "yes", 1, 0),
    log_Size = log10(Size),
    log_Distance = log10(Distance),
    # Parse release date and calculate time since 2020
    Release_date_parsed = as.Date(ReleaseDate),
    Days_since_2020 = as.numeric(Release_date_parsed - as.Date("2020-01-01")),
    Years_since_2020 = Days_since_2020 / 365.25
  ) %>%
  filter(!is.na(Release_date_parsed))

print(dim(data_temporal))
summary(data_temporal$Years_since_2020)

# Distribution of release dates by group
cat("\n=== Release date distribution by Group ===\n")
data_temporal %>%
  group_by(Group) %>%
  summarise(
    n = n(),
    min_date = min(Release_date_parsed),
    max_date = max(Release_date_parsed),
    mean_years = mean(Years_since_2020)
  ) %>%
  print()

# ============================================================================
# Mixed-effects models: Testing release date effects
# ============================================================================

# Model A: Size only (baseline)
modelA <- lmer(log_Distance ~ log_Size + 
               (1 + log_Size | Group), 
               data = data_temporal)

# Model B: Size + Release date (test temporal confound)
modelB <- lmer(log_Distance ~ log_Size + Years_since_2020 + 
               (1 + log_Size | Group), 
               data = data_temporal)

# Model C: Size + Release date + Reasoning (add reasoning effect)
modelC <- lmer(log_Distance ~ log_Size + Years_since_2020 + Reasoning_binary + 
               (1 + log_Size | Group), 
               data = data_temporal)

# Model D: Size + Release date + Reasoning + Size×Reasoning (add interaction)
modelD <- lmer(log_Distance ~ log_Size * Reasoning_binary + Years_since_2020 + 
               (1 + log_Size | Group), 
               data = data_temporal)

# Model comparison
cat("\n=== Model Comparison ===\n")
anova(modelA, modelB, modelC, modelD)

cat("\n=== Model A: Size only ===\n")
summary(modelA)

cat("\n=== Model B: Size + Release date ===\n")
summary(modelB)

cat("\n=== Model C: Size + Release date + Reasoning ===\n")
summary(modelC)

cat("\n=== Model D: Size + Release date + Reasoning + Size x Reasoningn ===\n")
summary(modelD)

# ============================================================================
# Cohort analysis: Generation effects
# ============================================================================

# Classify by release year
data_temporal <- data_temporal %>%
  mutate(
    Release_year = year(Release_date_parsed),
    Generation = case_when(
      Release_year <= 2022 ~ "Early (≤2022)",
      Release_year == 2023 ~ "Mid (2023)",
      Release_year >= 2024 ~ "Late (≥2024)"
    ),
    Generation = factor(Generation, levels = c("Early (≤2022)", "Mid (2023)", "Late (≥2024)"))
  )

cat("\n=== Sample sizes by Generation ===\n")
table(data_temporal$Generation)

# Descriptive statistics by generation
cat("\n=== Descriptive statistics by Generation ===\n")
data_temporal %>%
  group_by(Generation) %>%
  summarise(
    n = n(),
    mean_distance = mean(Distance),
    sd_distance = sd(Distance),
    mean_size = mean(Size),
    reasoning_yes_pct = mean(Reasoning_binary) * 100
  ) %>%
  print()

# Model with generation as categorical variable
modelE <- lmer(log_Distance ~ log_Size + Generation + 
               (1 + log_Size | Group), 
               data = data_temporal)

cat("\n=== Model E: with Generation (categorical) ===\n")
summary(modelE)

# ============================================================================
# Residual analysis: Size-adjusted temporal trends
# ============================================================================

# Calculate residuals after controlling for size
model_size_only <- lmer(log_Distance ~ log_Size + (1 + log_Size | Group), 
                        data = data_temporal)
data_temporal$residual_distance <- residuals(model_size_only)

# Correlation between residuals and release year
cat("\n=== Correlation: Residual Distance vs Release Year ===\n")
cor_test <- cor.test(data_temporal$residual_distance, 
                     data_temporal$Years_since_2020, 
                     method = "spearman")
print(cor_test)

# ============================================================================
# Size-stratified analysis: 7B models over time
# ============================================================================

# Focus on 7B-class models
data_7B <- data_temporal %>%
  filter(Size >= 6 & Size <= 9)

if(nrow(data_7B) >= 5) {
  cat("\n=== 7B models: Release date effect ===\n")
  model_7B <- lm(log_Distance ~ Years_since_2020, data = data_7B)
  summary(model_7B)
  
  cat("\n7B models over time:\n")
  data_7B %>%
    select(Model, Size, Release_date_parsed, Distance) %>%
    arrange(Release_date_parsed) %>%
    print()
}

# ============================================================================
# Predictions and interpretation summary
# ============================================================================

# Calculate fitted values from best model (Model D)
data_temporal$fitted_best <- predict(modelD)
data_temporal$fitted_original <- 10^data_temporal$fitted_best

# Summary of results
cat("\n=== INTERPRETATION SUMMARY ===\n")
best_model_summary <- summary(modelD)
coefs <- fixef(modelD)

cat(sprintf("Effect of model size (log_Size): %.4f (α = %.3f)\n", 
            coefs["log_Size"], -coefs["log_Size"]))
cat(sprintf("Effect of release date: %.4f per year\n", 
            coefs["Years_since_2020"]))
cat(sprintf("  → Distance %s by %.1f%% per year\n",
            ifelse(coefs["Years_since_2020"] < 0, "decreases", "increases"),
            abs((10^coefs["Years_since_2020"] - 1) * 100)))
cat(sprintf("Effect of Reasoning (main): %.4f\n", 
            coefs["Reasoning_binary"]))
cat(sprintf("  → Distance %s by %.1f%% when Reasoning=yes\n",
            ifelse(coefs["Reasoning_binary"] < 0, "decreases", "increases"),
            abs((10^coefs["Reasoning_binary"] - 1) * 100)))
cat(sprintf("Size × Reasoning interaction: %.4f\n", 
            coefs["log_Size:Reasoning_binary"]))
cat(sprintf("  → Reasoning effect %s in larger models\n",
            ifelse(coefs["log_Size:Reasoning_binary"] > 0, "decreases", "increases")))


# ============================================================================
# FIGURE 4: Temporal trend in residual distance
# ============================================================================

fig4 <- ggplot(data_temporal, aes(x = Release_date_parsed, y = residual_distance)) +
  geom_point(aes(shape = Group), size = 3, alpha = 0.6) +
  geom_smooth(method = "lm", color = "black", se = TRUE) +
  labs(x = "Release Date",
       y = "Residual Distance (after controlling for size)",
       title = "Temporal trend in model alignment") +
  theme_bw(base_size = 12) +
  theme(
    axis.title = element_text(size = 14),
    axis.text = element_text(size = 12),
    legend.position = "right"
  )

ggsave("figure_temporal_residual.pdf", plot = fig4, 
       width = 8, height = 6, device = cairo_pdf)
ggsave("figure_temporal_residual.png", plot = fig4, 
       width = 8, height = 6, dpi = 300)

cat("\n=== ANALYSIS COMPLETE ===\n")