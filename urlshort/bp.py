from crypt import methods
import imp
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, session, jsonify
import json
import os
import datetime
user_files = "/Users/jacobchencha/Documents/code/flask_tutorial/url-shortener/static/user_files"
bp = Blueprint('urlshort', __name__)
@bp.route('/')
def home():
    return render_template('home.html', name = "jacob", urls = session.keys())
@bp.route('/about')
def about():
    return {"message":"we are awesome"}

@bp.route('/your-url', methods=['POST', 'GET'])
def your_url():
    if request.method == 'GET':
        return redirect(url_for('urlshort.home'))
    if request.method=='POST':
        if 'url' in request.form.keys():
            save_url()
        elif 'file' in request.files.keys():
            save_file()
        code = request.form['code']
        return render_template("your_url.html", 
            code = code,
            )
@bp.route('/<string:code>')
def redirect_url(code):
    with open('urls.json','r') as url_file:
        urls = json.load(url_file)
        if code in urls.keys():
            if 'url' in urls[code].keys():
                return redirect(urls[code]['url'])
            elif 'file' in urls[code].keys():
                filename = os.path.basename(urls[code]['file'])
                return redirect(url_for('static',filename='user_files/' + filename))
            return redirect(urls[code]['url'])
        else:
            abort(404)
    return code
@bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@bp.route('/api/list-urls')    
def api():
    return jsonify(list(session.keys())), 200
def save_url():
        if check_exists():
            flash("URL already exists")
            return redirect(url_for('urlshort.home'))
        save_to_urls()

def save_file():
    urls = {}
    f = request.files['file']
    code = request.form['code']
    full_name = os.path.join(user_files, f.filename)
    f.save(full_name)
    append_urls(full_name)
    return redirect(url_for('urlshort.home'))

def save_to_urls():
    append_urls()

def append_urls(filename=False):
    with open('urls.json','r') as url_file:
        urls = json.load(url_file)
        code = request.form['code']
        url_to = filename if filename else request.form['url']
        key = "file" if filename else "url"
        urls[code]= {key: url_to}
        with open('urls.json', 'w') as url_file:
            json.dump(urls,url_file)
        session[code] = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
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

