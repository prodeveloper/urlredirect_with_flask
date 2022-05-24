from crypt import methods
from flask import Flask, render_template, request, redirect, url_for
import json
import os
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html', name = "jacob")
@app.route('/about')
def about():
    return {"message":"we are awesome"}
@app.route('/another')
def na_tena():
    return {"message":"another one"}
@app.route('/your-url', methods=['POST', 'GET'])
def your_url():
    if request.method == 'GET':
        return redirect(url_for('home'))
    if request.method=='POST':
        if check_exists():
            return redirect(url_for('home'))
        save_code()
        code = request.form['code']
        url_to = request.form['url']
        return render_template("your_url.html", 
            code = code,
            url_to = url_to
            )
def save_code():
    urls = {}
    code = request.form['code']
    url_to = request.form['url']
    urls[code]= {'url': url_to}
    with open('urls.json', 'w') as url_file:
        json.dump(urls,url_file)
def check_exists():
    if (os.path.exists('urls.json')==False):
        return False
    with open('urls.json','r') as url_file:
        urls = json.load(url_file)
        code = request.form['code']
        if code in urls.keys():
            return True
        else:
            return False
