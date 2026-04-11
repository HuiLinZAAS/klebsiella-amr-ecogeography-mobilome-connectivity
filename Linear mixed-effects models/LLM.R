# =========================================================
# AMR-Phylogeny Variance Partition Analysis
# Author: Feifan Shi
# Date: 2025-10
# Purpose: test whether phylogeny (ST) explains AMR variation
# =========================================================

setwd("G:/2025/202510/1015ST")

# --------------------------
# 1. Load packages
# --------------------------
library(readxl)
library(dplyr)
library(lme4)
library(lmerTest)
library(broom)
library(openxlsx)
library(ggplot2)

# --------------------------
# 2. Input files
# --------------------------
main_file <- "Supplementary Table 5 A collection of the global K. pneumoniae genome data.xlsx"
region_file <- "CountryCate.xlsx"

output_file <- "AMR_phylogeny_variance_partition.xlsx"
plot_folder <- "AMR_plots"

if (!dir.exists(plot_folder)) dir.create(plot_folder)

# AMR variables
amr_vars <- c("Resistance_score",
              "Resistance_genes",
              "Resistance_classes",
              "Virulence_score")

# --------------------------
# 3. Load data
# --------------------------
main <- read_xlsx(main_file)
region <- read_xlsx(region_file)

df <- main %>%
  left_join(region, by = "Country") %>%
  mutate(Region2 = case_when(
    Country == "China" ~ "China",
    Country == "USA" ~ "USA",
    Region == "Europe" ~ "Europe",
    Region == "Africa" ~ "Africa",
    TRUE ~ NA_character_
  )) %>%
  filter(Region2 %in% c("China","USA","Europe","Africa"),
         Source %in% c("Human","Nonhuman")) %>%
  mutate(Source = factor(Source, levels = c("Human","Nonhuman")))

# --------------------------
# 4. Run models
# --------------------------
results <- list()

for (v in amr_vars) {
  
  df_v <- df %>% filter(!is.na(.data[[v]]))
  if (nrow(df_v) < 100) next
  
  # Mixed model with phylogeny (ST)
  m1 <- lmer(as.formula(paste(v, "~ Region2 + Source + (1|ST)")),
             data = df_v)
  
  # Linear model without phylogeny
  m0 <- lm(as.formula(paste(v, "~ Region2 + Source")),
           data = df_v)
  
  # variance of ST
  vc <- as.data.frame(VarCorr(m1))
  phylo_var <- vc$vcov[vc$grp == "ST"]
  resid_var <- vc$vcov[vc$grp == "Residual"]
  
  phylo_prop <- phylo_var / (phylo_var + resid_var)
  
  # summary table
  res <- data.frame(
    Variable = v,
    Phylogeny_prop = round(phylo_prop, 3),
    R2_fixed = round(summary(m0)$r.squared, 3),
    logLik_m1 = as.numeric(logLik(m1)),
    logLik_m0 = as.numeric(logLik(m0)),
    delta_logLik = as.numeric(logLik(m1) - logLik(m0))
  )
  
  results[[v]] <- list(summary = res,
                       coef = broom::tidy(m1, effects = "fixed"))
  
  # plot
  p <- ggplot(df_v, aes(x = Region2, y = .data[[v]], fill = Source)) +
    geom_boxplot() +
    theme_bw() +
    labs(title = paste(v, "by region and source"),
         x = "Region", y = v)
  
  ggsave(paste0(plot_folder, "/", v, "_boxplot.png"),
         p, width = 7, height = 4)
}

# --------------------------
# 5. Save results
# --------------------------
wb <- createWorkbook()

for (v in names(results)) {
  addWorksheet(wb, paste0(v, "_summary"))
  writeData(wb, paste0(v, "_summary"), results[[v]]$summary)
  
  addWorksheet(wb, paste0(v, "_coef"))
  writeData(wb, paste0(v, "_coef"), results[[v]]$coef)
}

saveWorkbook(wb, output_file, overwrite = TRUE)

cat("Done!\nResults saved to:", output_file, "\n")