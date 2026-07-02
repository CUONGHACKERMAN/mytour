# Workspace Agent Rules

## System Overview & Tech Stack
This project is a multi-tenant tour agency system. All code, database queries, and business logic must align with the system architecture and tech stack below:
* **Tech Stack**: Python FastAPI, PostgreSQL, SQLAlchemy (v2.0+), Alembic, Pydantic (v2).
* **Architecture**: Flat Domain-Driven Design (DDD) with a shared Generic Repository pattern.

---

## Core Domains & Contexts

### 1. Tenant & Organization Management (Multi-Tenancy)
* **Tenant Isolation**: Data and operations must strictly be scoped per tenant (organization), ensuring complete data privacy and security across agencies.
* **Access Control**: Role-Based Access Control (RBAC) within each organization (e.g., Admin, Tour Manager, Booking Agent, Resource Coordinator).
* **Tenant Configuration**: Customized settings per organization, such as branding, currency, time zone, and localized policies.

### 2. Tour Management
* **Tour Definition**: Creation and cataloging of tour packages, itineraries, duration, included/excluded services, and dynamic pricing rules.
* **Schedules & Departures**: Management of tour departure dates, seat capacity, availability, and real-time status (e.g., Open, Guaranteed, Sold Out, Cancelled).
* **Itinerary & Activity Mapping**: Detailed day-by-day schedules detailing activities, locations, and assigned resources.

### 3. Booking Management
* **Booking Lifecycle**: Reservation creation, status tracking (Pending, Confirmed, Cancelled, Completed), modifications, and cancellations.
* **Passenger Details**: Capturing traveler information, special requirements (dietary, mobility, age groups), and documentation.
* **Pricing & Invoicing**: Automated calculation of total booking costs based on passenger types, add-ons, discounts, and payment status tracking.

### 4. Resource Management
Centralized repository and allocation system for third-party service providers and inventory:
* **Accommodation (Hotels/Resorts)**: Room allocation, contract pricing, check-in/check-out dates, and availability.
* **Transportation (Vehicle Providers)**: Fleet management, driver assignments, transfers, and vehicle capacity.
* **Tickets & Attractions**: Entry tickets, passes, show tickets, and time-slot vouchers.
* **Personnel & Guides**: Assignment of tour leaders, local guides, and support staff to specific tour departures.

### 5. Customer Management (CRM)
* **Customer Profiles**: Centralized database storing customer contact details, passport/ID info, emergency contacts, and preferences.
* **Booking History**: Tracking past and upcoming trips, total spend, and customer interactions.
* **Communication & Engagement**: Notification tracking, automated emails/reminders, and feedback collection.

---

## Architectural & Development Rules
1. **Flat DDD Domain Layout**: Business logic is organized in flat domain directories under `app/domains/<domain>/` containing `router.py`, `service.py`, `models.py`, and `schemas.py`. Avoid deep directory nesting.
2. **Generic Repository Pattern**: Database persistence utilizes a shared `BaseRepository` class in `app/core/repository.py` providing generic SQLAlchemy CRUD operations while automatically enforcing tenant isolation (`tenant_id`).
3. **Multi-Tenancy Enforcement**: All database queries and domain operations must strictly enforce tenant scoping and RBAC authorization.
4. **Code Quality & Guidelines**: Maintain clean code separation as documented in [project-structure.md](file:///home/cuongnguyen/mytour/backend/md/project-structure.md).
