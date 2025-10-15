# GEMINI_PROJECT - FastAPI Task Automation Service

Automated task receiver that uses Gemini AI to generate web apps and deploys them to GitHub Pages.

## Quick Deploy to Hugging Face Spaces (5 minutes)

### Prerequisites
- GitHub account with a Personal Access Token (PAT) with `repo` scope
- Google Gemini API key
- Hugging Face account

### Steps

1. **Create a new Space on Hugging Face**
   - Go to https://huggingface.co/new-space
   - Choose **Docker** as the Space SDK
   - Name it (e.g., `gemini-task-processor`)
   - Set visibility (Public or Private)

2. **Push this repository to the Space**
   ```bash
   git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
   git push hf main
   ```

3. **Set secrets in Space Settings**
   - Go to your Space → Settings → Repository secrets
   - Add these four secrets:
     - `GEMINI_API_KEY` - your Google Generative AI API key
     - `GITHUB_TOKEN` - your GitHub personal access token
     - `GITHUB_USERNAME` - your GitHub username
     - `STUDENT_SECRET` - a shared secret for incoming requests

4. **Wait for build** (2-3 minutes)
   - The Space will automatically build the Docker image
   - Once deployed, your API will be live at `https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space`

5. **Test the endpoint**
   - Visit `https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/docs` for the interactive API docs

## Local Development

### Setup
```powershell
# Copy example env and fill in values
Copy-Item .env.example .env
notepad .env

# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest -q

# Start server
uvicorn main:app --reload
```

### Test with Docker locally
```powershell
# Build and run
.\run.ps1

# Or manually
docker build -t gemini_project:local .
docker run --rm -p 8080:8080 --env-file .env gemini_project:local
```

## Getting API Keys

### GitHub Personal Access Token
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` scope (or `public_repo` for public repos only)
3. Copy the token (starts with `ghp_`)

### Google Gemini API Key
1. Go to https://aistudio.google.com/app/apikey
2. Create API key
3. Enable the Generative Language API if needed
4. Copy the key

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Generative AI API key | `AIza...` |
| `GITHUB_TOKEN` | GitHub PAT with repo scope | `ghp_...` |
| `GITHUB_USERNAME` | Your GitHub username | `yourname` |
| `STUDENT_SECRET` | Shared secret for request auth | `my-secret-123` |

## Architecture

- **FastAPI** - REST API framework
- **Gemini AI** - Code generation via Google's LLM
- **GitPython** - Git operations for deployment
- **GitHub API** - Repository creation and Pages config
- **Pydantic** - Settings validation and request models

## Project Structure

```
.
├── main.py              # FastAPI app and orchestration
├── config.py            # Settings with env validation
├── models.py            # Pydantic request models
├── requirements.txt     # Python dependencies
├── Dockerfile           # Production container
├── .env.example         # Template for secrets
├── tests/               # Unit tests
└── scripts/             # Helper scripts
```

## Troubleshooting

**Space build fails**: Check logs in the Space's "Logs" tab. Common issues:
- Missing or invalid environment variables
- Dockerfile syntax errors

**App crashes on startup**: Usually missing env vars. Check with:
```bash
python scripts/check_env.py
```

**GitHub API errors**: Verify your PAT has correct scopes and isn't expired.

**Gemini API errors**: Check quota limits and API key validity.

## License

MIT
