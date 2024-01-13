from flask import Flask
import json
import os

app = Flask(__name__)

@app.route('/')
def process():
    response = '{"msg":"Server api is runing and waiting for requests..."}'
    
    return json.loads(response)
