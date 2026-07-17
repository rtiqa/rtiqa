# System Modules

Version: 1.0

Status: Approved

---

# Purpose

This document defines the official modules of the Rtiqa platform.

Every feature, screen, API, database table, and AI capability belongs to one official module.

No module may be added without updating this document.

---

# Core Modules

## 1. Tenant Management

Responsibilities

- Multi-Tenant Architecture
- Institution Isolation
- Subscription
- Settings

Source

- Rtiqa Custom

---

## 2. School Management

Responsibilities

- Schools
- Branches
- Academic Years
- Terms
- Departments

Source

- ERPNext Education + Rtiqa

---

## 3. Student Management

Responsibilities

- Student Profile
- Enrollment
- Attendance
- Performance

Source

- ERPNext Education

---

## 4. Parent Portal

Responsibilities

- Children
- Attendance
- Grades
- Notifications
- Communication

Source

- Rtiqa Custom

---

## 5. Teacher Management

Responsibilities

- Teachers
- Assignments
- Schedules
- Performance

Source

- ERPNext Education

---

## 6. Learning Management

Responsibilities

- Courses
- Lessons
- Videos
- Assignments
- Quizzes
- Certificates

Source

- Frappe LMS

---

## 7. Examination System

Responsibilities

- Exams
- Question Bank
- Auto Grading
- Results

Source

- ERPNext Education + Rtiqa

---

## 8. Academic Management

Responsibilities

- Subjects
- Curriculum
- Timetable
- Classrooms

Source

- ERPNext Education

---

## 9. AI Platform

Responsibilities

- AI Assistant
- AI Search
- RAG
- Recommendations
- AI Tutor
- AI Analytics

Source

- Rtiqa Custom

---

## 10. Offline Synchronization

Responsibilities

- Local Storage
- Offline Queue
- Conflict Resolution
- Automatic Synchronization

Source

- Rtiqa Custom

---

## 11. Mobile Platform

Responsibilities

- Android
- iOS
- Offline Mode
- Push Notifications

Source

- Rtiqa Custom

---

## 12. User Management

Responsibilities

- Users
- Roles
- Permissions
- Authentication

Source

- Frappe

---

## 13. Finance

Responsibilities

- Fees
- Payments
- Invoices
- Reports

Source

- ERPNext

---

## 14. Communication

Responsibilities

- Email
- SMS
- Push Notifications
- Announcements

Source

- Rtiqa Custom

---

## 15. Reports

Responsibilities

- Dashboards
- Statistics
- Academic Reports
- Financial Reports

Source

- ERPNext + Rtiqa

---

## 16. File Management

Responsibilities

- Documents
- Images
- Videos
- Attachments

Source

- Frappe + Supabase

---

## 17. System Administration

Responsibilities

- Configuration
- Logs
- Monitoring
- Backup
- Restore

Source

- Frappe + Rtiqa

---

# Module Rules

Every module must:

- Be independent.
- Have clear responsibilities.
- Expose APIs only when necessary.
- Support future expansion.
- Follow Offline-First architecture.
- Be AI-ready.

---

# Official Modules Count

Current Official Modules

17

Additional modules require architecture approval.

---

Approved

Project:
Rtiqa

Document:
06_MODULES.md

Version:
1.0
