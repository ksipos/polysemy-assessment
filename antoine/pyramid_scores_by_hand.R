my_score = function(level,n_levels,coverage){
  coverage/(2^(n_levels-level))
}

levels = 1:3

# word 1
covs = c(3/4,7/16,10/64)
sum(unlist(lapply(levels,function(level) my_score(level,length(levels),covs[level]))))

# word 2
covs = c(1/4,4/16,7/64)
sum(unlist(lapply(levels,function(level) my_score(level,length(levels),covs[level]))))


