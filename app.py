from flask import Flask, request
import boto3
import json
import os

#############################################################################

ngrokserver = "https://a92f-197-153-96-243.ngrok-free.app"

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
s3 = boto3.client('s3')

#############################################################################

def saveData(data):
    s3.put_object(
        Body=json.dumps(data),
        Bucket="cyclic-outstanding-tank-top-tick-eu-west-3",
        Key="data/data.json"
    ) 

def loadData():
    data = s3.get_object(
        Bucket="cyclic-outstanding-tank-top-tick-eu-west-3",
        Key="data/data.json"
    )
    return json.loads(data['Body'].read())

#response = s3_client.delete_object(Bucket=bucket_name, Key=file_name)

#############################################################################

@app.route('/')
def wlcom():
    response = '<marquee><h1>This is a flask API for the HPRAPP</h1><h2>Created by AhmedRem</h2></marquee>'
    return response

#############################################################################

@app.route('/newuser', methods=['POST'])
def adduser():
    response = ''
    try:        
        user = request.get_json()
        email = list(user.keys())
        email = email[0]
        data = loadData()
        if(not email in data.keys()):
            data[email] = user.get(email)
        saveData(data)
        response = "new user was added sucessfully to json file !"
    except Exception as e :
        response = str(e)
    return response

#############################################################################

@app.route('/bf', methods=['POST'])
def bigf():
    response = ''
    try:  
        user = request.get_json()
        email = list(user.keys())
        email = email[0]
        data = loadData()
        data[email]["bf"] = user.get(email).get("bf")
        saveData(data)
        response = user.get(email).get("bf")
        #response = "user updated successfully in json file"
    except Exception as e :
        response = str(e)
    return response

#############################################################################

@app.route('/img', methods=['POST'])
def getimage():
    response = ''
    try:  
        user = request.get_json()
        email = list(user.keys())
        email = email[0]
        data = loadData()
        data[email]["img"] = user.get(email).get("img")
        saveData(data)
        link = {"server":ngrokserver}
        response = json.dumps(link)
        #response = user.get(email).get("img")
        #response = "user updated successfully in json file"
    except Exception as e :
        response = str(e)
    return response

#############################################################################

@app.route('/lstusers', methods=['GET'])
def lstusers():
    response = ''
    try:  
        response = loadData()
    except Exception as e :
        response = str(e)
    return response

#############################################################################

@app.route('/delall', methods=['GET'])
def delall():
    response = ''
    try:  
        data = {"email":{"bf":{"o":"","c":"","e":"","a":"","n":""},"img":""}}
        saveData(data)
        response = "JSON reseted successfully !"
    except Exception as e :
        response = str(e)
    return response

#############################################################################

@app.route('/lnk', methods=['GET'])
def lnk():
    response = ''
    try:  
        link = {"server":"null"}
        response = json.dumps(link)
    except Exception as e :
        response = str(e)
    return response

#############################################################################
