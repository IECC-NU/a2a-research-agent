# 🔬 Deep Research Agent - A2A Compliant

Advanced autonomous research agent with multi-tool orchestration, domain filtering, and Agent-to-Agent (A2A) protocol support.

## 🌟 Features

- **Multi-Tool Research**: Perplexity, Tavily, and Exa integration
- **Domain Filtering**: Focus research on specific authoritative sources
- **Specialized Search**: Pre-configured tools for academic, business, and tech news
- **A2A Protocol**: Full Agent-to-Agent communication support
- **Intelligent Orchestration**: Autonomous tool selection and parallel execution
- **Quality Ranking**: Built-in evaluation system for source credibility

## 🏗️ Architecture

```
deep-research-agent/
├── agent.py           # Main agent with Gemini LLM
├── tools.py           # Search tools with domain filtering
├── a2a_server.py      # A2A protocol HTTP endpoints
├── examples.py        # Usage examples
└── README.md          # This file
```

## 🚀 Quick Start

### 1. Installation

```bash
pip install google-adk tavily-python exa-py openai python-dotenv flask
```

### 2. Environment Setup

Create a `.env` file:

```env
PERPLEXITY_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
EXA_API_KEY=your_key_here
GOOGLE_API_KEY=your_gemini_key_here
```

### 3. Basic Usage

```python
from tools import search_tavily

# Search academic sources only
result = search_tavily(
    query="quantum computing breakthroughs",
    include_domains=["arxiv.org", "nature.com", "ieee.org"],
    search_depth="advanced"
)
print(result)
```

## 🔧 Tools Available

### Primary Tools

#### 1. `search_perplexity_tool`
**Best for**: Real-time news, current events, quick facts
```python
search_perplexity(
    query="latest AI news",
    return_citations=True
)
```

#### 2. `search_tavily_tool`
**Best for**: Structured research, market data, comprehensive web search
```python
search_tavily(
    query="AI market analysis",
    include_domains=["bloomberg.com", "reuters.com"],
    exclude_domains=["reddit.com"],
    search_depth="advanced",
    max_results=10
)
```

#### 3. `search_exa_tool`
**Best for**: Deep semantic search, technical papers, specific insights
```python
search_exa(
    query="neural architecture search methods",
    include_domains=["arxiv.org", "openreview.net"],
    num_results=5,
    use_autoprompt=True,
    highlights=True
)
```

### Specialized Tools

#### 4. `search_academic_tool`
Pre-configured for academic sources (arXiv, PubMed, IEEE, Nature, Science)
```python
search_academic_papers("CRISPR gene editing advances")
```

#### 5. `search_tech_news_tool`
Pre-configured for tech news (TechCrunch, The Verge, Wired, Ars Technica)
```python
search_tech_news("latest smartphone releases")
```

#### 6. `search_business_tool`
Pre-configured for business sources (Bloomberg, Reuters, WSJ, Forbes, McKinsey)
```python
search_business_data("cryptocurrency market trends")
```

## 🌐 A2A Protocol Integration

### Start the A2A Server

```bash
python a2a_server.py
```

Server runs on `http://localhost:5000`

### Agent Discovery

```bash
curl http://localhost:5000/.well-known/agent-card.json
```

Returns:
```json
{
  "name": "deep-research-agent",
  "version": "2.0.0",
  "capabilities": {
    "skills": [
      {
        "name": "web_search",
        "parameters": {
          "query": {"type": "string", "required": true},
          "include_domains": {"type": "array", "required": false}
        }
      },
      ...
    ]
  }
}
```

### Execute Task via A2A

```python
import requests

task = {
    "skill": "web_search",
    "parameters": {
        "query": "renewable energy innovations",
        "tool": "tavily",
        "include_domains": ["nature.com", "science.org"]
    }
}

response = requests.post(
    'http://localhost:5000/a2a/task',
    json=task
)

result = response.json()
```

## 📋 Usage Patterns

### Pattern 1: Direct Tool Usage

```python
from tools import search_tavily

# Academic research with domain filtering
result = search_tavily(
    query="quantum error correction",
    include_domains=[
        "arxiv.org",
        "nature.com",
        "science.org"
    ],
    search_depth="advanced"
)
```

### Pattern 2: Using Specialized Wrappers

```python
from tools import search_academic_papers, search_business_data

# Academic search (auto-configured domains)
academic_result = search_academic_papers(
    "machine learning interpretability"
)

# Business intelligence
business_result = search_business_data(
    "global semiconductor market"
)
```

### Pattern 3: Config File-Based Research

```python
import json
from tools import search_tavily

# Load domains from config
with open('research_domains.json', 'r') as f:
    config = json.load(f)

# Use loaded domains
result = search_tavily(
    query="climate change research",
    include_domains=config['environmental_sources'],
    search_depth="advanced"
)
```

Example `research_domains.json`:
```json
{
  "environmental_sources": [
    "nature.com",
    "science.org",
    "ipcc.ch",
    "noaa.gov"
  ],
  "medical_sources": [
    "pubmed.ncbi.nlm.nih.gov",
    "nejm.org",
    "thelancet.com"
  ]
}
```

### Pattern 4: Multi-Agent Collaboration

```python
import requests

class AnalystAgent:
    def __init__(self):
        self.research_url = "http://localhost:5000"
    
    def research_and_analyze(self, topic):
        # Call research agent via A2A
        task = {
            "skill": "business_research",
            "parameters": {"query": topic}
        }
        
        response = requests.post(
            f"{self.research_url}/a2a/task",
            json=task
        )
        
        research_data = response.json()
        
        # Your analysis logic here
        analysis = self.analyze(research_data)
        return analysis

analyst = AnalystAgent()
result = analyst.research_and_analyze("AI market")
```

## 🎯 Domain Filtering Examples

### Academic Research
```python
academic_domains = [
    "arxiv.org",
    "scholar.google.com",
    "pubmed.ncbi.nlm.nih.gov",
    "ieee.org",
    "acm.org",
    "springer.com",
    "nature.com",
    "science.org"
]

result = search_tavily(
    query="deep learning architectures",
    include_domains=academic_domains
)
```

### Business Intelligence
```python
business_domains = [
    "bloomberg.com",
    "reuters.com",
    "wsj.com",
    "ft.com",
    "forbes.com",
    "mckinsey.com",
    "gartner.com",
    "forrester.com"
]

result = search_exa(
    query="fintech market analysis",
    include_domains=business_domains
)
```

### Government & Official Sources
```python
government_domains = [
    "*.gov",  # All US government sites
    "europa.eu",
    "who.int",
    "un.org"
]

result = search_tavily(
    query="healthcare policy updates",
    include_domains=government_domains
)
```

### Excluding Low-Quality Sources
```python
result = search_tavily(
    query="technology trends",
    exclude_domains=[
        "reddit.com",
        "quora.com",
        "twitter.com",
        "facebook.com"
    ]
)
```

## 🤝 Team Collaboration Setup

### For Team Members

1. **Create team config files**:

```bash
mkdir team_configs
```

```json
// team_configs/medical_research.json
{
  "include_domains": [
    "pubmed.ncbi.nlm.nih.gov",
    "nejm.org",
    "thelancet.com"
  ],
  "search_depth": "advanced",
  "max_results": 20
}
```

2. **Share A2A endpoint**:

```
Research Agent Endpoint: https://research-agent.company.com
Agent Card: https://research-agent.company.com/.well-known/agent-card.json
```

3. **Use from any agent**:

```python
import requests

# Any team member's agent can use this
response = requests.post(
    'https://research-agent.company.com/a2a/task',
    json={
        "skill": "academic_research",
        "parameters": {
            "query": "cancer immunotherapy"
        }
    },
    headers={'Authorization': f'Bearer {API_TOKEN}'}
)
```

## 🔍 Research Quality System

The agent uses a built-in quality evaluation system:

### Scoring Criteria
- **Relevance (0-10)** × 0.35
- **Credibility (0-10)** × 0.25
  - High (10): .gov, .edu, peer-reviewed journals
  - Medium (5): Reputable news sources
  - Low (2): Blogs, forums
- **Recency (0-10)** × 0.15
- **Completeness (0-10)** × 0.15
- **Actionability (0-10)** × 0.10

**Overall Score** = Weighted sum
**Filter threshold**: 6.0

## 📊 Output Format

The agent generates structured Markdown reports:

```markdown
# Research Report: [Topic]

## 📊 Executive Summary
[2-3 paragraph summary]

## 🔍 Research Methodology
- Tools Used: Perplexity, Tavily, Exa
- Domains Focused: [List]
- Sources Analyzed: 25

## 📈 Key Findings

### Market Size
- Global market: $X billion (Source: URL)
- Growth rate: X% CAGR

### Key Players
| Company | Market Share | Source |
|---------|-------------|---------|
| ... | ... | ... |

## 🎯 Critical Analysis
- Contradictions: [List any]
- Data Gaps: [What's missing]
- Confidence: High/Medium/Low

## 📚 Sources
1. [Tool] - [URL] - [Description]
...
```

## 🐛 Troubleshooting

### Issue: "No API key found"
```bash
# Check .env file exists and has correct keys
cat .env

# Load environment variables
source .env  # Linux/Mac
# or
set -a; source .env; set +a
```

### Issue: "Domain filtering not working"
```python
# Make sure you're using Tavily or Exa, not Perplexity
# Perplexity doesn't support include_domains

# ❌ Won't work
search_perplexity(query="test", include_domains=["arxiv.org"])

# ✅ Will work
search_tavily(query="test", include_domains=["arxiv.org"])
```

### Issue: "A2A server not responding"
```bash
# Make sure server is running
python a2a_server.py

# Check port is not blocked
curl http://localhost:5000/health
```

## 📚 API Reference

See `examples.py` for complete usage examples of all patterns.

## 🤝 Contributing

To extend the agent:

1. Add new specialized search functions to `tools.py`
2. Update `agent.py` instruction with new capabilities
3. Add new skill to A2A agent card in `agent.py`
4. Add handler in `a2a_server.py`
5. Document in this README

## 📄 License

MIT License

## 🙏 Credits

Built with:
- Google Gemini (LLM)
- Tavily (Structured Search)
- Exa (Neural Search)
- Perplexity (AI Search)
- Google ADK (Agent Framework)

---

**For support or questions, contact your team's AI/ML engineering lead.**
