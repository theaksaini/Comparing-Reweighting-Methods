rm(list = ls())
cat("\014")
setwd('~/Desktop/Comparing-Reweighting-Methods-arxiv/Results')

library(ggplot2)
library(cowplot)
library(dplyr)
library(PupillometryR)

NAMES <- c('Evolved','Deterministic','Equal')

# Define all configurations to process
configurations <- list(
  list(hv_file = 'hv_roc_dpd/hv_test.csv', 
       plot_name = "roc_dpd.pdf", 
       plot_title = "Hypervolume for Pareto Front (AUROC, Dem. Parity) on Test Set"),
  list(hv_file = 'hv_roc_sfn/hv_test.csv', 
       plot_name = "roc_sfn.pdf", 
       plot_title = "Hypervolume for Pareto Front (AUROC, Subgroup FN) on Test Set"),
  list(hv_file = 'hv_acc_dpd/hv_test.csv', 
       plot_name = "acc_dpd.pdf", 
       plot_title = "Hypervolume for Pareto Front (Acc., Dem. Parity) on Test Set"),
  list(hv_file = 'hv_acc_sfn/hv_test.csv', 
       plot_name = "acc_sfn.pdf", 
       plot_title = "Hypervolume for Pareto Front (Acc., Subgroup FN) on Test Set")
)

TASKS <- c('heart_disease', 'student_math', 'student_por', 'creditg', 'titanic', 'us_crime', 'compas_violent', 'nlsy', 'compas', 'pmad_rus_phq', 'pmad_rus_epds')
SHAPE <- c(21,24,22)
cb_palette <- c('#D81B60','#1E88E5','#FFC107')
TSIZE <- 19
data_dir <- ''

p_theme <- theme(
  plot.title = element_text( face = "bold", size = 22, hjust=0.5),
  panel.border = element_blank(),
  panel.grid.minor = element_blank(),
  legend.title=element_text(size=22),
  legend.text=element_text(size=23),
  axis.title = element_text(size=23),
  axis.text = element_text(size=19),
  legend.position="bottom",
  panel.background = element_rect(fill = "#f1f2f5",
                                  colour = "white",
                                  linewidth = 0.5, linetype = "solid")
)

# Loop through each configuration
for (config in configurations) {
  
  hv_file_name <- config$hv_file
  final_plot_name <- config$plot_name
  final_plot_title <- config$plot_title
  
  cat(paste("\n\nProcessing:", hv_file_name, "\n"))
  
  # Check if file exists before processing
  if (!file.exists(hv_file_name)) {
    cat(paste("File not found:", hv_file_name, "- Skipping\n"))
    next
  }

testing <- read.csv(hv_file_name, header = TRUE, stringsAsFactors = FALSE)
testing$exp <- gsub('Evolved Weights', 'Evolved', testing$ex)
testing$exp <- gsub('Deterministic Weights', 'Deterministic', testing$ex)
testing$exp <- gsub('Equal Weights', 'Equal', testing$ex)
testing$exp <- gsub('Transfer_Weights_Holdout', 'Transferred', testing$ex)
testing$exp <- gsub('Evolved_Weights_Holdout', 'Evolved', testing$ex)
testing$exp <- factor(testing$exp, levels = NAMES)


# testing 

# task 1

task_1_p <- filter(testing, dataset == TASKS[1]) %>%
  ggplot(., aes(x = exp, y = hv, color = exp, fill = exp, shape = exp)) +
  geom_flat_violin(position = position_nudge(x = .1, y = 0), scale = 'width', alpha = 0.2, width = 1.5) +
  geom_boxplot(color = 'black', width = .07, outlier.shape = NA, alpha = 0.0, size = 1.0, position = position_nudge(x = .16, y = 0)) +
  geom_point(position = position_jitter(width = 0.02, height = 0.0001), size = 1.5, alpha = 1.0) +
  scale_y_continuous(
    name="Volume",
  ) +
  scale_x_discrete(
    name="Population Size"
  )+
  scale_shape_manual(values=SHAPE)+
  scale_colour_manual(values = cb_palette, ) +
  scale_fill_manual(values = cb_palette) +
  ggtitle(TASKS[1])+
  p_theme + coord_flip()

# task 2

task_2_p <- filter(testing, dataset == TASKS[2]) %>%
  ggplot(., aes(x = exp, y = hv, color = exp, fill = exp, shape = exp)) +
  geom_flat_violin(position = position_nudge(x = .1, y = 0), scale = 'width', alpha = 0.2, width = 1.5) +
  geom_boxplot(color = 'black', width = .07, outlier.shape = NA, alpha = 0.0, size = 1.0, position = position_nudge(x = .16, y = 0)) +
  geom_point(position = position_jitter(width = 0.02, height = 0.0001), size = 1.5, alpha = 1.0) +
  scale_y_continuous(
    name="Volume",
  ) +
  scale_x_discrete(
    name="Population Size"
  )+
  scale_shape_manual(values=SHAPE)+
  scale_colour_manual(values = cb_palette, ) +
  scale_fill_manual(values = cb_palette) +
  ggtitle(TASKS[2])+
  p_theme+ coord_flip()

# task 3

task_3_p <- filter(testing, dataset == TASKS[3]) %>%
  ggplot(., aes(x = exp, y = hv, color = exp, fill = exp, shape = exp)) +
  geom_flat_violin(position = position_nudge(x = .1, y = 0), scale = 'width', alpha = 0.2, width = 1.5) +
  geom_boxplot(color = 'black', width = .07, outlier.shape = NA, alpha = 0.0, size = 1.0, position = position_nudge(x = .16, y = 0)) +
  geom_point(position = position_jitter(width = 0.02, height = 0.0001), size = 1.5, alpha = 1.0) +
  scale_y_continuous(
    name="Volume",
  ) +
  scale_x_discrete(
    name="Population Size"
  )+
  scale_shape_manual(values=SHAPE)+
  scale_colour_manual(values = cb_palette, ) +
  scale_fill_manual(values = cb_palette) +
  ggtitle(TASKS[3])+
  p_theme+ coord_flip()

# task 4

task_4_p <- filter(testing, dataset == TASKS[4]) %>%
  ggplot(., aes(x = exp, y = hv, color = exp, fill = exp, shape = exp)) +
  geom_flat_violin(position = position_nudge(x = .1, y = 0), scale = 'width', alpha = 0.2, width = 1.5) +
  geom_boxplot(color = 'black', width = .07, outlier.shape = NA, alpha = 0.0, size = 1.0, position = position_nudge(x = .16, y = 0)) +
  geom_point(position = position_jitter(width = 0.02, height = 0.0001), size = 1.5, alpha = 1.0) +
  scale_y_continuous(
    name="Volume",
  ) +
  scale_x_discrete(
    name="Population Size"
  )+
  scale_shape_manual(values=SHAPE)+
  scale_colour_manual(values = cb_palette, ) +
  scale_fill_manual(values = cb_palette) +
  ggtitle(TASKS[4])+
  p_theme+ coord_flip()

# task 5

task_5_p <- filter(testing, dataset == TASKS[5]) %>%
  ggplot(., aes(x = exp, y = hv, color = exp, fill = exp, shape = exp)) +
  geom_flat_violin(position = position_nudge(x = .1, y = 0), scale = 'width', alpha = 0.2, width = 1.5) +
  geom_boxplot(color = 'black', width = .07, outlier.shape = NA, alpha = 0.0, size = 1.0, position = position_nudge(x = .16, y = 0)) +
  geom_point(position = position_jitter(width = 0.02, height = 0.0001), size = 1.5, alpha = 1.0) +
  scale_y_continuous(
    name="Volume",
  ) +
  scale_x_discrete(
    name="Population Size"
  )+
  scale_shape_manual(values=SHAPE)+
  scale_colour_manual(values = cb_palette, ) +
  scale_fill_manual(values = cb_palette) +
  ggtitle(TASKS[5])+
  p_theme+ coord_flip()

# task 6

task_6_p <- filter(testing, dataset == TASKS[6]) %>%
  ggplot(., aes(x = exp, y = hv, color = exp, fill = exp, shape = exp)) +
  geom_flat_violin(position = position_nudge(x = .1, y = 0), scale = 'width', alpha = 0.2, width = 1.5) +
  geom_boxplot(color = 'black', width = .07, outlier.shape = NA, alpha = 0.0, size = 1.0, position = position_nudge(x = .16, y = 0)) +
  geom_point(position = position_jitter(width = 0.02, height = 0.0001), size = 1.5, alpha = 1.0) +
  scale_y_continuous(
    name="Volume",
  ) +
  scale_x_discrete(
    name="Population Size"
  )+
  scale_shape_manual(values=SHAPE)+
  scale_colour_manual(values = cb_palette, ) +
  scale_fill_manual(values = cb_palette) +
  ggtitle(TASKS[6])+
  p_theme+ coord_flip()

# task 7

task_7_p <- filter(testing, dataset == TASKS[7]) %>%
  ggplot(., aes(x = exp, y = hv, color = exp, fill = exp, shape = exp)) +
  geom_flat_violin(position = position_nudge(x = .1, y = 0), scale = 'width', alpha = 0.2, width = 1.5) +
  geom_boxplot(color = 'black', width = .07, outlier.shape = NA, alpha = 0.0, size = 1.0, position = position_nudge(x = .16, y = 0)) +
  geom_point(position = position_jitter(width = 0.02, height = 0.0001), size = 1.5, alpha = 1.0) +
  scale_y_continuous(
    name="Volume",
  ) +
  scale_x_discrete(
    name="Population Size"
  )+
  scale_shape_manual(values=SHAPE)+
  scale_colour_manual(values = cb_palette, ) +
  scale_fill_manual(values = cb_palette) +
  ggtitle(TASKS[7])+
  p_theme+ coord_flip()

# task 8

task_8_p <- filter(testing, dataset == TASKS[8]) %>%
  ggplot(., aes(x = exp, y = hv, color = exp, fill = exp, shape = exp)) +
  geom_flat_violin(position = position_nudge(x = .1, y = 0), scale = 'width', alpha = 0.2, width = 1.5) +
  geom_boxplot(color = 'black', width = .07, outlier.shape = NA, alpha = 0.0, size = 1.0, position = position_nudge(x = .16, y = 0)) +
  geom_point(position = position_jitter(width = 0.02, height = 0.0001), size = 1.5, alpha = 1.0) +
  scale_y_continuous(
    name="Volume",
  ) +
  scale_x_discrete(
    name="Population Size"
  )+
  scale_shape_manual(values=SHAPE)+
  scale_colour_manual(values = cb_palette, ) +
  scale_fill_manual(values = cb_palette) +
  ggtitle(TASKS[8])+
  p_theme+ coord_flip()

# task 9

task_9_p <- filter(testing, dataset == TASKS[9]) %>%
  ggplot(., aes(x = exp, y = hv, color = exp, fill = exp, shape = exp)) +
  geom_flat_violin(position = position_nudge(x = .1, y = 0), scale = 'width', alpha = 0.2, width = 1.5) +
  geom_boxplot(color = 'black', width = .07, outlier.shape = NA, alpha = 0.0, size = 1.0, position = position_nudge(x = .16, y = 0)) +
  geom_point(position = position_jitter(width = 0.02, height = 0.0001), size = 1.5, alpha = 1.0) +
  scale_y_continuous(
    name="Volume",
  ) +
  scale_x_discrete(
    name="Population Size"
  )+
  scale_shape_manual(values=SHAPE)+
  scale_colour_manual(values = cb_palette, ) +
  scale_fill_manual(values = cb_palette) +
  ggtitle(TASKS[9])+
  p_theme+ coord_flip()

# task 10

task_10_p <- filter(testing, dataset == TASKS[10]) %>%
  ggplot(., aes(x = exp, y = hv, color = exp, fill = exp, shape = exp)) +
  geom_flat_violin(position = position_nudge(x = .1, y = 0), scale = 'width', alpha = 0.2, width = 1.5) +
  geom_boxplot(color = 'black', width = .07, outlier.shape = NA, alpha = 0.0, size = 1.0, position = position_nudge(x = .16, y = 0)) +
  geom_point(position = position_jitter(width = 0.02, height = 0.0001), size = 1.5, alpha = 1.0) +
  scale_y_continuous(
    name="Volume",
  ) +
  scale_x_discrete(
    name="Population Size"
  )+
  scale_shape_manual(values=SHAPE)+
  scale_colour_manual(values = cb_palette, ) +
  scale_fill_manual(values = cb_palette) +
  ggtitle(TASKS[10])+
  p_theme+ coord_flip()

# task 11

task_11_p <- filter(testing, dataset == TASKS[11]) %>%
  ggplot(., aes(x = exp, y = hv, color = exp, fill = exp, shape = exp)) +
  geom_flat_violin(position = position_nudge(x = .1, y = 0), scale = 'width', alpha = 0.2, width = 1.5) +
  geom_boxplot(color = 'black', width = .07, outlier.shape = NA, alpha = 0.0, size = 1.0, position = position_nudge(x = .16, y = 0)) +
  geom_point(position = position_jitter(width = 0.02, height = 0.0001), size = 1.5, alpha = 1.0) +
  scale_y_continuous(
    name="Volume",
  ) +
  scale_x_discrete(
    name="Population Size"
  )+
  scale_shape_manual(values=SHAPE)+
  scale_colour_manual(values = cb_palette, ) +
  scale_fill_manual(values = cb_palette) +
  ggtitle(TASKS[11])+
  p_theme+ coord_flip()

# task 12

task_12_p <- filter(testing, dataset == TASKS[12]) %>%
  ggplot(., aes(x = exp, y = hv, color = exp, fill = exp, shape = exp)) +
  geom_flat_violin(position = position_nudge(x = .1, y = 0), scale = 'width', alpha = 0.2, width = 1.5) +
  geom_boxplot(color = 'black', width = .07, outlier.shape = NA, alpha = 0.0, size = 1.0, position = position_nudge(x = .16, y = 0)) +
  geom_point(position = position_jitter(width = 0.02, height = 0.0001), size = 1.5, alpha = 1.0) +
  scale_y_continuous(
    name="Volume",
  ) +
  scale_x_discrete(
    name="Population Size"
  )+
  scale_shape_manual(values=SHAPE)+
  scale_colour_manual(values = cb_palette, ) +
  scale_fill_manual(values = cb_palette) +
  ggtitle(TASKS[12])+
  p_theme+ coord_flip()


# legend
legend <- cowplot::get_legend(
  task_1_p +
    guides(
      shape=guide_legend(ncol=1,title="Weight Strategy",reverse = TRUE,title.position="left", title.hjust = 0.5),
      color=guide_legend(ncol=1,title="Weight Strategy",reverse = TRUE,title.position="left", title.hjust = 0.5),
      fill=guide_legend(ncol=1,title="Weight Strategy",reverse = TRUE,title.position="left", title.hjust = 0.5)
    ) +
    theme(
      legend.position = "top",
      legend.box="vertical",
      legend.justification="center",
      legend.text = element_text(size = 20),
      legend.key.width = grid::unit(1.4, "cm"),
      legend.spacing.x = grid::unit(0.4, "cm"),
      legend.margin = margin(t = 8, r = 10, b = 8, l = 10)
    )
)


col1_theme <- theme(legend.position = "none", axis.title.y = element_blank(), axis.title.x = element_blank(),
                    axis.text.y = element_blank(), axis.ticks.y = element_blank())

col1 <- plot_grid(
  task_1_p + ggtitle(TASKS[1]) + col1_theme,
  task_2_p + ggtitle(TASKS[2]) + col1_theme,
  task_3_p + ggtitle(TASKS[3]) + col1_theme,
  task_4_p + ggtitle(TASKS[4]) + col1_theme,
  ncol=4,
  rel_heights = c(1.0,1.0,1.0,1.0),
  label_size = TSIZE
)

col2 <- plot_grid(
  task_5_p + ggtitle(TASKS[5]) + col1_theme,
  task_6_p + ggtitle(TASKS[6]) + col1_theme,
  task_7_p + ggtitle(TASKS[7]) + col1_theme,
  task_8_p + ggtitle(TASKS[8]) + col1_theme,
  ncol=4,
  rel_heights = c(1.0,1.0,1.0,1.0),
  label_size = TSIZE
)

col3 <- plot_grid(
  task_9_p + ggtitle(TASKS[9]) + col1_theme,
  task_10_p + ggtitle(TASKS[10]) + col1_theme,
  task_11_p + ggtitle(TASKS[11]) + col1_theme,
  #task_12_p + ggtitle(TASKS[12]) + col1_theme,
  ncol=4,
  rel_heights = c(1.0,1.0,1.0,1.0),
  label_size = TSIZE
)

colb <-  theme(legend.position = "none", axis.title.y = element_blank(), axis.text.y = element_blank(), axis.ticks.y = element_blank())


fig <- plot_grid(
  ggdraw() + draw_label(final_plot_title, fontface='bold', size = 24) + p_theme,
  col1,
  col2,
  col3,
  legend,
  nrow=5,
  rel_heights = c(0.15,1.0,1.0,1.0,0.42),
  label_size = TSIZE
)

fig

save_plot(
  paste(filename =final_plot_name),
  fig,
  base_width=20,
  base_height=12
)

cat(paste("Saved plot to:", final_plot_name, "\n"))

} # End of configuration loop

cat("\n\nAll plots generated successfully!\n")

