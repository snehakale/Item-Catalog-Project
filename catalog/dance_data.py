''' This is dance_data.py file.
    This creates test data for danceschool app database.
'''

# Importing required sqlalchemy modules
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Importing required classes from database_setup.py file.
from database_setup import Base, User, DanceSchool, DanceClass

# Creating engine for danceschoolapp database
engine = create_engine('sqlite:///dancedataapp.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object.
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Creating a dummy user
User1 = User(name="Tester", email="tester@gmail.com",
             picture='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=0ahUKEwj2g56Z7L7XAhUL4SYKHRLzD6MQjRwIBw&url=https%3A%2F%2Fnelsonvets.co.uk%2Funknown%2F&psig=AOvVaw14UMfE0eIwLlTTW5OGEYAI&ust=1510775673253353')
session.add(User1)
session.commit()

# Creating data for dance school and classes
# data for The City Dance Academy
danceschool1 = DanceSchool(user_id=1, name="The City Dance Academy",
                           address="405,Main street,Alpharetta,GA, 30004")
session.add(danceschool1)
session.commit()

danceclass1 = DanceClass(user_id=1, name="Jazz",
                         description="Learn both Tap dance and Jitterbug on the Jazz music",
                         teacher="Tony T", sessions="15", fees="50",
                         danceschool=danceschool1)
session.add(danceclass1)
session.commit()

danceclass2 = DanceClass(user_id=1, name="Ballet (Beginner)",
                         description="In this beginner class, you will improve technique and expand your basic ballet training.",
                         teacher="Rachel", sessions="5", fees="80",
                         danceschool=danceschool1)
session.add(danceclass2)
session.commit()

danceclass3 = DanceClass(user_id=1, name="Ballet (Updated)",
                         description="Classiscal Ballet above the beginner level in relaxed atmosphere",
                         teacher="Rachel", sessions="5", fees="100",
                         danceschool=danceschool1)
session.add(danceclass3)
session.commit()

danceclass4 = DanceClass(user_id=1, name="Salsa Blast",
                         description="Learn club style Salsa alongwith burning out your calories",
                         teacher="Bennie", sessions="10", fees="35",
                         danceschool=danceschool1)
session.add(danceclass4)
session.commit()

# data for Hit the Floor Dance School
danceschool2 = DanceSchool(user_id=1, name="Hit the Floor Dance School",
                           address="101,Dance Hall,Atlanta,GA,30303")
session.add(danceschool2)
session.commit()

danceclass1 = DanceClass(user_id=1, name="Hip-Hop Hit",
                         description="Learn Hip-Hop and Contemporary dance styles",
                         teacher="John", sessions="10", fees="30",
                         danceschool=danceschool2)
session.add(danceclass1)
session.commit()

danceclass2 = DanceClass(user_id=1, name="Ballet (Beginner)",
                         description="In this beginner class, you will improve technique and expand your basic ballet training.",
                         teacher="Sara W", sessions="5", fees="75",
                         danceschool=danceschool2)
session.add(danceclass2)
session.commit()

danceclass3 = DanceClass(user_id=1, name="Ballet (Updated)",
                         description="Classiscal Ballet above the beginner level in relaxed atmosphere",
                         teacher="Sara W", sessions="5", fees="100",
                         danceschool=danceschool2)
session.add(danceclass3)
session.commit()

# data for Dance of India
danceschool3 = DanceSchool(user_id=1, name="Dance of India",
                           address="1234,Perimieter Hall,Atlanta,GA, 30333")
session.add(danceschool3)
session.commit()

danceclass1 = DanceClass(user_id=1, name="Kathak",
                         description="Learn Kathak dance enjoying classical Indian music",
                         teacher="Seema", sessions="20", fees="50",
                         danceschool=danceschool3)
session.add(danceclass1)
session.commit()

danceclass2 = DanceClass(user_id=1, name="Bharathnatyam",
                         description="Learn Bharathnatyam dance based on south Indian music",
                         teacher="Laxmi", sessions="20", fees="50",
                         danceschool=danceschool3)
session.add(danceclass2)
session.commit()

danceclass3 = DanceClass(user_id=1, name="Bolywood Dance",
                         description="Learn  bolywood style dance on bolywood music",
                         teacher="Seema", sessions="10", fees="50",
                         danceschool=danceschool3)
session.add(danceclass3)
session.commit()

danceclass4 = DanceClass(user_id=1, name="Bhangara Dance",
                         description="Learn Bhangara dance enjoying punjabi bhangara music",
                         teacher="Sony", sessions="10", fees="50",
                         danceschool=danceschool3)
session.add(danceclass4)
session.commit()

# data for Fitness and Dance
danceschool4 = DanceSchool(user_id=1, name="Fitness and Dance",
                           address="3456, North Park Center, Alpharetta, Ga,30005")
session.add(danceschool4)
session.commit()

danceclass1 = DanceClass(user_id=1, name="Zumba",
                         description="Enjoy Zumba dance burning down the calories",
                         teacher="Kelly", sessions="20", fees="20",
                         danceschool=danceschool4)
session.add(danceclass1)
session.commit()

danceclass2 = DanceClass(user_id=1, name="Salsa",
                         description="Learn Salsa enjoying Salsa music and stay fit!",
                         teacher="Kelly", sessions="20", fees="20",
                         danceschool=danceschool4)
session.add(danceclass2)
session.commit()

print "Added Dance Data!"
