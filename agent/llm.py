# agent/llm.py
from httpx import _content
import os
import httpx
from dotenv import load_dotenv
from templates.messages import get_template

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL     = "https://api.groq.com/openai/v1/chat/completions"
MODEL        = "llama-3.3-70b-versatile"

STAGE_CONTEXT = {
    "pre_7":  "7 days before payment is due",
    "pre_3":  "3 days before payment is due",
    "pre_1":  "1 day before (or today if delta=0) payment is due",
    "post_1": "1 day overdue",
    "post_7": "7 days overdue",
    "post_15":"15 days overdue — serious",
    "post_30":"30+ days overdue — escalation",
}

TONE_BY_RISK = {
    "low":    "warm and friendly",
    "medium": "professional and firm",
    "high":   "urgent and direct",
}

def _build_prompt(customer, stage, days_delta, channel):
    stage_desc = STAGE_CONTEXT.get(stage, stage)
    tone       = TONE_BY_RISK.get(customer.get("risk_tier", "low"), "professional")
    length     = "150–200 words, formal" if channel == "email" else "50–80 words, conversational"

    return (
        f"Generate a payment {channel} message for a collections agent.\n\n"
        f"Customer: {customer['customer_name']}\n"
        f"Amount due: {customer['currency']} {customer['amount_due']}\n"
        f"Due date: {customer['due_date']}\n"
        f"Days delta: {days_delta:+d} (negative = before due, positive = overdue)\n"
        f"Stage: {stage_desc}\n"
        f"Risk tier: {customer.get('risk_tier', 'low')}\n"
        f"Tone: {tone}\n"
        f"Channel: {channel} — keep it {length}\n\n"
        + (
            "Return ONLY in this exact format, nothing else:\nSUBJECT: <subject line here>\nBODY: <full message body here>"
            if channel == "email"
            else "Return ONLY the message text. No subject line, no markdown, no extra text."
        )
    )

def generate_message(customer, stage, days_delta, channel):
    if not GROQ_API_KEY:
        print("[LLM] No API key — using template fallback.")
        return get_template(stage, channel, customer)

    try:
        response = httpx.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type":  "application/json",
            },
            json={
                "model":       MODEL,
                "max_tokens":  512,
                "temperature": 0.4,
                "messages": [
                    {
                        "role":    "system",
                        "content": (
                            "You are a professional collections assistant. "
                            "Follow instructions exactly. Return only what is asked, "
                            "no preamble, no extra text."
                            "Sign off all messages as: Collections Team, Insignytics."
                            
                        ),
                    },
                    {
                        "role":    "user",
                        "content": _build_prompt(customer, stage, days_delta, channel),
                    },
                ],
            },
            timeout=15.0,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"].strip()

        if channel == "email":
            subject, body = "", content
            for line in content.splitlines():
                if line.startswith("SUBJECT:"):
                    subject = line.replace("SUBJECT:", "").strip()
                elif line.startswith("BODY:"):
                    body = content[content.find("BODY:") + 5:].strip()
                    break
            return {"subject": subject, "body": body}
        return content

    except Exception as e:
        print(f"[LLM] API error: {e} — falling back to template.")
        return get_template(stage, channel, customer)