# agent/scheduler.py
from agent.scanner import scan
from agent.llm import generate_message
from agent.email_sender import send_email
from agent.whatsapp_sender import send_whatsapp
from agent.logger import log_communication, mark_stage_done

def run_collection_cycle():
    print("\n[Agent] ── Starting collection cycle ──")
    actions = scan()

    if not actions:
        print("[Agent] No actions needed. All stages up to date.")
        return

    print(f"[Agent] {len(actions)} action(s) queued.\n")

    for action in actions:
        customer    = action["customer"]
        stage       = action["stage"]
        delta       = action["days_delta"]
        invoice_ref = action["invoice_ref"]
        channel     = customer["preferred_channel"]
        customer_id = customer["customer_id"]

        # 1. Generate message
        message = generate_message(customer, stage, delta, channel)

        # 2. Send
        if channel == "email":
            subject  = message["subject"]
            body     = message["body"]
            ok, err  = send_email(customer["email"], subject, body)
            msg_text = f"Subject: {subject}\n\n{body}"
        else:
            ok, err  = send_whatsapp(customer["phone"], message)
            msg_text = message

        # 3. Log every attempt regardless of outcome
        log_communication(
            customer_id  = customer_id,
            invoice_ref  = invoice_ref,
            stage        = stage,
            channel      = channel,
            status       = "sent" if ok else "failed",
            message_text = msg_text,
            error_detail = err,
        )

        # 4. Only mark done if actually sent — failed stages retry next cycle
        if ok:
            mark_stage_done(customer_id, invoice_ref, stage)
            print(f"  ✓  {customer['customer_name']:20s} | {stage:8s} | {channel}")
        else:
            print(f"  ✗  {customer['customer_name']:20s} | {stage:8s} | {channel} | ERR: {err}")

    print("\n[Agent] ── Cycle complete ──\n")