from flask import Flask, render_template, redirect

import redis
import rom
from rom import util

util.set_connection_settings(host='localhost', db=2)

app = Flask(__name__)

# Models

class User(rom.Model):
	email = rom.String(required=True, unique=True, suffix=True)
	name = rom.String(required=True)
	created_at = rom.Float(default=time.time)
	last_push = rom.Float(default=0)
	push_subscriber_id = rom.String()

class Group(rom.Model):
	name = rom.String(required=True, unique=True)

class GroupMember(rom.Model):
	group_name = rom.String(required=True)
	member_email = rom.String(required=True)

class Event(rom.Model):
	event_hash = rom.String(required=True)
	organizer_email = rom.String(required=True)
	date = rom.String(required=True)
	place = rom.String(required=True)

class EventAttendees(rom.Model):
	event_hash = rom.String(required=True)
	member_email = rom.String(required=True)
	member_choice = rom.String(required=True)



@app.route('/')
def home_view():
	return render_template('index.html')


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8500, debug=True)