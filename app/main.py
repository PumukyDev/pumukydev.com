from flask import Flask, render_template, request, abort
import json, os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def load_json_data(filename):
    path = os.path.join('data', filename)
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def paginate(data, page, per_page=4):
    start = (page - 1) * per_page
    end = start + per_page
    return data[start:end]

@app.route('/cards/<section>')
def cards_fragment(section):
    if section not in ['projects', 'experience']:
        abort(404)

    try:
        data = load_json_data(f"{section}.json")
    except FileNotFoundError:
        abort(404)

    page = int(request.args.get('page', 1))
    sliced = paginate(data, page)
    next_page = page + 1 if page * 5 < len(data) else None

    return render_template('cards_fragment.html', cards=sliced, next_page=next_page)
