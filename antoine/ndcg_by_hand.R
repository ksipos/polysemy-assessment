
dcg = function(x) {
  sum(unlist(lapply(1:length(x), function(i) (2^x[i] - 1)/log(i+1))))
}

ours = c(7,9,8,10,6,5,4,3,2,1)
truth = rev(1:10)

dcg(ours)/dcg(truth)


# random baseline simulation
scores = list()
for (run in 1:10){
  ours = sample(1:10,10)
  scores[[run]] = dcg(ours)/dcg(truth)
}

mean(unlist(scores))


