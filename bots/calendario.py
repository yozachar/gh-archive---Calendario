# Calendario/calendario.py

import tweepy
import logging
import datetime as dt
from config import create_api


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
daily_tweet = ''


def print_progress(string, progress, ratio):
	global daily_tweet
	daily_tweet += string+'\n'+'▰' * \
		int(progress) + '▱'*(20-int(progress)) + ' ' + str(round(ratio*100, 2))+"%\n"
	print(daily_tweet)


def calculate_progress():
	year = int(dt.datetime.today().strftime("%Y"))
	leap_year = True if year % 4 == 0 else False

	#Week Progress
	week_day = int(dt.datetime.today().strftime('%w'))
	week_ratio = (week_day+1) / 7  # b'cos python week starts @ sunday = 0
	week_progress = week_ratio * 20
	print_progress("Week Progress:", week_progress, week_ratio)

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
	print_progress("Month Progress:", month_progress, month_ratio)

	#Year Progress
	no_of_days = 366 if leap_year else 365
	day_of_year = dt.datetime.now().timetuple().tm_yday
	year_ratio = day_of_year / no_of_days
	year_progress = year_ratio * 20
	print_progress("Year Progress:", year_progress, year_ratio)


if __name__ == "__main__":
	api = create_api()
	calculate_progress()
	try:
		api.update_status(daily_tweet)
	except tweepy.TweepError as error:
		if error.api_code == 187:
			print('duplicate message')
	else:
	   raise error
