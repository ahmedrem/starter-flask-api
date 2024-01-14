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
    try:  
        response = request.get_json()
        #data = '{"email":"'+respnse.get("email")+'"}'
        with open('data.json', 'w') as f:
            json.dump(response, f)
    except:
        response = '{"msg":"Failed to load data from Auth !"}'

    return response



@app.route('/bigf', methods=['POST'])
def bigf():
    response = ''
    try:  
        response = request.get_json()
        
    except:
        response = '{"msg":"Failed to load data request !"}'

    return response
