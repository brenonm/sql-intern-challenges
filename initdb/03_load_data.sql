-- CASE 1
COPY case1.users(user_id, created_at, country, marketing_source)
FROM '/data/case1_users.csv' WITH (FORMAT csv, HEADER true);

COPY case1.products(product_id, category, brand, cost)
FROM '/data/case1_products.csv' WITH (FORMAT csv, HEADER true);

COPY case1.subscriptions(subscription_id, user_id, plan, start_date, end_date, status)
FROM '/data/case1_subscriptions.csv' WITH (FORMAT csv, HEADER true);

COPY case1.orders(order_id, user_id, order_date, status, channel)
FROM '/data/case1_orders.csv' WITH (FORMAT csv, HEADER true);

COPY case1.order_items(order_id, product_id, qty, unit_price)
FROM '/data/case1_order_items.csv' WITH (FORMAT csv, HEADER true);

COPY case1.returns(return_id, order_id, product_id, qty, return_date, reason)
FROM '/data/case1_returns.csv' WITH (FORMAT csv, HEADER true);

COPY case1.campaign_attribution(user_id, campaign_id, touched_at)
FROM '/data/case1_campaign_attribution.csv' WITH (FORMAT csv, HEADER true);

-- CASE 2
COPY case2.accounts(account_id, name, created_at, tier)
FROM '/data/case2_accounts.csv' WITH (FORMAT csv, HEADER true);

COPY case2.app_users(user_id, account_id, created_at, role)
FROM '/data/case2_app_users.csv' WITH (FORMAT csv, HEADER true);

COPY case2.events(event_id, user_id, event_ts, event_type, page, session_id, properties_jsonb)
FROM '/data/case2_events.csv' WITH (FORMAT csv, HEADER true);

COPY case2.tickets(ticket_id, account_id, created_at, status, priority, closed_at)
FROM '/data/case2_tickets.csv' WITH (FORMAT csv, HEADER true);

COPY case2.ticket_events(ticket_id, event_ts, new_status, actor_user_id)
FROM '/data/case2_ticket_events.csv' WITH (FORMAT csv, HEADER true);