<div align="center">

# 💳 PayFlow
### Cloud-Native UPI Payment Processing Platform

**From code to cloud, fully automated.** 🚀

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=00C7B7)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)

![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=flat-square&logo=jenkins&logoColor=white)
![SonarQube](https://img.shields.io/badge/SonarQube-4E9BCD?style=flat-square&logo=sonarqube&logoColor=white)
![Trivy](https://img.shields.io/badge/Trivy-1904DA?style=flat-square&logo=aquasecurity&logoColor=white)
![ArgoCD](https://img.shields.io/badge/Argo%20CD-EF7B4D?style=flat-square&logo=argo&logoColor=white)
![Helm](https://img.shields.io/badge/Helm-0F1689?style=flat-square&logo=helm&logoColor=white)
![Istio](https://img.shields.io/badge/Istio-466BB0?style=flat-square&logo=istio&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana&logoColor=white)

![Status](https://img.shields.io/badge/status-active-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)
![Maintained](https://img.shields.io/badge/maintained-yes-success?style=flat-square)

</div>

<br>

PayFlow is a simulated **UPI payment processing platform** built with FastAPI, PostgreSQL, Redis, Docker and Kubernetes — backed by a complete DevOps delivery pipeline spanning Jenkins, SonarQube, OWASP Dependency Check, Trivy, Argo CD, Helm, Istio, Prometheus and Grafana.

The project demonstrates an end-to-end DevOps workflow covering **CI, DevSecOps, containerization, Kubernetes deployment, GitOps, service-mesh traffic management, and monitoring/alerting.**

<br>

## 🎯 Project Goals

- 🏗️ Build a realistic backend payment-processing service
- 🐳 Containerize the application using Docker
- 🔐 Automate CI and security checks with Jenkins
- ☸️ Deploy the application to Kubernetes using Helm
- 🔄 Implement GitOps with Argo CD
- 🔀 Demonstrate v1/v2 traffic management with Istio
- 📊 Monitor application and Kubernetes metrics with Prometheus and Grafana
- 🚨 Demonstrate payment failure-rate alerting

<br>

## 🏗️ Architecture

```mermaid
flowchart TD
    Dev([👨‍💻 Developer]) --> GH[(📦 GitHub)]
    GH --> CI[⚙️ Jenkins CI]

    subgraph CI_PIPE[" "]
        direction TB
        T[🧪 Tests] --> SQ[🔍 SonarQube]
        SQ --> ODC[🛡️ OWASP Dependency Check]
        ODC --> DB[🐳 Docker Build]
        DB --> TV[🔎 Trivy Scan]
        TV --> DP[📤 Docker Push]
    end

    CI --> CI_PIPE
    CI_PIPE --> DH[(🐳 Docker Hub)]
    DH --> GO[🌿 GitOps Branch]
    GO --> ACD[🔄 Argo CD]

    ACD --> K8S

    subgraph K8S["☸️ Kubernetes / Minikube"]
        direction TB
        IG[🚪 Istio Gateway] --> VS[🔀 VirtualService]
        VS --> V1[PayFlow v1]
        VS --> V2[PayFlow v2]
        V1 --> DATA[(🗄️ PostgreSQL + Redis)]
        V2 --> DATA
        V1 -.metrics.-> PR[📈 Prometheus]
        V2 -.metrics.-> PR
        PR --> GR[📊 Grafana]
    end

    style Dev fill:#6366f1,color:#fff,stroke:#4338ca
    style GH fill:#24292e,color:#fff,stroke:#000
    style CI fill:#D24939,color:#fff,stroke:#a12e22
    style DH fill:#2496ED,color:#fff,stroke:#0b5ed7
    style GO fill:#22c55e,color:#fff,stroke:#15803d
    style ACD fill:#EF7B4D,color:#fff,stroke:#c2531f
    style IG fill:#466BB0,color:#fff,stroke:#2d4a80
    style VS fill:#466BB0,color:#fff,stroke:#2d4a80
    style V1 fill:#0ea5e9,color:#fff,stroke:#0369a1
    style V2 fill:#8b5cf6,color:#fff,stroke:#6d28d9
    style DATA fill:#4169E1,color:#fff,stroke:#1e3a8a
    style PR fill:#E6522C,color:#fff,stroke:#b8391c
    style GR fill:#F46800,color:#fff,stroke:#c25300
```

<br>

## ⭐ Key Features

<table>
<tr>
<td valign="top" width="50%">

### 🧩 Application
- FastAPI REST API
- Simulated UPI payment processing
- PostgreSQL persistence
- Redis caching
- Payment status tracking
- Idempotency-key support
- Health endpoint
- Prometheus metrics endpoint

### 🔐 DevSecOps
- Jenkins CI pipeline
- Automated tests
- SonarQube code-quality analysis
- OWASP Dependency Check
- Trivy container vulnerability scanning
- Multi-stage Docker build
- Non-root application container

</td>
<td valign="top" width="50%">

### ☸️ Kubernetes
- Minikube multi-node cluster
- Helm deployment
- Kubernetes Services
- Health/readiness probes
- Multiple API replicas
- PostgreSQL and Redis workloads

### 🌿 GitOps
- GitHub GitOps branch
- Argo CD
- Automatic synchronization
- Self-healing
- Declarative Kubernetes deployment

### 🔀 Istio
- Istio Gateway
- VirtualService / DestinationRule
- v1/v2 application subsets
- Weighted traffic routing
- Progressive rollout & rollback

### 📊 Observability
- Prometheus metrics + ServiceMonitor
- Grafana dashboards
- Payment & failure-rate metrics
- Grafana alert rule

</td>
</tr>
</table>

> ℹ️ Email notification delivery and ELK/Kibana centralized logging were intentionally left outside the final project scope.

<br>

## 🧰 Technology Stack

| Category | Technology |
|---|---|
| 🐍 **Backend** | Python, FastAPI |
| 🗄️ **Database** | PostgreSQL |
| ⚡ **Cache** | Redis |
| 🧪 **Testing** | Pytest |
| 🐳 **Containerization** | Docker, Docker Compose |
| ⚙️ **CI** | Jenkins |
| 🔍 **Code Quality** | SonarQube |
| 🛡️ **Dependency Security** | OWASP Dependency Check |
| 🔎 **Image Security** | Trivy |
| 📦 **Container Registry** | Docker Hub |
| ☸️ **Orchestration** | Kubernetes / Minikube |
| 📦 **Packaging** | Helm |
| 🔄 **GitOps** | Argo CD |
| 🔀 **Service Mesh** | Istio |
| 📈 **Metrics** | Prometheus |
| 📊 **Visualization** | Grafana |
| 🌿 **Source Control** | Git / GitHub |

<br>

## 📁 Project Structure

```
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
```

<br>

## 🚀 Getting Started

### 1️⃣ Clone

```bash
git clone https://github.com/rithuraj6/payflow.git
cd payflow
```

### 2️⃣ Run locally with Docker Compose

```bash
docker compose up --build
```

The local PayFlow API can be exposed on the configured application port.

📖 **Swagger / OpenAPI:** `http://localhost:<port>/docs`

<br>

## ☸️ Kubernetes Deployment

The project uses a Helm chart for Kubernetes deployment.

```bash
helm lint helm/payflow
```

**Install:**

```bash
helm install payflow ./helm/payflow \
  --namespace default
```

**Check:**

```bash
kubectl get pods
kubectl get services
```

<br>

## 🔄 CI/CD Workflow

```mermaid
flowchart LR
    A[👨‍💻 Git Push] --> B[⚙️ Jenkins]
    B --> C[✅ Checkout]
    C --> D[🧪 Python Tests]
    D --> E[🔍 SonarQube]
    E --> F[🛡️ OWASP Check]
    F --> G[🐳 Docker Build]
    G --> H[🔎 Trivy Scan]
    H --> I[📤 Docker Push]
    I --> J[(🐳 Docker Hub)]
    J --> K[🌿 GitOps Update]
    K --> L[🔄 Argo CD]
    L --> M[☸️ Kubernetes]

    style A fill:#6366f1,color:#fff
    style B fill:#D24939,color:#fff
    style J fill:#2496ED,color:#fff
    style L fill:#EF7B4D,color:#fff
    style M fill:#326CE5,color:#fff
```

> 💡 **Design principle:** CI builds and validates the application, while Argo CD handles Kubernetes deployment from the GitOps state.

<br>

## 🌿 GitOps Workflow

```mermaid
flowchart TD
    A[📦 Application Repository] --> B[⚙️ Jenkins]
    B --> C[🐳 Container Image]
    C --> D[🌿 GitOps Branch]
    D --> E[🔄 Argo CD]
    E --> F{Detect Change}
    F --> G[🔃 Sync]
    G --> H[🚀 Deploy]
    H --> I[💚 Self-Heal]
    I --> J[☸️ Kubernetes]

    style E fill:#EF7B4D,color:#fff
    style J fill:#326CE5,color:#fff
```

This separates application build responsibilities from deployment state management.

<br>

## 🔀 Istio Traffic Management

PayFlow contains two application versions: **PayFlow v1** and **PayFlow v2**.

Istio uses a `DestinationRule` to define subsets:

```yaml
subsets:
  - name: v1
    labels:
      version: v1

  - name: v2
    labels:
      version: v2
```

A `VirtualService` controls the traffic distribution:

```yaml
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
```

### 📈 Progressive Traffic Rollout

| Stage | v1 | v2 |
|:---:|:---:|:---:|
| 1 | 🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦 100% | — |
| 2 | 🟦🟦🟦🟦🟦🟦🟦🟦🟦⬜ 90% | 🟪 10% |
| 3 | 🟦🟦🟦🟦🟦🟦🟦⬜⬜⬜ 70% | 🟪🟪🟪 30% |
| 4 | 🟦🟦🟦🟦🟦⬜⬜⬜⬜⬜ 50% | 🟪🟪🟪🟪🟪 50% |
| 5 | — | 🟪🟪🟪🟪🟪🟪🟪🟪🟪🟪 100% |

⏪ **Rollback:** `100% v2 → 100% v1`

> ⚠️ Traffic weights represent routing proportions over requests; a small test sample will not necessarily produce exact percentages.

<br>

## 📊 Monitoring

PayFlow exposes Prometheus metrics through **`/metrics`**, discovered via a Kubernetes `ServiceMonitor`.

```mermaid
flowchart LR
    A[🧩 PayFlow API] --> B[📍 /metrics]
    B --> C[📈 Prometheus]
    C --> D[📊 Grafana]

    style A fill:#00C7B7,color:#000
    style C fill:#E6522C,color:#fff
    style D fill:#F46800,color:#fff
```

**Payment failure-rate query:**

```promql
100 *
sum(increase(payflow_payments_total{status="FAILED"}[15m]))
/
clamp_min(sum(increase(payflow_payments_total[15m])), 1)
```

This calculates the percentage of failed payments over the selected 15-minute window.

<br>

## 🚨 Alerting

**Alert rule:** `PayFlow High Failure Rate`

| Property | Value |
|---|---|
| 🎯 Condition | `WHEN Query A IS ABOVE 50` |
| ⏱️ Evaluation interval | Every 1 minute |
| ⏳ Pending period | 1 minute |

> ℹ️ Email notification delivery was not included in the final project demonstration.

<br>

## 🔐 Security Pipeline

```mermaid
flowchart TD
    A[📄 Source Code] --> B[🧪 Automated Tests]
    B --> C[🔍 SonarQube]
    C --> D[🛡️ OWASP Dependency Check]
    D --> E[🐳 Docker Build]
    E --> F[🔎 Trivy Image Scan]
    F --> G[📦 Docker Registry]

    style A fill:#64748b,color:#fff
    style C fill:#4E9BCD,color:#fff
    style D fill:#7c3aed,color:#fff
    style F fill:#1904DA,color:#fff
    style G fill:#2496ED,color:#fff
```

The Docker runtime also uses a **dedicated non-root user**.

<br>

## 🩺 Health & Troubleshooting

**Health & Metrics**
```bash
GET /health
GET /metrics
```

**Kubernetes**
```bash
kubectl get pods
kubectl get services
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl get events --sort-by=.lastTimestamp
```

**Helm**
```bash
helm list
helm status payflow
helm history payflow
helm get values payflow
```

**Argo CD**
```bash
argocd app get payflow
argocd app sync payflow
argocd app history payflow
```

**Istio**
```bash
istioctl analyze
istioctl proxy-status
istioctl proxy-config clusters <pod-name>
```

<br>

## 🧪 Example Payment Flow

```mermaid
sequenceDiagram
    participant C as 📱 Client
    participant IG as 🚪 Istio Gateway
    participant API as 🧩 PayFlow API
    participant PG as 🗄️ PostgreSQL
    participant R as ⚡ Redis
    participant P as 📈 Prometheus
    participant G as 📊 Grafana

    C->>IG: POST /payments
    IG->>API: Route request
    API->>API: Validate request
    API->>API: Check idempotency
    API->>API: Process simulated UPI payment
    API->>PG: Store payment
    API->>R: Update/cache data
    API-->>P: Expose metrics
    P-->>G: Feed dashboards
    API-->>C: Response
```

<br>

## 📌 Interview Talking Points

<table>
<tr>
<td>✅ Linux & containerized app operations</td>
<td>✅ Docker image optimization</td>
</tr>
<tr>
<td>✅ CI/CD pipeline design</td>
<td>✅ DevSecOps security gates</td>
</tr>
<tr>
<td>✅ Kubernetes deployments & services</td>
<td>✅ Helm chart management</td>
</tr>
<tr>
<td>✅ GitOps with Argo CD</td>
<td>✅ Service-mesh traffic management</td>
</tr>
<tr>
<td>✅ Progressive application rollout</td>
<td>✅ Rollback strategies</td>
</tr>
<tr>
<td>✅ Prometheus metrics</td>
<td>✅ Grafana dashboards & alerting</td>
</tr>
<tr>
<td colspan="2" align="center">✅ Application troubleshooting</td>
</tr>
</table>

<br>

## 🎯 Project Outcome

<div align="center">

**Code → Test → Secure → Build → Containerize → Publish → GitOps → Deploy → Route → Monitor → Alert**

</div>

PayFlow demonstrates an end-to-end DevOps workflow. The objective is not simply to deploy an API, but to demonstrate how a modern DevOps engineer takes an application from source code to an **observable Kubernetes workload**.

<br>

---

<div align="center">

## 👨‍💻 Author

**Rithu Raj R**
*DevOps Engineer | Python Developer*

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/-Django/FastAPI-092E20?style=flat-square&logo=django&logoColor=white)
![Linux](https://img.shields.io/badge/-Linux-FCC624?style=flat-square&logo=linux&logoColor=black)
![Docker](https://img.shields.io/badge/-Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/-Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white)
![Jenkins](https://img.shields.io/badge/-Jenkins-D24939?style=flat-square&logo=jenkins&logoColor=white)
![Helm](https://img.shields.io/badge/-Helm-0F1689?style=flat-square&logo=helm&logoColor=white)
![ArgoCD](https://img.shields.io/badge/-Argo%20CD-EF7B4D?style=flat-square&logo=argo&logoColor=white)
![Istio](https://img.shields.io/badge/-Istio-466BB0?style=flat-square&logo=istio&logoColor=white)
![AWS](https://img.shields.io/badge/-AWS-232F3E?style=flat-square&logo=amazon-aws&logoColor=white)
![Prometheus](https://img.shields.io/badge/-Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/-Grafana-F46800?style=flat-square&logo=grafana&logoColor=white)

</div>
