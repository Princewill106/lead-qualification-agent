"""Lead Qualification Agent (BANT)."""
import argparse
import csv
import json
import re
from pathlib import Path

import llm

MIN_BUDGET = 300_000
SENIOR = ["ceo", "founder", "director", "owner", "head of", "md", "manager", "principal", "proprietor"]
NEED = ["automate", "automation", "chatbot", "training", "workflow", "ai", "crm", "save time", "whatsapp"]
URGENT = ["asap", "urgent", "this week", "this month", "immediately", "next week"]
LATER = ["next year", "someday", "just browsing", "maybe later", "no rush"]


def parse_budget(text: str):
    best = 0
    for m in re.finditer(r"(?:ngn|₦)?\s?(\d[\d,.]*)\s?(k|m|million)?\b", text.lower()):
        n = float(m.group(1).replace(",", ""))
        unit = m.group(2)
        n *= 1_000 if unit == "k" else 1_000_000 if unit in ("m", "million") else 1
        best = max(best, n)
    return best or None


def score(lead: dict) -> dict:
    t = lead["message"].lower()
    reasons, s = {}, {}
    budget = parse_budget(lead["message"])
    s["budget"] = 25 if budget and budget >= MIN_BUDGET else 10 if budget else 5
    reasons["budget"] = f"NGN {budget:,.0f}" if budget else "not stated"
    senior = next((w for w in SENIOR if w in t), None)
    s["authority"] = 25 if senior else 8
    reasons["authority"] = senior or "role unclear"
    needs = [w for w in NEED if re.search(r"\b" + w + r"\b", t)]
    s["need"] = min(25, 10 * len(needs))
    reasons["need"] = ", ".join(needs) or "no clear need"
    if any(w in t for w in URGENT):
        s["timeline"], reasons["timeline"] = 25, "urgent"
    elif any(w in t for w in LATER):
        s["timeline"], reasons["timeline"] = 0, "not soon"
    else:
        s["timeline"], reasons["timeline"] = 12, "unspecified"
    total = sum(s.values())
    tier = "HOT" if total >= 70 else "WARM" if total >= 45 else "COLD"
    return {**lead, "scores": s, "reasons": reasons, "total": total, "tier": tier}


def first_reply(lead: dict) -> str:
    name = lead["name"].split()[0]
    templates = {
        "HOT": f"Hi {name}, thanks for reaching out. I can help with this. Are you free for a 20-minute call today or tomorrow?",
        "WARM": f"Hi {name}, thanks for your message. Could you share a bit more about your timeline and the process you want to automate?",
        "COLD": f"Hi {name}, thanks for getting in touch! Here's a short guide on where AI automation saves businesses time. Happy to chat whenever you're ready.",
    }
    better = llm.complete(f"Improve this sales reply, keep it under 40 words: {templates[lead['tier']]}"
                          f"\nLead said: {lead['message']}")
    return (better or templates[lead["tier"]]).strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", default="sample_leads.json")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    leads = [score(l) for l in json.loads(Path(a.input).read_text())]
    leads.sort(key=lambda l: -l["total"])
    Path("output").mkdir(exist_ok=True)
    with open("output/scored_leads.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["name", "source", "tier", "total", "budget", "authority", "need", "timeline"])
        for l in leads:
            w.writerow([l["name"], l["source"], l["tier"], l["total"]] + [l["reasons"][k] for k in
                       ("budget", "authority", "need", "timeline")])
    for l in leads:
        print(f"{l['tier']:<5} {l['total']:>3}  {l['name']:<18} ({l['source']})")
        print(f"      {l['reasons']}")
        print(f"      reply: {first_reply(l)}\n")
    print("Saved output/scored_leads.csv")


if __name__ == "__main__":
    main()
