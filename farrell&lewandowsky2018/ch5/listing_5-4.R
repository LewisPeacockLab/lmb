# listing 5.4

# Read in the data
# Rows are participants, columns are serial positions
spcdat <- read.table("freeAccuracy.txt")
#------------------------------------------
pdf(file="gap_plot.pdf", width=4, height=4)
par(mfrow=c(1,1))

library(cluster)
gskmn <- clusGap(spcdat, FUN = kmeans, nstart = 20, K.max = 8, B=500)
plot(gskmn, ylim=c(0.15, 0.5))

dev.off()

#------------------------------------------
pdf(file="kmeansSPC.pdf", width=8, height=4)
par(mfrow=c(1,2))
plot(colMeans(spcdat), ylim=c(0,1), type="b",
     xlab="Serial Position", ylab="Proportion Correct", main=NULL)

kmres <- kmeans(spdcat, centers=3, nstart=10)
matplot(t(kmres$centers), type="b", ylim=c(0,1),
        xlab="Serial Position", ylab="Proportion Correct")
dev.off()