from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=True)
    last_name = db.Column(db.String(120), nullable=False)
    age = db.Column( db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column( db.String, nullable=False)
    motorcycles = db.relationship("Motorcycles", backref="users", lazy=True)
    comments  = db.relationship("Comments", backref="users", lazy=True)
    rents =  db.relationship("Rents", backref="users", lazy=True)
    # how you create the data in the database to be saved....
    def __init__(self, fn, ln, age, email,username, password,role):
        self.first_name = fn
        self.last_name = ln
        self.age = age
        self.email = email
        self.username = username
        self.password = password
        self.role = role
        

    def to_json(self):
        return {
        "id": self.id,
        "username":self.username,
        "email": self.email,
      # "password":self.password
    }
    
    
class Comments(db.Model):
    __tablename__ = 'comments'
    id=db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    moto_id =db.Column(db.Integer, db.ForeignKey('motorcycles.id'))
    title = db.Column(db.String(20), nullable=False)
    comment = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
  
    
    def __init__(self, user_id, moto_id, title, comment):
        # self.id= id
        self.user_id = user_id
        self.moto_id= moto_id
        self.title = title
        self.comment = comment
        self.date = datetime.now()
     
    def to_json(self):
        return {
        "id":self.id,
        "user_id":self.user_id,
        "moto_id":self.moto_id,
        "title": self.title,
        "comment": self.comment,
        "date": self.date
    }   
        
        
class Motorcycles(db.Model):
    __tablename__ ='motorcycles'    
    id = db.Column( db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    make = db.Column( db.String, nullable=False)
    model=db.Column( db.String, nullable=False)
    year=db.Column(db.String, nullable=False)
    price=db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=False)
    photo = db.Column(db.String)
    rents = db.relationship("Rents", backref="motorcycles", lazy=True)
    comments = db.relationship("Comments", backref="motorcycles", lazy=True)
    def __init__(self,user_id, make,model,year,price,description,photo):
        # self.id=id
        self.user_id = user_id
        self.make = make
        self.model = model
        self.year = year
        self.price = price
        self.description = description
        self.photo = photo
        
    def to_json(self):
        return {
            "id":self.id,
            'make':self.make,
            'model':self.model,
            'year':self.year,
            'price':self.price,
            'description':self.description,
            'photo':self.photo
        }
    
class Rents(db.Model):
    __tablename__ = 'rent'
    id=db.Column( db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    moto_id = db.Column(db.Integer, db.ForeignKey('motorcycles.id'))
    start_date = db.Column( db.String, nullable=False)
    end_date = db.Column(db.String, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    confirmed = db.Column(db.Boolean)
   
    def __init__(self, user_id, moto_id, start_date, end_date):
        self.user_id = user_id
        self.moto_id = moto_id
        self.start_date = start_date
        self.end_date = end_date
        # self.total_price=total_price
        self.confirmed = False
        
    def to_json(self):
        return {
            'id':self.id,
            'moto_id':self.moto_id,
            'start_date':self.start_date,
            'end_date':self.end_date,
            'total_price':self.total_price,
            'confirmed':self.confirmed
           
        }
    def charge_total(self,moto_id):
        days = int(self.end_date[-2:]) - int(self.start_date[-2:])
        
        
        moto_qs = Motorcycles.query.filter_by(id=moto_id)
        print(moto_qs)
        
        if moto_qs:
            moto = moto_qs.first()
            print(moto)
            print(moto.price)
            return moto.price * days
        return 0   