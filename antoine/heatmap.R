library(xtable)
library(fields)
library(reticulate)
library(pheatmap)
library(RColorBrewer)

use_condaenv('my_env_3') # just a Python 3 environment with the 'rbo' module installed

rbo = import('rbo') # see https://github.com/changyaochen/rbo

method_names_en = c('wikipedia','oxford','ontonotes','wordnet_original','wordnet_restricted','wndomains')
method_names_fr = c('larousse','wikipedia')

my_metrics = c('cosine','kendall','spearman','ndcg','p@k','rbo')

# = = = = = = = = = = = = = = = = functions

dcg = function(x) {
  sum(unlist(lapply(1:length(x), function(i) (2^x[i] - 1)/log2(i+1))))
}

normalize = function(x){
  (x-min(x))/(max(x)-min(x))
}

# taken from https://stackoverflow.com/questions/18303420/how-to-map-a-vector-to-a-different-range-in-r
normalize_range = function(x,from_to){
  (x - min(x)) / max(x - min(x)) * (from_to[2] - from_to[1]) + from_to[1]
}

my_cos_sim = function(x,y){
  dot_product = sum(x*y)
  denominator = sqrt(sum(x^2)) * sqrt(sum(y^2))
  stopifnot(denominator>0)
  dot_product/denominator
}

score_ranking = function(evaluated,gt,metric){
  # evaluated and gt (ground truth) are named lists of words and their scores, sorted by decreasing order of scores
  # metric should be one of c('cosine','kendall','spearman','ndcg','p@k','rbo')
  
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
    to_return = rs$rbo(p=0.98)
    
  } else if (metric %in% c('kendall','spearman')){
    
    gt = gt[overlapping_words] # align the two rankings based on words
    evaluated = evaluated[overlapping_words]
    to_return = cor(as.numeric(evaluated),as.numeric(gt),method=metric)
    
  } else if (metric == 'p@k'){
    
    # what proportion of the top 10% evaluated words are in the top 10% ground truth words?
    top10pct_gt = names(gt)[1:round(0.1*length(gt))]
    to10pct_eval = names(evaluated)[1:round(0.1*length(evaluated))]
    to_return = length(which(to10pct_eval%in%top10pct_gt))/length(to10pct_eval)
    
  } else if (metric == 'cosine'){
    
    gt = gt[overlapping_words] # align the two rankings based on words
    evaluated = evaluated[overlapping_words]
    to_return = my_cos_sim(as.numeric(evaluated),as.numeric(gt))
    
  }
  
  to_return
  
}

# = = = = = = = = = = = = = = = = arguments

args = commandArgs(trailingOnly=TRUE)

# Rscript --vanilla heatmap.R path_root metric
# example: Rscript --vanilla heatmap.R C:/Users/mvazirg/Desktop/polysemous_words/ ndcg

new_range = c(1,100) # range to which all scores are mapped when normalizing

path_root = as.character(args[1])
metric = as.character(args[2])
language = as.character(args[3])

if (is.na(metric)){
  stop('please specify a metric')
}

if (!metric%in%my_metrics){
  stop('metric is not supported')
}

if (is.na(language)){
  stop('please specify a language')
}

if (!language%in%c('english','french')){
  stop(paste(language,'is currently not supported!'))
}

if (language=='english'){
  method_names_optim = method_names_en
}

if (language=='french'){
  method_names_optim = method_names_fr
}

# relevant links about rbo:
# - http://codalism.com/research/papers/wmz10_tois.pdf 

path_to_plots = paste0(path_root,'/antoine/plots/',language,'/')
path_to_grid = paste0(path_root,'/pyramid_matching/results/',language,'/')
path_to_baselines = paste0(path_root,'/evaluating/',language,'/scores_baselines/')
path_to_evaluation = paste0(path_root,'/evaluating/',language,'/scores_evaluation/')
path_to_best_combos = paste0(path_root,'/evaluating/',language,'/best_combos_per_metric/')
path_to_save_console = paste0(path_root,'/antoine/console_output/',language,'/')

con = file(paste0(path_to_save_console,metric,'_output_console.txt'))
sink(con, append=TRUE)

# = = = = = = = = = = = = = = = = finding best parameter combination

method_names = list.files(path_to_baselines) # not including frequency!
rankings = lapply(method_names,function(x) readLines(paste0(path_to_baselines,x)))

method_names = unlist(lapply(method_names,function(x) if (grepl('wordnet',x)){unlist(strsplit(x,split='\\.'))[1]} else {unlist(strsplit(x,split='_'))[1]}))

for_latex = unlist(lapply(rankings,length)) # original lengths

rankings = lapply(rankings,function(x) {
  lapply(x,function(y){
    elts = unlist(strsplit(y,split=','))
    to_return = as.numeric(elts[2])
    names(to_return) = elts[1]
    to_return = to_return[!to_return==0] # remove entries with null score (NA words)
    to_return
  })
})

for_latex = rbind(for_latex,unlist(lapply(rankings,length))) # after removing 0-score words
rownames(for_latex) = c('before','after')
colnames(for_latex) = method_names
print(xtable(for_latex))

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

# remove combinations for which there is no ranking (the scores were all the same, so normalization failed)
# this corresponds to the combinations with only one level in the pyramid
lens = unlist(lapply(rankings_combo,length))
names(rankings_combo)[which(lens==0)]
rankings_combo = rankings_combo[!lens==0]
combos = combos[!lens==0]

# = = = = = = = = finding out the best combo = = = = = = = = = = = = 

# the best combo is the one that for a given metric, performs the best across all methods (on average)

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

# = = generate heatmap of scores vs PCA dimensions vs pyramid levels = =

pca_dims = unlist(lapply(names(mean_scores), function(x) unlist(strsplit(x,split='_'))[1]))
pca_dims = sort(unique(as.numeric(gsub('pca','',pca_dims))),decreasing=FALSE)

my_levels = unlist(lapply(names(mean_scores), function(x) unlist(strsplit(x,split='_'))[2]))
my_levels = sort(unique(as.numeric(gsub('L','',my_levels))),decreasing=FALSE)

for_heatmap = matrix(nrow=length(my_levels),ncol=length(pca_dims))

for (i in 1:length(my_levels)){
  for (j in 1:length(pca_dims)){
    for_heatmap[i,j] = mean_scores[[paste0('pca',pca_dims[j],'_L',my_levels[i])]]
  }
}

pdf(paste0(path_to_plots,'heatmap_parameters_',metric,'.pdf'),paper='a4r',width=7.5,height=7.5)

x = my_levels
y = pca_dims
z = t(apply(for_heatmap, 2, rev)) # see: https://stackoverflow.com/questions/31882079/r-image-plots-matrix-rotated

image.plot(z,col=colorRampPalette(brewer.pal(n=7,name='Blues'))(100)[1:100],xaxt='n',yaxt='n',xlab='nb of PCA dimensions',ylab='nb of pyramid levels',main=metric,cex.main=2.5,cex.lab=1.5)

axis(1,at=seq(0,1,length.out=length(y)),label=y)
axis(2,at=seq(0,1,length.out=length(x)),label=rev(x))

dev.off()


# = = generate LaTeX table = =

#  (will be saved to text file where console output is re-directed)

mean_scores = sort(mean_scores,decreasing=TRUE)
to_print = as.data.frame(c(head(mean_scores),tail(mean_scores)))
best_name = rownames(to_print)[1]
rownames(to_print) = gsub('pca','D',rownames(to_print))
rownames(to_print) = gsub('\\_','',rownames(to_print))
print(xtable(to_print))

# = = = =

best_name_renamed = rownames(to_print)[1]

pdf(paste0(path_to_plots,'boxplot_',metric,'.pdf'),width=4,height=6.5,paper='a4')
    
    par(mgp=c(1.5,0.5,0)) # title, tick labels, ticks
    par(mar=c(8,4,8,4)) # bottom, left, top, right
    
    boxplot(mean_scores,ylab=paste(metric,'(%)'),boxwex=0.8)
    title(paste(metric,'distribution'), sub=paste0('n=',length(mean_scores)),line=0.5)
    
dev.off()

# = = = = = = = = = = = = = = = = = = = = = = =

file.copy(from=paste0(path_to_grid,best_name),to=paste0(path_to_evaluation,best_name_renamed),overwrite=TRUE)

file.copy(from=paste0(path_to_grid,best_name),to=paste0(path_to_best_combos,best_name_renamed),overwrite=TRUE)


method_names = list.files(path_to_evaluation)

rankings = lapply(method_names,function(x) readLines(paste0(path_to_evaluation,x))) # this time, including frequency!

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

# plot average distribution of GT rankings (including 'frequency')
all_points_gt = c(rankings[['frequency']],rankings[['ontonotes']],rankings[['oxford']],rankings[['wikipedia']],rankings[['wndomains']],rankings[['wordnet_original']],rankings[['wordnet_restricted']])


pdf(paste0(path_to_plots,'random_distribution_vs_all.pdf'),paper='a4r',width=5,height=5)

hist(all_points_gt,probability=TRUE,xlab='normalized scores',ylab='probability',
     main=NULL,col='skyblue',border=FALSE, ylim=c(0,0.07))

n_runs = 30
rankings[['random']] = lapply(1:n_runs,function(x){
  to_return = rlnorm(length(rankings[['frequency']]),meanlog=0,sdlog=0.6) # sample from lognormal distribution
  names(to_return) = sample(names(rankings[['frequency']]),length(rankings[['frequency']]),replace=FALSE)
  sort(normalize_range(to_return,new_range),decreasing=TRUE)
})

avg_random = unlist(rankings[['random']])
avg_random_density = density(avg_random)

lines(avg_random_density$x,avg_random_density$y, lwd=2, col='blue')

dev.off()

# re-order/re-name to optimize the heatmap (our method, random, and frequency first)
method_names = c(c(best_name_renamed,'random','frequency'),method_names_optim)
method_names_pretty = gsub('wikipedia','wiki',method_names)
method_names_pretty = gsub('random','rand',method_names_pretty)
method_names_pretty = gsub('frequency','freq',method_names_pretty)
method_names_pretty = gsub('oxford','oxf',method_names_pretty)
method_names_pretty = gsub('ontonotes','ON',method_names_pretty)
method_names_pretty = gsub('wordnet_','wn',method_names_pretty)
method_names_pretty = gsub('wn','WN',method_names_pretty)
method_names_pretty = gsub('original','',method_names_pretty)
method_names_pretty = gsub('domains','dom',method_names_pretty)
method_names_pretty = gsub('restricted','red',method_names_pretty)

pdf(paste0(path_to_plots,'score_distributions.pdf'),paper='a4r',width=10,height=7)
    
    par(mfrow=c(2,4))
    
    method_counter = 1
    
    for (name in tail(method_names,-1)){ # all except pyramid (will be plotted separately)
      if (name=='random'){
        to_hist = rankings[[name]][[1]]
      } else {
        to_hist = rankings[[name]]
      }
      hist(to_hist,xlim=new_range,col='skyblue',border=FALSE,main=tail(method_names_pretty,-1)[[method_counter]],xlab='normalized scores',ylab='counts')
      method_counter = method_counter + 1
    }
    
dev.off()

# we plot the heatmap of average performance (across all methods) for each combination of D and L parameters

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

if (metric != 'ndcg'){ # symmetric metric, show only one triangle
  scores[upper.tri(scores)] = NA
  scores_show = scores
  scores_show[upper.tri(scores_show)] = ''
} else {
  scores_show = scores
}

pdf(paste0(path_to_plots,'heatmap_',metric,'.pdf'),paper='a4r',width=15,height=7.5)
    
    pheatmap(scores,cluster_rows=FALSE,cluster_cols=FALSE,scale='none',fontsize=20,display_numbers=scores_show,col=colorRampPalette(brewer.pal(n=7,name='Blues'))(100)[1:55],angle_col=45,main=metric,na_col='#FFFFFF') # evaluated methods as columns
    
dev.off()

sink()
