## Project Title
### Item Catalog
This is Item Catalog project. The website contains information for dance schools (category) and list of dance classes (items) associated with each dance school. This itegrates third party user regisration and authentication and provides the CRUD operations facility to the authenticated users.

## Pre-Requisites
1. Download the project folder from given github repository location. 
2. To run this project you will need to install following :
    1) [python 3](https://www.python.org/downloads/)
    2) [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads) to install and manage the VM

## Installation 
1. Download the given project folder.
2. Install Vagrant and VirtualBox. 
This will give you the supported database and ORM needed for this project.
3. You can use Github to fork and clone the repository [here](https://github.com/udacity/fullstack-nanodegree-vm) for VM configuration. 
4. From your terminal, inside the vagrant subdirectory, run the command **vagrant up**. This will cause Vagrant to download the Linux operating system and install it.
5. When vagrant up is finished running, you will get your shell prompt back. At this point, you can run **vagrant ssh** to log in to your newly installed Linux VM!
6. From the downloaded project folder, get the folder **catalog** and place it in **vagrant** directory,which is shared with your virtual machine. cd into **vagrant** directory and run the python files from the terminal as follows :
    (1) `vagrant@vagrant:/vagrant$ python catalog/database_setup.py`
    for the database *dancedataapp* to be set up with the rquired tables.
    (2) `vagrant@vagrant:/vagrant$ python catalog/dance_data.py`
    for the initial test data to be loaded into the set database.
    (3) `vagrant@vagrant:/vagrant$ python catalog/application.py`
    to run the website.
    Access and test your application by visiting http://localhost:8000 locally on your browser.

## Code Example 
This project contains three python file.
1) `database_setup.py`
    (1) It imports sqlalchemy ORM's required modules. 
    eg. `from sqlalchemy import Column, ForeignKey,.... `
    (2) It defines classes for tables with the required column definitions.
    eg. `class DanceSchool(Base):`
    `__tablename__ = 'danceschool'`
    `id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False) ...`
    (3) It holds definition for creating sqlite db engine
    eg. `engine = create_engine('sqlite:///dancedataapp.db')`
    
2) `dance_data.py`
    (1) It imports sqlalchmey ORM's required modules.
    eg. `from sqlalchemy.orm import sessionmaker`
    (2) It holds definition for creating sqlite db engine
    eg. `engine = create_engine('sqlite:///dancedataapp.db')`
    (3) It creates an instance for DBSession object which establishes all conversations with the database and provides the *staging zone* for all the objects loaded into the database session.
    eg. `DBSession = sessionmaker(bind=engine)`
    (4) It creates objects holding the data to be loaded into the tables and uses sesiion object to commit the transactions.
    eg. `danceschool1 = DanceSchool(user_id=1, name="The City Dance Academy",
                           address="405,Main street,Alpharetta,GA, 30004")
session.add(danceschool1)
session.commit()`
    
3. `applicatioan.py` 
    (1) It imports sqlalchmey ORM's required modules.
    eg. `from sqlalchemy.orm import sessionmaker` 
    It also imports Flask's required modules.
    eg. `from flask import Flask, render_template, requesest...`
    (2) It created anti-forgery state token for making login safe.
    eg. `state = ''.join(random.choice(string.ascii_uppercase + ...`
    (3) It defines the functions to authenticate the user and let the authorized user to be logged in.
eg. `def fbconnect() ....`
    (4) It defines the functions to let the User to do CRUD operations .
    eg. `def editDanceSchool(dance_school_id)....`
    (5) It provides JSON API endpoints.
    eg. `@app.route('/danceschools/<int:dance_school_id>/danceclasses/JSON')
def showDanceClassesJSON(dance_school_id)...`

This project also contains HTML files under folder **templates** for giving the view for the application. 
eg. `<section class="main-section flex-item">
          <h3>Dance Schools :</h3>
          <div class="top-div">
              <div class="left-top-div">
		              {% for d in danceSchools %}
                  <p>
                      <span class="title">
                    	{{ d.name }}
                    	</span> ....`

Also css file under **static** folder for styling the web pages 
eg. `.login-box {
    align-self: center;
    border: 8px solid #911454;
    ...`
    
## References 
1. [SQLAlchemy Documentation](http://docs.sqlalchemy.org/en/latest/)
2. [Flask Python microframework](http://flask.pocoo.org/docs/0.12/)
3. [Python and JSON API implementation](http://www.pythonforbeginners.com/api/python-api-and-json)

## Author
Sneha Kale