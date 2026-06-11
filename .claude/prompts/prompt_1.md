You are a senior backend developer reviewing a FastAPI + PostgreSQL project
for a hardware inventory management system (Stockmaster).

## TASK 1 — Rename to Portuguese
- Read the entire `app/` backend folder
- Rename ALL variables, functions, class attributes, schema fields,
  route parameters and comments from English to Portuguese
- Keep Python reserved words and framework keywords in English
  (def, class, return, router, db, etc.)
- Fix all imports and references after renaming

## TASK 2 — Improve the data model
Analyze the current models and suggest + implement improvements such as:
- Supplier model (fornecedor): name, CNPJ, phone, email, address
- Purchase order model (pedido_compra): link supplier to stock entries
- Client model (cliente): for sales tracking
- Sale model (venda): group multiple products in one sale transaction
- Price history model (historico_preco): track price changes over time
- Any other table you judge necessary for a complete hardware system

For each new model also create:
- The SQLAlchemy model
- Pydantic schemas (create, update, response)
- Repository with basic queries
- Service with business rules
- Router with CRUD endpoints
- Register the router in main.py

## TASK 3 — Auto-generate SKU
- Implement automatic SKU generation on product creation
- Pattern: category prefix (3 letters) + sequential number (e.g. PAR-0001)
- SKU should NOT be required in the ProductCreate schema anymore

## TASK 4 — SQL Script
- Update `banco/create_database.sql` outside of the app folder to include all new tables,
  enums, indexes and triggers

## IMPORTANT
- Show me a complete plan of everything you found and intend to change
- Wait for my confirmation before applying any changes
- After applying, run a final check to make sure there are no broken imports
- Do NOT overcomplicate the system — work with what is already there,
  do not add unnecessary layers or abstractions
- Remove ALL authentication-related code (JWT, login, register,
  get_current_user, security.py, auth router, auth service, auth schemas)
  since authentication will not be used in this project
- The core features that must work perfectly are:
    - Products CRUD
    - Categories CRUD
    - Stock movements (buy/sell/adjust/write-off)
    - Suppliers CRUD
    - Sales history
    - Dashboard metrics (most/least sold, stock alerts, inventory value, etc.)