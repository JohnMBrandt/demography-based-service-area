data_format <- function(dataframe, column, number, county, plot_title) {
  col2 <- deparse(substitute(column))
  county <- deparse(substitute(county))
  
  top <- dataframe %>%
    arrange(desc(dataframe[[col2]]))
  top <- top[0:number,]
  top$color <- "Top"

  bottom <- dataframe %>%
    arrange(dataframe[[col2]])
  bottom <- bottom[0:number,]
  bottom$color <- "Bottom"
  
  extremes <<- rbind(top,bottom)

  plot <- ggplot(data=extremes, aes(x=reorder(extremes[[county]], extremes[[col2]]), y=extremes[[col2]]))+
    geom_col(aes(fill=extremes$color))+
    coord_flip()+
    theme_bw(base_size=13)+
    xlab("")+
    ylab("")+
    theme(legend.position = "none",
          panel.grid.major.y=element_blank(),
          panel.grid.minor.y=element_blank(),
          panel.grid.minor.x=element_blank(),
          panel.grid.major.x=element_line(color="grey90"),
          axis.ticks = element_line(color="grey90"),
          axis.ticks.y=element_blank(),
          axis.title.x=element_blank(),
          strip.background=element_blank(),
          plot.margin=margin(0.6,0.6,0.6,0.6, "cm"),
          legend.title=element_blank(),
          plot.title = element_text(size=12),
          panel.border=element_rect(color="grey60"))+
    ggtitle(plot_title)
  
  result <<- plot
}

data_format(gisdata, perc_pop, 10, County, "Total population")


black_top <- gisdata %>%
  arrange(desc(black_diff))
black_top <- black_top[0:10,]

black_bottom <- gisdata %>%
  arrange(black_diff)

black_bottom <- black_bottom[0:10,]
topbottom <- rbind(black_top, black_bottom)


bl_plot <- ggplot(data=topbottom, aes(x=reorder(County, black_diff), y=black_diff))+
  geom_col()+
  coord_flip()+
  theme_bw(base_size=13)+
  xlab("")+
  ylab("")+
  theme(legend.position = "bottom",
        panel.grid.major.y=element_blank(),
        panel.grid.minor.y=element_blank(),
        panel.grid.minor.x=element_blank(),
        panel.grid.major.x=element_line(color="grey90"),
        axis.ticks = element_line(color="grey90"),
        axis.ticks.y=element_blank(),
        axis.title.x=element_blank(),
        strip.background=element_blank(),
        plot.margin=margin(0.6,0.6,0.6,0.6, "cm"),
        legend.title=element_text(size=11),
        plot.title = element_text(size=12),
        panel.border=element_rect(color="grey60"))+
  ggtitle("Black females")+
  scale_fill_manual(values=c("#377eb8", "#e41a1c"), labels=c("Democrats", "Republicans"), name="Millions of dollars more donated to")+
  scale_y_continuous(expand=c(0,0), limits=c(-0.5,0.5))

sing_top <- gisdata %>%
  arrange(desc(mom_diff))
sing_top <- sing_top[0:10,]

sing_bottom <- gisdata %>%
  arrange(mom_diff)

sing_bottom <- sing_bottom[0:4,]
topbottom_sing <- rbind(sing_top, sing_bottom)

sm_plot <- ggplot(data=topbottom_sing, aes(x=reorder(County, mom_diff), y=mom_diff))+
  geom_col()+
  coord_flip()+
  theme_bw(base_size=13)+
  xlab("")+
  ylab("")+
  theme(legend.position = "bottom",
        panel.grid.major.y=element_blank(),
        panel.grid.minor.y=element_blank(),
        panel.grid.minor.x=element_blank(),
        panel.grid.major.x=element_line(color="grey90"),
        axis.ticks = element_line(color="grey90"),
        axis.ticks.y=element_blank(),
        axis.title.x=element_blank(),
        strip.background=element_blank(),
        plot.margin=margin(0.6,0.6,0.6,0.6, "cm"),
        legend.title=element_text(size=11),
        plot.title = element_text(size=12),
        panel.border=element_rect(color="grey60"))+
  ggtitle("Single mothers")+
  scale_fill_manual(values=c("#377eb8", "#e41a1c"), labels=c("Democrats", "Republicans"), name="Millions of dollars more donated to")+
  scale_y_continuous(expand=c(0,0), limits=c(-0.5,0.5))

multiplot(result, bl_plot, sm_plot, cols=3)