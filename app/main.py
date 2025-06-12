from flask import Flask, render_template, request, abort
import json
import os
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
    """Return a slice of data for the given page."""
    start = (page - 1) * per_page
    end = start + per_page
    return data[start:end]

@app.route('/cards/<section>')
def cards_fragment(section):
    """
    Return a fragment of cards for the given section (projects or experience).
    Includes pagination via the 'page' query parameter.
    """
    if section not in ['projects', 'experience']:
        abort(404)

    try:
        data = load_json_data(f"{section}.json")
    except FileNotFoundError:
        abort(404)

    page = int(request.args.get('page', 1))
    sliced = paginate(data, page)
    next_page = page + 1 if page * 4 < len(data) else None

    return render_template('cards_fragment.html', cards=sliced, next_page=next_page)
