from flask import render_template, request, redirect, url_for
from app import app
from bardapi import Bard
import os

token="None"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        global token 
        token = request.form.get('psid')
        # Process the key and retrieve data based on it


        
        return redirect(url_for('chat'))

    return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        #call


        

    return render_template('chat.html')