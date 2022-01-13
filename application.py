from flask import Flask, session
from flask import request, jsonify, json
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_s3 import FlaskS3
from werkzeug.utils import secure_filename 
from Upload import upload_image

import jwt

app = Flask(__name__)
app.config['FLASKS3_BUCKET_NAME'] = 'motophoto'

CORS(app)
bcrypt = Bcrypt(app)
import os
from dotenv import load_dotenv
load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

import models
models.db.init_app(app)



def root():
    return 'okkkk'
app.route('/', methods=["GET"])(root)


# @app.route('/upload', methods=["POST"])
# def upload():
#     image = request.files["file"]
#     if image:
#         filename = secure_filename(image.filename)
#         # image.save(filename)
#         # s3.upload_file(Bucket="motophoto", Filename=filename, Key=filename)
#         print("Upload done")
#     return "ok"
    
    
    
# get all the bikes
@app.route('/motorcycles', methods=["GET"])
def get_all_bikes():
    bikes_qs = models.Motorcycles.query.all() 
    return {
        "bikes": [b.to_json() for b in bikes_qs]
        # "ok"
    }
    
#   get on moto details
@app.route("/motorcycles/<int:moto_id>", methods=["GET"])
def get_details(moto_id):
    moto_qs = models.Motorcycles.query.filter_by(id=moto_id).first_or_404()
    return moto_qs

# create a motorscyle post
@app.route('/motorcycles/create/<int:user_id>', methods=["POST"])
def create_motorcycle(user_id):
  
    motorcycle = models.Motorcycles(
        
        user_id = user_id,
        make=request.json["make"],
        model=request.json["model"],
        year=request.json["year"],
        price = request.json["price"],
        description=request.json["description"],
        photo=request.json["photo"]
        
    )
   
    models.db.session.add(motorcycle)
    models.db.session.commit()
    return {
    "motorcycle": motorcycle.to_json()
    }
    
# sign up a user
@app.route('/auth/signup', methods=["POST"])
def create_user():
    user = models.Users(
        fn = request.json["first_name"],
        ln = request.json["last_name"],
        age = request.json["age"],
        email = request.json["email"],
        username = request.json["username"],
        password = request.json["password"],
        role = request.json["role"]
        
    )
    models.db.session.add(user)
    models.db.session.commit()
    return {
        'user created': user.id
    }

# rent a bike by id,
@app.route( "/rent/<int:user_id>/<int:moto_id>", methods=["POST"])
def rent_moto(user_id,moto_id):
    moto = models.Motorcycles.query.filter_by(id=moto_id).first()
    
    rent_moto = models.Rents(
        user_id=user_id,
        moto_id=moto.id,
        start_date=request.json["start_date"],
        end_date=request.json["end_date"],
        # total_price=request.json["total_price"],
        # confirmed= True

    )
    rent_moto.total_price = rent_moto.charge_total(moto_id)
    models.db.session.add(rent_moto)
    models.db.session.commit()
    return {
        'rent created': rent_moto.to_json(),
        # 'total': rent_moto.charge_total(moto_id)
    }
    
    # get rented bikes
@app.route("/motorcycles/rented/<int:user_id>", methods=["GET"])
def get_rented(user_id):
    try:
        rented_motos = models.Rents.query.filter_by(user_id=user_id)
        print(rented_motos)
        return {
            "rented_motos": [r.to_json() for r in rented_motos]
        }
    except Exception as e:
        return jsonify({"error" : f'{e}'})


# comment on the bike
@app.route("/comment/<int:user_id>/<int:moto_id>", methods=["POST"])
def commment_bike(user_id, moto_id):
    try:
                
        comment = models.Comments(
            user_id=user_id,
            moto_id=moto_id,
            title=request.json["title"],
            comment=request.json["comment"],  
      
        )
        print(comment.to_json())
        models.db.session.add(comment)
        models.db.session.commit()
        return {
            "comment created": comment.to_json()
        }
    except Exception as e:
        return jsonify({"error" : f'{e}'})
 
 #get comments for one bike
@app.route("/comments/<int:moto_id>", methods=["GET"])   
def get_comments(moto_id):
    comments = models.Comments.query.filter_by(moto_id=moto_id)
    # print(comments)
    return {
    "comments": [c.to_json() for c in comments]
    }
# #############not workinhg
# delete a moto
@app.route("/delete/<int:moto_id>", methods=["DELETE"])
def delete_moto(moto_id):
    print(moto_id)
    try:
        deleted_moto = models.Motorcycles.query.filter_by(id=moto_id).first()
        # print(deleted_moto)
        # it doesnt delete but it changes the user_id = 0
        # deleted_moto.user_id = 0
        models.db.session.delete(deleted_moto)
        models.db.session.commit()
        return {
            "deleted moto": deleted_moto.to_json()
            # jsonify(deleted_moto)
        }
    except Exception as e:
        # print(e)
        return jsonify({"error" : f'{e}'})
    
    
# update a moto info (only the price)
@app.route("/update/<int:moto_id>", methods=["PUT"])
def update_moto(moto_id):
    try:
        update_moto = models.Motorcycles.query.filter_by(id=moto_id).first()
        # update_moto.make = request.json["make"]
        # update_moto.model = request.json["model"]
        update_moto.price =request.json["price"]
        # update_moto.description =request.json["description"]
        
        models.db.session.add(update_moto)
        models.db.session.commit()
        return {
            "updated moto": update_moto.to_json()
        }
    except Exception as e:
        # print(e)
        return jsonify({"error" : f'{e}'})
         

# get the posts for my bike
@app.route("/myBike/<int:user_id>", methods=["GET"])
def my_bikes(user_id):
    try:
        my_bike = models.Motorcycles.query.filter_by(user_id=user_id)
      
        return {
            "my_posts": [m.to_json() for m in my_bike]
        }
    
    except Exception as e:
        # print(e)
        return jsonify({"error" : f'{e}'})
  
      
      
@app.route("/signup", methods=["POST"])
def signup():
    hashed_pw = bcrypt.generate_password_hash(request.json["password"]).decode("utf-8")
    try:
        user = models.Users(
            fn=request.json["first_name"],
            ln=request.json["last_name"],
            age=request.json["age"],
            email=request.json["email"],
            username=request.json["username"],
            password=hashed_pw,
            role=request.json["role"]
            
        )   
        models.db.session.add(user)
        models.db.session.commit()
        # encrypted_id = jwt.encode({"user_id":user.id},  os.environ.get("JWT_SECRET"), algorithm="HS256")
        return {"user":user.to_json()
        # "user_id":encrypted_id}
        }
    except Exception as e:
    # # Remeber to inluce 400 so that fronten knows it
        return jsonify({"message" : f'{e}'}), 400
    # except sqlalchemy.exc.IntegrityError:
    # # Remeber to inluce 400 so that fronten knows it
    #     return {"message": 'Email must be unique'}, 400
    
@app.route("/signin", methods=["POST"])
def signin():
    user = models.Users.query.filter_by(username=request.json["username"]).first_or_404()
    if bcrypt.check_password_hash(user.password, request.json["password"]):
        # encrypted_id = jwt.encode({"userId":user.id}, os.environ.get("JWT_SECRET"), algorithm="HS256")
        return {
            "user": user.to_json(),
            # "userId": encrypted_id
        }
    else:
        return {
        "message": "Login failed"
        }, 401
        

@app.route('/users/verify', methods=["GET"])
def verify_user():


  user = models.Users.query.filter_by(id=request.headers["Authorization"]).first() # How to 
  if not user:
    return {
      "message": "user not found"
    }, 404


  return {"user": user.to_json()}

@app.route('/user/<int:user_id>', methods=["GET"])
def get_one_user(user_id):
    user = models.Users.query.filter_by(id=user_id).first_or_404()
    return {
        "user": user.to_json()
    }
@app.route('/motorcycle/<int:moto_id>', methods=["GET"])
def get_one_moto(moto_id):
    moto = models.Motorcycles.query.filter_by(id=moto_id).first_or_404()
    return {
        "moto": moto.to_json()
    }

if __name__ == '__main__':
    port = os.environ.get('PORT') or 5000
    app.run('0.0.0.0', port=port, debug=True)