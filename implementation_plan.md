# Goal Description
Develop Phase 4: Frontend Architecture. This phase transitions Synapse-AI-ERP from a robust backend intelligence stack to a modern, premium, interactive user interface. We will build a Next.js (React) application that consumes our frozen Phase 3 API contracts.

## User Review Required
> [!IMPORTANT]
> Please review this frontend architecture plan. Once approved, I will bootstrap the Next.js application, install the necessary dependencies (like Tailwind CSS and Framer Motion), and begin building the components.

## Open Questions
> [!TIP]
> 1. Do you have a preferred UI component library (e.g., shadcn/ui, Radix, Chakra) or should I stick to raw Tailwind + Headless UI? (I recommend shadcn/ui for a premium, accessible foundation).
> 2. For the 3D Warehouse/Supply Chain components, are you comfortable using `@react-three/fiber` and `@react-three/drei`?

## Proposed Changes

### Next.js Application Scaffold
- Initialize a new Next.js 14 App Router project in the `frontend/` directory.
- Configure Tailwind CSS for styling and Framer Motion for micro-animations.

#### [NEW] `frontend/package.json`
- Next.js, React, Tailwind CSS, Framer Motion, Axios (for API consumption), Lucide-React (icons).

#### [NEW] `frontend/app/layout.tsx`
- The root layout including the global navigation bar with button-style navigation: `[Dashboard] [Inventory] [Forecast] [Suppliers] [Simulation] [Analytics]`.

### Core Pages (App Router)

#### [NEW] `frontend/app/page.tsx` (Dashboard)
- Implements the "What needs my attention right now?" view.
- 4 Key Health Metrics cards (Inventory Health, Stockout Risks, Supplier Risk, Forecast Accuracy).
- Interactive charts and ABC distribution visualization.

#### [NEW] `frontend/app/inventory/page.tsx`
- Displays Inventory Mathematics (Safety Stock, ROP, EOQ, ABC, Reorder Recommendations).
- Stockout Risk and Dead Stock warnings.

#### [NEW] `frontend/app/forecasting/page.tsx`
- Interactive visualization of the XGBoost predictions vs historical demand.

#### [NEW] `frontend/app/suppliers/page.tsx`
- Supplier comparison matrices.
- Supplier Performance Score, Lead-Time Analytics, and Delay Risk.

#### [NEW] `frontend/app/simulation/page.tsx`
- The flagship What-If Simulation Engine UI.
- Form inputs for Scenario configuration (Delay, Demand Spike, etc).
- Split-pane or side-by-side display of BASELINE vs SCENARIO.
- Impact metrics and dynamic rule-based recommendations.

### 3D Visualizations

#### [NEW] `frontend/3d/warehouse/WarehouseScene.tsx`
- A React-Three-Fiber component visualizing the physical warehouse storage zones.
- Highlights product locations and stockout warnings in 3D space.

#### [NEW] `frontend/3d/supply-chain/NetworkScene.tsx`
- A 3D graph representing nodes (Suppliers, Warehouses, Customers) and edges (Shipments, Lead Times, Risks).

### API Integration Layer

#### [NEW] `frontend/lib/api/`
- Axios client configured to talk to `http://localhost:8000/api/v1`.
- Typed response wrappers matching our frozen Python Pydantic schemas.

## Verification Plan

### Automated Tests
- Unit tests for the API client layers.
- Component rendering tests for critical UI elements like the Simulation dashboard.

### Manual Verification
- Launch the backend API.
- Launch the Next.js dev server.
- Visually verify the Dashboard metrics fetch correctly.
- Run a What-If simulation from the UI and verify the impact cascade renders appropriately in the split view.
- Interact with the 3D Warehouse to ensure WebGL performance is smooth and responsive.
