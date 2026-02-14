# Phase V: Advanced Cloud Deployment

**Status:** 🚧 In Development
**Due Date:** January 18, 2026
**Points:** 300

## Overview

Deploy a production-grade, event-driven Todo Chatbot with advanced features to cloud Kubernetes:
- Advanced todo features (recurring tasks, reminders, priorities, tags)
- Event-driven architecture with Kafka
- Dapr for distributed application runtime
- Cloud deployment on Azure (AKS), Google Cloud (GKE), or DigitalOcean (DOKS)

## Technology Stack

| Component | Technology |
|-----------|------------|
| Cloud Platform | Azure AKS / Google GKE / DigitalOcean DOKS |
| Event Streaming | Kafka (Confluent/Redpanda Cloud or Strimzi) |
| Distributed Runtime | Dapr |
| Orchestration | Kubernetes + Helm |
| CI/CD | GitHub Actions |
| Monitoring | Prometheus + Grafana (optional) |

## Features

### Part A: Advanced Features

**Intermediate Level:**
- ✅ Task priorities (high/medium/low)
- ✅ Tags and categories
- ✅ Search and filter
- ✅ Sort tasks (by date, priority, alphabetically)

**Advanced Level:**
- ✅ Recurring tasks (daily, weekly, monthly)
- ✅ Due dates with time
- ✅ Reminder notifications

### Part B: Event-Driven Architecture

**Kafka Topics:**
- `task-events` - All CRUD operations
- `reminders` - Scheduled reminder triggers
- `task-updates` - Real-time client sync

**Event Consumers:**
- Recurring Task Service - Auto-creates next occurrence
- Notification Service - Sends reminders
- Audit Service - Maintains activity log

### Part C: Dapr Integration

**Building Blocks Used:**
- Pub/Sub - Kafka abstraction
- State Management - Conversation state
- Service Invocation - Inter-service communication
- Jobs API - Scheduled reminders
- Secrets Management - API keys and credentials

## Architecture

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                              KUBERNETES CLUSTER (Cloud)                               │
│                                                                                       │
│  ┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐        │
│  │    Frontend Pod     │   │    Backend Pod      │   │  Notification Pod   │        │
│  │ ┌───────┐ ┌───────┐ │   │ ┌───────┐ ┌───────┐ │   │ ┌───────┐ ┌───────┐ │        │
│  │ │ Next  │ │ Dapr  │ │   │ │FastAPI│ │ Dapr  │ │   │ │Notif  │ │ Dapr  │ │        │
│  │ │  App  │◀┼▶Sidecar│ │   │ │+ MCP  │◀┼▶Sidecar│ │   │ │Service│◀┼▶Sidecar│ │        │
│  │ └───────┘ └───────┘ │   │ └───────┘ └───────┘ │   │ └───────┘ └───────┘ │        │
│  └──────────┬──────────┘   └──────────┬──────────┘   └──────────┬──────────┘        │
│             │                         │                         │                    │
│             └─────────────────────────┼─────────────────────────┘                    │
│                                       │                                              │
│                          ┌────────────▼────────────┐                                 │
│                          │    DAPR COMPONENTS      │                                 │
│                          │  ┌──────────────────┐   │                                 │
│                          │  │ pubsub.kafka     │───┼────▶ Kafka Cluster             │
│                          │  ├──────────────────┤   │                                 │
│                          │  │ state.postgresql │───┼────▶ Neon DB                    │
│                          │  ├──────────────────┤   │                                 │
│                          │  │ jobs             │   │  (Scheduled triggers)           │
│                          │  ├──────────────────┤   │                                 │
│                          │  │ secretstores.k8s │   │  (API keys, credentials)        │
│                          │  └──────────────────┘   │                                 │
│                          └─────────────────────────┘                                 │
│                                                                                       │
│  ┌─────────────────────┐                                                             │
│  │  Recurring Task Pod │                                                             │
│  │ ┌───────┐ ┌───────┐ │                                                             │
│  │ │Service│ │ Dapr  │ │                                                             │
│  │ │       │◀┼▶Sidecar│ │                                                             │
│  │ └───────┘ └───────┘ │                                                             │
│  └─────────────────────┘                                                             │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
phase-5-cloud/
├── services/
│   ├── frontend/          # Next.js app
│   ├── backend/           # FastAPI + MCP
│   ├── notification/      # Notification service
│   └── recurring-task/    # Recurring task service
├── k8s/
│   ├── base/              # Base Kubernetes manifests
│   ├── overlays/
│   │   ├── local/         # Minikube config
│   │   └── production/    # Cloud config
│   └── dapr-components/   # Dapr component configs
├── helm/
│   └── todo-advanced/     # Helm chart
├── .github/
│   └── workflows/
│       ├── ci.yml         # Build and test
│       └── cd.yml         # Deploy to cloud
├── kafka/
│   └── strimzi/           # Kafka operator configs
└── README.md
```

## Cloud Provider Setup

### Option 1: Azure (AKS) - $200 Credit for 30 Days

```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login
az login

# Create resource group
az group create --name todo-rg --location eastus

# Create AKS cluster
az aks create \
  --resource-group todo-rg \
  --name todo-cluster \
  --node-count 2 \
  --enable-addons monitoring \
  --generate-ssh-keys

# Get credentials
az aks get-credentials --resource-group todo-rg --name todo-cluster
```

### Option 2: Google Cloud (GKE) - $300 Credit for 90 Days

```bash
# Install gcloud CLI
curl https://sdk.cloud.google.com | bash

# Login
gcloud auth login

# Create GKE cluster
gcloud container clusters create todo-cluster \
  --zone us-central1-a \
  --num-nodes 2 \
  --machine-type e2-medium

# Get credentials
gcloud container clusters get-credentials todo-cluster --zone us-central1-a
```

### Option 3: DigitalOcean (DOKS) - $200 Credit for 60 Days

```bash
# Install doctl
brew install doctl  # macOS
# or download from: https://github.com/digitalocean/doctl/releases

# Authenticate
doctl auth init

# Create cluster
doctl kubernetes cluster create todo-cluster \
  --region nyc1 \
  --node-pool "name=worker-pool;size=s-2vcpu-4gb;count=2"

# Get credentials
doctl kubernetes cluster kubeconfig save todo-cluster
```

### Option 4: Oracle Cloud (OKE) - Always Free Tier ⭐ Recommended

```bash
# Best for learning - no time pressure
# 4 OCPUs, 24GB RAM always free
# Sign up at: https://www.oracle.com/cloud/free/
```

## Kafka Setup

### Option 1: Redpanda Cloud (Recommended) ⭐

```bash
# Sign up at: https://redpanda.com/cloud
# Create Serverless cluster (free tier)
# Create topics: task-events, reminders, task-updates
# Copy bootstrap server URL and credentials
```

### Option 2: Self-Hosted with Strimzi

```bash
# Install Strimzi operator
kubectl create namespace kafka
kubectl apply -f 'https://strimzi.io/install/latest?namespace=kafka'

# Deploy Kafka cluster
kubectl apply -f kafka/strimzi/kafka-cluster.yaml
```

## Dapr Setup

```bash
# Install Dapr CLI
curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | bash

# Initialize Dapr on Kubernetes
dapr init -k

# Deploy Dapr components
kubectl apply -f k8s/dapr-components/
```

## Deployment Steps

### 1. Local Testing (Minikube)

```bash
# Start Minikube
minikube start --cpus=4 --memory=8192

# Install Dapr
dapr init -k

# Deploy Kafka (Strimzi)
kubectl apply -f kafka/strimzi/

# Deploy application
helm install todo-advanced ./helm/todo-advanced -f helm/todo-advanced/values-local.yaml
```

### 2. Cloud Deployment

```bash
# Set up cloud cluster (see Cloud Provider Setup above)

# Install Dapr
dapr init -k

# Create secrets
kubectl create secret generic app-secrets \
  --from-literal=database-url=$DATABASE_URL \
  --from-literal=openai-api-key=$OPENAI_API_KEY \
  --from-literal=kafka-username=$KAFKA_USERNAME \
  --from-literal=kafka-password=$KAFKA_PASSWORD

# Deploy with Helm
helm install todo-advanced ./helm/todo-advanced -f helm/todo-advanced/values-production.yaml
```

### 3. CI/CD with GitHub Actions

The `.github/workflows/cd.yml` pipeline will:
1. Build Docker images
2. Push to container registry
3. Deploy to Kubernetes
4. Run smoke tests

```bash
# Set GitHub secrets:
# - KUBE_CONFIG
# - DOCKER_USERNAME
# - DOCKER_PASSWORD
# - DATABASE_URL
# - OPENAI_API_KEY
```

## Event Flow Examples

### Recurring Task Flow

```
User completes task → Backend publishes to task-events
                    → Recurring Task Service consumes event
                    → Checks if task is recurring
                    → Creates next occurrence
                    → Publishes task-created event
```

### Reminder Flow

```
User sets due date → Backend schedules Dapr Job
                   → Job fires at reminder time
                   → Publishes to reminders topic
                   → Notification Service consumes
                   → Sends push/email notification
```

## Monitoring and Observability

### Dapr Dashboard

```bash
dapr dashboard -k
```

### Kafka Monitoring

```bash
# If using Strimzi
kubectl port-forward svc/kafka-ui 8080:8080 -n kafka
```

### Application Logs

```bash
# View logs with Dapr sidecar
kubectl logs <pod-name> -c daprd
kubectl logs <pod-name> -c app
```

## Submission Requirements

- ✅ GitHub repository with all source code
- ✅ Deployed application URL (cloud)
- ✅ All advanced features implemented
- ✅ Event-driven architecture with Kafka
- ✅ Dapr integration
- ✅ CI/CD pipeline configured
- ✅ Demo video (max 90 seconds)
- ✅ WhatsApp number for presentation

## Bonus Features (+600 Points)

- [ ] **Reusable Intelligence** (+200) - Claude Code Subagents and Agent Skills
- [ ] **Cloud-Native Blueprints** (+200) - Agent Skills for deployment
- [ ] **Multi-language Support** (+100) - Urdu chatbot support
- [ ] **Voice Commands** (+200) - Voice input for todo commands

## Resources

### Cloud Platforms
- [Azure Free Account](https://azure.microsoft.com/en-us/free/)
- [Google Cloud Free Tier](https://cloud.google.com/free)
- [DigitalOcean Credits](https://www.digitalocean.com/)
- [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/)

### Event Streaming
- [Redpanda Cloud](https://redpanda.com/cloud)
- [Confluent Cloud](https://www.confluent.io/confluent-cloud/)
- [Strimzi Operator](https://strimzi.io/)

### Dapr
- [Dapr Documentation](https://docs.dapr.io/)
- [Dapr Building Blocks](https://docs.dapr.io/concepts/building-blocks-concept/)
- [Dapr Components](https://docs.dapr.io/reference/components-reference/)

---

**Hackathon:** GIAIC Hackathon II - The Evolution of Todo
**Repository:** https://github.com/abdul-ahad-26/02_todo_app
