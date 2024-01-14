from flask import Flask, request
import boto3
import json
import os

#############################################################################

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
    return data['Body'].read()
    #return json.loads(data['Body'].read())

#############################################################################

@app.route('/')
def wlcom():
    response = '<marquee><h1>This is a flask API for the HPRAPP</h1><h2>Created by AhmedRem</h2></marquee>'
    return response

#############################################################################

@app.route('/auth', methods=['POST'])
def auth():
    response = ''
    try :  
        data = request.get_json()
        saveData(data)
        response = "data was stored successfully in json file !"
    except Exception as e :
        response = str(e)
        #response = str(os.listdir(os.getcwd()))
    return response

#response = s3_client.delete_object(Bucket=bucket_name, Key=file_name)

#############################################################################

@app.route('/bigf', methods=['POST'])
def bigf():
    response = ''
    try:  
        response = request.get_json()   
    except Exception as e :
        response = str(e)
    return response

#############################################################################

@app.route('/adduser', methods=['POST'])
def adduser():
    response = ''
    try:  
        user = request.get_json()
        olddata = json.loads(loadData())
        response = olddata
        #newdata = json.dumps(olddata)        
        #saveData(newdata)
        #response = "data was stored successfully in json file !"
    except Exception as e :
        response = str(e)
    return response

#############################################################################

@app.route('/lstusers', methods=['GET'])
def lstusers():
    response = ''
    try:  
        response = json.loads(loadData())
    except Exception as e :
        response = str(e)
    return response

#############################################################################

@app.route('/delall', methods=['GET'])
def delall():
    response = ''
    try:  
        var = {"users":[{"email":"root","bf":"root","img":"root"}]}
        saveData(json.dumps(var))
        response = "list reseted successfully !"
    except Exception as e :
        response = str(e)
    return response

#############################################################################
