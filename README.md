# Clonehub ⚡

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![PyWebView](https://img.shields.io/badge/PyWebView-Native_GUI-success?style=for-the-badge)

A high-performance, cross-platform desktop application designed to manage and clone multiple GitHub repositories concurrently. Built with a lightweight Python backend and a responsive, cyberpunk-inspired UI.

Clonehub leverages Git's blobless cloning features and Python's `asyncio` to saturate network bandwidth, dramatically reducing the time required to onboard new environments or backup enterprise repository ecosystems.

## 🚀 Key Features

* **Concurrent Operations:** Clones multiple repositories simultaneously using asynchronous subprocesses.
* **Network Optimized:** Implements Git `--filter=blob:none` by default to minimize initial network payload.
* **Seamless Authentication:** Integrates a local ephemeral server for secure GitHub OAuth 2.0 device flow—no manual Personal Access Tokens (PAT) required.
* **Native GUI:** Renders a modern React/Tailwind frontend inside a native OS window (WebView2/WebKit) without the overhead of Electron.

## 🛠️ Tech Stack

* **Backend:** Python, `asyncio`, FastAPI (for OAuth local callback)
* **Frontend:** HTML5, Tailwind CSS (via CDN)
* **System Wrapper:** PyWebView
* **Version Control Integration:** System Git CLI

## ⚙️ Installation & Setup

### Prerequisites
* Git installed and added to the system PATH.
* Python 3.10 or higher.
* A GitHub OAuth App registered in your Developer Settings (Callback URL: `http://127.0.0.1:8000/callback`).

### 1. Clone the repository
```bash
git clone [https://github.com/pablomrtinezzz/Clonehub.git](https://github.com/pablomrtinezzz/Clonehub.git)
cd Clonehub
