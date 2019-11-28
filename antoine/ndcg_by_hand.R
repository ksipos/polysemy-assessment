
dcg = function(x) {
  sum(unlist(lapply(1:length(x), function(i) (2^x[i] - 1)/log(i+1))))
}

# = = = = = 

ours = c(7,9,8,10,6,5,4,3,2,1)
truth = rev(1:10)

dcg(ours)/dcg(truth)

# = = = = = = = random baseline simulation = = = = = = =

truth = rev(1:100)
dcg_truth = dcg(truth)

scores = lapply(1:200, function(run) {
  ours = sample(1:100,100)
  dcg(ours)/dcg_truth
})

mean(unlist(scores))


truth = rev(1:100) + 900 # the values of the scores do not change the results (+-900)
dcg_truth = dcg(truth)

scores = lapply(1:200, function(run) {
  ours = sample(1:100,100) + 900
  dcg(ours)/dcg_truth
})

mean(unlist(scores))


