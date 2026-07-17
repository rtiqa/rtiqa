# Technical Stack
Version: 1.0
Status: Approved

---

# Purpose

This document defines the official technology stack of the Rtiqa platform.

All development, AI-generated code, infrastructure decisions, deployment, and future contributions MUST follow this document.

Changing any technology listed here requires an architecture review.

---

# Core Philosophy

Rtiqa is NOT built from scratch.

The platform is built by extending mature open-source software while adding original capabilities in artificial intelligence, synchronization, automation, and offline-first operation.

---

# Official Architecture

Base Platform

- Frappe Framework

Core Business System

- ERPNext

Learning Management

- Frappe LMS

Education Components

- ERPNext Education

Custom Platform

- Rtiqa Custom App

---

# Programming Languages

Backend

- Python 3.12+

Frontend

- JavaScript (ES2023)
- HTML5
- CSS3

Framework UI

- Vue.js (Official Frappe Frontend)

---

# Database

Primary Database

- MariaDB

Caching

- Redis

Background Jobs

- Redis Queue (RQ)

---

# Artificial Intelligence

Architecture

- Retrieval-Augmented Generation (RAG)

Primary Models

- OpenAI

Supported Models

- Google Gemini
- Anthropic Claude

Embedding Models

- Configurable
- OpenAI Embeddings by default

Vector Database

- To be selected during AI implementation phase.

---

# Storage

Object Storage

- Supabase Storage

Local Storage

- Docker Volumes

Backups

- Automated Scheduled Backups

---

# Authentication

Primary Authentication

- Frappe Authentication

Supported Authentication

- OAuth
- Google Login (Future)

---

# Containers

Container Engine

- Docker

Orchestration

- Docker Compose

Future Upgrade

- Kubernetes

---

# Reverse Proxy

Primary

- Caddy

Alternative

- Nginx

---

# DNS

DNS Provider

- Cloudflare

Domain

- rtiqa.com

SSL

- Cloudflare SSL

---

# Version Control

Repository

- GitHub

Branch Strategy

- main
- develop
- feature/*

---

# CI/CD

Platform

- GitHub Actions

Deployment

- Automated Docker Deployment

---

# Monitoring

Future Monitoring Stack

- Prometheus

- Grafana

- Sentry

---

# Secrets Management

Production Secrets

- GitHub Secrets

Container Secrets

- Docker Secrets

---

# Development Principles

The project must:

- Prefer configuration over modification.
- Avoid changing Frappe Core whenever possible.
- Place all custom logic inside the Rtiqa application.
- Keep AI modules isolated.
- Maintain upgrade compatibility.
- Support offline-first architecture.
- Remain modular and extensible.

---

# Architecture Decision

The following decision is officially approved.

Rtiqa SHALL be built on:

- Frappe Framework
- ERPNext
- ERPNext Education
- Frappe LMS

The development team SHALL extend these systems instead of rebuilding existing functionality from scratch.

Custom innovation will be implemented inside the dedicated Rtiqa application.

This decision remains effective unless replaced by a future Architecture Decision Record (ADR).

---

Approved by

Project: Rtiqa

Document:
04_TECH_STACK.md

Version:
1.0
