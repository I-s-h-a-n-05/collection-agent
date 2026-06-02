# templates/messages.py

TEMPLATES = {
    "pre_7": {
        "email": {
            "subject": "Payment Reminder: {currency} {amount_due} due in 7 days",
            "body": (
                "Dear {customer_name},\n\n"
                "This is a friendly reminder that a payment of {currency} {amount_due} "
                "is due on {due_date} (7 days from now).\n\n"
                "Please ensure funds are arranged in advance to avoid any late charges.\n\n"
                "If you have already processed this payment, please disregard this message.\n\n"
                "Regards,\nCollections Team"
            ),
        },
        "whatsapp": (
            "Hi {customer_name}! 👋 Friendly reminder: your payment of "
            "{currency} {amount_due} is due on {due_date} (7 days). "
            "Please plan ahead. Reply if you need help."
        ),
    },
    "pre_3": {
        "email": {
            "subject": "Payment Due in 3 Days: {currency} {amount_due}",
            "body": (
                "Dear {customer_name},\n\n"
                "Your payment of {currency} {amount_due} is due in 3 days on {due_date}.\n\n"
                "Please initiate the transfer at your earliest convenience.\n\n"
                "Regards,\nCollections Team"
            ),
        },
        "whatsapp": (
            "Hi {customer_name}, just 3 days left! Payment of {currency} {amount_due} "
            "due on {due_date}. Please process soon. 🙏"
        ),
    },
    "pre_1": {
        "email": {
            "subject": "REMINDER: Payment Due Tomorrow — {currency} {amount_due}",
            "body": (
                "Dear {customer_name},\n\n"
                "Your payment of {currency} {amount_due} is due tomorrow ({due_date}).\n\n"
                "Please ensure the payment is processed today to avoid overdue charges.\n\n"
                "Regards,\nCollections Team"
            ),
        },
        "whatsapp": (
            "⚠️ Hi {customer_name}, your payment of {currency} {amount_due} is due "
            "tomorrow ({due_date}). Please pay today to avoid delays."
        ),
    },
    "post_1": {
        "email": {
            "subject": "Payment Overdue by 1 Day: {currency} {amount_due}",
            "body": (
                "Dear {customer_name},\n\n"
                "Your payment of {currency} {amount_due} was due on {due_date} and "
                "remains unpaid.\n\n"
                "Please process this immediately to avoid further escalation.\n\n"
                "Regards,\nCollections Team"
            ),
        },
        "whatsapp": (
            "Hi {customer_name}, your payment of {currency} {amount_due} was due "
            "on {due_date} and is now overdue. Please pay immediately. ⚠️"
        ),
    },
    "post_7": {
        "email": {
            "subject": "OVERDUE 7 Days: Immediate Payment Required — {currency} {amount_due}",
            "body": (
                "Dear {customer_name},\n\n"
                "Your payment of {currency} {amount_due} (due {due_date}) is now 7 days overdue.\n\n"
                "We request you to make this payment immediately. Continued non-payment "
                "may result in account restrictions.\n\n"
                "Regards,\nCollections Team"
            ),
        },
        "whatsapp": (
            "🔴 {customer_name}, your payment of {currency} {amount_due} is 7 days overdue "
            "(was due {due_date}). Immediate payment required. Please respond."
        ),
    },
    "post_15": {
        "email": {
            "subject": "URGENT: 15-Day Overdue — {currency} {amount_due}",
            "body": (
                "Dear {customer_name},\n\n"
                "Despite previous reminders, your payment of {currency} {amount_due} "
                "(due {due_date}) remains outstanding for 15 days.\n\n"
                "This is a serious matter. Please contact us within 48 hours or "
                "your account may be referred to our collections department.\n\n"
                "Regards,\nCollections Team"
            ),
        },
        "whatsapp": (
            "🚨 URGENT {customer_name}: {currency} {amount_due} is 15 days overdue "
            "(due {due_date}). Contact us within 48 hrs to avoid escalation."
        ),
    },
    "post_30": {
        "email": {
            "subject": "FINAL NOTICE: Payment Escalation — {currency} {amount_due}",
            "body": (
                "Dear {customer_name},\n\n"
                "Your account has been flagged for escalation. Payment of "
                "{currency} {amount_due} (due {due_date}) is now 30+ days overdue.\n\n"
                "This matter will be escalated to senior management and may affect "
                "your credit standing. Immediate action is required.\n\n"
                "Regards,\nCollections Team"
            ),
        },
        "whatsapp": (
            "🚨 FINAL NOTICE {customer_name}: {currency} {amount_due} overdue 30+ days. "
            "Escalating to management. Call us NOW to resolve."
        ),
    },
}

def get_template(stage, channel, customer):
    tmpl = TEMPLATES.get(stage, {}).get(channel)
    if not tmpl:
        return None
    data = {
        "customer_name": customer["customer_name"],
        "amount_due":    customer["amount_due"],
        "currency":      customer["currency"],
        "due_date":      customer["due_date"],
    }
    if channel == "email":
        return {
            "subject": tmpl["subject"].format(**data),
            "body":    tmpl["body"].format(**data),
        }
    return tmpl.format(**data)