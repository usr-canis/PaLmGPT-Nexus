from flask import render_template, request, redirect, url_for
from app import app
from bardapi import Bard

#for gpt
import ssl
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util.ssl_ import create_urllib3_context

CIPHERS = "ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384"

class TlsAdapter(HTTPAdapter):
    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)
        
    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = create_urllib3_context(ciphers=CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(*pool_args, ssl_context=ctx, **pool_kwargs)

def send_request(prompt):
    adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)  # prioritize TLS 1.2 
    session = requests.session()
    session.mount("https://", adapter)

    response = session.post("https://chatbot.theb.ai/api/chat-process", json={
        "prompt": f"{prompt}"
    },
    headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0"}, stream=True)

    output = ""
    for chunk in response.iter_content(chunk_size=1024):
        output += chunk.decode("utf-8")

    return output

#actual routes.py starts 
token = "None"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        global token
        token = request.form.get('psid')  
        return redirect(url_for('chat'))

    return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        global token
        bard = Bard(token=token)
        bardresponse = bard.get_answer(prompt)
        gairesponse = send_request(prompt)
        return render_template('chat.html', answerbard=bardresponse,answergpt=gairesponse)
    return render_template('chat.html')