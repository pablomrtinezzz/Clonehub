import webview
import threading
import uvicorn
import requests
import webbrowser
import asyncio
import subprocess
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch credentials securely
CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8000/callback"

# Safety check to prevent running without credentials
if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("CRITICAL: Missing GitHub OAuth credentials in .env file.")

app = FastAPI()
oauth_event = threading.Event()
github_token = None

@app.get("/callback")
def oauth_callback(code: str):
    """
    Handles the GitHub redirect, exchanges code for token, and signals the UI.
    """
    global github_token
    token_url = "https://github.com/login/oauth/access_token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    headers = {"Accept": "application/json"}
    response = requests.post(token_url, json=payload, headers=headers)
    data = response.json()
    
    if "access_token" in data:
        github_token = data["access_token"]
        oauth_event.set()
        # Cyberpunk style success page
        return HTMLResponse(
            "<body style='background:#0f172a;color:#10b981;font-family:monospace;display:flex;align-items:center;justify-content:center;height:100vh;'>"
            "<h2>[ AUTHENTICATION SUCCESSFUL. YOU MAY CLOSE THIS TAB. ]</h2></body>"
        )
    return HTMLResponse("<h2>[ AUTHENTICATION FAILED ]</h2>")

def start_oauth_server():
    """ Runs FastAPI on a background thread. """
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="critical")

async def clone_repo(repo_url: str, target_dir: str) -> bool:
    """ Executes git clone concurrently with blob filtering. """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
        
    # Inject OAuth token into URL for silent authentication
    auth_url = repo_url.replace("https://", f"https://oauth2:{github_token}@")
    command = ["git", "clone", "--filter=blob:none", auth_url, target_dir]
    
    process = await asyncio.create_subprocess_exec(
        *command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    await process.communicate()
    return process.returncode == 0

class BackendApi:
    def __init__(self):
        self.server_started = False

    def authenticate(self):
        """ Triggers the OAuth flow. Expected to be called from JS. """
        global github_token
        github_token = None
        oauth_event.clear()
        
        if not self.server_started:
            threading.Thread(target=start_oauth_server, daemon=True).start()
            self.server_started = True

        auth_url = f"https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=repo"
        webbrowser.open(auth_url)
        
        # Block until callback is hit
        oauth_event.wait()
        return True if github_token else False

    def fetch_repositories(self):
        """ Retrieves repositories via REST API. """
        if not github_token:
            return {"error": "Not authenticated"}
            
        headers = {
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        response = requests.get("https://api.github.com/user/repos?per_page=100&sort=updated", headers=headers)
        
        if response.status_code == 200:
            repos = response.json()
            return [{"name": r["name"], "url": r["clone_url"]} for r in repos]
        return {"error": "Failed to fetch repositories"}

    def clone_selected(self, mappings):
        """ 
        Executes the async cloning loop. 
        mappings format: [{'url': str, 'path': str}]
        """
        if not github_token:
            return "Not authenticated"
            
        async def run_batch():
            tasks = [clone_repo(m['url'], m['path']) for m in mappings]
            results = await asyncio.gather(*tasks)
            return sum(results)
            
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        success_count = loop.run_until_complete(run_batch())
        return f"[ SUCCESS: {success_count}/{len(mappings)} REPOSITORIES CLONED ]"

if __name__ == '__main__':
    api = BackendApi()
    # Create native window embedding index.html
    webview.create_window(
        'NeonClone - High-Speed Git Multi-Cloner', 
        'index.html', 
        js_api=api, 
        width=1000, 
        height=750,
        background_color='#0f172a'
    )
    webview.start(debug=True)