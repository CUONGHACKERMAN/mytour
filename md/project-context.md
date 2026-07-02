# Project Context: Multi-Tenant Tour Agency System

## System Overview
This project is a multi-tenant system designed for tour agencies (tenants/organizations) to manage their operations, resources, bookings, and customer relationships in an isolated, secure environment.

---

## Core Domains & Contexts

### 1. Tenant & Organization Management (Multi-Tenancy)
* **Tenant Isolation**: Data and operations are scoped per tenant (organization), ensuring complete data privacy and security across agencies.
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
