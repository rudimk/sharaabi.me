from flask import Flask, render_template, redirect, jsonify, request, session
from blitzdb import FileBackend, Document
import hashlib
import datetime
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.debug = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
backend = FileBackend("./drunk-db")
toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Models
'''
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

'''

class User(Document):
	pass

class Group(Document):
	pass

class Event(Document):
	pass

@app.route('/')
def home_view():
	return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup_view():
	if request.method == 'POST':
		user_name = request.form['name']
		user_email = request.form['email']
		user_password = request.form['password']
		password_hash = hashlib.sha224(user_password).hexdigest()
		user_created_at = datetime.datetime.now()
		new_user = User({'name':user_name, 'email':user_email, 'password':password_hash, 'created_at':user_created_at, 'push_subscriber_id':''})
		backend.save(new_user)
		backend.commit()
		session["user_id"] = new_user.pk
		return redirect('/')
	return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login_view():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		user_query = backend.filter(User, {'email':email})
		if len(user_query) == 1:
			# User exists, now check for the right password
			password_hash = hashlib.sha224(password).hexdigest()
			if user_query[0].password == password_hash:
				# The user is logged in
				session["user_id"] = user_query[0].pk
				return redirect('/')
			else:
				return redirect('/login')
		else:
			return redirect('/signup')
	return render_template('login.html')


@app.route('/logout')
def logout_view():
	session["user_id"] = None
	return redirect('/')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8500, debug=True)