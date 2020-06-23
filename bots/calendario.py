'''
* Author: joe733
* Mail: jovial7joe@hotmail.com
* Python: Version 3.6+
* Dependency: tweepy module
* ------------------------------------------------
* Purpose: Being time consious is always important.
'''

import tweepy
import logging
import datetime as dt
from config import create_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

daily_tweet = ''
fb, nb = '✅', '⬜️' # filled and null bullets


def print_progress(string, progress, ratio):
	'''Prints year's progress'''
	global daily_tweet
	daily_tweet += string+'\n'+fb*int(progress) + nb*(20-int(progress)) + ' ' + str(int(ratio*100))+"%\n"


def calculate_progress():
	'''Calculates year's progress'''
	year = int(dt.datetime.today().strftime("%Y"))
	leap_year = True if year % 4 == 0 else False

	#Week Progress
	week_day = int(dt.datetime.today().strftime('%w'))
	week_ratio = (week_day+1) / 7  # b'cos python week starts @ sunday = 0
	week_progress = week_ratio * 20
	print_progress("Week:", week_progress, week_ratio)

	#Month Progress
	day_of_month = int(dt.datetime.today().strftime("%d"))
	month = dt.datetime.today().month
	if month == 2:
		len_of_month = 29 if leap_year else 28
	elif month <= 7:
		len_of_month = 30 if month % 2 == 0 else 31
	else:
		len_of_month = 31 if month % 2 == 0 else 30
	month_ratio = day_of_month / len_of_month
	month_progress = month_ratio * 20
	print_progress("Month:", month_progress, month_ratio)

	#Year Progress
	no_of_days = 366 if leap_year else 365
	day_of_year = dt.datetime.now().timetuple().tm_yday
	year_ratio = day_of_year / no_of_days
	year_progress = year_ratio * 20
	print_progress("Year:", year_progress, year_ratio)


if __name__ == "__main__":
	'''My driver code'''
	api = create_api()
	calculate_progress()
	tweet_this = dt.datetime.today().strftime('%y • %m • %d') + '\n\n' + daily_tweet
	try:
		api.update_status(tweet_this)
	except tweepy.TweepError as error:
		if error.api_code == 187:
			print('duplicate message')
