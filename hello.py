from flask import Flask
import mysql.connector
import json
import os

app = Flask(__name__)
# hello.py
print("Hello, world! This is a new feature!")

group_name = os.getenv("DATABASE_NAME")

mydb = mysql.connector.connect(user='root', password='secret',
                              host='mysql', 
                              port='3306',
                              database=group_name,
                              )

@app.route('/hello/<name>', methods=['GET'])
def hello(name):
    return f'Hello, {name}!'

@app.route('/students', methods=['GET'])
def all_students():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Students")
    myresult = mycursor.fetchall()
    all_students = {}
    for i in myresult:
        student = {"ID": i[0], "first_name": i[1], "middle_name": i[2], "second_name": i[3], "email": i[4]}
        all_students[i[0]] = student
    return json.dumps(all_students)

@app.route('/students/<id>', methods=['GET'])
def student_by_id(id):
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM Students WHERE id = {id}")
    myresult = mycursor.fetchone()
    return json.dumps(
        {"first_name": myresult[1],
         "middle_name": myresult[2], 
         "second_name": myresult[3], 
         "email": myresult[4]})
