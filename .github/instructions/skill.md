# FODEC Development Skill

## Mission

You are collaborating on the **FODEC** project.

Your primary objective is not only to generate working code, but also to preserve the architecture, maintainability and long-term quality of the project.

Whenever a tradeoff exists between writing quick code and preserving the architecture, always preserve the architecture.

---

# Read First

Before implementing any feature, review the following documents in order:

1. README.md
2. docs/architecture.md
3. docs/deployment.md
4. docs/ADR/

Architecture Decision Records are mandatory.

If a proposed implementation conflicts with an ADR, stop and explain the conflict before generating code.

---

# Project Overview

FODEC is a self-service portal for members of an employee fund.

Current technology stack:

* Python
* FastAPI
* Docker
* Google Cloud Run
* Firebase Hosting
* React
* Google Sheets (temporary data source)

Google Sheets is an infrastructure detail, not part of the business logic.

The architecture must allow replacing Google Sheets without changing the API or the frontend.

---

# Architecture Rules

Always respect the following layers.

```text
API
 ↓
Services
 ↓
Repositories
 ↓
External Clients
```

Responsibilities:

API

* HTTP endpoints
* Request validation
* Response mapping

Services

* Business rules
* Orchestration
* Use cases

Repositories

* Data access
* Persistence
* Infrastructure abstraction

Clients

* External APIs
* Google APIs
* SMTP
* SMS
* Other providers

Business logic never belongs in API, Repository or Client.

---

# FastAPI Rules

There must be only one FastAPI application.

Always use APIRouter.

Never instantiate FastAPI more than once.

Future endpoints should remain compatible with API versioning.

---

# Dependency Rules

requirements.txt must contain only direct project dependencies.

Never add transitive dependencies manually.

Always prefer standard library modules whenever appropriate.

---

# Docker Rules

Docker is the official execution environment.

Every feature must work both:

* locally
* inside Docker
* in Cloud Run

Do not introduce environment-specific behavior.

---

# Cloud Rules

Current platform:

Frontend

Firebase Hosting

Backend

Cloud Run

Container Registry

Artifact Registry

Cloud Region

us-central1

Always preserve compatibility with this deployment model.

---

# Security Rules

Never:

* commit secrets
* commit passwords
* commit API keys
* commit credentials

Always use environment variables.

Future secret management will use Google Secret Manager.

Never log sensitive user information.

---

# Code Style

Prioritize:

* readability
* simplicity
* descriptive names
* small functions
* low coupling
* high cohesion

Avoid unnecessary abstractions.

Do not optimize prematurely.

Comments should explain **why**, not **what**.

---

# Project Philosophy

Build today.

Prepare for tomorrow.

Avoid overengineering.

Keep the architecture flexible.

Every component should be replaceable with minimal impact.

---

# Current Project Status

Completed

* React application
* Firebase Hosting
* FastAPI
* APIRouter
* Docker
* Google Cloud Project
* Billing
* Budget
* Google Cloud services

In Progress

* Artifact Registry
* Cloud Build
* Cloud Run deployment

Upcoming

* Google Sheets integration
* OTP authentication
* Member consultation
* Reports

---

# Definition of Done

A task is considered complete only if:

* Code compiles.
* Application starts successfully.
* Docker image builds successfully.
* Existing functionality is preserved.
* Documentation is updated if necessary.
* Architecture rules are respected.

---

# Expected AI Behavior

Before generating code:

1. Understand the requested feature.

2. Verify whether an ADR already covers the decision.

3. Reuse existing components whenever possible.

4. Prefer extending existing Services over creating new ones.

5. Preserve the existing architecture.

6. If an implementation violates an ADR, explain the issue before proceeding.

7. If there are multiple valid implementations, recommend the one that best aligns with the current architecture.

8. Never sacrifice maintainability for short-term convenience.

9. If documentation should change as part of the task, suggest the corresponding updates.

10. Think as a long-term collaborator, not only as a code generator.

---

# Final Goal

The objective is not simply to build software.

The objective is to build software that remains understandable, maintainable and evolvable for many years.
