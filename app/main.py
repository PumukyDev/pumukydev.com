from flask import Flask, render_template, request, abort
import json
import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# --- Fragmentos reutilizables para proyectos y experiencia ---

def load_json_data(filename):
    path = os.path.join(os.path.dirname(__file__), 'data', filename)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def paginate(data, page, per_page):
    start = (page - 1) * per_page
    end = start + per_page
    return data[start:end]

@app.route('/cards/<section>')
def cards_fragment(section):
    if section not in ['projects', 'experience']:
        abort(404)

    page = int(request.args.get('page', 1))
    per_page = 5
    try:
        data = load_json_data(f"{section}.json")
    except FileNotFoundError:
        abort(404)

    sliced = paginate(data, page, per_page)
    if not sliced:
        abort(404)

    return render_template('cards_fragment.html', cards=sliced)

# --- GitHub preview image fetching ---

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = "PumukyDev"
REPO_LIST = ["url-shortener", "pi-pumukychat"]
PREVIEW_DIR = os.path.join(app.static_folder, "previews")
os.makedirs(PREVIEW_DIR, exist_ok=True)

def fetch_preview_image(repo):
    query = {
        "query": f"""
        {{
          repository(owner: "{OWNER}", name: "{repo}") {{
            openGraphImageUrl
          }}
        }}
        """
    }

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.github.com/graphql", json=query, headers=headers)
    response.raise_for_status()

    return response.json()["data"]["repository"]["openGraphImageUrl"]

def download_preview_images():
    for repo in REPO_LIST:
        try:
            url = fetch_preview_image(repo)
            path = os.path.join(PREVIEW_DIR, f"{repo}.png")
            r = requests.get(url)
            r.raise_for_status()
            with open(path, "wb") as f:
                f.write(r.content)
            print(f"✅ {repo} guardado en {path}")
        except Exception as e:
            print(f"❌ Error con {repo}: {e}")
