# Phase IV: Local Kubernetes Deployment

**Status:** 🚧 In Development
**Due Date:** January 4, 2026
**Points:** 250

## Overview

Deploy the Todo Chatbot on a local Kubernetes cluster using:
- Docker for containerization
- Minikube for local Kubernetes
- Helm Charts for package management
- kubectl-ai and kagent for AI-assisted operations

## Technology Stack

| Component | Technology |
|-----------|------------|
| Containerization | Docker (Docker Desktop) |
| Docker AI | Docker AI Agent (Gordon) |
| Orchestration | Kubernetes (Minikube) |
| Package Manager | Helm Charts |
| AI DevOps | kubectl-ai, kagent |
| Application | Phase III Todo Chatbot |

## Features

### Cloud Native Deployment
- ✅ Containerized frontend and backend
- ✅ Kubernetes manifests and Helm charts
- ✅ Local deployment on Minikube
- ✅ Service discovery and load balancing
- ✅ ConfigMaps and Secrets management
- ✅ Health checks and readiness probes

### AIOps Integration
- Docker AI Agent (Gordon) for intelligent Docker operations
- kubectl-ai for natural language Kubernetes commands
- kagent for cluster analysis and optimization

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    MINIKUBE CLUSTER                       │
│                                                           │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   │
│  │  Frontend   │   │  Backend    │   │  Postgres   │   │
│  │   Pod       │──▶│   Pod       │──▶│   (Neon)    │   │
│  │  (Next.js)  │   │  (FastAPI)  │   │  (External) │   │
│  └─────────────┘   └─────────────┘   └─────────────┘   │
│         │                  │                             │
│         └──────────────────┘                             │
│                    │                                     │
│            ┌───────▼────────┐                            │
│            │  Ingress/LB    │                            │
│            └────────────────┘                            │
└──────────────────────────────────────────────────────────┘
```

## Project Structure

```
phase-4-kubernetes/
├── docker/
│   ├── frontend.Dockerfile
│   └── backend.Dockerfile
├── k8s/
│   ├── frontend-deployment.yaml
│   ├── backend-deployment.yaml
│   ├── services.yaml
│   ├── configmaps.yaml
│   └── secrets.yaml
├── helm/
│   └── todo-chatbot/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
└── README.md
```

## Prerequisites

- Docker Desktop 4.53+ (with Gordon enabled)
- Minikube installed
- kubectl installed
- Helm 3+ installed
- kubectl-ai installed (optional)
- kagent installed (optional)

## Getting Started

### 1. Install Minikube

```bash
# macOS
brew install minikube

# Windows (with Chocolatey)
choco install minikube

# Linux
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

### 2. Start Minikube

```bash
minikube start --driver=docker --cpus=4 --memory=8192
```

### 3. Build Docker Images

```bash
# Using Docker AI (Gordon)
docker ai "Build frontend and backend images for the todo app"

# Or manually
docker build -t todo-frontend:latest -f docker/frontend.Dockerfile ../phase-3-chatbot/frontend
docker build -t todo-backend:latest -f docker/backend.Dockerfile ../phase-3-chatbot/backend
```

### 4. Deploy with Helm

```bash
# Install the Helm chart
helm install todo-chatbot ./helm/todo-chatbot

# Or using kubectl-ai
kubectl-ai "deploy the todo chatbot with 2 replicas"
```

### 5. Access the Application

```bash
# Get the service URL
minikube service todo-frontend --url

# Or use port forwarding
kubectl port-forward service/todo-frontend 3000:3000
```

## AIOps Commands

### Docker AI (Gordon)

```bash
# Check capabilities
docker ai "What can you do?"

# Build and optimize images
docker ai "Build optimized production images for my todo app"

# Troubleshoot
docker ai "Why is my container failing to start?"
```

### kubectl-ai

```bash
# Deploy resources
kubectl-ai "deploy the todo frontend with 2 replicas"

# Scale services
kubectl-ai "scale the backend to handle more load"

# Debug issues
kubectl-ai "check why the pods are failing"
```

### kagent

```bash
# Analyze cluster
kagent "analyze the cluster health"

# Optimize resources
kagent "optimize resource allocation for the todo app"
```

## Deployment Checklist

- [ ] Docker images built and tagged
- [ ] Kubernetes manifests created
- [ ] Helm chart configured
- [ ] Secrets and ConfigMaps set up
- [ ] Services exposed correctly
- [ ] Health checks configured
- [ ] Resource limits defined
- [ ] Application accessible via Minikube

## Troubleshooting

### Common Issues

**Pods not starting:**
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

**Service not accessible:**
```bash
kubectl get services
minikube service list
```

**Image pull errors:**
```bash
# Load local images into Minikube
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
```

## Submission Requirements

- ✅ GitHub repository with Kubernetes manifests
- ✅ Helm charts for deployment
- ✅ Instructions for local Minikube setup
- ✅ Demo video (max 90 seconds)
- ✅ WhatsApp number for presentation

## Resources

- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [kubectl-ai](https://github.com/sozercan/kubectl-ai)
- [Docker AI (Gordon)](https://docs.docker.com/desktop/features/ai/)

---

**Hackathon:** GIAIC Hackathon II - The Evolution of Todo
**Repository:** https://github.com/abdul-ahad-26/02_todo_app
