from flask import Flask, request
import json
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']


@app.route('/')
def wlcom():
    response = '<marquee><h1>This is a flask API for the HPRAPP</h1><h2>Created by AhmedRem</h2></marquee>'
    
    return response



@app.route('/auth', methods=['POST'])
def auth():
    response = ''
    try :  
        data = request.get_json()
        #data = '{"email":"'+respnse.get("email")+'"}'
        with open('static/data.json', 'w') as f:
            json.dump(data, f)
        response = "data was stored successfully in json file !"
    except Exception as e :
        #response = str(e)
        response = os.listdir(os.getcwd())

    return response



@app.route('/bigf', methods=['POST'])
def bigf():
    response = ''
    try:  
        response = request.get_json()
        
    except:
        response = '{"msg":"Failed to load data request !"}'

    return response
