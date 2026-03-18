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
6) Subscription continuation risk: what % of ended subscriptions belong to users who did not place any order within 7 days after the subscription end date?
7) For each user: first order date, second order date, and days between them.
8) Return rate by category (returned qty / sold qty) + most common return reason per category.
9) Data quality investigation: identify orders whose status appears inconsistent with their item and return activity
  - Cancelled orders that still have positive sold value
  - Paid orders whose returned value exceeds sold value

## Bonus
1) Identify top 5% users by net revenue and their favorite category.