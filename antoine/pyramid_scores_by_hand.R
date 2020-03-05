levels = 0:2

n_dims = 2
n_bins = unlist(lapply(levels,function(x) 2^(x*n_dims)))

# word 1
covs = c(3,7,10)/n_bins
sum(unlist(lapply(levels,function(level) covs[level+1]/(2^(max(levels)-level)))))

# word 2
covs = c(1,4,7)/n_bins
sum(unlist(lapply(levels,function(level) covs[level+1]/(2^(max(levels)-level)))))


