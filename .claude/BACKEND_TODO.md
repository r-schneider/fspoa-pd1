# Backend TODO

Items the old frontend expected but the backend never implemented.
All items below have been resolved on the frontend side — no backend changes are required.

## Resolved without backend changes

| Old frontend call | Status | Resolution |
|---|---|---|
| `PATCH /fornecedores/{id}/toggle-ativo` | No such route | Replaced with `PUT /fornecedores/{id}` sending `{ ativo: !current }` |
| `GET /saidas/produtos` | No such route | Replaced with `GET /produtos?ativo=true` |
| `POST /saidas/` | No such route | Replaced with `POST /estoque/saida` |
| `GET /saidas/` | No such route | Replaced with `GET /estoque/historico` filtered client-side by `direcao === "SAIDA"` |

## Missing features (future work)

- No authentication / user system — all endpoints are open
- No monthly sales/revenue metric in `/dashboard/metricas` (only `saidas_hoje`)
- No location/warehouse field on products
- Product ranking (`/dashboard/mais-vendidos`) does not return category name
- No pagination UI in frontend tables
