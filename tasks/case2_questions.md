# Case 2 — Event Tracking + Performance + Intro NoSQL (Intermediate+)

Schema: `case2.*`

## Deliverables
- `case2_answers.sql`
- `perf_notes.md` with EXPLAIN ANALYZE before/after
- `nosql_notes.md` describing a user profile document

## Questions
1) Funnel (last 30 days): per account, conversion from page_view → add_to_cart → checkout (by session_id).
2) Session length: median session length per account (define session length as max(event_ts)-min(event_ts) per session).
3) DAU/WAU ratio per account tier.
4) Checkout rate by device and utm_campaign (from properties_jsonb).
5) Top 3 pages leading to checkout (previous event per session using window functions).
6) Ticket performance: time-to-close by priority; find accounts with ticket spikes that coincide with checkout drop WoW.
7) Performance: Run the provided slow query (below), add indexes, rerun EXPLAIN (ANALYZE, BUFFERS), explain tradeoffs.
8) NoSQL intro: propose a user_profile document schema and 3 access patterns.

### Slow query to optimize
(You can paste this into psql and measure EXPLAIN ANALYZE.)

SELECT a.account_id, date_trunc('day', e.event_ts) AS day, count(*) AS checkouts
FROM case2.events e
JOIN case2.app_users u ON u.user_id = e.user_id
JOIN case2.accounts a ON a.account_id = u.account_id
WHERE e.event_type = 'checkout'
  AND e.event_ts >= now() - interval '30 days'
  AND (e.properties_jsonb->>'device') IN ('web','ios','android')
GROUP BY 1,2
ORDER BY day DESC;