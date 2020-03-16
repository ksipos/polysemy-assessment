# if words are ranked the same way/in reversed way, both methods return 1 or -1
cor(c(1,2,10,100,1000),c(1,2,3,4,5),method='kendall')
cor(c(1,2,10,100,1000),c(1,2,3,4,5),method='spearman')

# if rankings differ, methods differ
cor(c(1,2,10,100,1000),c(2,1,3,4,5),method='spearman')
cor(c(1,2,10,100,1000),c(2,1,3,4,5),method='kendall')

# spearman equals pearson on the ranks
cor(c(1,2,10,100,1000),c(2,1,3,4,5),method='spearman')
cor(order(c(1,2,10,100,1000)),order(c(2,1,3,4,5)),method='pearson')

# = = computing kendall by hand = =

x = order(c(1,2,10,100,1000))
y = order(c(2,1,3,4,5))
n = length(x)


n_concordant = 0
n_discordant = 0

for (i in 1:(n-1)){
  for (j in i:n){
    if (i == j){
      next
    }
    cat('\n',i,j)
    if (x[i] < x[j] & y[i] < y[j]){
      n_concordant = n_concordant + 1
    } else {
      n_discordant = n_discordant + 1
    }
  }
}

tau = 2*(n_concordant - n_discordant)/(n*(n-1))

tau # which is equal to cor(x,y,method='kendall')


# = = = more compact way = = =

sum = 0 
for (i in 1:(n-1)){
  for (j in i:n){
    if (i == j){
      next
    }
    sum = sum + sign(x[i] - x[j]) * sign(y[i] - y[j])
  }
}

tau = 2*sum/(n*(n-1))

tau

