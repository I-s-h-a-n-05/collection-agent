# agent/scanner.py
import csv
import os
from datetime import date, datetime
from agent.logger import is_stage_done

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'customers.csv')

# (stage_id, threshold_days) — negative = before due, positive = overdue
STAGES = [
    ("pre_7",  -7),
    ("pre_3",  -3),
    ("pre_1",  -1),
    ("post_1",  1),
    ("post_7",  7),
    ("post_15", 15),
    ("post_30", 30),
]

def load_customers():
    customers = []
    with open(DATA_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            customers.append(dict(row))
    return customers

def days_delta(due_date_str):
    due = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    return (date.today() - due).days   # negative = before due, positive = overdue

def get_pending_stage(delta, customer_id, invoice_ref):
    # All stages whose threshold has been reached
    applicable = [
        (stage_id, threshold)
        for stage_id, threshold in STAGES
        if delta >= threshold
    ]
    # Walk from most recent → oldest. Return first unsent stage.
    for stage_id, _ in reversed(applicable):
        if not is_stage_done(customer_id, invoice_ref, stage_id):
            return stage_id
    return None

def scan():
    customers = load_customers()
    actions = []
    for customer in customers:
        customer_id  = customer['customer_id']
        due_date     = customer['due_date']
        invoice_ref  = f"{customer_id}_{due_date}"   # synthetic unique key
        delta        = days_delta(due_date)
        stage        = get_pending_stage(delta, customer_id, invoice_ref)
        if stage:
            actions.append({
                "customer":    customer,
                "invoice_ref": invoice_ref,
                "stage":       stage,
                "days_delta":  delta,
            })
    return actions

if __name__ == "__main__":
    results = scan()
    if not results:
        print("[Scanner] No actions needed.")
    else:
        for a in results:
            c = a['customer']
            print(f"  {c['customer_name']:20s} | {a['stage']:8s} | delta={a['days_delta']:+d}d | {c['preferred_channel']}")