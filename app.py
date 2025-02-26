from flask import Flask, request, render_template, redirect, jsonify
from pymongo import MongoClient

# add mongo cluster
client=MongoClient("mongodb+srv://abubakar:abubakar@practicedb.oawi8.mongodb.net/?retryWrites=true&w=majority&appName=practicedb")

db=client["day_1_3"]
collection=db["user1"]

app = Flask(__name__)

# homepage
@app.route('/', methods=['GET'])
def homepage():
    return render_template('web_page.html')

# add a new user
@app.route('/new_user_form', methods=['POST'])
def new_user_form():
    id = request.form['id']
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']
    data={
        "_id":id, 
        "name":name, 
        "email":email,
        "password": password,
        "role": role
        }
    collection.insert_one(data)
    return redirect('/')

# update existing user
@app.route("/update_user", methods=['POST'])
def update_user_form():
    id = request.form['id']
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']
    data={"$set":{
        # "_id":id, 
        "name":name, 
        "email":email,
        "password": password,
        "role": role
        }}
    collection.update_one({"_id":id}, data)
    # collection.update_one(id, data)
    return redirect('/')

# delete a user
@app.route('/delete_user_form', methods=['POST'])
def delete_user_form():
    
    id = request.form['id']
    password = request.form['password']
    
    data = {"_id": id,
            "password":password}
    collection.delete_one(data)
    return redirect('/')


@app.route('/read_user_form', methods=['POST'])
def read_user_form():
    print("requested======")
    # id = request.form['id']  # Use .get() to avoid KeyError
    id = request.form.get('id')  # Use .get() to avoid KeyError
    
    # print(request.methods)
    print(request.headers)
    # print(request.body)
    if not id:
        return jsonify({"error": "ID is required"}), 400  # Bad request if ID is missing

    user = collection.find_one({"_id": id})
    # print(user)

    if user:
        return ({
            "id": user["_id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }),200
    
    return jsonify({"error": "User not found"}), 404  # Always return a response



if __name__=='__main__':
    app.run()