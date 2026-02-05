# 🚀 Deployment Guide

## Local Development

### 1. Setup Environment

```bash
# Clone or copy the project
cd deep-research-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your API keys
nano .env
```

### 2. Run Locally

```bash
# Start the A2A server
python a2a_server.py

# Server will be available at http://localhost:5000
```

### 3. Test the Agent

```bash
# Test health endpoint
curl http://localhost:5000/health

# Test agent discovery
curl http://localhost:5000/.well-known/agent-card.json

# Test search
curl -X POST http://localhost:5000/a2a/task \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "web_search",
    "parameters": {
      "query": "AI breakthroughs 2025",
      "tool": "tavily"
    }
  }'
```

## Production Deployment

### Option 1: Docker Deployment

#### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY agent.py tools.py a2a_server.py ./
COPY domain_configs.json .

# Expose port
EXPOSE 5000

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "a2a_server:app"]
```

#### Build and Run

```bash
# Build image
docker build -t deep-research-agent .

# Run container
docker run -d \
  --name research-agent \
  -p 5000:5000 \
  -e PERPLEXITY_API_KEY=$PERPLEXITY_API_KEY \
  -e TAVILY_API_KEY=$TAVILY_API_KEY \
  -e EXA_API_KEY=$EXA_API_KEY \
  -e GOOGLE_API_KEY=$GOOGLE_API_KEY \
  deep-research-agent

# Check logs
docker logs -f research-agent
```

### Option 2: Cloud Deployment (Google Cloud Run)

#### 1. Create cloudbuild.yaml

```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/research-agent', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/research-agent']
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'research-agent'
      - '--image'
      - 'gcr.io/$PROJECT_ID/research-agent'
      - '--platform'
      - 'managed'
      - '--region'
      - 'us-central1'
      - '--allow-unauthenticated'
```

#### 2. Deploy

```bash
# Set project
gcloud config set project YOUR_PROJECT_ID

# Set secrets
gcloud secrets create perplexity-api-key --data-file=- <<< "$PERPLEXITY_API_KEY"
gcloud secrets create tavily-api-key --data-file=- <<< "$TAVILY_API_KEY"
gcloud secrets create exa-api-key --data-file=- <<< "$EXA_API_KEY"
gcloud secrets create google-api-key --data-file=- <<< "$GOOGLE_API_KEY"

# Deploy
gcloud builds submit --config cloudbuild.yaml

# Your agent will be available at:
# https://research-agent-XXXXX.run.app
```

### Option 3: AWS Lambda (Serverless)

#### 1. Create lambda_function.py wrapper

```python
import json
from a2a_server import app

def lambda_handler(event, context):
    from werkzeug.wrappers import Request, Response
    
    # Convert Lambda event to Flask request
    with app.request_context(Request.from_values(
        path=event['path'],
        method=event['httpMethod'],
        headers=event['headers'],
        data=event.get('body', '')
    )):
        response = app.full_dispatch_request()
        
    return {
        'statusCode': response.status_code,
        'headers': dict(response.headers),
        'body': response.get_data(as_text=True)
    }
```

#### 2. Deploy with Serverless Framework

```yaml
# serverless.yml
service: research-agent

provider:
  name: aws
  runtime: python3.11
  environment:
    PERPLEXITY_API_KEY: ${env:PERPLEXITY_API_KEY}
    TAVILY_API_KEY: ${env:TAVILY_API_KEY}
    EXA_API_KEY: ${env:EXA_API_KEY}
    GOOGLE_API_KEY: ${env:GOOGLE_API_KEY}

functions:
  api:
    handler: lambda_function.lambda_handler
    events:
      - http:
          path: /{proxy+}
          method: ANY
```

```bash
# Deploy
serverless deploy
```

## Team Setup

### 1. Share Agent Card URL

After deployment, share with your team:

```
Agent Discovery URL: https://your-domain.com/.well-known/agent-card.json
```

### 2. Create Team Config Repository

```bash
# Create a shared config repository
mkdir team-research-configs
cd team-research-configs

# Add domain configs for different use cases
echo '{
  "include_domains": ["arxiv.org", "nature.com"],
  "search_depth": "advanced"
}' > academic_config.json

echo '{
  "include_domains": ["bloomberg.com", "reuters.com"],
  "search_depth": "advanced"
}' > business_config.json

# Commit and push to shared repo
git init
git add .
git commit -m "Add team research configs"
git push origin main
```

### 3. Team Member Usage

```python
# Any team member can use:
import requests

AGENT_URL = "https://research-agent.company.com"

def my_agent_task():
    task = {
        "skill": "academic_research",
        "parameters": {
            "query": "machine learning research"
        }
    }
    
    response = requests.post(
        f"{AGENT_URL}/a2a/task",
        json=task,
        headers={'Authorization': f'Bearer {API_TOKEN}'}
    )
    
    return response.json()
```

## Monitoring & Logging

### Add Logging to a2a_server.py

```python
import logging
from logging.handlers import RotatingFileHandler

# Setup logging
handler = RotatingFileHandler('research_agent.log', maxBytes=10000000, backupCount=3)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# Log requests
@app.before_request
def log_request():
    app.logger.info(f"Request: {request.method} {request.path}")

@app.after_request
def log_response(response):
    app.logger.info(f"Response: {response.status_code}")
    return response
```

### Monitor with Google Cloud

```bash
# View logs
gcloud run logs tail research-agent --project YOUR_PROJECT_ID

# View metrics
gcloud monitoring dashboards create --config-from-file=dashboard.yaml
```

## Security Best Practices

### 1. Add Authentication

```python
from functools import wraps
from flask import request

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Unauthorized"}), 401
        
        token = auth_header.split(' ')[1]
        if token != os.getenv('A2A_API_KEY'):
            return jsonify({"error": "Invalid token"}), 401
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/a2a/task', methods=['POST'])
@require_auth
def handle_a2a_task():
    # ... existing code
```

### 2. Rate Limiting

```bash
pip install flask-limiter
```

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour", "10 per minute"]
)

@app.route('/a2a/task', methods=['POST'])
@limiter.limit("10 per minute")
def handle_a2a_task():
    # ... existing code
```

### 3. API Key Management

Never commit API keys! Use:
- **Local**: `.env` file (gitignored)
- **Docker**: Environment variables
- **Cloud**: Secret managers (GCP Secret Manager, AWS Secrets Manager)

## Troubleshooting Deployment

### Issue: "Module not found"
```bash
# Ensure all files are included in deployment
ls -la
# Should see: agent.py, tools.py, a2a_server.py, domain_configs.json
```

### Issue: "API key not found"
```bash
# Check environment variables are set
printenv | grep API

# For Docker
docker exec research-agent printenv | grep API

# For Cloud Run
gcloud run services describe research-agent --region us-central1
```

### Issue: "Port already in use"
```bash
# Find process using port 5000
lsof -i :5000

# Kill it
kill -9 <PID>

# Or use a different port
PORT=5001 python a2a_server.py
```

## Performance Optimization

### 1. Caching Results

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def cached_search(query, tool):
    # Cache results for repeated queries
    if tool == "tavily":
        return search_tavily(query)
    # ... etc
```

### 2. Async Operations

```python
import asyncio
import aiohttp

async def parallel_search(queries):
    tasks = [search_async(q) for q in queries]
    results = await asyncio.gather(*tasks)
    return results
```

## Support & Maintenance

- Monitor error logs regularly
- Update API keys before expiration
- Keep dependencies updated: `pip install --upgrade -r requirements.txt`
- Test after updates: `python examples.py`

---

**Need help? Contact your DevOps or ML Engineering team.**
