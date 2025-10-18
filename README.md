# 🎬 Video Streaming Platform

**Author:** Ali Shahrabi  
**Framework:** Django (v5.2.7)  
**REST Framework:** Django REST Framework (DRF)  
**API Documentation:** drf-spectacular + Swagger UI  
**Authentication:** Token-based Authentication  
**Permission Control:** DRF `IsAuthenticated`  
**Status:** In Development  

---

## 📌 Project Overview

A **Video Streaming Backend** built with **Django REST Framework**, featuring user authentication, subscription management, and secure API documentation.  
The system provides endpoints for managing **videos**, **users**, and **subscription plans**, ensuring that only authenticated users can access protected content.

---

## 🏗️ Tech Stack

- **Python** 3.12  
- **Django** 5.2.7  
- **Django REST Framework (DRF)**  
- **drf-spectacular** (for OpenAPI/Swagger documentation)  
- **SQLite3 / PostgreSQL** (configurable)  
- **Token Authentication**

---

## 🔑 Authentication

The project uses **Token Authentication** via DRF.

| Endpoint | Method | Description | Permission |
|-----------|---------|-------------|-------------|
| `/api/auth/register/` | `POST` | Register a new user | Public |
| `/api/auth/login/` | `POST` | Obtain auth token | Public |
| `/api/auth/logout/` | `POST` | Logout (requires token) | `IsAuthenticated` |

> After login, every request must include the `Authorization: Token <your_token>` header.

---

## 📺 App Structure

### **Applications**
- `account` – Handles authentication, registration, and login/logout logic.
- `videos` – Manages video data and streaming content.
- `subscriptions` – Handles subscription plans and user subscriptions.

---

## 💳 Subscription System

### Models:
- **SubscriptionPlan**
  - `name`
  - `price`
  - `duration_days`
- **Subscription**
  - `user`
  - `plan`
  - `start_date`
  - `end_date`

### Serializer Highlights:
- Nested serializers for `plan` details.
- `plan_id` handled with `PrimaryKeyRelatedField`.

### Sample POST Request
```json
{
  "plan_id": 2,
  "start_date": "2025-10-14T10:00:00Z",
  "end_date": "2026-10-14T10:00:00Z"
}

