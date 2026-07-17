# System Architecture

Version: 1.0

Status: Approved

---

# Purpose

This document defines the official software architecture of the Rtiqa platform.

All future development MUST follow this architecture.

---

# Architecture Philosophy

Rtiqa is built by extending mature open-source systems instead of rebuilding existing functionality.

The platform follows a modular architecture where every major component has a single responsibility.

---

# High-Level Architecture

Client Applications

↓

Cloudflare

↓

Caddy Reverse Proxy

↓

Docker Compose

↓

Frappe Framework

├── ERPNext

├── ERPNext Education

├── Frappe LMS

└── Rtiqa Custom App

↓

MariaDB

↓

Redis

↓

AI Services

↓

Supabase Storage

---

# Main Components

## Cloudflare

Responsibilities

- DNS
- SSL
- Security
- CDN
- DDoS Protection

---

## Caddy

Responsibilities

- Reverse Proxy
- HTTPS
- Routing

---

## Docker

Responsibilities

- Containerization
- Development
- Deployment

---

## Frappe Framework

Responsibilities

- Core Framework
- User Management
- Permissions
- APIs

---

## ERPNext

Responsibilities

- Business Logic
- Education
- Administration

---

## Frappe LMS

Responsibilities

- Courses
- Lessons
- Learning Experience

---

## Rtiqa Custom App

Responsibilities

- AI Features
- Offline Synchronization
- Custom Modules
- Integrations

---

## MariaDB

Responsibilities

- Main Database

---

## Redis

Responsibilities

- Cache
- Queue
- Background Jobs

---

## Supabase

Responsibilities

- Object Storage
- Future Realtime Services

---

## AI Layer

Responsibilities

- RAG
- Embeddings
- AI Agents
- Recommendations
- AI Search

---

# Design Principles

- Modular Architecture
- Offline First
- AI First
- Upgrade Friendly
- Scalable
- Secure
- Maintainable

---

# Architecture Decision

The official architecture of Rtiqa consists of:

Cloudflare

↓

Caddy

↓

Docker

↓

Frappe Framework

↓

ERPNext

↓

ERPNext Education

↓

Frappe LMS

↓

Rtiqa Custom App

↓

MariaDB

↓

Redis

↓

Supabase

↓

AI Services

No component may bypass this architecture without an approved Architecture Decision.

---

Approved

Project: Rtiqa

Document:
05_ARCHITECTURE.md

Version:
1.0
