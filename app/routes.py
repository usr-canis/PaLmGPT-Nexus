from flask import render_template, request, redirect, url_for
from app import app

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        key = request.form.get('key')
        # Process the key and retrieve data based on it

        return redirect(url_for('chat'))

    return render_template('index.html')