web application/stitch/projects/11725227052415550926/screens/4185741238636717826
# Role & Context
You are a Principal UI/UX Designer and Senior Frontend Engineer specializing in enterprise SaaS and travel management systems. Your goal is to build a complete, high-density, accessible, and user-friendly interface for a modern **Tour Agency ERP** (managing bookings, itineraries, custom tour packaging, passenger manifests, vendor payments, and inventory).

---

## 1. Design System & Visual Identity

### Color Tokens
* **Primary (Brand & Action):** `#74BDDA` (Soft Sky Blue)
  * Hover / Active: `#5aaecf` / `#469bbd`
  * Subdued / Surface Tint: `#eef7fa`
* **Secondary (Accents & Highlights):** `#95DEE4` (Fresh Aqua Mint)
  * Accent Badge / Highlight Surface: `#e6f9fa`
* **Backgrounds & Canvas:**
  * App Background: `#F8FAFC` (Soft Slate White)
  * Panel / Card / Table Background: `#FFFFFF`
  * Elevated Layers (Drawers / Popovers): `#FFFFFF`
* **Typography & Neutrals (High Contrast, Readable):**
  * Text Primary (Headings, primary data): `#1E293B` (Slate 800)
  * Text Secondary (Labels, subtexts, metadata): `#64748B` (Slate 500)
  * Text Muted (Placeholders, disabled): `#94A3B8` (Slate 400)
  * Borders & Dividers: `#E2E8F0` (Slate 200)
* **Functional & Status Colors (Muted Travel Tones):**
  * Success (Confirmed / Paid): `#10B981` (Surface: `#ECFDF5`)
  * Warning (Pending / In-Review): `#F59E0B` (Surface: `#FFFBEB`)
  * Danger / Cancellation: `#EF4444` (Surface: `#FEF2F2`)
  * Information / Draft: `#74BDDA` (Surface: `#EEF7FA`)

### Shape, Radius & Elevation
* **Curvy & Soft UI:**
  * Small elements (Badges, chips, buttons, inputs): `rounded-lg` (8px–10px)
  * Panels, Cards, Metric tiles, and Drawers: `rounded-2xl` (16px–20px)
  * Inner table containers: `rounded-xl` (12px–14px) with subtle 1px border (`#E2E8F0`)
* **Shadows:** Soft, diffused shadows for layers—avoid heavy or dark drop-shadows.
  * Base: `0 1px 3px rgba(15, 23, 42, 0.04)`
  * Floating / Active Panel: `0 10px 25px -5px rgba(116, 189, 218, 0.12), 0 8px 10px -6px rgba(15, 23, 42, 0.04)`

---

## 2. Structural & Layout Architecture

* **Collapsible Left Sidebar:**
  * Navigation for Bookings, Tours & Packages, Manifests, CRM/Customers, Guides/Suppliers, Finance, and Settings.
  * Curvy active indicator pill styled with `#74BDDA` tint and deep `#1E293B` text.
* **Top Command Bar:**
  * Global search bar (shortcut: `⌘+K`), agency switch selector, date-range picker, notifications pill, and user profile pill.
* **Multi-Panel Split Workspace:**
  * Main Content Canvas + Contextual Right Slide-over Panel (Drawer) for seamless master-detail drill-downs without page switching.

---

## 3. Data-Dense Table Experience (ERP Core)

* **Table Container Specifications:**
  * Outer border `rounded-xl` with smooth overflow clipping.
  * **Sticky Header:** Sticky column header row with a subtle background `#F8FAFC`, uppercase sub-text typography (`text-xs font-semibold text-slate-500 tracking-wider`).
  * **Row Ergonomics:** Alternating hover highlight (`hover:bg-[#EEF7FA]/60`), height `48px` to `56px` for touch/click ergonomics.
  * **Cell Visuals:** Avatars with initials for guides/customers, color-coded pill status chips with soft pastel fills, inline quick-action icon clusters on hover.
  * **Inline Expansion:** Expandable rows showing sub-itinerary breakdowns or passenger lists without leaving the table.
  * **Sticky Actions Column:** Rightmost column fixed with actions (`Edit`, `Duplicate`, `View Manifest`, `Export PDF`).

---

## 4. Strict Frontend (FE) UX Rules & Constraints

1. **Zero Nested Modals ("No Popup on Popup"):**
   * Never open a dialog/modal from inside an existing dialog/modal.
   * Use **Slide-Over Drawers (`Sheet`)** for item creation and deep edits.
   * If a secondary action is needed inside a drawer (e.g., "Add New Customer" while building an itinerary), use an **in-place Accordion / Multi-step Wizard** or an inline combobox creation pattern.
2. **Context-Preserving Filtering:**
   * Global table filters (Status, Date Range, Destination, Tour Leader) must be inline above the table header with removable pill tags (`Badge` with `x`).
3. **Optimistic Feedback & Confirmations:**
   * Destructive actions (e.g., "Cancel Tour") require an inline popover confirmation with double-click/explicit text confirm, not a full blocking alert dialog.
4. **Empty & Loading States:**
   * Skeletons reflecting table rows and metric cards during fetching.
   * Illustrated, friendly empty states with a direct primary action button (e.g., *"No active tour bookings found. Create Booking"*).

---

## 5. Required Screens & Key Components to Generate

1. **Dashboard & Booking Management:**
   * 4 Top KPI metric cards (Total Bookings, Active Tours, Pending Manifests, Revenue) using soft curvy borders and `#95DEE4` accent lines.
   * Main Filterable Tour Booking Table (Columns: Booking ID, Tour Package, Customer/Lead, Departure Date, Seats Booked/Capacity, Total Amount, Status, Actions).
2. **Right Detail Drawer (`SlideOver`):**
   * Triggered by clicking any table row.
   * Shows passenger breakdown, flight/transport itinerary timeline, payment status bar, and direct guide assignment dropdown.
3. **Interactive Filter Toolbar:**
   * Search input with icon, destination multi-select dropdown, date range pill, and quick-filter toggle chips ("Departing This Week", "Unassigned Guides", "Unpaid").

---

## Technical Stack & Component Conventions
* Framework: React / Next.js with TypeScript & Tailwind CSS.
* Component Base: Radix UI / Shadcn UI / Lucide-React Icons.
* Ensure all elements comply with WCAG 2.1 AA for text contrast on light backgrounds.
