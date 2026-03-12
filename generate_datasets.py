import csv
import json
import os
import random
from datetime import datetime, timedelta, date

# ----------------------------
# Config
# ----------------------------
SEED = 42
OUT_DIR = "data"

# Size knobs (tweak if needed)
CASE1_USERS = 1200
CASE1_PRODUCTS = 250
CASE1_ORDERS = 9000
CASE1_MAX_ITEMS_PER_ORDER = 5
CASE1_RETURN_RATE = 0.09

CASE2_ACCOUNTS = 120
CASE2_USERS = 2500
CASE2_EVENTS = 180000   # enough for indexing to matter but still laptop-friendly
CASE2_TICKETS = 3500
CASE2_TICKET_EVENTS_MAX = 8

START_DATE = date.today() - timedelta(days=180)  # ~6 months back
END_DATE = date.today()

random.seed(SEED)

# ----------------------------
# Helpers
# ----------------------------
def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def rand_date(start: date, end: date) -> date:
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, max(delta, 0)))

def rand_dt(start: datetime, end: datetime) -> datetime:
    delta = int((end - start).total_seconds())
    return start + timedelta(seconds=random.randint(0, max(delta, 1)))

def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)

def pick_weighted(items, weights):
    return random.choices(items, weights=weights, k=1)[0]

def iso_date(d: date) -> str:
    return d.isoformat()

def iso_dt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")

# ----------------------------
# Case 1 data generation
# Schema: case1.users, subscriptions, orders, order_items, products, returns, campaign_attribution
# ----------------------------
def gen_case1():
    marketing_sources = ["google", "facebook", "organic", "referral", "email", "tiktok"]
    countries = ["BR", "US", "MX", "CA", "PT"]
    plans = ["basic", "pro", "enterprise"]
    channels = ["web", "ios", "android", "phone"]
    order_statuses = ["paid", "paid", "paid", "cancelled", "refunded"]  # skew to paid
    categories = ["beer", "snacks", "coffee", "cleaning", "pets", "personal_care", "dairy", "produce"]
    brands = ["Acme", "Nova", "Zeta", "Orbit", "Prime", "Vale", "Sol", "Rio"]

    # Users
    users = []
    for uid in range(1, CASE1_USERS + 1):
        created = rand_date(START_DATE, END_DATE)
        users.append([
            uid,
            iso_date(created),
            random.choice(countries),
            pick_weighted(marketing_sources, [28, 18, 25, 8, 12, 9]),
        ])

    # Products
    products = []
    for pid in range(1, CASE1_PRODUCTS + 1):
        cat = random.choice(categories)
        brand = random.choice(brands)
        cost = round(random.uniform(1.0, 60.0), 2)
        products.append([pid, cat, brand, cost])

    # Subscriptions (not every user)
    subs = []
    sub_id = 1
    for u in users:
        uid = u[0]
        if random.random() < 0.62:
            plan = pick_weighted(plans, [60, 30, 10])
            s = rand_date(u_created := date.fromisoformat(u[1]), END_DATE)
            # some are active, some churned
            if random.random() < 0.55:
                # active
                e = None
                status = "active"
            else:
                # ended
                e = rand_date(s + timedelta(days=14), min(END_DATE, s + timedelta(days=180)))
                status = "cancelled" if random.random() < 0.7 else "expired"
            subs.append([sub_id, uid, plan, iso_date(s), iso_date(e) if e else "", status])
            sub_id += 1

    # Orders + Items
    orders = []
    order_items = []
    order_id = 1

    # Make some users frequent buyers
    heavy_buyers = set(random.sample(range(1, CASE1_USERS + 1), k=int(CASE1_USERS * 0.12)))

    for _ in range(CASE1_ORDERS):
        uid = random.randint(1, CASE1_USERS)
        if uid in heavy_buyers and random.random() < 0.6:
            od = rand_date(END_DATE - timedelta(days=90), END_DATE)
        else:
            od = rand_date(START_DATE, END_DATE)

        status = random.choice(order_statuses)
        channel = pick_weighted(channels, [55, 18, 20, 7])
        orders.append([order_id, uid, iso_date(od), status, channel])

        n_items = random.randint(1, CASE1_MAX_ITEMS_PER_ORDER)
        picked_products = random.sample(range(1, CASE1_PRODUCTS + 1), k=min(n_items, CASE1_PRODUCTS))
        for pid in picked_products:
            qty = random.randint(1, 4)
            # price: cost * margin + noise
            cost = products[pid - 1][3]
            unit_price = round(cost * random.uniform(1.25, 2.4), 2)
            order_items.append([order_id, pid, qty, unit_price])

        order_id += 1

    # Returns (only for paid orders)
    returns = []
    return_id = 1
    paid_orders = [o for o in orders if o[3] == "paid"]
    reasons = ["damaged", "late_delivery", "wrong_item", "changed_mind", "quality_issue"]

    # build item lookup per order
    items_by_order = {}
    for oi in order_items:
        items_by_order.setdefault(oi[0], []).append(oi)

    for o in paid_orders:
        if random.random() < CASE1_RETURN_RATE:
            oid = o[0]
            od = date.fromisoformat(o[2])
            # pick 1 item from that order
            oi = random.choice(items_by_order[oid])
            pid = oi[1]
            sold_qty = oi[2]
            rqty = random.randint(1, sold_qty)
            rdate = rand_date(od, min(END_DATE, od + timedelta(days=30)))
            returns.append([return_id, oid, pid, rqty, iso_date(rdate), random.choice(reasons)])
            return_id += 1

    # Campaign attribution (touch points)
    campaign_attrib = []
    campaign_ids = list(range(1, 26))
    for uid in range(1, CASE1_USERS + 1):
        if random.random() < 0.55:
            touches = random.randint(1, 4)
            for _ in range(touches):
                touched = rand_date(START_DATE, END_DATE)
                campaign_attrib.append([uid, random.choice(campaign_ids), iso_date(touched)])

    # Write CSVs
    ensure_dir(OUT_DIR)
    write_csv(f"{OUT_DIR}/case1_users.csv",
              ["user_id", "created_at", "country", "marketing_source"], users)

    write_csv(f"{OUT_DIR}/case1_products.csv",
              ["product_id", "category", "brand", "cost"], products)

    write_csv(f"{OUT_DIR}/case1_subscriptions.csv",
              ["subscription_id", "user_id", "plan", "start_date", "end_date", "status"], subs)

    write_csv(f"{OUT_DIR}/case1_orders.csv",
              ["order_id", "user_id", "order_date", "status", "channel"], orders)

    write_csv(f"{OUT_DIR}/case1_order_items.csv",
              ["order_id", "product_id", "qty", "unit_price"], order_items)

    write_csv(f"{OUT_DIR}/case1_returns.csv",
              ["return_id", "order_id", "product_id", "qty", "return_date", "reason"], returns)

    write_csv(f"{OUT_DIR}/case1_campaign_attribution.csv",
              ["user_id", "campaign_id", "touched_at"], campaign_attrib)

# ----------------------------
# Case 2 data generation
# Schema: case2.accounts, app_users, events (with jsonb), tickets, ticket_events
# ----------------------------
def gen_case2():
    tiers = ["free", "pro", "enterprise"]
    roles = ["member", "admin", "viewer"]
    event_types = ["page_view", "add_to_cart", "checkout", "login", "search", "support_click"]
    pages = ["/", "/pricing", "/dashboard", "/settings", "/products", "/checkout", "/help", "/search", "/cart"]

    devices = ["ios", "android", "web"]
    campaigns = ["spring", "summer", "brand", "retarget", "influencer", "newsletter"]
    countries = ["BR", "US", "MX", "CA", "PT", "AR"]

    # Accounts
    accounts = []
    for aid in range(1, CASE2_ACCOUNTS + 1):
        created = rand_date(START_DATE, END_DATE - timedelta(days=30))
        tier = pick_weighted(tiers, [55, 30, 15])
        accounts.append([aid, f"Account_{aid:03d}", iso_date(created), tier])

    # Users
    users = []
    user_id = 1
    users_per_account = [0] * (CASE2_ACCOUNTS + 1)
    for _ in range(CASE2_USERS):
        aid = random.randint(1, CASE2_ACCOUNTS)
        users_per_account[aid] += 1
        created = rand_date(date.fromisoformat(accounts[aid - 1][2]), END_DATE)
        role = pick_weighted(roles, [78, 12, 10])
        users.append([user_id, aid, iso_date(created), role])
        user_id += 1

    # Events
    events = []
    # Session IDs: keep them short and group events
    now0 = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start_dt = now0 - timedelta(days=180)
    end_dt = now0 + timedelta(days=1) - timedelta(seconds=1)

    # Make "power" accounts with more events
    power_accounts = set(random.sample(range(1, CASE2_ACCOUNTS + 1), k=int(CASE2_ACCOUNTS * 0.15)))

    # map users by account for selection
    users_by_account = {}
    for u in users:
        users_by_account.setdefault(u[1], []).append(u[0])

    event_id = 1
    for _ in range(CASE2_EVENTS):
        aid = random.randint(1, CASE2_ACCOUNTS)
        uid = random.choice(users_by_account[aid])

        # skew timestamps: more recent, and power accounts heavier
        if aid in power_accounts and random.random() < 0.7:
            ts = rand_dt(end_dt - timedelta(days=30), end_dt)
        else:
            ts = rand_dt(start_dt, end_dt)

        # build session id: user + day bucket + random
        session_id = f"s{uid}_{ts.strftime('%Y%m%d')}_{random.randint(1, 60)}"

        # event type skew: lots of page_view, fewer checkout
        et = pick_weighted(event_types, [55, 10, 3, 8, 18, 6])
        page = random.choice(pages)

        props = {
            "device": pick_weighted(devices, [18, 22, 60]),
            "utm_campaign": pick_weighted(campaigns, [20, 15, 25, 15, 10, 15]),
            "country": random.choice(countries),
        }

        # add some occasional numeric property
        if et in ("add_to_cart", "checkout"):
            props["cart_value"] = round(random.uniform(10, 400), 2)
            props["items"] = random.randint(1, 8)

        events.append([event_id, uid, iso_dt(ts), et, page, session_id, json.dumps(props, ensure_ascii=False)])
        event_id += 1

    # Tickets
    tickets = []
    ticket_events = []
    ticket_id = 1
    ticket_statuses = ["open", "pending", "solved", "closed"]
    priorities = ["low", "medium", "high", "urgent"]

    # account-level "bad weeks": some accounts get spikes
    spiky_accounts = set(random.sample(range(1, CASE2_ACCOUNTS + 1), k=int(CASE2_ACCOUNTS * 0.1)))

    for _ in range(CASE2_TICKETS):
        aid = random.randint(1, CASE2_ACCOUNTS)
        created = rand_date(START_DATE, END_DATE)
        priority = pick_weighted(priorities, [35, 40, 18, 7])

        # spike: concentrate tickets in last 30 days for spiky accounts
        if aid in spiky_accounts and random.random() < 0.7:
            created = rand_date(END_DATE - timedelta(days=30), END_DATE)

        # close time depends on priority
        base_days = {"low": 10, "medium": 7, "high": 4, "urgent": 2}[priority]
        closed = created + timedelta(days=max(0, int(random.gauss(base_days, 2))))
        if closed > END_DATE or random.random() < 0.25:
            status = pick_weighted(["open", "pending"], [60, 40])
            closed_at = ""
        else:
            status = pick_weighted(["solved", "closed"], [60, 40])
            closed_at = iso_date(closed)

        tickets.append([ticket_id, aid, iso_date(created), status, priority, closed_at])

        # ticket event history
        # pick an actor from that account
        actor = random.choice(users_by_account[aid])
        te_count = random.randint(2, CASE2_TICKET_EVENTS_MAX)
        t_start = datetime.combine(created, datetime.min.time()) + timedelta(hours=random.randint(0, 12))

        current = "open"
        for i in range(te_count):
            # step forward in time
            t_ts = t_start + timedelta(hours=random.randint(1, 36) * i)
            if i == te_count - 1 and closed_at:
                new_status = "closed"
            else:
                new_status = pick_weighted(ticket_statuses, [35, 30, 20, 15])
            current = new_status
            ticket_events.append([ticket_id, iso_dt(t_ts), current, actor])

        ticket_id += 1

    # Write CSVs
    ensure_dir(OUT_DIR)
    write_csv(f"{OUT_DIR}/case2_accounts.csv",
              ["account_id", "name", "created_at", "tier"], accounts)

    write_csv(f"{OUT_DIR}/case2_app_users.csv",
              ["user_id", "account_id", "created_at", "role"], users)

    write_csv(f"{OUT_DIR}/case2_events.csv",
              ["event_id", "user_id", "event_ts", "event_type", "page", "session_id", "properties_jsonb"], events)

    write_csv(f"{OUT_DIR}/case2_tickets.csv",
              ["ticket_id", "account_id", "created_at", "status", "priority", "closed_at"], tickets)

    write_csv(f"{OUT_DIR}/case2_ticket_events.csv",
              ["ticket_id", "event_ts", "new_status", "actor_user_id"], ticket_events)


def main():
    ensure_dir(OUT_DIR)
    gen_case1()
    gen_case2()
    print(f"✅ Generated CSVs in ./{OUT_DIR}/")
    print("Next: docker compose up -d  (or build the image)")

if __name__ == "__main__":
    main()