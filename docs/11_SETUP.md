# Development Environment Setup

Version: 1.0

Status: Approved

---

# Purpose

This document defines the official development environment for the Rtiqa platform.

Every developer and AI agent must use this setup.

---

# Operating System

Supported

- Ubuntu 24.04 LTS
- Debian 12

Recommended

Ubuntu 24.04 LTS

---

# Required Software

- Git
- Docker
- Docker Compose
- Python 3.12
- Node.js LTS
- Yarn
- Bench CLI

---

# Source Control

Repository

GitHub

Branch Strategy

- main
- develop
- feature/*
- hotfix/*

---

# Development Stack

Framework

- Frappe Framework

Applications

- ERPNext
- ERPNext Education
- Frappe LMS
- Rtiqa

---

# Containers

Required Containers

- Backend
- Frontend
- MariaDB
- Redis Cache
- Redis Queue
- Redis SocketIO
- Scheduler
- Worker
- Caddy

---

# Environment Variables

Examples

- DATABASE_URL
- REDIS_URL
- SITE_NAME
- SECRET_KEY
- OPENAI_API_KEY
- GEMINI_API_KEY
- SUPABASE_URL
- SUPABASE_KEY

---

# Code Standards

Python

- Black
- Ruff

JavaScript

- ESLint
- Prettier

---

# Git Rules

Every commit must

- Be atomic
- Have a clear message
- Pass validation

---

# Development Principles

- Docker First
- Configuration as Code
- Infrastructure as Code
- Reproducible Environment

---

Approved

Project:
Rtiqa

Document:
11_SETUP.md

Version:
1.0
