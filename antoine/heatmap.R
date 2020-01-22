#!/usr/bin/Rscript

library(reticulate)
library(pheatmap)
library(RColorBrewer)

use_condaenv('my_env_3')

rbo = import('rbo') # see https://github.com/changyaochen/rbo

# = = = = = = = = = = = = = = = = functions

dcg = function(x) {
  sum(unlist(lapply(1:length(x), function(i) (2^x[i] - 1)/log2(i+1))))
}

normalize = function(x){
  (x-min(x))/(max(x)-min(x))
}

# taken from https://stackoverflow.com/questions/18303420/how-to-map-a-vector-to-a-different-range-in-r
normalize_range = function(x, from_to){
  (x - min(x)) / max(x - min(x)) * (from_to[2] - from_to[1]) + from_to[1]
}


score_ranking = function(evaluated,gt,metric){
  # evaluated and gt are named lists of words and their scores, sorted by decreasing order of scores
  # metric should be one of c('kendall','spearman','ndcg','p@k','rbo')
  
  evaluated_words = names(evaluated)
  overlapping_words = intersect(evaluated_words,names(gt))
  
  evaluated = evaluated[evaluated_words%in%overlapping_words]
  evaluated_words = evaluated_words[evaluated_words%in%overlapping_words]
  gt = gt[names(gt)%in%overlapping_words]
  
  if (metric=='ndcg'){
    
    final_scores = as.numeric(gt[evaluated_words]) # replace words in the evaluated method's ranking by their scores in the GT
    truth = sort(final_scores,decreasing=TRUE) # best possible way to position the evaluated words
    to_return = dcg(final_scores)/dcg(truth)
    
  } else if (metric=='rbo'){
    
    # rbo accepts lists of unique elements only, so we replace the ground truth scores by unique integers
    # ! the assumption is that gt is already sorted by decreasing order!
    names_gt = names(gt)
    gt = normalize_range(rev(1:length(gt)),c(1,100))
    names(gt) = names_gt
    
    final_scores = as.numeric(gt[evaluated_words]) # replace words in the evaluated method's ranking by their scores in the GT
    
    truth = sort(final_scores,decreasing=TRUE) # best possible way to position the evaluated words
    
    rs = rbo$RankingSimilarity(final_scores,truth)
    to_return = rs$rbo(p=0.9)
    
  } else if (metric %in% c('kendall','spearman')){
    
    gt = gt[overlapping_words] # align the two rankings based on words
    to_return = cor(as.numeric(evaluated),as.numeric(gt),method=metric)
    
  } else if (metric == 'p@k'){
    
    # what proportion of the top 10% evaluated words are in the top 10% ground truth words?
    top10pct_gt = names(gt)[1:round(0.1*length(gt))]
    to10pct_eval = names(evaluated)[1:round(0.1*length(evaluated))]
    to_return = length(which(to10pct_eval%in%top10pct_gt))/length(to10pct_eval)
    
  }
  
  to_return
  
}

# = = = = = = = = = = = = = = = =

#args = commandArgs(trailingOnly=TRUE)

# Rscript --vanilla heatmap.R path_root metric get_best
# example: Rscript --vanilla heatmap.R C:/Users/mvazirg/Desktop/polysemous_words/ ndcg 1

# if get_best==1, the best parameter combination is obtained
# if get_best==0, the best parameter combination (whose ranking should have been copied from '.\pyramid_matching\results\' to 'path_to_evaluation' and renamed, e.g., 'D6L11') is compared to the ground truths

new_range = c(1,100) # range to which all scores are mapped when normalizing

best_name = 'foo' #'D6L12'

path_root = 'C:/Users/mvazirg/Desktop/polysemous_words/' #as.character(args[1])
metric = 'rbo' #as.character(args[2])
get_best = 0 #as.numeric(args[3])

if (!metric%in%c('kendall','spearman','ndcg','p@k','rbo')){
  stop("metric is not one of 'kendall','spearman','ndcg','p@k','rbo'")
}

# relevant links about the metrics:
# - https://en.wikipedia.org/wiki/Learning_to_rank#Evaluation_measures
# see: https://stats.stackexchange.com/questions/8071/how-to-choose-between-pearson-and-spearman-correlation
# - http://codalism.com/research/papers/wmz10_tois.pdf 

path_to_plots = paste0(path_root,'/antoine/plots/')
path_to_grid = paste0(path_root,'/pyramid_matching/results/')
path_to_baselines = paste0(path_root,'/evaluating/scores_baselines/')
path_to_evaluation = paste0(path_root,'/evaluating/scores_evaluation/')

# = = = = = = = = = = = = = = = =

if(get_best==1){
  
  method_names = list.files(path_to_baselines) # not including frequency
  rankings = lapply(method_names,function(x) readLines(paste0(path_to_baselines,x)))
  
  method_names = unlist(lapply(method_names,function(x) if (grepl('wordnet',x)){unlist(strsplit(x,split='\\.'))[1]} else {unlist(strsplit(x,split='_'))[1]}))
  
  rankings = lapply(rankings,function(x) {
    lapply(x,function(y){
      elts = unlist(strsplit(y,split=','))
      to_return = as.numeric(elts[2])
      names(to_return) = elts[1]
      to_return = to_return[!to_return==0] # remove entries with null score (NA words)
      to_return
    })
  })
  
  rankings = lapply(rankings,function(x) sort(normalize_range(unlist(x),new_range),decreasing=TRUE))
  names(rankings) = method_names
  
  # = = = = = = = = = = = = = = = =
  
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
      u_x = u_x[!u_x==0] # remove entries with null score (NA words)
      to_return = normalize_range(u_x,new_range)
    }
    sort(to_return,decreasing=TRUE)
  })
  
  names(rankings_combo) = combos
  
  # remove combinations for which the scores are all the same
  lens = unlist(lapply(rankings_combo,length))
  names(rankings_combo)[which(lens==0)]
  rankings_combo = rankings_combo[!lens==0]
  combos = combos[!lens==0]
  
  # = = = = = = = = finding out the best combo = = = = = = = = = = = = 
  
  stopifnot(names(rankings_combo)==combos)
  
  mean_scores = list()
  
  for (combo in combos){
    
    evaluated = rankings_combo[[combo]]
    
    scores = list()
    for (gt_name in method_names){ # kept all names as a sanity check (to verify we get ones on the diagonal) 
      gt = rankings[[gt_name]]
      scores[[gt_name]] = score_ranking(evaluated,gt,metric)
    }
    
    mean_scores[[combo]] = mean(unlist(scores))
    
  }
  
  mean_scores = round(unlist(mean_scores)*100,2)
  
  cat('\n best combos:\n')
  print(head(sort(mean_scores,decreasing=TRUE)))
  cat('\n worst combos:\n')
  print(tail(sort(mean_scores,decreasing=TRUE)))
  cat('\n * * * best combo:',names(sort(mean_scores,decreasing=TRUE))[1],'* * *')
  
  pdf(paste0(path_to_plots,'boxplot_',metric,'.pdf'),width=4,height=6.5,paper='a4')
      
      par(mgp=c(1.5,0.5,0)) # title, tick labels, ticks
      par(mar=c(8,4,8,4)) # bottom, left, top, right
      
      boxplot(mean_scores,ylab=paste(metric,'(%)'),boxwex=0.8)
      title(paste(metric,'distribution'), sub=paste0('n=',length(mean_scores)),line=0.5)
      
  dev.off()

}

# = = = = = = = = = = = = = = = = = = = = = = =

if (get_best==0){
  
  method_names = list.files(path_to_evaluation) # should not include frequency
  
  rankings = lapply(method_names,function(x) readLines(paste0(path_to_evaluation,x)))
  
  method_names = unlist(lapply(method_names,function(x) if (grepl('wordnet',x)){unlist(strsplit(x,split='\\.'))[1]} else {unlist(strsplit(x,split='_'))[1]}))
  
  rankings = lapply(rankings,function(x) {
    lapply(x,function(y){
      elts = unlist(strsplit(y,split=','))
      to_return = as.numeric(elts[2])
      names(to_return) = elts[1]
      to_return = to_return[!to_return==0] # remove entries with null score (NA words)
      to_return
    })
  })
  
  rankings = lapply(rankings,function(x) sort(normalize_range(unlist(x),new_range),decreasing=TRUE))
  names(rankings) = method_names
  
  avg_len = round(mean(unlist(lapply(rankings,length))))
  
  n_runs = 30
  rankings[['random']] = lapply(1:n_runs,function(x){
    to_return = rlnorm(avg_len,meanlog=0,sdlog=1) # sample from lognormal distribution
    names(to_return) = sample(names(rankings[['frequency']]),avg_len,replace=FALSE)
    sort(normalize_range(to_return,new_range),decreasing=TRUE)
  })
  
  # re-order/re-name to optimize the heatmap (our method, random, and frequency first)
 method_names = c(best_name,'random','frequency','google','ontonotes','wikipedia','wndomains','wordnet_original','wordnet_restricted')
 method_names_pretty = gsub('_',' ',method_names)
  
  pdf(paste0(path_to_plots,'score_distributions.pdf'),paper='a4r',width=10,height=7)
      
      par(mfrow=c(2,4))
      
      for (name in tail(method_names,-1)){ # all except pyramid (will be plotted separately)
        if (name=='random'){
          to_hist = rankings[[name]][[1]]
        } else {
          to_hist = rankings[[name]]
        }
        hist(to_hist,xlim=new_range,col='skyblue',border=FALSE,main=name,xlab='normalized scores',ylab='counts')
      }
      
  dev.off()
  
  
  scores = matrix(nrow=length(method_names),ncol=length(method_names))
  i = 1 # col index (evaluated methods)
  j = 1 # row index (GTs)
  
  for (name in method_names){ # column name
    
    evaluated = rankings[[name]]
    
    for (gt_name in method_names){ # kept all names as a sanity check (to verify we get ones on the diagonal) 
      gt = rankings[[gt_name]]
      
      if (name == 'random' & gt_name != 'random'){
        all_scores = unlist(lapply(evaluated,function(x) score_ranking(x,gt,metric)))
        scores[j,i] = mean(all_scores)
      } else if (name != 'random' & gt_name == 'random'){
        all_scores = unlist(lapply(gt,function(x) score_ranking(evaluated,x,metric)))
        scores[j,i] = mean(all_scores)
      } else if (name == 'random' & gt_name == 'random'){
        all_scores = unlist(lapply(evaluated,function(x){
          mean(unlist(lapply(gt,function(y) score_ranking(x,y,metric))))
        }))
        scores[j,i] = mean(all_scores)
      } else {
      scores[j,i] = score_ranking(evaluated,gt,metric)
      }
      
      j = j + 1
      
    }
    
    j = 1
    i = i + 1
    
  }
  
  scores = round(scores*100,2)
  rownames(scores) = method_names_pretty
  colnames(scores) = method_names_pretty
  
  pdf(paste0(path_to_plots,'heatmap_',metric,'.pdf'),paper='a4r',width=15,height=7.5)
      
      pheatmap(scores,cluster_rows=FALSE,cluster_cols=FALSE,scale='none',fontsize=18,display_numbers=TRUE,col=colorRampPalette(brewer.pal(n=7,name='Blues'))(100)[1:55],angle_col=45,main=metric) # evaluated methods as columns
      
  dev.off()
  
}

