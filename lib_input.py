#!/usr/bin/python
# coding: utf-8
"""
This module contains functions used to parse the user input necessary.
User input includes:
	* With the option "--words", an user can specify the number of words 
	to be in the word timeline. If not specified this number is set as 
	the constant defined in below.
	* cluster_usernames.csv: an optional file with specific usernames to be 
	considered by the script. If this file is present, all usernames not in it
	WILL NOT BE CONSIDERED by the script.
"""

import csv
import getopt
import os
import subprocess
import shutil

import sys

DEFAULT_INPUT_DELIMITER = '|'
NUMBER_OF_WORDS_FOR_TIMELINE = 10

def options_parser(argv):
	"""
	Returns the number of words specified as an argument in the terminal 
	when running the script. If not specified, this number is set as the constant
	defined in the beginning of this module.
	"""
	arguments = {}
	try:
		opts, args = getopt.getopt(argv[1:], 'w:', ['words='])
	except getopt.GetoptError:
		print("Invalid parameters. Aborting.")
		sys.exit(2)
	for opt, arg in opts:
		if opt in ('-w', '--words'):
			arguments['number_of_words'] = int(arg)
	if('number_of_words' not in arguments):
		arguments['number_of_words'] = NUMBER_OF_WORDS_FOR_TIMELINE # setting default number of words	
	return(arguments)

def load_filter_list(filename):
	""" 
	Reads a cluster_usernames.csv file if present and returns a 
	list of the usernames in it. If no username is in the file, 
	or the file is not present, it returns an empty list.
	"""
	filter_strings = []
	try:
		with open(filename, 'rt', encoding="utf8") as csvfile:
			csv_in = csv.reader(csvfile, delimiter='|', quotechar='"')
			next(csv_in)
			for line in csv_in:
				filter_strings.append(line[0].lower())
	except :
		filter_strings = {}
	if len(filter_strings) == 0:
		return []
	else:		
		return filter_strings

def load_user_relations(filename):
	""" 
	Reads a user_relations.csv file if present and returns a 
	dictionary of usernames and tuples in the format(followers_count, friends_count). If no username is in the file, 
	or the file is not present, it returns an empty dictionary.
	"""
	user_relations = {}
	try:
		with open(filename, 'rt', encoding="utf8") as csvfile:
			csv_in = csv.reader(csvfile, delimiter='|', quotechar='"')
			next(csv_in)
			for line in csv_in:
				username = line[0]
				followers_count = line[1]
				friends_count = line[2]
				user_relations[username] = (followers_count, friends_count)
	except:
		user_relations = {}
	return user_relations
	

def remove_null_byte():
	"""
	Calls a bash script to rewrite the tweets.csv file renaming it 
	as tweets_FIXED.csv without the null byte character
	tweets_FIXED.csv is the file is that will be used by the script.
	Yes, it can be done in Python, but is not a priority currently.
	"""
	subprocess.call(["sh", "remove_null_byte.sh"])

def cleanup():
	"""
	Cleanup after the script runs. A RESULTS folder is created and 
	the generated files are moved there.
	"""
	str_destination = "RESULTS"
	os.remove("tweets_FIXED.csv")

	# Deletes the RESULTS folder, if there is one.	
	try:
		shutil.rmtree(str_destination)
	except FileNotFoundError:
		pass

	# Creating the results folder.
	os.mkdir(str_destination)

	# Moving CSV files.
	shutil.move('dates.csv', str_destination)
	shutil.move('mentions.csv', str_destination)
	shutil.move('hashtags.csv', str_destination)
	shutil.move('hashtags_without_accents.csv', str_destination) #Added 14/05/2014
	shutil.move('locations.csv', str_destination)
	shutil.move('top_urls.csv', str_destination)
	shutil.move('top_words.csv', str_destination)
	shutil.move('top_tweets.csv', str_destination)
	shutil.move('users_by_date.csv', str_destination)
	shutil.move('users_activity.csv', str_destination)
	shutil.move('hashtags_network.csv', str_destination)
	shutil.move('hashtags_network_without_accents.csv', str_destination)#Added 15/05/2014

	shutil.move('tweets_with_links.csv', str_destination)
	shutil.move('tweets_without_RTs.csv', str_destination)
	shutil.move('tweets_of_a_specific_hashtag.csv', str_destination)
	shutil.move('tweets_without_hashtags.csv', str_destination)

	shutil.move('user_influence.csv', str_destination)
	
	try:	
		shutil.move('words_per_period.csv', str_destination)
		shutil.move('tweets_filtered_media.csv', str_destination)
		shutil.move('tweets_filtered_no_media.csv', str_destination)
	except FileNotFoundError:
		pass

	# Moving txt files.
	shutil.move('top_words_wordle.txt', str_destination)
	shutil.move('top_hashtags_wordle.txt', str_destination)
	shutil.move('top_hashtags_without_accents_wordle.txt', str_destination) #Added 14/05/2014
	
