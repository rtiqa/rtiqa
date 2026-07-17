# Database Architecture

Version: 1.0

Status: Approved

---

# Purpose

This document defines the official database architecture of the Rtiqa platform.

All database objects must follow this specification.

---

# Database Engine

Primary Database

- MariaDB

Framework

- Frappe ORM

Storage Engine

- InnoDB

Character Set

- utf8mb4

Collation

- utf8mb4_unicode_ci

---

# Database Principles

- Multi-Tenant Ready
- Normalized Design
- AI Ready
- Upgrade Friendly
- High Performance
- Secure
- Auditable

---

# Core Data Domains

## Tenant

Stores institution information.

Examples

- Institution
- Subscription
- Settings

---

## Academic

Stores academic data.

Examples

- Academic Year
- Term
- Department
- Grade
- Section
- Classroom

---

## Student

Stores student information.

Examples

- Student
- Enrollment
- Attendance
- Academic Record

---

## Parent

Stores parent information.

Examples

- Parent
- Student Relationship
- Contact Information

---

## Teacher

Stores teacher information.

Examples

- Teacher
- Assignment
- Schedule

---

## Learning

Stores learning content.

Examples

- Course
- Module
- Lesson
- Quiz
- Assignment
- Certificate

---

## Examination

Stores examination data.

Examples

- Exam
- Question
- Question Bank
- Answer
- Result

---

## Finance

Stores financial records.

Examples

- Fee Structure
- Invoice
- Payment
- Receipt

---

## Communication

Stores communication records.

Examples

- Email
- SMS
- Push Notification
- Announcement

---

## AI

Stores AI-related information.

Examples

- AI Session
- Conversation
- Embedding
- Vector Reference
- Recommendation
- Search History

---

## File Management

Stores uploaded files.

Examples

- Image
- Video
- PDF
- Attachment

---

## Audit

Stores system logs.

Examples

- Audit Log
- Activity Log
- Login History
- Error Log

---

# Relationships

Tenant

↓

School

↓

Academic Year

↓

Class

↓

Student

↓

Course

↓

Lesson

↓

Assessment

↓

Result

---

# Indexing Rules

Every table must have

- Primary Key
- Created Index
- Modified Index

Search-heavy tables should include

- Full Text Index
- Composite Indexes

---

# Security Rules

- Row Permission Enforcement
- Role-Based Access
- Audit Logging
- Soft Delete when applicable
- Encryption for sensitive data

---

# Backup Strategy

- Daily Backup
- Weekly Full Backup
- Point-in-Time Recovery
- Automated Restore Testing

---

Approved

Project:
Rtiqa

Document:
07_DATABASE.md

Version:
1.0
