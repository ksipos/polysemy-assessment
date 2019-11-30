library(pheatmap)
library(RColorBrewer)

dcg = function(x) {
  sum(unlist(lapply(1:length(x), function(i) (2^x[i] - 1)/log2(i+1))))
}

# see: https://en.wikipedia.org/wiki/Learning_to_rank#Evaluation_measures

# TODO method should be one of c('kendall','spearman','ndcg','p@k') # TODO 2010 paper rank biased overlap (available in R)
# TODO random

# apparently the differences are that Pearson benchmarks linear relationship, while Spearman benchmarks monotonic relationship (few infinities more general case, but for some power tradeoff).
# see: https://stats.stackexchange.com/questions/8071/how-to-choose-between-pearson-and-spearman-correlation

cor(,method=)

normalize = function(x){
  (x-min(x))/(max(x)-min(x))
}

path_to_grid = 'C:/Users/mvazirg/Desktop/polysemous_words/pyramid_matching/results/'
path_to_baselines = 'C:/Users/mvazirg/Desktop/polysemous_words/evaluating/scores_baselines/'

# = = = = = = = = = = = = = = = = 

method_names = list.files(path_to_baselines) # not including frequency
rankings = lapply(method_names,function(x) readLines(paste0(path_to_baselines,x)))

method_names = unlist(lapply(method_names,function(x) if (grepl('wordnet',x)){unlist(strsplit(x,split='\\.'))[1]} else {unlist(strsplit(x,split='_'))[1]}))

rankings = lapply(rankings,function(x) {
  lapply(x,function(y){
    elts = unlist(strsplit(y,split=','))
    to_return = as.numeric(elts[2])
    names(to_return) = elts[1]
    to_return
  })
})

rankings = lapply(rankings,function(x) normalize(unlist(x)))
names(rankings) = method_names


# = = 

combos = list.files(path_to_grid)
rankings_combo = lapply(combos,function(x) readLines(paste0(path_to_grid,x)))

rankings_combo = lapply(rankings_combo,function(x) {
  lapply(x,function(y){
    elts = unlist(strsplit(y,split=','))
    to_return = as.numeric(elts[2])
    names(to_return) = elts[1]
    to_return
  })
})

rankings_combo = lapply(rankings_combo,function(x) {
  u_x = unlist(x)
  if(max(u_x)==min(u_x)){
    to_return = NULL
  } else {
    to_return = normalize(u_x)
  }
  to_return
})

names(rankings_combo) = combos

lens = unlist(lapply(rankings_combo,length))

names(rankings_combo)[which(lens==0)]

rankings_combo = rankings_combo[!lens==0]
combos = combos[!lens==0]

# = = = = = = = = finding out the best combo = = = = = = = = = = = = 

stopifnot(names(rankings_combo)==combos)

mean_ndcgs = list()

for (combo in combos){
  
  evaluated = rankings_combo[[combo]]
  evaluated = evaluated[!evaluated==0] # remove entries with null scores (NA words)
  sorted_evaluated = sort(evaluated,decreasing=TRUE) # sort based on scores
  sorted_evaluated_words = names(sorted_evaluated) # retain only words
  
  ndcgs = list()
  for (gt_name in method_names){ # kept all names as a sanity check (to verify we get ones on the diagonal) 
    gt = rankings[[gt_name]]
    
    gt = gt[!gt==0] # remove entries with null score (NA words)
    
    overlapping_words = intersect(sorted_evaluated_words,names(gt))
    sorted_evaluated_words = sorted_evaluated_words[sorted_evaluated_words%in%overlapping_words]
    gt = gt[names(gt)%in%overlapping_words]
    
    # replace words in the evaluated method's ranking by their scores in the GT
    final_scores = as.numeric(gt[sorted_evaluated_words])
    truth = sort(final_scores,decreasing=TRUE)
    
    ndcgs[[gt_name]] = dcg(final_scores)/dcg(truth)
    
  }
  
  mean_ndcgs[[combo]] = mean(unlist(ndcgs))
  
}

mean_ndcgs = round(unlist(mean_ndcgs)*100,2)

sort(mean_ndcgs,decreasing=TRUE)

boxplot(mean_ndcgs)

# = = = = = = = = = = = = = = = = = = = = = = =

path_to_evaluation = 'C:/Users/mvazirg/Desktop/polysemous_words/evaluating/scores_evaluation/'

method_names = list.files(path_to_evaluation) # not including frequency
rankings = lapply(method_names,function(x) readLines(paste0(path_to_evaluation,x)))

method_names = unlist(lapply(method_names,function(x) if (grepl('wordnet',x)|grepl('pca',x)){unlist(strsplit(x,split='\\.'))[1]} else {unlist(strsplit(x,split='_'))[1]}))

rankings = lapply(rankings,function(x) {
  lapply(x,function(y){
    elts = unlist(strsplit(y,split=','))
    to_return = as.numeric(elts[2])
    names(to_return) = elts[1]
    to_return
  })
})

rankings = lapply(rankings,function(x) normalize(unlist(x)))
names(rankings) = method_names


ndcgs = matrix(nrow=length(method_names),ncol=length(method_names))

i = 1 # col index (evaluated methods)
j = 1 # row index (GTs)

for (name in method_names){ # column name
  
  evaluated = rankings[[name]]
  evaluated = evaluated[!evaluated==0] # remove entries with null scores (NA words)
  sorted_evaluated = sort(evaluated,decreasing=TRUE) # sort based on scores
  sorted_evaluated_words = names(sorted_evaluated) # retain only words

  for (gt_name in method_names){ # kept all names as a sanity check (to verify we get ones on the diagonal) 
    gt = rankings[[gt_name]]
    
    gt = gt[!gt==0] # remove entries with null score (NA words)
    
    overlapping_words = intersect(sorted_evaluated_words,names(gt))
    sorted_evaluated_words = sorted_evaluated_words[sorted_evaluated_words%in%overlapping_words]
    gt = gt[names(gt)%in%overlapping_words]
    
    # replace words in the evaluated method's ranking by their scores in the GT
    final_scores = as.numeric(gt[sorted_evaluated_words])
    truth = sort(final_scores,decreasing=TRUE)
    
    ndcgs[j,i] = dcg(final_scores)/dcg(truth)
    
    j = j + 1
    
  }
  
  j = 1
  i = i + 1
    
}

ndcgs = round(ndcgs*100,2)
rownames(ndcgs) = method_names
colnames(ndcgs) = method_names

pheatmap(ndcgs,cluster_rows=FALSE,cluster_cols=FALSE,scale='none',fontsize=20,display_numbers=TRUE,col=colorRampPalette(brewer.pal(n=7,name='Blues'))(100)[1:55],angle_col=45,main='evaluated methods as columns')



