import sys
import random
from numpy import ndarray

MAX_K=5
MAX_N=500

d_matrix = ndarray((MAX_N, MAX_N))
f_matrix = ndarray((MAX_K, MAX_N, MAX_N))


def main():

	n_fac = 30 # number of facilities/locations in the QAP
	n_k = 2
	corr = 0
	max_flow = 100
	max_dist = 100

	arg = sys.argv[1:]
	if len(arg) == 1:
		if arg[0] == "-h":
			print("You have requested help with the -h argument. \nOther optional parameters are: -n positive integer : number of facilities/locations -k positive integer : number of objectives -c1 real in the interval [-1,1]: correlation between objectives 1 and 2 -c2 real in the interval [-1,1]: correlation between objectives 1 and 3 -c3 real in the interval [-1,1]: correlation between objectives 1 and 4 -c4 real in the interval [-1,1]: correlation between objectives 1 and 5 -ov real in the interval [0:1]: sets the fraction of flows that are correlated -A integer : flow control parameter (must be set less than B; negative values cause a sparse matrix) -B positive integer : flow control parameter -K positive integer : maximum number of points in a small cluster  -M non-negative integer : radius of large clusters -m non-negative integer : radius of small clusters -s positive long : random seed\n Default values are: n = 30, k = 2, c1 = 0, c2 = 0, c3 = 0, c4 = 0, A = -5, B = 5, m = 100, M = 0, K = 1, ov = 0.7, s = 23453464")
			sys.exit()

	if len(arg) > 1 and len(arg)%2 == 0:
		for i in range(0,len(arg),2):
			if arg[i] == "-n":
				n_fac = arg[i+1]
			elif arg[i] == "-k":
				n_k = arg[i+1]
			elif arg[i] == "-c":
				corr = arg[i+1]
			elif arg[i] == "-f":
				max_flow = arg[i+1]
			elif arg[i] == "-d":
				max_dist = arg[i+1]
			elif arg[i] == "-s":
				seed = arg[i+1]
			else:
				print("Undefined command line parameter entered. Do \"./makeQAPrl -h\" for help with parameters.")
				sys.exit()

	if int(n_fac) > int(MAX_N) :
		print("Number of facilities too high. Maximum is currently set at "+str(MAX_N));
		sys.exit()

	if float(corr) > 1.0 or float(corr) < (-1.0):
			print("Correlations must be in the interval [-1,1]")
			sys.exit()

	if int(n_k) > int(MAX_K):
		print("number of objectives too high. Maximum is currently set at "+str(MAX_K))
		sys.exit()


	for i in range(0,int(n_fac)):
		for j in range(0,int(n_fac)):
			if i == j:
				d_matrix[i][i]=0
			else:
				d1 = 1 + int(max_dist*random.random())
				d_matrix[i][j]=d1
				d_matrix[j][i]=d1

		for i in range(0,int(n_fac)):
			for j in range(0,int(n_fac)):
				if i == j:
					f_matrix[0][i][i]=0
				else:
					r1 = random.random()
					f1 = 1+int(max_flow*r1)
					f_matrix[0][i][j]=f1
					f_matrix[0][j][i]=f1
					for k in range(1,int(n_k)):
						if i == j:
							f_matrix[k][i][i]=0
						else:
							r2 = random.random()
							if corr >= 0:
								fk = 1+int(max_flow*correl_val(r1,corr))
							else:
								fk = 1+int(max_flow*(1.0-correl_val(r1,corr)))
							f_matrix[k][i][j]=fk
							f_matrix[k][j][i]=fk
	print_output(int(n_k),int(n_fac))

def correl_val(v,c):
	p = 0.5
	if c == 1:
		return v

	if c == 0:
		return random.random()

	while True:
		q = random.random()
		diff = q - v
		if diff < 0:
			diff*=-1
		w = math.exp(-(diff*diff)/(2.0*(1.0-math.pow(c,p))*(1.0-math.pow(c,p))))/(1.0-math.pow(c,p))*2.506
		r = random.random()*1.0/(1.0-math.pow(c,p))*2.506
		if w >= r:
			break
	return q

	
def print_output(n_k,n_fac):
	print (str(n_k)+" "+str(n_fac))

	for i in range (0,n_fac):
		for j in range (0,n_fac):
			print int(d_matrix[i][j]),
		print("")

	for k in range(0,n_k):
		print("")
		for i in range(0,n_fac):
			for j in range(0,n_fac):
				print int(f_matrix[k][i][j]),
			print("")

if __name__ == '__main__':
    main()