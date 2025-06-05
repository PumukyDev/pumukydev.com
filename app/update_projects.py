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

def load_blacklist(path="blacklist.txt"):
    if not os.path.exists(path):
        return set()
    with open(path, "r") as f:
        return set(line.strip() for line in f if line.strip())

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

def calculate_score(stars, updated_at):
    score = stars * 5
    dt = datetime.fromisoformat(updated_at.rstrip("Z")).replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    days = (now - dt).days
    if days <= 5:
        score += 20
    elif days <= 20:
        score += 10
    elif days <= 30:
        score += 5
    elif days <= 365:
        score += 1
    return score

def update_projects():
    res = requests.get(API_URL, headers=HEADERS)
    res.raise_for_status()
    repos = res.json()

    result = []

    blacklist = load_blacklist()

    for repo in repos:
        if repo["fork"] or repo["name"] in blacklist:
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

        score = calculate_score(repo["stargazers_count"], repo["updated_at"])

        homepage = repo.get("homepage")
        if homepage:
            if homepage.startswith("https://pumukydev.github.io"):
                score += 20
            else:
                score += 50

        project = {
            "name": name,
            "description": repo.get("description", ""),
            "tags": repo.get("topics", []),
            "stars": repo["stargazers_count"],
            "updated": format_updated_at(repo["updated_at"]),
            "cover": f"/static/previews/{name}.png" if image_url else "",
            "github": repo["html_url"],
            "score": score
        }

        if homepage and not homepage.startswith("https://pumukydev.github.io"):
            project["website"] = homepage

        result.append(project)

    result.sort(key=lambda r: r["score"], reverse=True)

    os.makedirs("data", exist_ok=True)
    with open("data/projects.json", "w") as f:
        json.dump(result, f, indent=2)

    print("✅ Repositorios actualizados.")

if __name__ == "__main__":
    update_projects()
