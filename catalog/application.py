'''
    This is application.py python program,
    which holds the functions to perform necessary CRUD opearations
    as well as to authenticate and register user and JSON API endpoints
    to show the data in json format.
'''

# Importing required Flask, SQLAlchemy, OAuth and other python modules
from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, DanceSchool, DanceClass
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

# Client ID for future login use.
CLIENT_ID = json.loads(
    open('catalog/client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Dance Schools App"


# Connecting to Database and creating database session
engine = create_engine('sqlite:///dancedataapp.db')
Base.metadata.bind = engine
# DBsession object
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Creating anti-forgery state token for safe login
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# fbconnect function to connect via facebook login
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    # Validating state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('catalog/fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('catalog/fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    token = result.split(',')[0].split(':')[1].replace('"', '')
    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # User picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['picture'] = data["data"]["url"]

    # Checking if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    
    flash("Now logged in as %s" % login_session['username'])
    return output

# function gconnect to connect via gmail account
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validating state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtaining authorization code
    code = request.data

    try:
        # Upgrading the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('catalog/client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Checking that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verifying that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verifying that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Storing the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    
    # Getting user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# Disconnect based on provider to let user logged out
@app.route('/logout')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showDanceSchools'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showDanceSchools'))


# function to get logged out via facebook
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# function to get logged out via gmail account
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        #del login_session['access_token']
        #del login_session['gplus_id']
        #del login_session['username']
        #del login_session['email']
        #del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Function to create new user
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# Function to get User information
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# Function to get user id via its email
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Function to show all dance schools
@app.route('/')
@app.route('/danceschools/')
def showDanceSchools():
    danceSchools = session.query(DanceSchool).all()
    if 'username' not in login_session:
        return render_template('publicDanceSchools.html', danceSchools=danceSchools)
    else:
        return render_template('danceSchools.html', danceSchools=danceSchools)


# Function to create a new dance school
@app.route('/danceschools/new/', methods=['GET','POST'])
def createDanceSchool():
    if 'username' not in login_session:
        return redirect('/login')
    else:
        if request.method == 'POST':
            name = request.form['name']
            address = request.form['address']
            user_id = login_session['user_id']
            danceSchoolToAdd = DanceSchool(name=name, address=address,
                                           user_id=user_id)
            session.add(danceSchoolToAdd)
            session.commit()
            flash('New Dance School has been created!')
            return redirect(url_for('showDanceSchools'))
        else:
            return render_template('addDanceSchool.html')


# Function to edit a dance school data
@app.route('/danceschools/<int:dance_school_id>/edit/', methods=['GET','POST'])
def editDanceSchool(dance_school_id):
    danceSchoolToUpdate = session.query(DanceSchool).filter_by(id=dance_school_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if danceSchoolToUpdate.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this dance school. Please create your own dance school in order to edit.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            danceSchoolToUpdate.name = request.form['name']
        if request.form['address']:
            danceSchoolToUpdate.address = request.form['address']
        session.add(danceSchoolToUpdate)
        session.commit()
        flash('Dance School %s has been updated!' % (danceSchoolToUpdate.name))
        return redirect(url_for('showDanceSchools'))
    else:
        return render_template('editDanceSchool.html', danceSchool=danceSchoolToUpdate, dance_school_id=dance_school_id)


# Function to delete a dance school
@app.route('/danceschools/<int:dance_school_id>/delete/', methods=['GET','POST'])
def deleteDanceSchool(dance_school_id):
    danceSchoolToDelete = session.query(DanceSchool).filter_by(id=dance_school_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if danceSchoolToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this dance school. Please create your own dance school in order to delete.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(danceSchoolToDelete)
        flash('Dance School %s has been deleted!' %(danceSchoolToDelete.name)) 
        session.commit()
        return redirect(url_for('showDanceSchools'))
    else:
        return render_template('deleteDanceSchool.html', danceSchool=danceSchoolToDelete, dance_school_id=dance_school_id)


# Function to show all dance classes for a dance school
@app.route('/danceschools/<int:dance_school_id>/danceclasses/')
def showDanceClasses(dance_school_id):
    danceSchool = session.query(DanceSchool).filter_by(id=dance_school_id).one()
    danceClasses = session.query(DanceClass).filter_by(dance_school_id=dance_school_id).all()
    creator = getUserInfo(danceSchool.user_id)
    if 'username' not in login_session or danceSchool.user_id != login_session['user_id']:
        return render_template('publicDanceClasses.html', danceClasses=danceClasses, danceSchool=danceSchool)
    else:
        return render_template('danceClasses.html',danceClasses=danceClasses, danceSchool=danceSchool)


# Function to create a new dance class
@app.route('/danceschools/<int:dance_school_id>/danceclasses/new/', methods=['GET','POST'])
def createDanceClass(dance_school_id):
    danceSchool = session.query(DanceSchool).filter_by(id=dance_school_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if danceSchool.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to create a new dance class. Please create your own dance school in order to create a new dance class.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        teacher = request.form['teacher']
        sessions = request.form['sessions']
        fees = request.form['fees']
        user_id = login_session['user_id']
        danceClassToAdd = DanceClass(name=name, description=description,
                                     teacher=teacher,sessions=sessions,
                                     fees=fees, user_id=user_id, dance_school_id=dance_school_id)
        session.add(danceClassToAdd)
        session.commit()
        flash('New Dance Class has been created!')
        return redirect(url_for('showDanceClasses', dance_school_id=dance_school_id))
    else:
        return render_template('addDanceClass.html', danceSchool=danceSchool)


# Function to edit a dance class
@app.route('/danceschools/<int:dance_school_id>/danceclasses/<int:dance_class_id>/edit/', methods=['GET','POST'])
def editDanceClass(dance_school_id, dance_class_id):
    danceSchool = session.query(DanceSchool).filter_by(id=dance_school_id).one()
    danceClassToEdit = session.query(DanceClass).filter_by(id=dance_class_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if danceSchool.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this dance class. Please create your own dance school in order to edit a dance class.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':                          
        if request.form['name']:
            danceClassToEdit.name = request.form['name']
        if request.form['description']:
            danceClassToEdit.description = request.form['description']
        if request.form['teacher']:
            danceClassToEdit.teacher = request.form['teacher']
        if request.form['sessions']:
            danceClassToEdit.sessions = request.form['sessions']
        if request.form['fees']:
            danceClassToEdit.fees = request.form['fees']
            
        session.add(danceClassToEdit)
        session.commit()
        flash('Dance Class %s has been updated!' %(danceClassToEdit.name))
        return redirect(url_for('showDanceClasses', dance_school_id=dance_school_id))
    else:
        return render_template('editDanceClass.html', danceSchool=danceSchool, danceClass=danceClassToEdit, dance_class_id=dance_class_id)


# Function to delete a dance class
@app.route('/danceschools/<int:dance_school_id>/danceclasses/<int:dance_class_id>/delete/', methods=['GET','POST'])
def deleteDanceClass(dance_school_id, dance_class_id):
    danceSchool = session.query(DanceSchool).filter_by(id=dance_school_id).one()
    danceClassToDelete = session.query(DanceClass).filter_by(id=dance_class_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if danceSchool.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this dance class. Please create your own dance school in order to delete a dance class.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(danceClassToDelete)
        flash('Dance Class %s has been deleted!' %(danceClassToDelete.name))
        session.commit()
        return redirect(url_for('showDanceClasses', dance_school_id=dance_school_id))
    else:
        return render_template('deleteDanceClass.html', danceSchool=danceSchool, danceClass=danceClassToDelete, dance_class_id=dance_class_id)


# JSON api endpoints - start
# for dance schools
@app.route('/danceschools/JSON')
def showDanceSchoolsJSON():
    danceSchools = session.query(DanceSchool).all()
    return jsonify(danceSchools=[d.serialize for d in danceSchools])


# for dance class
@app.route('/danceschools/<int:dance_school_id>/danceclasses/JSON')
def showDanceClassesJSON(dance_school_id):
    danceClasses = session.query(DanceClass).filter_by(dance_school_id=dance_school_id).all()
    return jsonify(danceClasses=[c.serialize for c in danceClasses])


# for a dance class
@app.route('/danceschools/<int:dance_school_id>/danceclasses/<int:dance_class_id>/JSON')
def showDanceClassJSON(dance_school_id,dance_class_id):
    danceClass = session.query(DanceClass).filter_by(id=dance_class_id).one()
    return jsonify(danceClass=danceClass.serialize)

# JSON api endpoints - end


# main function
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
