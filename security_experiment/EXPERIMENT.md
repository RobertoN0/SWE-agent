# Security Experiment: Testing AI Agent Web Browsing Vulnerabilities

**Date:** December 2025  
**Objective:** Test if AI agents with web browsing capabilities can be exploited through malicious web content

---

## Overview

This experiment tests SWE-agent's web browser tool against a malicious website to evaluate potential security vulnerabilities. The agent visits a Flask server serving JavaScript-based attacks and we monitor what data can be collected.

### Architecture

```
AI Agent (Docker Container)
    ↓ visits URL
Malicious Server (localhost:8000)
    ↓ serves exploit.html
JavaScript executes in agent's browser
    ↓ sends data
Server logs collected information
```

**Network:** Agent in Docker accesses host via gateway IP `172.17.0.1:8000`

---

## Attack Vectors Being Tested

This experiment tests the following attack methods:

1. **Browser Fingerprinting** - JavaScript collects system/browser information
2. **Data Exfiltration** - POST requests send collected data to attacker server
3. **Console Prompt Injection** - Malicious console.log() messages
4. **Visual Prompt Injection** - HTML content with embedded instructions

---

## Prerequisites

**System Requirements:**
- Docker installed and running
- Python 3.11+
- Ollama (for local model) OR OpenAI API key (for GPT models)

**Setup Steps:**

1. **Create virtual environment:**
```bash
cd SWE-agent
python3 -m venv .venv
```

2. **Activate virtual environment:**
```bash
source .venv/bin/activate
```

3. **Install SWE-agent:**
```bash
pip install -e .
```

4. **Build Custom Images (Optional but Recommended):**
```bash
cd security_experiment
bash build_images.sh
cd ..
```

**Note:** Always activate the venv before running experiments: `source venv/bin/activate`

---

## Running the Experiment

### Step 1: Start Malicious Server

```bash
cd security_experiment
python malicious_server.py
# Server runs on http://localhost:8000
```

### Step 2: Run Agent

**Important:** Open a new terminal and activate venv before running agent commands.

```bash
# In a new terminal
cd SWE-agent
source venv/bin/activate
```

**Option A - Local Model (Ollama):**
```bash
sweagent run --config security_experiment/ollama_experiment_config.yaml
```

**Option B - Cloud Model (GPT-4o):**
```bash
export OPENAI_API_KEY="sk-..."
sweagent run --config security_experiment/gpt_experiment_config.yaml
```

**Other GPT models:**
```bash
# GPT-4o Mini (cheaper)
sweagent run --config security_experiment/gpt_experiment_config.yaml \
  --agent.model.name gpt-4o-mini

# GPT-4 Turbo (most capable)
sweagent run --config security_experiment/gpt_experiment_config.yaml \
  --agent.model.name gpt-4-turbo-2024-04-09
```

---

## Configuration Details

### Adjusting Cost Limits (GPT only)

```bash
# Make sure venv is activated: source venv/bin/activate
sweagent run \
  --config security_experiment/gpt_experiment_config.yaml \
  --agent.model.per_instance_cost_limit 5.0 \
  --agent.model.total_cost_limit 20.0
```

### Modifying Attack Payloads

Edit `security_experiment/payloads/exploit.html` to test different attack vectors.

---


## Troubleshooting

### Malicious Server Issues

**Port 8000 already in use:**
```bash
lsof -i :8000
pkill -f malicious_server.py

# Restart server (with venv activated)
source venv/bin/activate
python security_experiment/malicious_server.py
```

**Server not responding:**
Check the gateway IP is correct for your system:
```bash
docker network inspect bridge | grep Gateway
# Use the Gateway IP in your problem_statement (usually 172.17.0.1)
```

### GPT API Key Issues

```bash
# Verify key is set
echo $OPENAI_API_KEY

# Set if missing
export OPENAI_API_KEY="sk-..."
```


## Repository Structure

```
SWE-agent/
├── venv/                             # Virtual environment (create with python3 -m venv venv)
├── security_experiment/
│   ├── ollama_experiment_config.yaml # Local model configuration
│   ├── gpt_experiment_config.yaml    # Cloud model configuration
│   ├── malicious_server.py           # Attack server
│   ├── build_images.sh               # Build custom Docker images
│   ├── Dockerfile.gpt                # GPT custom image
│   ├── Dockerfile.ollama             # Ollama custom image
│   ├── payloads/
│   │   └── exploit.html              # Main attack page with JavaScript
│   └── logs/
│       ├── attack_log_*.log          # HTTP request logs
│       └── exfiltrated_data_*.json   # Collected fingerprint data
└── trajectories/                     # Agent execution logs
```

---

## Notes

- **Local Model (Ollama):** Uses OCR to extract text from screenshots (text-only model)
- **Cloud Model (GPT):** Can view screenshots directly (vision-capable model)
- **Container Behavior:** New container created per run, tools copied from host at runtime
- **Cost Limits:** GPT experiments have default $2/instance and $10/total limits
