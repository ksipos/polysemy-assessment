
path_root = 'C:/Users/mvazirg/Desktop/polysemous_words/'

languages = c('english') # french
metrics = c('kendall','spearman','ndcg','p@k','rbo')

for (language in languages){
  for (metric in metrics){
    system(paste('Rscript --vanilla heatmap.R',path_root,metric,language))
    cat('\n * * * * * *',metric,'done * * * * * *')
  }
}

