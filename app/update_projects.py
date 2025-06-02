import os
import requests
import json
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = "PumukyDev"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

API_URL = f"https://api.github.com/users/{OWNER}/repos?per_page=100"
PREVIEW_DIR = os.path.join("static", "previews")
os.makedirs(PREVIEW_DIR, exist_ok=True)

def get_opengraph_image(repo):
    query = {
        "query": f"""
        {{
          repository(owner: "{OWNER}", name: "{repo}") {{
            openGraphImageUrl
          }}
        }}
        """
    }
    response = requests.post("https://api.github.com/graphql", json=query, headers=HEADERS)
    return response.json()["data"]["repository"]["openGraphImageUrl"]

def format_updated_at(iso_date):
    dt = datetime.fromisoformat(iso_date.rstrip("Z")).replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    delta = now - dt
    days = delta.days
    return f"{days} day{'s' if days != 1 else ''} ago"

def update_projects():
    res = requests.get(API_URL, headers=HEADERS)
    res.raise_for_status()
    repos = res.json()

    result = []

    for repo in repos:
        if repo["fork"]:
            continue

        name = repo["name"]
        print(f"Processing {name}...")
        try:
            image_url = get_opengraph_image(name)
            if image_url:
                image_data = requests.get(image_url).content
                with open(os.path.join(PREVIEW_DIR, f"{name}.png"), "wb") as f:
                    f.write(image_data)
        except Exception as e:
            print(f"⚠️  Could not fetch image for {name}: {e}")
            image_url = ""

        result.append({
            "name": name,
            "description": repo.get("description", ""),
            "tags": repo.get("topics", []),
            "stars": repo["stargazers_count"],
            "updated": format_updated_at(repo["updated_at"]),
            "cover": f"/static/previews/{name}.png" if image_url else ""
        })

    os.makedirs("data", exist_ok=True)
    with open("data/projects.json", "w") as f:
        json.dump(result, f, indent=2)

    print("✅ Repositorios actualizados.")

if __name__ == "__main__":
    update_projects()
