import datetime
import warnings

from os import getcwd, system
from sys import platform, path
from time import sleep
from threading import Thread

import pandas as pd

# use stocksp.func() to invoke func() from StocksParser
# use newsp.func() to invoke func() from NewsParser
import StocksParser.StocksParser as stocksp	
import NewsParser as newsp	
import Algorythms.stocks_check as stocksch
import Algorythms.Classification as classify
import Algorythms.Create_features as features
import Algorythms.Predict as predictor

#
# Configuration
#

DEBUG = 0

if platform == "linux" or platform == "linux2":
	path.insert(0, getcwd() + '/NewsParser/Linux')
elif platform == "win32":
	path.insert(0, getcwd() + '/NewsParser/Windows')

warnings.filterwarnings('ignore')

#
# Paths
#

STOCKS_DIR	= getcwd()		# Directory with parced stocks. Ends with '\' or '/'.
NEWS_DIR 	= getcwd() 		# Directory with parced news. Ends with '\' or '/'.
NEWSS_DIR 	= getcwd()		# Directory with processed news. Ends with '\' or '/'.
TRAIN_PATH 	= getcwd()		# Path to train set.
PICKLE_PATH	= getcwd()		# Path to predicktor binary file
MAIN_FILE 	= 'company.csv' 	# Path to list of companies.
    
if platform == "win32":
	STOCKS_DIR += '\\StocksP\\'
	NEWS_DIR += '\\NewsP\\'
	NEWSS_DIR += '\\NewssP\\'
	TRAIN_PATH += '\\Algorythms\\train.csv'
	PICKLE_PATH += '\\Algorythms\\Predictor.pickle'
	
else: # Linux and Mac OS X
	STOCKS_DIR += '/StocksP/'
	NEWS_DIR += '/NewsP/'
	NEWSS_DIR += '/NewssP/'
	TRAIN_PATH += '/Algorythms/train.csv'
	PICKLE_PATH += '/Algorythms/Predictor.pickle'

system('mkdir ' + STOCKS_DIR)
system('mkdir ' + NEWS_DIR)
system('mkdir ' + NEWSS_DIR)

#
# Useful constants
#

DATE_START = 0
DATE_CLOSE = 0

#
# Implementation
#

def update():
	"""This function asks user if he or 
	she wants to update data to the newest.
	If the answer is 'yes' performs update
	"""
	
	print('\n\nWould you like to update these files?')
	print('\t1 - yes\n\t2 - no')
	
	answer = 0
	while answer != 1 and answer != 2:
		print(' > ', end='')
		
		try:
			answer = int(input())
		except ValueError:
			continue
		
	if answer == 2:
		return

	stocksp.main_(MAIN_FILE, STOCKS_DIR)
	print('\nWaiting for news... It may take a while\n')
	newsp.main_(MAIN_FILE, NEWS_DIR)
	classify.main_(MAIN_FILE, NEWS_DIR, NEWSS_DIR, TRAIN_PATH)
	
	

if __name__ == '__main__':
	"""Main code of this file
	Performs all the actions of application
	"""
	
	if DEBUG:
		print('MAIN_FILE  : ' + MAIN_FILE)
		print('STOCKS_DIR : ' + STOCKS_DIR)
		print('NEWS_DIR   : ' + NEWS_DIR)
		print('NEWSS_DIR  : ' + NEWSS_DIR)
		print('TRAIN_PATH : ' + TRAIN_PATH)
		
	list_of_companies = pd.read_csv(MAIN_FILE)
	
	update()

	# Raw working data
	data = features.main_(list_of_companies, NEWSS_DIR, STOCKS_DIR)
	
	predictions = predictor.prediction(PICKLE_PATH, data)
	names = list_of_companies.Company.values
	
	print("\n")
	
	valueToString = lambda value : "вырастет" if value == 1 else "упадёт"
	
	for name, prediction in zip(names, predictions):
		print("{} - {}".format(name, valueToString(prediction)))
		
	print("")
