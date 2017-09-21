import sys
from numpy import ndarray
import math
import random

MAX_K=5
MAX_N=500
XYpos = ndarray((MAX_N, 2))
d_matrix = ndarray((MAX_N, MAX_N))
f_matrix = ndarray((MAX_K, MAX_N, MAX_N))
n_fac = 30 # number of facilities/locations in the QAP
n_k = 2
overlap=1.0


def main():

	corr=ndarray((MAX_N,),float)
	
	M=0
	K=1
	m=100
	A=-5
	B=5
	
	n_fac = 30 # number of facilities/locations in the QAP
	n_k = 2
	overlap=1.0

	arg = sys.argv[1:]
	if len(arg) == 1:
		if arg[0] == "-h":
			print("You have requested help with the -h argument. \nOther optional parameters are: -n positive integer : number of facilities/locations -k positive integer : number of objectives -c1 real in the interval [-1,1]: correlation between objectives 1 and 2 -c2 real in the interval [-1,1]: correlation between objectives 1 and 3 -c3 real in the interval [-1,1]: correlation between objectives 1 and 4 -c4 real in the interval [-1,1]: correlation between objectives 1 and 5 -ov real in the interval [0:1]: sets the fraction of flows that are correlated -A integer : flow control parameter (must be set less than B; negative values cause a sparse matrix) -B positive integer : flow control parameter -K positive integer : maximum number of points in a small cluster  -M non-negative integer : radius of large clusters -m non-negative integer : radius of small clusters -s positive long : random seed\n Default values are: n = 30, k = 2, c1 = 0, c2 = 0, c3 = 0, c4 = 0, A = -5, B = 5, m = 100, M = 0, K = 1, ov = 0.7, s = 23453464")
			sys.exit()

	if len(arg) > 1 and len(arg)%2 == 0:
		for i in range(0,len(arg),2):
			if arg[i] == "-n":
				n_fac = arg[i+1]
			elif arg[i] == "-A":
				A = arg[i+1]
			elif arg[i] == "-B":
				B = arg[i+1]
			elif arg[i] == "-M":
				M = arg[i+1]
			elif arg[i] == "-K":
				K = arg[i+1]
			elif arg[i] == "-m":
				m = arg[i+1]
			elif arg[i] == "-ov":
				overlap = arg[i+1]
			elif arg[i] == "-k":
				n_k = arg[i+1]
			elif arg[i] == "-c1":
				corr[1] = arg[i+1]
			elif arg[i] == "-c2":
				corr[2] = arg[i+1]
			elif arg[i] == "-c3":
				corr[3] = arg[i+1]
			elif arg[i] == "-c4":
				corr[4] = arg[i+1]
			elif arg[i] == "-s":
				seed = arg[i+1]
			else:
				print("Undefined command line parameter entered. Do \"./makeQAPrl -h\" for help with parameters.")
				sys.exit()

	if int(n_fac) > int(MAX_N) :
		print("Number of facilities too high. Maximum is currently set at "+str(MAX_N));
		sys.exit()

	for k in range(0,int(n_k)):
		if corr[k] > 1.0 or corr[k] < (-1.0):
			print("Correlations must be in the interval [-1,1]")
			sys.exit()

	if int(n_k) > int(MAX_K):
		print("number of objectives too high. Maximum is currently set at "+str(MAX_K))
		sys.exit()

	if int(B) < 0:
		print("B must be a positive integer")
		sys.exit()

	if int(A) >= int(B):
		print("A must be less than B")
		sys.exit()

	if int(K) < 0:
		print("K must be a positive integer")
		sys.exit()

	if int(M) < 0:
		print("M must be a positive integer")
		sys.exit()

	if int(m) < 0:
		print("m must be a positive integer")
		sys.exit()
	
	point_in_plane(M, K, m, n_fac);

	max_dist=0
	for i in range(0,int(n_fac)):
		for j in range(0,int(n_fac)):
			d1=int(math.sqrt((XYpos[i][0]-XYpos[j][0])*(XYpos[i][0]-XYpos[j][0])+ ((XYpos[i][1]-XYpos[j][1]))*((XYpos[i][1]-XYpos[j][1]))))
			d_matrix[i][j] = d1
			d_matrix[j][i] = d1
			if d1 > max_dist:
				max_dist = d1

	max_flow=0

	for i in range(0,int(n_fac)):
		for j in range(0,int(n_fac)):
			if i == j:
				f_matrix[0][i][i]=0
			else:
				r1 = random.random()
				f1 = int(math.pow(10,((int(B)-int(A))*r1+int(A))))
				f_matrix[0][i][j] = f1
				f_matrix[0][j][i] = f1
				if f1 > max_flow:
					max_flow = f1
				for k in range(1,int(n_k)):
					if i == j:
						f_matrix[k][i][i]=0
					else:
						r2 = random.random()
						if r2 > int(overlap):
							if f_matrix[0][i][j] == 0:
								r2 = random.random()*int(B)
								fk = int(math.pow(10,r2))
								f_matrix[k][i][j] = fk
								f_matrix[k][j][i] = fk
							else:
								fk = 0
								f_matrix[k][i][j] = fk
								f_matrix[k][j][i] = fk
						else:
							r2 = random.random()
							if int(corr[k]) >= 0:
								val = correl_val(r1,corr[k])
							else:
								val = 1.0 - correl_val(r1,-corr[k])
							fk = int(math.pow(10,((int(B)-int(A))*val+int(A))))
							f_matrix[k][i][j] = fk
							f_matrix[k][j][i] = fk

					if fk > max_flow:
						max_flow = fk

	print_output(int(n_k))



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


def print_output(n_k):
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



def point_in_plane(M, K, m, max_points):
	num_points=0
	
	while num_points < int(max_points):
		Theta = random.random()*2*math.pi
		R = int(random.random() * M)
		N = int((random.random() * K) + 1)
		for i in range (0,N):
			if num_points < int(max_points):
				theta = random.random()*2*math.pi
				r = int(random.random()*m)
				XYpos[num_points][0] = int(R * math.cos(Theta) + r * math.cos(theta))
				XYpos[num_points][1] = int(R * math.sin(Theta) + r * math.sin(theta))
				num_points+=1


if __name__ == '__main__':
    main()



