#Big old model
model {
	#Priors: all are uniform
	p ~ dbeta(1,1)
	q ~ dbeta(1,1)
	c ~ dbeta(1,1)
	
	#Data: multinomial as a function of predicted probabilites
	consistent[1:4] ~ dmulti(predprob[1,1:4],Nsubj[1])
	inconsistent[1:4] ~ dmulti(predprob[2,1:4],Nsubj[2])
	neutral[1:4] ~ dmulti(predprob[3,1:4],Nsubj[3])
	
	#Predictions for all three conditions
	#Row numbers rever to Table X.1
	
	#Consistent Condition
	predprob[1,1] = (1+p+q - p*q + 4 * p*c)/6 #row 1
	predprob[1,2] = (1 + p+q-p*q-2*p*c)/3 #row 2
	predprob[1,3] = (1 - p - q + p*q)/6 #row 3
	predprob[1,4] = (1 - p - q + p*q)/3 #row 4
	
	#Inconsistent condition
	predprob[2,1] = (1+p-q+p*q+4*p*c)/6 #row 5
	predprob[2,2] = (1 + p -q + p*q -2 * p*c)/3 #row 6
	predprob[2,3] = (1-p+q-p*q)/6 #row 7
	predprob[2,4] = (1-p+q-p*q)/3 #row 8
	
	#Neutral condition
	predprob[3,1] = (1+p+4*p*c)/6 #row 9
	predprob[3,2] = (1+p-2*p*c)/3 #row 10
	predprob[3,3] = (1-p)/6 #row 11
	predprob[3,4] = (1-p)/3 #row 12
}