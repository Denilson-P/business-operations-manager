# Business Operations Manager

Full-stack application developed to manage common business operations involving sales commissions, inventory movements, and overdue interest calculations.

The project was developed with a **FastAPI backend** and a **React + TypeScript frontend**, with a focus on clear business rules, separation of responsibilities, input validation, automated testing, and a simple user interface.

## Features

The application implements three main business operations:

- Sales commission calculation
- Inventory management
- Overdue interest calculation

The original sales and inventory information used by the application comes from the data provided with the technical challenge and is stored locally in JSON files.

---

## Business Rules and Implementation Decisions

### 1. Sales Commissions

The application calculates total sales and commissions for each seller.

Commission is calculated **individually for each sale** before the results are aggregated by seller.

| Sale Value | Commission Rate |
| --- | ---: |
| Below R$ 100.00 | 0% |
| R$ 100.00 to R$ 499.99 | 1% |
| R$ 500.00 or more | 5% |

### Boundary Cases

The implementation explicitly considers the limits between commission ranges:

| Sale | Applied Rate |
| ---: | ---: |
| R$ 99.99 | 0% |
| R$ 100.00 | 1% |
| R$ 499.99 | 1% |
| R$ 500.00 | 5% |

This distinction is important because applying a commission rate directly to the seller's total sales would produce a different result.

The correct process is:

```text
Sale
  ↓
Determine commission rate
  ↓
Calculate commission for that sale
  ↓
Repeat for all sales
  ↓
Aggregate results by seller
```

### Commission Results

Using the sales data supplied with the challenge, the application produces:

| Seller | Total Sales | Total Commission |
| --- | ---: | ---: |
| João Silva | R$ 10,754.70 | R$ 495.68 |
| Maria Souza | R$ 9,874.30 | R$ 465.95 |
| Carlos Oliveira | R$ 7,928.35 | R$ 379.37 |
| Ana Lima | R$ 8,763.95 | R$ 404.98 |

These values are calculated by the backend from the individual sales stored in `sales.json`.

---

### 2. Inventory Management

The inventory module loads the initial stock from the JSON data supplied with the challenge.

Initial inventory:

| Product Code | Product | Initial Stock |
| ---: | --- | ---: |
| 101 | Caneta Azul | 150 |
| 102 | Caderno Universitário | 75 |
| 103 | Borracha Branca | 200 |
| 104 | Lápis Preto HB | 320 |
| 105 | Marcador de Texto Amarelo | 90 |

Two movement types are supported:

```text
ENTRY
EXIT
```

An `ENTRY` increases the current stock:

```text
current stock + quantity
```

An `EXIT` decreases the current stock:

```text
current stock - quantity
```

### Inventory Validations

Before changing the inventory, the application validates that:

- The product exists.
- The quantity is greater than zero.
- The movement type is valid.
- An exit does not exceed the available stock.
- The request contains valid data.

The inventory is only persisted after the business validations succeed.

Therefore, an invalid operation does **not** modify the stored inventory.

### Movement Identification

Every successful stock movement receives a unique UUID.

The API response also contains:

- Product code
- Product description
- Movement type
- Movement quantity
- Previous stock
- Current stock
- Movement ID

Example:

```text
Previous stock: 150
Movement: ENTRY
Quantity: 20
Current stock: 170
```

For an exit:

```text
Previous stock: 170
Movement: EXIT
Quantity: 10
Current stock: 160
```

### Inventory HTTP Behavior

| Scenario | HTTP Status |
| --- | ---: |
| Successful movement | 201 Created |
| Product not found | 404 Not Found |
| Insufficient stock | 409 Conflict |
| Invalid request data | 422 Unprocessable Entity |

---

### 3. Interest Calculation

The interest module calculates overdue interest using a daily rate of:

```text
2.5% per day
```

The implementation uses **simple interest**.

The calculation is:

```text
interest = original value × 0.025 × days late
```

The final amount is:

```text
total value = original value + interest
```

### Example

For an original value of:

```text
R$ 1,000.00
```

that is 5 days overdue:

```text
interest = 1000 × 0.025 × 5
interest = 125
```

Therefore:

```text
Original value: R$ 1,000.00
Interest:       R$   125.00
Total value:    R$ 1,125.00
```

### Interest Validations and Decisions

The implementation also handles the following cases:

- The original value must be greater than zero.
- The current date is used as the calculation date.
- A payment due today has zero days late.
- A future due date produces zero interest.
- Only overdue days generate interest.
- Monetary results are rounded to two decimal places.

The number of overdue days is calculated as:

```text
calculation date - due date
```

with a minimum value of zero.

This prevents future dates from generating negative interest.

---

## Backend Architecture

The backend is organized by business feature.

Each feature contains its own route, controller, DTOs, and service.

```text
Route
  ↓
Controller
  ↓
Service
  ↓
Data
```

### Route

Responsible for defining the HTTP endpoint and connecting FastAPI with the application layer.

### Controller

Receives validated data from the route, delegates the operation to the service, and handles application-specific errors when necessary.

### Service

Contains the business rules and calculations.

Examples include:

- Selecting the correct commission percentage
- Aggregating commissions by seller
- Validating inventory movements
- Updating stock
- Calculating overdue days
- Calculating interest

### DTO

Pydantic models define and validate request and response structures.

They ensure invalid input is rejected before reaching the business logic.

### Data

The challenge does not require a database.

The supplied sales and inventory information is therefore stored in JSON files under:

```text
backend/app/data/
```

Inventory movements update the inventory JSON after successful validation.

---

## Frontend Architecture

The frontend is built with React and TypeScript.

It is separated into:

```text
Pages
  ↓
Services
  ↓
API
```

Additional modules provide shared types and formatting utilities.

### Pages

The application contains three main screens:

- Commissions
- Inventory
- Interest

### Services

Frontend services isolate HTTP communication from the React components.

Axios is used to communicate with the FastAPI backend.

### Types

TypeScript interfaces describe the API request and response structures used by the frontend.

### Utilities

Shared utilities are used for operations such as:

- BRL currency formatting
- Date formatting

---

## Project Structure

```text
business-operations-manager/
├── backend/
│   ├── app/
│   │   ├── data/
│   │   │   ├── inventory.json
│   │   │   └── sales.json
│   │   │
│   │   ├── routes/
│   │   │   ├── commissions/
│   │   │   │   ├── controller.py
│   │   │   │   ├── dto.py
│   │   │   │   ├── route.py
│   │   │   │   └── service.py
│   │   │   │
│   │   │   ├── interest/
│   │   │   │   ├── controller.py
│   │   │   │   ├── dto.py
│   │   │   │   ├── route.py
│   │   │   │   └── service.py
│   │   │   │
│   │   │   └── inventory/
│   │   │       ├── controller.py
│   │   │       ├── dto.py
│   │   │       ├── route.py
│   │   │       └── service.py
│   │   │
│   │   └── main.py
│   │
│   ├── tests/
│   │   ├── test_commission_service.py
│   │   ├── test_interest_service.py
│   │   └── test_inventory_service.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Commissions.tsx
│   │   │   ├── Interest.tsx
│   │   │   └── Inventory.tsx
│   │   │
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   ├── commissionService.ts
│   │   │   ├── interestService.ts
│   │   │   └── inventoryService.ts
│   │   │
│   │   ├── types/
│   │   ├── utils/
│   │   ├── app.tsx
│   │   ├── main.tsx
│   │   └── styles.css
│   │
│   └── package.json
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## Technologies

### Backend

- Python 3.12
- FastAPI
- Pydantic
- Pytest

### Frontend

- React
- TypeScript
- Vite
- Axios
- CSS

### Development

- Git
- GitHub
- Python virtual environment
- npm

---

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/v1/commissions` | Returns sales totals and commissions grouped by seller |
| GET | `/api/v1/inventory` | Returns the current inventory |
| POST | `/api/v1/inventory/movements` | Registers an inventory movement |
| POST | `/api/v1/interest/calculate` | Calculates overdue interest |

---

## Running the Backend

From the project root:

```bash
cd backend
```

Create the virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the API:

```bash
fastapi dev app/main.py
```

The backend will normally be available at:

```text
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI automatically provides interactive Swagger documentation.

With the backend running, access:

```text
http://127.0.0.1:8000/docs
```

The available endpoints can be tested directly through this interface.

---

## Running the Frontend

Open another terminal and navigate to:

```bash
cd frontend
```

Install the dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

The backend must also be running for the frontend to load and modify application data.

---

## Automated Tests

The backend contains automated tests for the three business domains.

Run them from the backend directory with the virtual environment activated:

```bash
python -m pytest
```

The current test suite contains **20 tests**.

### Commission Tests

The tests validate:

- Sales below R$ 100.00
- The R$ 100.00 boundary
- Sales between R$ 100.00 and R$ 500.00
- The R$ 500.00 boundary
- Commission aggregation

### Inventory Tests

The tests validate:

- Inventory retrieval
- Stock entries
- Stock exits
- Product validation
- Insufficient stock
- Invalid quantities
- Movement information
- Inventory persistence behavior

Inventory tests use temporary JSON data so automated tests do not modify the original challenge inventory.

### Interest Tests

The tests validate:

- Overdue payments
- Multiple overdue days
- Payments due today
- Future due dates
- Invalid monetary values

Interest tests use a fixed calculation date where necessary, keeping the expected results deterministic and independent of the day on which the test suite is executed.

---

## Frontend Production Build

To verify that the frontend can be compiled successfully:

```bash
cd frontend
npm run build
```

Vite generates the production files under:

```text
frontend/dist/
```

---

## Validation

The application was validated at different levels during development:

```text
Business rules
    ↓
Automated backend tests
    ↓
API validation through Swagger
    ↓
Frontend integration
    ↓
Production frontend build
```

The final backend test suite passes successfully with:

```text
20 passed
```

The three business operations were also validated through the frontend against the FastAPI backend.

---

## Development Workflow

The project was developed incrementally using feature branches and pull requests.

The main functional deliveries were separated into:

```text
Project Setup
    ↓
Commission Management
    ↓
Inventory Management
    ↓
Interest Calculation
    ↓
Application Integration and Documentation
```

This keeps each change focused and makes the implementation history easier to review.

---

## License

This project is licensed under the terms available in the `LICENSE` file.