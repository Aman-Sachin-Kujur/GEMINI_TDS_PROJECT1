# 🤖 Gemini Task Automation System

**An AI-powered task automation service that receives task descriptions, generates complete web applications using Gemini AI, and automatically deploys them to GitHub Pages.**

## 🎯 What Does This Project Do?

This is an **automated code generation and deployment pipeline** that:

1. **Receives Task Requests** via REST API (POST /ready endpoint)
2. **Generates Code** using Google's Gemini AI based on natural language descriptions
3. **Creates GitHub Repositories** automatically for each task
4. **Deploys to GitHub Pages** making the generated apps instantly accessible
5. **Notifies Completion** by sending deployment details to a callback URL

### 🔄 Complete Workflow

```
User sends task request → API validates → Gemini generates code → 
Creates GitHub repo → Commits & pushes → Enables GitHub Pages → 
Sends notification with live URL
```

## ✨ Key Features

- **Fully Generic** - No hardcoded templates, pure AI-driven generation
- **Background Processing** - Returns HTTP 200 immediately, processes asynchronously
- **Round-based Updates** - Round 1 creates new repos, Round 2+ updates existing ones
- **Attachment Support** - Can include images (logos, mockups, sample data) for AI context
- **Robust Error Handling** - Detailed logging with specific error types
- **JSON Schema Enforcement** - Ensures structured, parseable AI responses
- **Exponential Backoff** - Retries for GitHub API operations
- **Docker Ready** - Production-ready containerization

## 📋 How It Works (Technical Deep Dive)

### 1️⃣ Request Reception
```json
POST /ready
{
  "email": "user@example.com",
  "secret": "auth-token",
  "task": "chess-game",
  "round": 1,
  "brief": "Create a chess game with...",
  "checks": ["Has license", "Works in browser"],
  "evaluation_url": "https://callback.example.com",
  "attachments": []
}
```

### 2️⃣ AI Code Generation
- Sends task brief + checks + attachments to **Gemini 2.5 Flash**
- Uses **JSON schema** to enforce structured output
- AI generates all files (HTML, CSS, JS, README, LICENSE)
- Returns: `{"files": [{"path": "index.html", "content": "..."}]}`

### 3️⃣ GitHub Repository Setup
- **Round 1:** Creates new repository via GitHub API
- **Round 2+:** Clones existing repo, updates files
- Configures git with user credentials
- Commits with descriptive messages

### 4️⃣ Deployment
- Pushes to GitHub with retry logic (5 attempts, exponential backoff)
- Enables GitHub Pages via API
- Waits for Pages to become active

### 5️⃣ Notification
- POSTs deployment results to `evaluation_url`:
```json
{
  "email": "user@example.com",
  "task": "chess-game",
  "repo_url": "https://github.com/user/chess-game",
  "pages_url": "https://user.github.io/chess-game",
  "commit_sha": "abc123..."
}
```

## 🚀 Deployment Options

### Option 1: Docker (Recommended)
```bash
docker build -t gemini-automation .
docker run -p 8080:8080 \
  -e GEMINI_API_KEY=your_key \
  -e GITHUB_TOKEN=your_token \
  -e GITHUB_USERNAME=your_username \
  -e STUDENT_SECRET=your_secret \
  gemini-automation
```

### Option 2: Cloud Platform
Deploy to any platform supporting Docker:
- **Hugging Face Spaces** (includes GPU option)
- **Google Cloud Run** (serverless, auto-scaling)
- **AWS ECS/Fargate** (enterprise-grade)
- **Azure Container Instances** (pay-per-use)
- **DigitalOcean App Platform** (simple, affordable)

### Option 3: Local Development
```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/GEMINI_TDS_PROJECT1.git
cd GEMINI_TDS_PROJECT1

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\Activate.ps1  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 5. Run server
uvicorn main:app --reload --port 8080
```

Access at: `http://localhost:8080`

## 🔑 Required API Keys

### 1. Google Gemini API Key
- Go to: https://aistudio.google.com/app/apikey
- Click "Create API Key"
- Copy the key (starts with `AIza...`)
- **Free tier:** 15 requests/minute, 1500 requests/day

### 2. GitHub Personal Access Token
- Go to: GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
- Click "Generate new token (classic)"
- Select scopes: `repo` (full control of private repositories)
- Generate and copy token (starts with `ghp_...`)
- **Never commit this token!**

### 3. Student Secret (Custom Auth)
- Create your own secret string (e.g., `my-secret-key-12345`)
- Used to authenticate incoming requests
- Can be any string you choose

## ⚙️ Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=AIzaSy...your_key_here
GITHUB_TOKEN=ghp_...your_token_here
GITHUB_USERNAME=your_github_username
STUDENT_SECRET=your_custom_secret_string
```

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | ✅ Yes | Google Generative AI API key for code generation |
| `GITHUB_TOKEN` | ✅ Yes | GitHub PAT with `repo` scope for repo operations |
| `GITHUB_USERNAME` | ✅ Yes | Your GitHub username for repository creation |
| `STUDENT_SECRET` | ✅ Yes | Shared secret for authenticating incoming requests |

## 📊 Project Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Client    │─────▶│  FastAPI     │─────▶│  Gemini AI  │
│  (Postman)  │◀─────│  /ready      │◀─────│  (Code Gen) │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  GitPython   │
                     │  (Local Ops) │
                     └──────────────┘
                            │
                            ▼
                     ┌──────────────┐      ┌─────────────┐
                     │  GitHub API  │─────▶│GitHub Pages │
                     │ (Create Repo)│      │  (Deploy)   │
                     └──────────────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │ Callback URL │
                     │ (Notify Done)│
                     └──────────────┘
```

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **API Framework** | FastAPI | High-performance REST API |
| **AI Model** | Gemini 2.5 Flash | Code generation from natural language |
| **Validation** | Pydantic | Request/config validation |
| **Git Operations** | GitPython | Local repo management |
| **GitHub Integration** | GitHub REST API | Repo creation, Pages deployment |
| **Async Tasks** | asyncio | Background task processing |
| **HTTP Client** | httpx | Async HTTP requests |
| **Container** | Docker | Production deployment |

## 📁 Project Structure

```
GEMINI_TDS_PROJECT1/
├── main.py              # FastAPI app + orchestration logic
├── config.py            # Environment config with validation
├── models.py            # Pydantic request/response models
├── requirements.txt     # Python dependencies
├── Dockerfile           # Production container definition
├── .dockerignore        # Docker build exclusions
├── .gitignore           # Git exclusions
├── .env.example         # Template for environment variables
├── LICENSE              # MIT license
└── README.md            # This file
```

## 📖 API Documentation

### POST /ready

**Description:** Submit a task for AI-powered code generation and deployment

**Request Body:**
```json
{
  "email": "user@example.com",
  "secret": "your_student_secret",
  "task": "unique-task-id",
  "round": 1,
  "nonce": "unique-request-id",
  "brief": "Detailed description of what to build...",
  "checks": ["Requirement 1", "Requirement 2"],
  "evaluation_url": "https://webhook.site/your-id",
  "attachments": [
    {
      "name": "logo.png",
      "url": "data:image/png;base64,iVBORw0KGgo..."
    }
  ]
}
```

**Response:**
```json
{
  "message": "Task received successfully!",
  "task_id": "unique-task-id"
}
```

**Status Codes:**
- `200 OK` - Task accepted, processing in background
- `403 Forbidden` - Invalid secret
- `422 Unprocessable Entity` - Invalid request format

### Callback Notification

When deployment completes, the API POSTs to your `evaluation_url`:

```json
{
  "email": "user@example.com",
  "task": "unique-task-id",
  "round": 1,
  "nonce": "unique-request-id",
  "repo_url": "https://github.com/username/unique-task-id",
  "commit_sha": "abc123def456...",
  "pages_url": "https://username.github.io/unique-task-id"
}
```

## 🧪 Testing

### Test with Postman / cURL

**1. Get a webhook URL:**
- Go to https://webhook.site
- Copy your unique URL

**2. Send test request:**

```bash
curl -X POST http://localhost:8080/ready \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "secret": "your_student_secret",
    "task": "hello-world-test",
    "round": 1,
    "nonce": "test-001",
    "brief": "Create a simple hello world webpage with a gradient background and centered text saying Hello World!",
    "checks": ["Has index.html", "Has MIT license", "Text displays"],
    "evaluation_url": "YOUR_WEBHOOK_URL_HERE",
    "attachments": []
  }'
```

**3. Check results:**
- API returns immediately: `{"message": "Task received successfully!"}`
- Watch webhook.site for completion notification (~30-60 seconds)
- Visit the `pages_url` in notification to see live site

### Example Tasks

<details>
<summary><b>Calculator App</b></summary>

```json
{
  "email": "test@example.com",
  "secret": "your_secret",
  "task": "calculator-app",
  "round": 1,
  "nonce": "calc-001",
  "brief": "Create a calculator with: 1) Basic operations (+, -, ×, ÷), 2) Clear button, 3) Decimal support, 4) Keyboard input, 5) Responsive design with Tailwind CSS",
  "checks": [
    "Has MIT license",
    "README explains usage",
    "Calculator performs addition",
    "Calculator performs subtraction",
    "Has clear button",
    "Responsive design"
  ],
  "evaluation_url": "https://webhook.site/your-id",
  "attachments": []
}
```
</details>

<details>
<summary><b>Todo List</b></summary>

```json
{
  "email": "test@example.com",
  "secret": "your_secret",
  "task": "todo-list-app",
  "round": 1,
  "nonce": "todo-001",
  "brief": "Create a todo list with: 1) Add new tasks, 2) Mark tasks as complete, 3) Delete tasks, 4) LocalStorage persistence, 5) Filter by All/Active/Completed, 6) Task counter, 7) Beautiful UI with animations",
  "checks": [
    "Can add tasks",
    "Can mark complete",
    "Can delete tasks",
    "Tasks persist on refresh",
    "Has filter buttons",
    "Shows task count"
  ],
  "evaluation_url": "https://webhook.site/your-id",
  "attachments": []
}
```
</details>

<details>
<summary><b>Chess Game (With Attachments)</b></summary>

```json
{
  "email": "test@example.com",
  "secret": "your_secret",
  "task": "chess-game-pro",
  "round": 1,
  "nonce": "chess-001",
  "brief": "Create a chess game with: 1) Full chess rules, 2) Drag-and-drop pieces, 3) Move validation, 4) Check/Checkmate detection, 5) Timed modes (Blitz 5min, Rapid 10min), 6) Move history, 7) Captured pieces display",
  "checks": [
    "All pieces move correctly",
    "Check detection works",
    "Checkmate ends game",
    "Timer counts down",
    "Move history displays"
  ],
  "evaluation_url": "https://webhook.site/your-id",
  "attachments": []
}
```
</details>

## 🐛 Troubleshooting

### Common Issues

**Problem:** `403 Forbidden` response
- **Solution:** Check that `secret` in request matches `STUDENT_SECRET` env var

**Problem:** Task accepted but no notification received
- **Solution:** Check Hugging Face Space logs or local console for errors. Common causes:
  - Invalid GitHub token or insufficient permissions
  - Gemini API quota exceeded
  - Invalid evaluation_url

**Problem:** GitHub API errors (403, 404)
- **Solution:** Verify GitHub token has `repo` scope:
  ```bash
  curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user
  ```

**Problem:** Gemini AI returns invalid JSON
- **Solution:** Check logs for response. The system now has improved error handling with specific error messages.

**Problem:** Pages deployment times out
- **Solution:** GitHub Pages can take 1-2 minutes to activate. The system retries 5 times with exponential backoff.

### Debug Mode

Enable detailed logging:
```python
# In main.py, add at top:
import logging
logging.basicConfig(level=logging.DEBUG)
```

Or set environment variable:
```bash
export LOG_LEVEL=DEBUG  # Linux/Mac
$env:LOG_LEVEL="DEBUG"  # Windows PowerShell
```

### Viewing Logs

**Docker:**
```bash
docker logs -f CONTAINER_ID
```

**Hugging Face Space:**
Go to Space → "Logs" tab

## 🔒 Security Best Practices

1. **Never commit `.env` file** - Already in `.gitignore`
2. **Rotate API keys regularly** - Every 90 days recommended
3. **Use environment-specific secrets** - Different keys for dev/prod
4. **Limit GitHub token scope** - Only `repo` or `public_repo` needed
5. **Validate incoming requests** - `secret` field prevents unauthorized access
6. **Monitor API usage** - Check Gemini and GitHub API quotas

## 📈 Performance & Limits

| Metric | Value | Notes |
|--------|-------|-------|
| Average task duration | 30-60s | Depends on complexity |
| Gemini API rate limit | 15/min | Free tier |
| GitHub API rate limit | 5000/hour | Authenticated |
| Max attachment size | ~10MB | Base64 encoding adds 33% |
| Concurrent tasks | Unlimited | Background processing |

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- [ ] Add support for GitLab/Bitbucket deployment
- [ ] Implement task queue with Redis
- [ ] Add progress tracking API
- [ ] Support multiple AI models (Claude, GPT-4)
- [ ] Add unit tests
- [ ] Implement rate limiting
- [ ] Add metrics/monitoring

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- **Google Gemini AI** - Code generation capabilities
- **FastAPI** - Modern Python web framework
- **GitHub** - Repository hosting and Pages deployment
- **Hugging Face** - Spaces platform for easy deployment

---

**Built for TDS Project 1** - Automated task generation and deployment system
