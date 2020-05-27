import numpy as np
import sys
import csv
import random
import math

advertiser_dict = {}
queries = []
query_dict = {}

if len(sys.argv) != 2:
    print('python adwords.py algorithm')
    sys.exit(1)

algorithm = sys.argv[1]

file = open('queries.txt','r')
reader = csv.reader(file)
for line in reader:
	queries.append(line[0])

def findQuery():
	file1 = open('bidder_dataset.csv','r')
	reader = csv.reader(file1)
	next(reader,None)
	for line in reader:
		tmp = []
		if line[1] not in query_dict:
			query_dict[line[1]]=[]
		tmp = [line[0],float(line[2])]	
		query_dict[line[1]].append(tmp)	
	return query_dict

def findAdv():
	file2 = open('bidder_dataset.csv','r')
	reader = csv.reader(file2)
	next(reader,None)
	for line in reader:
		if line[3] !='':
			advertiser_dict[line[0]]=float(line[3])
	return advertiser_dict

def findSpent():
	spent_dict = {}
	file2 = open('bidder_dataset.csv','rb')
	reader = csv.reader(file2)
	next(reader,None)
	for line in reader:
		if line[3] !='':
			spent_dict[line[0]]=float(0)
	return spent_dict	


def greedy(queries,query_dict,advertiser_dict):
	
	rev= 0
	for query in queries:
		
		highest_bidder = ''
		highest_bid = 0.0
		
		for arr in query_dict[query]:
				
			if (highest_bid < arr[1]) and (advertiser_dict[arr[0]] >= arr[1]):
				highest_bid = float(arr[1])
				highest_bidder = arr[0]

		if highest_bidder not in '':
			rev =  rev + highest_bid
			advertiser_dict[highest_bidder] = advertiser_dict[highest_bidder] - highest_bid
			
	return rev

def balance(queries,query_dict,advertiser_dict):
	
	rev = 0
	for query in queries:
		highest_bidder = ''
		max_budget = 0.0
		
		for arr in query_dict[query]:
			if ((advertiser_dict[arr[0]] >= arr[1]) and (max_budget < advertiser_dict[arr[0]])): 
				highest_bidder = arr[0]
				highest_bid = arr[1]
				max_budget = advertiser_dict[arr[0]]
			
		if highest_bidder not in '' :
			rev =  rev + highest_bid
			advertiser_dict[highest_bidder] = advertiser_dict[highest_bidder] - highest_bid	
			
	return rev


def msvv(queries,query_dict,advertiser_dict):

	spent_dict = {keys:0 for keys in advertiser_dict}
	rev = 0
	for query in queries:
		highest_bidder = ''
		highest_value = 0.0
		
		for arr in query_dict[query]:
			if ( advertiser_dict[arr[0]] >= arr[1] + spent_dict[arr[0]] ) :

				frac = (spent_dict[arr[0]])/advertiser_dict[arr[0]]
				tmp = 1- math.exp(frac-1)
				
				if (highest_value <= (arr[1]*tmp)):  
					highest_bid = arr[1]
					highest_bidder = arr[0]
					highest_value =  arr[1]*tmp
					
		if highest_bidder not in '':
			rev =  rev + highest_bid
			spent_dict[highest_bidder] = spent_dict[highest_bidder] + highest_bid	
			
	return rev


random.seed(0)


def optimal():
	advertiser_dict = findAdv()
	OPT = 0.0
	for keys in advertiser_dict:
		OPT+=advertiser_dict[keys]
	return OPT

query_dict = findQuery()
advertiser_dict = findAdv()
rev = 0

if algorithm=='greedy':
	revenue = greedy(queries,query_dict.copy(),advertiser_dict.copy())	

	for i in range(0, 100) :
		random.shuffle(queries)
		rev += greedy(queries,query_dict.copy(),advertiser_dict.copy())

elif algorithm == 'msvv':	
	revenue = msvv(queries,query_dict.copy(),advertiser_dict.copy())
	
	for i in range(0, 100) :
		random.shuffle(queries)
		rev += msvv(queries,query_dict.copy(),advertiser_dict.copy())

elif algorithm == 'balance':
	revenue = balance(queries,query_dict.copy(),advertiser_dict.copy())
	
	for i in range(0, 100) :
		random.shuffle(queries)
		rev += balance(queries,query_dict.copy(),advertiser_dict.copy())
	
else:
	sys.exit(1)

rev = rev / 100
OPT = optimal()
print ("Revenue : " + str(round(revenue,2)))
print ("Competitive Ratio :" + str(round(float(rev) / float(OPT),2)))
