
#library(crop)

path_to_plot = './'

col1 = 'tomato1'
col2 = 'steelblue1'

pdf(paste0(path_to_plot,'pyramid_illustration.pdf'),paper='a4r')

par(mar=c(18.5,1.5,18.5,0)) # bottom, left, top, and right
par(mfrow=c(1,3))
par(mgp=c(0.5,0,0))

set.seed(11272019)
plot(rnorm(10,0,1.1),rnorm(10,0,1.1),xlab='dimension 1',ylab='dimension 2',pch=16,cex=2,col=col2,xaxt='n',yaxt='n')
title('level 1',line=1)
points(rnorm(10,-0.35,0.4),rnorm(10,-1.1,0.4),pch=15,cex=1.7,col=col1)
grid(lwd=1,lty='solid',col='grey',nx=2,ny=0)
grid(lwd=1,lty='dashed',col='grey',nx=0,ny=2)
legend('topright',legend=c('word 1','word 2'),pch=c(16,15),col=c(col2,col1),bg='white')

set.seed(11272019)
plot(rnorm(10,0,1.1),rnorm(10,0,1.1),xlab='dimension 1',ylab='dimension 2',pch=16,cex=2,col=col2,xaxt='n',yaxt='n')
title('level 2',line=1)
points(rnorm(10,-0.35,0.4),rnorm(10,-1.1,0.4),pch=15,cex=1.7,col=col1)
grid(lwd=1,lty='solid',col='grey',nx=4,ny=0)
grid(lwd=1,lty='dashed',col='grey',nx=0,ny=4)

set.seed(11272019)
plot(rnorm(10,0,1.1),rnorm(10,0,1.1),xlab='dimension 1',ylab='dimension 2',pch=16,cex=2,col=col2,xaxt='n',yaxt='n')
title('level 3',line=1)
points(rnorm(10,-0.35,0.4),rnorm(10,-1.1,0.4),pch=15,cex=1.7,col=col1)
grid(lwd=1,lty='solid',col='grey',nx=8,ny=0)
grid(lwd=1,lty='dashed',col='grey',nx=0,ny=8)

dev.off()
