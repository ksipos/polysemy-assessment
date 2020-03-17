path_root = 'C:/Users/mvazirg/Desktop/polysemous_words/'

setwd(paste0(path_root,'antoine/')) # where code is located

languages = c('english') # c('english','french')
metrics = c('cosine','spearman','kendall','p@k','ndcg','rbo')

for (language in languages){
  for (metric in metrics){
    system(paste('Rscript --vanilla heatmap.R',path_root,metric,language))
    cat('\n * * * * * *',metric,'done * * * * * *')
  }
}

