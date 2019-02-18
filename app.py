from flask import Flask,render_template,request, flash, redirect, url_for, session, logging
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
from wtforms import Form, StringField, IntegerField, TextAreaField, PasswordField, validators, SelectField
from passlib.hash import sha256_crypt
from functools import wraps
from flask_wtf import FlaskForm

app = Flask(__name__)
app.secret_key = 'some secret key'
#config MySQL
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='Vamsi@123_'
app.config['MYSQL_DB']='DBMS'
app.config['MYSQL_CURSORCLASS']='DictCursor'
#initialize MySQL
mysql = MySQL(app)


@app.route('/')
def index():
 	return render_template('home.html')

@app.route('/About')
def About():
	return render_template('About.html')
@app.route('/Home')
def Home():
	return render_template('home.html')


#====================================================================================================================
#==============================================FORMS=================================================================
#====================================================================================================================

#users tables

class RegisterForm(Form):
	login_id = IntegerField('Login Id',[validators.DataRequired()])
	room_no = IntegerField('Room Number',[validators.DataRequired()])
	f_name = StringField('First Name',[validators.Length(min=5,max=100)])
	l_name = StringField('Last name',[validators.Length(min=5,max=100)])
	typeuser = SelectField('Type', choices = [('res', 'Resident'),('usr', 'User'),('wkr', 'Worker'),('wkres', 'Worker & Resident')])
	total_members= IntegerField('Total Members')
	phone_number = IntegerField('Phone Number')
	password=PasswordField('Password',[
			validators.DataRequired(),
			validators.EqualTo('confirm', message='Password do not match')
	])
	confirm= PasswordField('Confirm Password')

# Form for Updating users lists
class UpdateForm(Form):
	login_id = IntegerField('Login Id')
	room_no = IntegerField('Room Number')
	f_name = StringField('First Name',[validators.Length(min=5,max=100)])
	l_name = StringField('Last name',[validators.Length(min=5,max=100)])
	typeuser = SelectField('Type', choices = [('res', 'Resident'),('usr', 'User'),('wkr', 'Worker'),('wkres', 'Worker & Resident')])
	total_members= IntegerField('Total Members')
	phone_number = IntegerField('Phone Number')
# Form for offers
class offersform(Form):
	# offer_id = IntegerField('OFFER ID')
	room_no = IntegerField('Room Number')
	price = IntegerField('Price')
	features = StringField('Features')
	typeofroom = SelectField('Type of Room', choices = [('ac','AC'),('nonac','NON-AC'),('atcbath','Attached Bathroom'),('acbath','AC With Attached Bathroom'),('ncbbath','Non-Ac With Bathroom')])
	floor = StringField('Floor')
# Form for bidding
class bidform(Form):
	amount = IntegerField('Bidding Value')
class compform(Form):
	login_id = IntegerField('Login Id')
	pdep = SelectField('Department To solve', choices = [('electrical', 'electrical'),('water', 'water'),('applainces', 'applainces'),('other', 'other')])
	descp = StringField('Descrption about problem')
#workers department
class depform(Form):
	login_id=IntegerField('Login Id')
	department =SelectField('Department To solve', choices = [('electrical', 'electrical'),('water', 'water'),('applainces', 'applainces'),('other', 'other')])


# Form for ADDING USER BY ADMIN
# class adduser(Form):
# 	login_id = IntegerField('Login Id')
# 	room_no = IntegerField('Room Number')
# 	f_name = StringField('First Name',[validators.Length(min=5,max=100)])
# 	l_name = StringField('Last name',[validators.Length(min=5,max=100)])
# 	typeuser = SelectField('Type', choices = [('res', 'Resident'),('usr', 'User'),('wkr', 'Worker'),('wkres', 'Worker & Resident')])
# 	total_members= IntegerField('Total Members')
# 	phone_number = IntegerField('Phone Number')
# 	password=PasswordField('Password',[
# 			validators.DataRequired(),
# 			validators.EqualTo('confirm', message='Password do not match')
# 	])
# 	confirm= PasswordField('Confirm Password')


#====================================================================================================================
#=======================================Logout/Register/Edditing/Adding/Userlogin====================================
#====================================================================================================================
@app.route('/register',methods=['GET', 'POST'])
def register():

	#import register()
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		login_id = form.login_id.data
		room_no = form.room_no.data
		f_name = form.f_name.data
		l_name = form.l_name.data
		total_members = form.total_members.data
		phone_number = form.phone_number.data
		password = form.password.data
		typeuser = form.typeuser.data
		# create DictCursor
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO users(login_id, room_no, f_name, l_name, total_members, phone_number, password, typeuser)VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (login_id, room_no, f_name, l_name, total_members, phone_number, password, typeuser))
		#commit to 
		mysql.connection.commit()
		cur.close()
		flash('Registered Successfully!!!', 'success')
		redirect(url_for('Home'))

	return render_template('register.html', form=form)

# Editting Usres By Admin
@app.route('/editprofile/<string:login_id>', methods=['GET', 'POST'])
def editprofile(login_id):
	#create Cursor
	cur = mysql.connection.cursor()
	#Get user by id
	result = cur.execute("SELECT * FROM users WHERE login_id = %s", [login_id])
	user = cur.fetchone()
	cur.close()
	#Getting the Registration form
	form = UpdateForm(request.form)

	#setting the users details
	form.login_id.data = user['login_id']
	form.room_no.data = user['room_no']
	form.f_name.data = user['f_name']
	form.l_name.data = user['l_name']
	form.typeuser.data = user['typeuser']
	form.total_members.data = user['total_members']
	form.phone_number.data = user['phone_number']
	print("Ur outside the if loop")
	print("\n\n\n and Values are")
	print("\n\n\n",form.f_name.data)

	if request.method == 'POST' and form.validate():
		login_id = request.form['login_id']
		room_no = request.form['room_no']
		f_name = request.form['f_name']
		l_name = request.form['l_name']
		typeuser = request.form['typeuser']
		total_members = request.form['total_members']
		phone_number = request.form['phone_number']
		print("Ur inside the if loop")

		#Create the cursor
		cur = mysql.connection.cursor()
		print("===========Near update statement==========")
		#executing the update sql command
		cur.execute ("UPDATE users SET login_id=%s, room_no=%s, f_name=%s, l_name=%s, total_members=%s, phone_number=%s,typeuser=%s WHERE login_id=%s", (login_id, room_no, f_name, l_name, total_members, phone_number,typeuser, login_id))

		#commit the cursor
		mysql.connection.commit()

		#close
		cur.close()

		flash("User details updates",'success')
	return render_template('userupdate.html', form=form)

	
#Adding users by ADMIN
@app.route('/adduser',methods=['POST', 'GET'])
def adduser():
	#import register()
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		login_id = form.login_id.data
		room_no = form.room_no.data
		f_name = form.f_name.data
		l_name = form.l_name.data
		typeuser = form.typeuser.data
		total_members = form.total_members.data
		phone_number = form.phone_number.data
		password = form.password.data
		# create DictCursor
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO users(login_id, room_no, f_name, l_name, total_members, phone_number, password, typeuser)VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (login_id, room_no, f_name, l_name, total_members, phone_number, password, typeuser))
		#commit to 
		mysql.connection.commit()
		cur.close()
		flash('User Added Successfully!!!', 'success')
		return redirect(url_for('dashboard'))

	return render_template('adduser.html', form=form)

#user login
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		#Getting form fields
		login_id = request.form['login_id']
		logid = request.form['login_id']
		l=logid
		password_candidate = request.form['password']
		# print(login_id)
		if login_id == '12345':

		# create cursor
			cur = mysql.connection.cursor()

		#getting user name
			result = cur.execute("SELECT * FROM users WHERE login_id = %s", [login_id])

			if result >0:
			# Get Stored hash
				data = cur.fetchone()
				password = data['password']

			# checking
				if password_candidate == password:
					app.logger.info('PASSWORD MATCHED')
					session['logged_in'] = True
					session['login_id'] = login_id
					return redirect(url_for('dashboard'))
				else:
					app.logger.info('PASSWORD NOT MATCHED')
					flash('Password Not Matched!! Try Again','danger')
					return render_template('login.html')
				#close
				cur.close()

			else:
				flash('No User Exsists With That Login Id!!\n Try With Valid Login ID ','danger')
				app.logger.info('NO USER')
		elif login_id != '12345':
			# create cursor
			cur = mysql.connection.cursor()

		#getting user name
			result = cur.execute("SELECT * FROM users WHERE login_id = %s", [login_id])

			if result >0:
			# Get Stored hash
				data = cur.fetchone()
				password = data['password']

			# checking
				if password_candidate == password:
					app.logger.info('PASSWORD MATCHED')
					session['logged_in'] = True
					session['login_id'] = login_id
					return render_template('users/index.html')
				else:
					app.logger.info('PASSWORD NOT MATCHED')
					flash('Password Not Matched!! Try Again','danger')
					return render_template('login.html')
				#close
				cur.close()
			else:
				flash('No User Exsists With That Login Id!!\n Try With Valid Login ID','danger')
				app.logger.info('NO USER')
		
	
	return render_template('login.html')
	return (l)
#security
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized , Please Login', 'danger')
			return render_template('login.html')
	return wrap

#logout
@app.route('/logout')
def logout():
	session.clear()
	flash('your logged out', 'success')
	return redirect(url_for('login'))

#Admin DAshboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
	#creating cursor
	cur  = mysql.connection.cursor()

	#getting the users
	cur.execute("SELECT * FROM users")

	users = cur.fetchall()
	cur.execute("SELECT * FROM offers")
	offers = cur.fetchall()
	#print(users)
	# close connection
	cur.close()
	return render_template('dashboard.html', users=users, offers=offers)
# Admin Total Bids
@app.route('/totalbids')
@is_logged_in
def totalbids():
	#creating cursor
	cur  = mysql.connection.cursor()

	#getting the users
	cur.execute("SELECT * FROM bidding")

	bidding = cur.fetchall()
	#print(users)
	# close connection
	cur.close()
	return render_template('totalbid.html', bidding = bidding)
# delete bid by admin
@app.route('/deletebidadmin/<string:id>', methods=['POST'])
def deletebidadmin(id):
	cur = mysql.connection.cursor()
	cur.execute("DELETE FROM bidding WHERE bid_id = %s",[id])
	mysql.connection.commit()
	cur.close()
	flash('user deleted','success')
	return redirect(url_for('totalbids'))
#Bidding Winner
@app.route('/winner/<string:room_no>', methods=['GET','POST'])
def winner(room_no):
	rmno = room_no
	#creating cursor
	cur  = mysql.connection.cursor()

	#getting the users
	cur.execute("SELECT bid_id,login_id,offer_id,price,room_no from bidding where room_no = %s order by price DESC;",[rmno])

	bidding = cur.fetchone()
	print(bidding)
	# close connection
	# win=cur.fetchone()
	# print("Wiiner details:-",win)
	cur.close()
	return render_template('totalbidwin.html', bidding = bidding)	
@app.route('/sendmsg/<string:bid_id>/<string:login_id>/<string:offer_id>/<string:price>/<string:room_no>', methods = ['GET','POST'])
def sendmsg(bid_id,login_id,offer_id,price,room_no):
	bid= bid_id
	logid = login_id
	ofid = offer_id
	pr = price
	rmno = room_no
	cur = mysql.connection.cursor()
	cur.execute("INSERT into message (bid_id,offer_id,room_no,price,login_id) VALUES (%s,%s,%s,%s,%s)",(bid,ofid,rmno,pr,logid))
	mysql.connection.commit()
	cur.close()
	return	redirect('dashboard')

# admin Complaints
@app.route('/complaints')
@is_logged_in
def complaintsadmin():
	#creating cursor
	cur  = mysql.connection.cursor()

	#getting the users
	cur.execute("SELECT * FROM compbox")

	compbox = cur.fetchall()
	#print(users)
	# close connection
	cur.close()
	return render_template('complaints.html', compbox = compbox)
#complaint dashboard
@app.route('/editcomplaint/<string:comp_id>', methods=['GET', 'POST'])
def editcomplaint(comp_id):
	#create Cursor
	cur = mysql.connection.cursor()
	#Get user by id
	cur.execute ("UPDATE compbox SET status='Solved' WHERE comp_id=%s", (comp_id))
	mysql.connection.commit()
	cur.close()
	flash("UComplaints details updates",'success')
	return redirect(url_for('complaintsadmin'))
@app.route('/editcomplaint2/<string:comp_id>', methods=['GET', 'POST'])
def editcomplaint2(comp_id):
	#create Cursor
	cur = mysql.connection.cursor()
	stat = 'None'
	#Get user by id
	cur.execute ("UPDATE compbox SET status='None' WHERE comp_id=%s", (comp_id))
	mysql.connection.commit()
	cur.close()
	flash("Complaints details updates",'success')
	return redirect(url_for('complaintsadmin'))
# Delete Complaint
@app.route('/deletcomplaint/<string:id>', methods=['POST'])
def deletecomplaint(id):
	cur = mysql.connection.cursor()
	cur.execute("DELETE FROM compbox WHERE comp_id = %s",[id])
	mysql.connection.commit()
	cur.close()
	flash('Complaint deleted','success')
	return redirect(url_for('complaintsadmin'))
@app.route('/userdashboard')
@is_logged_in
def userdashboard():
	return render_template('users/index.html')
#===========================================================================================================
#=======================================About Workers=======================================================
#===========================================================================================================
#define Workers
@app.route('/totalworkers')
def totalworkers():
	#creating cursor
	cur  = mysql.connection.cursor()

	#getting the users
	cur.execute("SELECT * FROM users WHERE typeuser!='res' and typeuser!='usr'")

	users = cur.fetchall()
	cur.execute("select users.login_id,users.f_name,users.phone_number,workshop.department from users inner join workshop on users.login_id = workshop.login_id;")
	work = cur.fetchall()
	# close connection
	cur.close()
	return render_template('workers.html', users = users,work = work)
#department edit
@app.route('/editdep/<string:login_id>', methods=['GET', 'POST'])
def editdep(login_id):
	logid = login_id
	cur = mysql.connection.cursor()
	#Get user by id
	result = cur.execute("SELECT * FROM workshop WHERE login_id = %s", [login_id])
	workshop = cur.fetchone()
	cur.close()
	#Getting the Registration form
	form = depform(request.form)

	#setting the users details
	form.department.data = workshop['department']

	if request.method == 'POST' and form.validate():
		login_id = logid
		department = request.form['department']
		#Create the cursor
		cur = mysql.connection.cursor()
		print("===========Near update statement==========")
		#executing the update sql command
		cur.execute ("UPDATE workshop SET department=%s WHERE login_id=%s", (department,login_id))

		#commit the cursor
		mysql.connection.commit()

		#close
		cur.close()
		return redirect(url_for('dashboard'))
	return render_template('editdep.html',form = form)
# add department
@app.route('/adddep/<string:login_id>', methods=['GET', 'POST'])
def adddep(login_id):
	logid = login_id
	form = depform(request.form)
	if request.method == 'POST' and form.validate():
		login_id = logid
		department = request.form['department']
		#Create the cursor
		cur = mysql.connection.cursor()
		print("===========Near update statement==========")
		#executing the update sql command
		cur.execute ("INSERT into workshop(login_id,department) Values(%s,%s)", (login_id,department))

		#commit the cursor
		mysql.connection.commit()

		#close
		cur.close()
		return redirect(url_for('dashboard'))
	return render_template('editdep.html',form = form)

#complaoint box\
@app.route('/compbox/<string:login_id>', methods=['GET', 'POST'])
def compbox(login_id):
	logid = login_id
	print("YAYAYYYAYAYAYA",logid)
	cur  = mysql.connection.cursor()

	#getting the users
	cur.execute("SELECT * FROM users WHERE login_id = %s", [logid] )
	#print(logid)
	users = cur.fetchone()
	cur.execute("SELECT * FROM message WHERE login_id = %s", [logid] )
	message = cur.fetchone()
	print(message)
	#print(users)
	# close connection
	cur.close()
	return render_template('users/compbox.html',users = users,message=message)
@app.route('/compbox/join/<string:login_id>/<string:room_no>/<string:msg_id>/<string:price>', methods = ['GET','POST'])
def join(login_id,room_no,msg_id,price):
	logid = login_id
	rmno = room_no
	msid = msg_id
	pr = price
	det = 'payed for Room No:- '+ rmno + '\nPrice Of:-' + pr
	cur = mysql.connection.cursor()
	cur.execute ("UPDATE users SET room_no=%s  WHERE login_id=%s", (rmno, logid))
	cur.execute("DELETE from message where msg_id=%s",[msid])
	cur.execute("INSERT into payment (login_id,details) VALUES(%s,%s)",(logid,det))
	mysql.connection.commit()
	cur.close()
	return redirect('userdashboard')

@app.route('/compbox/logout')
def complogout():
	session.clear()
	flash('your logged out', 'success')
	return redirect(url_for('login'))
@app.route('/compbox/userdashboard')
def compdash():
	return redirect(url_for('userdashboard'))
@app.route('/compbox/offers')
def compoffer():
	return redirect(url_for('offers'))
@app.route('/compbox/editprofile2/<string:login_id>', methods=['GET', 'POST'])
def editprofile2(login_id):
	#create Cursor
	cur = mysql.connection.cursor()
	#Get user by id
	result = cur.execute("SELECT * FROM users WHERE login_id = %s", [login_id])
	user = cur.fetchone()
	cur.close()
	#Getting the Registration form
	form = UpdateForm(request.form)

	#setting the users details
	form.login_id.data = user['login_id']
	form.room_no.data = user['room_no']
	form.f_name.data = user['f_name']
	form.l_name.data = user['l_name']
	form.typeuser.data = user['typeuser']
	form.total_members.data = user['total_members']
	form.phone_number.data = user['phone_number']
	print("Ur outside the if loop")
	print("\n\n\n and Values are")
	print("\n\n\n",form.f_name.data)

	if request.method == 'POST' and form.validate():
		login_id = request.form['login_id']
		room_no = request.form['room_no']
		f_name = request.form['f_name']
		l_name = request.form['l_name']
		typeuser = request.form['typeuser']
		total_members = request.form['total_members']
		phone_number = request.form['phone_number']
		print("Ur inside the if loop")

		#Create the cursor
		cur = mysql.connection.cursor()
		print("===========Near update statement==========")
		#executing the update sql command
		cur.execute ("UPDATE users SET login_id=%s, room_no=%s, f_name=%s, l_name=%s, total_members=%s, phone_number=%s,typeuser=%s WHERE login_id=%s", (login_id, room_no, f_name, l_name, total_members, phone_number,typeuser, login_id))

		#commit the cursor
		mysql.connection.commit()

		#close
		cur.close()

		flash("User details updates",'success')
		if login_id !=' 1234':
			return redirect(url_for('userdashboard'))
		else:
			return redirect(url_for('dashboard'))
	return render_template('userupdate.html', form=form)


#===========================================================================================================
#=======================================Delete User=========================================================
#===========================================================================================================
@app.route('/deleteuser/<string:id>', methods=['POST'])
def deleteuser(id):
	cur = mysql.connection.cursor()
	cur.execute("DELETE FROM users WHERE login_id = %s",[id])
	mysql.connection.commit()
	cur.close()
	flash('user deleted','success')
	return redirect(url_for('dashboard'))
#====================================================================================================================
#=================================================Everything On offers===============================================
#====================================================================================================================
@app.route('/editoffer/<string:offer_id>', methods=['GET', 'POST'])
def editoffer(offer_id):
	#create Cursor
	cur = mysql.connection.cursor()
	#Get user by id
	result = cur.execute("SELECT * FROM offers WHERE offer_id = %s", [offer_id])
	offer = cur.fetchone()
	cur.close()
	#Getting the Registration form
	form = offersform(request.form)

	#setting the users details
	form.room_no.data = offer['room_no']
	form.price.data = offer['price']
	form.features.data = offer['features']
	form.typeofroom.data = offer['type']
	form.floor.data = offer['floor']

	if request.method == 'POST' and form.validate():
		room_no = request.form['room_no']
		price = request.form['price']
		features = request.form['features']
		typeofroom = request.form['typeofroom']
		floor = request.form['floor']
		#Create the cursor
		cur = mysql.connection.cursor()
		print("===========Near update statement==========")
		#executing the update sql command
		cur.execute ("UPDATE offers SET room_no=%s, price=%s, features=%s, type=%s, floor=%s WHERE offer_id=%s", (room_no, price, features, typeofroom, floor, offer_id))

		#commit the cursor
		mysql.connection.commit()

		#close
		cur.close()

		flash("User details updates",'success')
		
		return redirect(url_for('dashboard'))
	return render_template('offerupdate.html', form=form)
@app.route('/addoffer',methods=['POST', 'GET'])
def addoffer():
	#import register()
	form = offersform(request.form)
	if request.method == 'POST' and form.validate():
		# offer_id = form.offer_id.data
		room_no = form.room_no.data
		price = form.price.data
		features = form.features.data
		typeofroom = form.typeofroom.data
		floor = form.floor.data
		# create DictCursor
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO offers(room_no, price, features , type, floor)VALUES(%s, %s, %s, %s, %s)", (room_no, price, features, typeofroom, floor))
		#commit to 
		mysql.connection.commit()
		cur.close()
		flash('Offer Added Successfully!!!', 'success')
		return redirect(url_for('dashboard'))

	return render_template('addoffer.html', form=form)

@app.route('/offers')
def offers():
	cur  = mysql.connection.cursor()

	#getting the users
	cur.execute("SELECT * FROM offers")

	offers = cur.fetchall()
	# close connection
	cur.close()
	return render_template('offers.html', offers=offers)
@app.route('/deleteoffer/<string:id>', methods=['POST'])
def deleteoffer(id):
	cur = mysql.connection.cursor()
	cur.execute("DELETE FROM offers WHERE offer_id = %s",[id])
	mysql.connection.commit()
	cur.close()
	flash('user deleted','success')
	return redirect(url_for('dashboard'))

#====================================================================================================================
#=================================================Everything On payments===============================================
#====================================================================================================================
@app.route('/payments/<string:login_id>', methods=['GET', 'POST'])
def payments(login_id):
	logid = login_id
	print("YAYAYYYAYAYAYA",logid)
	cur  = mysql.connection.cursor()

	#getting the users
	cur.execute("SELECT * FROM payment WHERE login_id = %s", [logid] )
	print(logid)
	payment = cur.fetchall()
	# close connection
	cur.close()
	return render_template('users/payments.html',payment = payment)
@app.route('/payments/logout')
def paylogout():
	session.clear()
	flash('your logged out', 'success')
	return redirect(url_for('login'))
@app.route('/payments/userdashboard')
def paydash():
	return redirect(url_for('userdashboard'))
# @app.route('/book/<string:room_no>/<string:login_id>', methods=['GET', 'POST'])
# def book(room_no,login_id):
# 	rmno = room_no
# 	print("Room NO:-",rmno)
# 	logid = login_id
# 	print("Log ID",logid)
# 	cur = mysql.connection.cursor()
# 	cur.execute("UPDATE users SET room_no=%s WHERE login_id=%s", (rmno, logid))
# 	mysql.connection.commit() 
# 	cur.close()
# 	flash('Successfully Changed room', 'success')
# 	return redirect('userdashboard')
@app.route('/book/<string:offer_id>//<string:room_no>', methods=['GET', 'POST'])
@is_logged_in
def bidw(offer_id,login_id,room_no):
	return render_template('addbid.html')

@app.route('/book/<string:offer_id>/<string:login_id>/<string:room_no>', methods=['GET', 'POST'])
@is_logged_in
def bid(offer_id,login_id,room_no):
	ofid = offer_id
	lgid = login_id
	rmno = room_no
	form = bidform(request.form)
	if request.method == 'POST' and form.validate():
		amount = form.amount.data
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO bidding(login_id, offer_id, price, room_no)VALUES(%s, %s,%s, %s)", (login_id,offer_id,amount, room_no))
		#commit to 
		mysql.connection.commit()
		cur.close()
		return redirect(url_for('userdashboard'))

	return render_template('addbid.html', form=form)
@app.route('/bidding/<string:login_id>', methods = ['GET', 'POST'])
def bidding(login_id):
	logid = login_id
	cur  = mysql.connection.cursor()
	#getting the users
	cur.execute("SELECT * FROM bidding WHERE login_id = %s", [logid] )
	# print(logid)
	bidding = cur.fetchall()
	# close connection
	cur.close()
	return render_template('users/bidding.html',bidding = bidding)
@app.route('/deletebid/<string:id>', methods=['POST'])
def deletebid(id):
	cur = mysql.connection.cursor()
	cur.execute("DELETE FROM bidding WHERE bid_id = %s",[id])
	mysql.connection.commit()
	cur.close()
	flash('user deleted','success')
	return redirect(url_for('userdashboard'))
@app.route('/bidding/userdashboard')
def biddash():
	return redirect(url_for('userdashboard'))
@app.route('/bidding/logout')
def bidlogout():
	session.clear()
	flash('your logged out', 'success')
	return redirect(url_for('login'))
#====================================================================================================================
#=================================================Everything On complaitns===============================================
#====================================================================================================================
@app.route('/complaint/<string:login_id>',methods=['GET','POST'])
def complaints(login_id):
	logid = login_id
	form = compform(request.form)
	if request.method == 'POST' and form.validate():
		login_id = logid
		pdep = form.pdep.data
		descp = form.descp.data
		# create DictCursor
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO compbox(login_id, pdep, descp)VALUES(%s, %s, %s)", (login_id, pdep, descp))
		#commit to 
		mysql.connection.commit()
		cur.close()
		flash('Complaint Posted Successfully!!!', 'success')
		return redirect(url_for('userdashboard'))
	cur  = mysql.connection.cursor()
	#getting the users
	cur.execute("SELECT * FROM compbox WHERE login_id = %s", [logid] )
	# print(logid)
	compbox = cur.fetchall()
	print(compbox)
	# close connection
	cur.close()
	return render_template('users/complaint.html',compbox = compbox,form=form)
@app.route('/complaint/userdashboard')
def complaintdash():
	return redirect(url_for('userdashboard'))
@app.route('/deletecomp/<string:id>', methods=['POST'])
def deletecomp(id):
	cur = mysql.connection.cursor()
	cur.execute("DELETE FROM compbox WHERE comp_id = %s",[id])
	mysql.connection.commit()
	cur.close()
	flash('Complaint deleted','success')
	return redirect(url_for('userdashboard'))
@app.route('/complaint/logout')
def complaintlogout():
	session.clear()
	flash('your logged out', 'success')
	return redirect(url_for('login'))

@app.route('/work/<string:login_id>', methods=['GET', 'POST'])
def workset(login_id):
	logid = login_id
	#create Cursor
	cur = mysql.connection.cursor()
	#Get user by id
	cur.execute ("SELECT department FROM workshop WHERE login_id = %s", [logid])
	dep = cur.fetchone()
	cur.close()
	return render_template('users/workset.html',dep = dep)
@app.route('/work/userdashboard')
def workdash():
	return redirect(url_for('userdashboard'))
@app.route('/work/logout')
def worklogout():
	session.clear()
	flash('your logged out', 'success')
	return redirect(url_for('login'))
#show works for wkr
@app.route('/work/showork/<string:department>',methods=['GET','POST'])
def showork(department):
	dep = department
	#create Cursor
	cur = mysql.connection.cursor()
	#Get user by id
	cur.execute ("SELECT * FROM compbox WHERE pdep = %s", [dep])
	dept = cur.fetchall()
	cur.close()
	return render_template('users/showork.html',dept=dept)
@app.route('/work/showork/editcomplaint/<string:comp_id>', methods=['GET', 'POST'])
def fixit(comp_id):
	#create Cursor
	cur = mysql.connection.cursor()
	#Get user by id
	cur.execute ("UPDATE compbox SET status='Solved' WHERE comp_id=%s", (comp_id))
	mysql.connection.commit()
	cur.close()
	flash("UComplaints details updates",'success')
	return redirect(url_for('userdashboard'))


if __name__=='__main__':
	app.secret_key = 'some secret key'
    #ebug(True)
	app.run(debug = True)
