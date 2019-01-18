#!/usr/bin/python

# Note: you can't view a list of all events on all days, despite the pull-down menu options.

# URL: https://schedule.sxsw.com/2019/03/08/events
# URL format: https://schedule.sxsw.com/2019/03/{DAY}/events

# HTML parser: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# installation (with pip):
# $ sudo pip install beautifulsoup4
# installation (without pip):
# $ sudo easy_install pip
# $ sudo pip install beautifulsoup4
from bs4 import BeautifulSoup

# regular expressions
import re

# URL stuff
import urllib

# CSV reader and write module
# https://docs.python.org/2/library/csv.html
#import csv

# numerical days, March 8 - 17
# note: single digit days need a leading 0
days = range (8,17)

# just print the lines for export to Excel
export = True

schedule_url = 'https://schedule.sxsw.com/2019/03/08/events'

socket = urllib.urlopen(schedule_url)
schedule_html = socket.read()
socket.close()

delimiter = '|'
raw_soup = BeautifulSoup(schedule_html, features="html.parser")
# replace most <br>s
soup_html = BeautifulSoup(str(raw_soup).replace('<br/>', delimiter), features="html.parser")

events = soup_html.find_all("div", class_="single-event")

# print column headings
if export:
	column_headings = ['number','title','date','time','location','room number','address','track','format','type']
	print delimiter.join(str(heading) for heading in column_headings)

# loop through events
for event in range(len(events)):
	event_index = event+1
	if not export:
		print event_index
	event_title = events[event].h4.text
	title = event_title.encode('utf-8', 'ignore')
	if not export:
		print title

	event_details = events[event].find_all("div",class_="text-tiny")
	date_and_time = event_details[0].text.split(delimiter)
	date = date_and_time[0].encode('utf-8', 'ignore')
	time = date_and_time[1].encode('utf-8', 'ignore')
	if not export:
		print date
		print time

	venue_info = event_details[1].text.split(delimiter)
	location = event_details[1].a.extract()
	loc = location.text.encode('utf-8', 'ignore')
	if not export:
		print loc
	try:
		room = event_details[1].a.extract()
	except AttributeError:
		room_number = '(None)'
	street = event_details[1].text[1:]
	try:
		room_number = room.text.encode('utf-8', 'ignore')
		if not export:
			print room_number
	except AttributeError:
		if not export:
			print room_number
	address = street.encode('utf-8', 'ignore')
	if not export:
		print address


	track_format_type_info = event_details[2].text.split(delimiter)
	track = track_format_type_info[0].encode('utf-8', 'ignore')
	format = track_format_type_info[1].encode('utf-8', 'ignore')
	type = track_format_type_info[2].encode('utf-8', 'ignore')
	if not export:
		print track
		print format
		print type

	if export:
		items = [event_index,title,date,time,loc,room_number,address,track,format,type]
		print delimiter.join(str(column) for column in items)

	# print empty line
	if not export:
		print 

