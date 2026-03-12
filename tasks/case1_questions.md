# Case 1 — Subscription + Orders Analytics (Basic → Intermediate)

Schema: `case1.*`

## Rules
- Use explicit JOINs (no implicit joins).
- Avoid SELECT * in final answers.
- Assume "net revenue" = sum(qty * unit_price) - sum(returned_qty * unit_price for returned items).

## Questions
1) List all users and their current subscription status (active/cancelled/expired/none).
2) Monthly gross revenue and net revenue for the last 6 months.
3) Top 3 categories by net revenue in the last 90 days.
4) Cohorts: users created per month and % who placed an order within 14 days of signup.
5) AOV by channel (exclude cancelled orders).
6) Renewal: % of subscriptions that have a new subscription within 7 days after an end_date.
7) For each user: first order date, second order date, and days between them.
8) Return rate by category (returned qty / sold qty) + most common return reason per category.
9) Data quality: find orders where computed item total differs from expected by > 1%.

## Bonus
1) Identify top 5% users by net revenue and their favorite category.