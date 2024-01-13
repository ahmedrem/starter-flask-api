from flask import Flask
import json
import os

app = Flask(__name__)

@app.route('/')
def process():
    response = '{"msg":"Server api is runing and waiting for requests..."}'
    
    return response


@app.route('/process', method=['POST'])
def process():
    response = ''
    try:  
        response = request.form["infos"]
        
    except:
        response = '{"msg":"Failed to load data request !"}'

    return json.loads(response)
