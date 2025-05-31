from flask import Flask, render_template, request, abort
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projects/fragment')
def projects_fragment():
    page = int(request.args.get('page', 1))
    per_page = 5

    json_path = os.path.join(os.path.dirname(__file__), 'data', 'projects.json')
    with open(json_path) as f:
        projects = json.load(f)

    start = (page - 1) * per_page
    end = start + per_page
    sliced = projects[start:end]

    if not sliced:
        abort(404)

    return render_template('projects_fragment.html', projects=sliced)
