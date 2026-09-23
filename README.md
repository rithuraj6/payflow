
💳 PayFlow --- Cloud-Native UPI Payment Processing Platform
From code to cloud, fully automated. 🚀

PayFlow is a simulated UPI payment processing platform built with
FastAPI, PostgreSQL, Redis, Docker and Kubernetes, with a complete
DevOps delivery pipeline using Jenkins, SonarQube, OWASP Dependency
Check, Trivy, Argo CD, Helm, Istio, Prometheus and Grafana.

The project demonstrates an end-to-end DevOps workflow covering CI,
DevSecOps, containerization, Kubernetes deployment, GitOps, service-mesh
traffic management, monitoring and alerting.

🎯 Project Goals
Build a realistic backend payment-processing service.

Containerize the application using Docker.

Automate CI and security checks with Jenkins.

Deploy the application to Kubernetes using Helm.

Implement GitOps with Argo CD.

Demonstrate v1/v2 traffic management with Istio.

Monitor application and Kubernetes metrics with Prometheus and
Grafana.

Demonstrate payment failure-rate alerting.

🏗️ Architecture
Developer
   │
   ▼
GitHub
   │
   ▼
Jenkins CI
   ├── Tests
   ├── SonarQube
   ├── OWASP Dependency Check
   ├── Trivy
   ├── Docker Build
   └── Docker Push
            │
            ▼
       Docker Hub
            │
            ▼
       GitOps Branch
            │
            ▼
         Argo CD
            │
            ▼
   ┌─────────────────────────────┐
   │ Kubernetes / Minikube       │
   │                             │
   │  Istio Gateway              │
   │       │                     │
   │       ▼                     │
   │  VirtualService             │
   │     ┌───────┴───────┐       │
   │     ▼               ▼       │
   │  PayFlow v1      PayFlow v2 │
   │     │               │       │
   │     └───────┬───────┘       │
   │             ▼               │
   │        PostgreSQL            │
   │        Redis                 │
   │                             │
   │  Prometheus → Grafana       │
   └─────────────────────────────┘
⭐ Key Features
Application
FastAPI REST API

Simulated UPI payment processing

PostgreSQL persistence

Redis caching

Payment status tracking

Idempotency-key support

Health endpoint

Prometheus metrics endpoint

DevSecOps
Jenkins CI pipeline

Automated tests

SonarQube code-quality analysis

OWASP Dependency Check

Trivy container vulnerability scanning

Multi-stage Docker build

Non-root application container

Kubernetes
Minikube multi-node cluster

Helm deployment

Kubernetes Services

Health/readiness probes

Multiple API replicas

PostgreSQL and Redis workloads

GitOps
GitHub GitOps branch

Argo CD

Automatic synchronization

Self-healing

Declarative Kubernetes deployment

Istio
Istio Gateway

VirtualService

DestinationRule

v1/v2 application subsets

Weighted traffic routing

Progressive rollout demonstration

Rollback capability

Observability
Prometheus metrics

ServiceMonitor

Grafana dashboards

Payment metrics

Failure-rate monitoring

Grafana alert rule

Email notification delivery and ELK/Kibana centralized logging were
intentionally left outside the final project scope.

🧰 Technology Stack
Category Technology

Backend Python, FastAPI
Database PostgreSQL
Cache Redis
Testing Pytest
Containerization Docker, Docker Compose
CI Jenkins
Code Quality SonarQube
Dependency Security OWASP Dependency Check
Image Security Trivy
Container Registry Docker Hub
Orchestration Kubernetes / Minikube
Packaging Helm
GitOps Argo CD
Service Mesh Istio
Metrics Prometheus
Visualization Grafana
Source Control Git / GitHub

📁 Project Structure
payflow/
├── app/
│   ├── main.py
│   ├── routes/
│   ├── services/
│   ├── models/
│   ├── database.py
│   └── ...
│
├── alembic/
│   └── migrations
│
├── helm/
│   └── payflow/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│
├── infra/
│   ├── istio/
│   └── monitoring/
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── Jenkinsfile
├── requirements.txt
└── README.md
🚀 Getting Started
1. Clone
git clone https://github.com/rithuraj6/payflow.git
cd payflow
2. Run locally with Docker Compose
docker compose up --build
The local PayFlow API can be exposed on the configured application port.

Swagger/OpenAPI:

http://localhost:<port>/docs
☸️ Kubernetes Deployment
The project uses a Helm chart for Kubernetes deployment.

helm lint helm/payflow
Install:

helm install payflow ./helm/payflow \
  --namespace default
Check:

kubectl get pods
kubectl get services
🔄 CI/CD Workflow
Developer
    │
    ▼
Git Push
    │
    ▼
Jenkins
    │
    ├── Checkout
    ├── Python tests
    ├── SonarQube
    ├── OWASP Dependency Check
    ├── Docker build
    ├── Trivy scan
    └── Docker push
             │
             ▼
        Docker Hub
             │
             ▼
        GitOps update
             │
             ▼
          Argo CD
             │
             ▼
        Kubernetes
The important design principle is that CI builds and validates the
application, while Argo CD handles Kubernetes deployment from the
GitOps state.

🌿 GitOps Workflow
Application Repository
        │
        ▼
     Jenkins
        │
        ▼
 Container Image
        │
        ▼
     GitOps Branch
        │
        ▼
      Argo CD
        │
        ├── Detect change
        ├── Sync
        ├── Deploy
        └── Self-heal
              │
              ▼
         Kubernetes
This separates application build responsibilities from deployment
state management.

🔀 Istio Traffic Management
PayFlow contains two application versions:

PayFlow v1
PayFlow v2
Istio uses a DestinationRule to define subsets:

subsets:
  - name: v1
    labels:
      version: v1

  - name: v2
    labels:
      version: v2
A VirtualService controls the traffic distribution.

Example:

http:
  - route:
      - destination:
          host: payflow-payflow
          subset: v1
        weight: 90

      - destination:
          host: payflow-payflow
          subset: v2
        weight: 10
This allows progressive traffic movement:

100% v1
   ↓
90% v1 / 10% v2
   ↓
70% v1 / 30% v2
   ↓
50% v1 / 50% v2
   ↓
0% v1 / 100% v2
If the new version needs to be rolled back:

100% v2
   ↓
100% v1
Traffic weights represent routing proportions over requests; a small
test sample will not necessarily produce exact percentages.

📊 Monitoring
PayFlow exposes Prometheus metrics through:

/metrics
Prometheus discovers the service using a Kubernetes ServiceMonitor.

PayFlow API
     │
     ▼
 /metrics
     │
     ▼
 Prometheus
     │
     ▼
 Grafana
Example payment failure-rate query:

100 *
sum(increase(payflow_payments_total{status="FAILED"}[15m]))
/
clamp_min(sum(increase(payflow_payments_total[15m])), 1)
This calculates the percentage of failed payments over the selected
15-minute window.

🚨 Alerting
A Grafana alert rule named:

PayFlow High Failure Rate
monitors the payment failure percentage.

Example condition:

WHEN Query A IS ABOVE 50
The rule is evaluated every minute with a one-minute pending period.

Email notification delivery was not included in the final project
demonstration.

🔐 Security Pipeline
The Jenkins pipeline includes multiple security gates:

Source Code
    │
    ▼
Automated Tests
    │
    ▼
SonarQube
    │
    ▼
OWASP Dependency Check
    │
    ▼
Docker Build
    │
    ▼
Trivy Image Scan
    │
    ▼
Docker Registry
The Docker runtime also uses a dedicated non-root user.

🩺 Health & Troubleshooting
Health endpoint:

GET /health
Metrics:

GET /metrics
Useful Kubernetes commands:

kubectl get pods
kubectl get services
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl get events --sort-by=.lastTimestamp
Useful Helm commands:

helm list
helm status payflow
helm history payflow
helm get values payflow
Useful Argo CD commands:

argocd app get payflow
argocd app sync payflow
argocd app history payflow
Useful Istio commands:

istioctl analyze
istioctl proxy-status
istioctl proxy-config clusters <pod-name>
🧪 Example Payment Flow
Client
  │
  │ POST /payments
  ▼
Istio Gateway
  │
  ▼
PayFlow API
  │
  ├── Validate request
  ├── Check idempotency
  ├── Process simulated UPI payment
  ├── Store payment in PostgreSQL
  ├── Update/cache data in Redis
  └── Expose metrics
           │
           ├──────────────► Prometheus
           │                    │
           │                    ▼
           │                 Grafana
           │
           ▼
       Response
📌 Interview Talking Points
This project demonstrates practical knowledge of:

Linux and containerized application operations

Docker image optimization

CI/CD pipeline design

DevSecOps security gates

Kubernetes deployments and services

Helm chart management

GitOps with Argo CD

Service-mesh traffic management

Progressive application rollout

Rollback strategies

Prometheus metrics

Grafana dashboards and alerting

Application troubleshooting

🎯 Project Outcome
PayFlow demonstrates an end-to-end DevOps workflow:

Code
 ↓
Test
 ↓
Secure
 ↓
Build
 ↓
Containerize
 ↓
Publish
 ↓
GitOps
 ↓
Deploy
 ↓
Route
 ↓
Monitor
 ↓
Alert
The objective is not simply to deploy an API, but to demonstrate how a
modern DevOps engineer takes an application from source code to an
observable Kubernetes workload.

👨‍💻 Author
Rithu Raj R

DevOps Engineer | Python Developer

Focus areas:

Python · Django/FastAPI · Linux · Docker · Kubernetes ·
Jenkins · Helm · Argo CD · Istio · AWS · Prometheus ·
Grafana
