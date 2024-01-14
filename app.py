from flask import Flask, request
import json
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']


@app.route('/')
def wlcom():
    response = '{"msg":"Server api is runing and waiting for requests..."}'
    
    return json.loads(response)

@app.route('/bigf', methods=['POST'])
def bigf():
    response = ''
    try:  
        response = request.get_json()
        
    except:
        response = '{"msg":"Failed to load data request !"}'

    return response
