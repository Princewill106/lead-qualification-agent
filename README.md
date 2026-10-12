# Lead Qualification Agent

> Score every inbound lead on budget, authority, need and timing, then route it before it goes cold.

![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Offline demo](https://img.shields.io/badge/demo-runs%20offline-brightgreen) ![n8n](https://img.shields.io/badge/n8n-importable%20workflow-EA4B71) ![n8n](https://img.shields.io/badge/n8n-importable%20workflow-EA4B71) ![Series](https://img.shields.io/badge/AI%20Automation-9%2F50-purple)

**Sector:** Sales & Marketing  ·  **Project 9 of 50** in my [AI Automation Projects series](https://github.com/Princewill106/Princewill106)

## The problem

Sales teams waste their best hours on enquiries that were never going to buy, while the hot lead who asked for a quote on Friday night hears back on Tuesday. Speed to lead matters more than almost anything else in conversion.

## How it works

```mermaid
flowchart LR
    S0["New lead"]
    S1["Extract signals"]
    S2["BANT score"]
    S3["Hot / warm / cold"]
    S4["Route + message"]
    S0 --> S1
    S1 --> S2
    S2 --> S3
    S3 --> S4
```

1. **Capture** — Leads arrive from any channel with free-text messages (`sample_leads.json`).
2. **Extract** — Budget figures, role/title, need keywords and timeline words are pulled from the text.
3. **Score** — Each BANT dimension scores 0–25 for a 0–100 total, with the reason for each score.
4. **Route** — Hot (70+) goes to sales immediately with a one-line summary; warm gets a follow-up within 48 hours; cold enters a nurture sequence.
5. **Message** — A first reply is drafted for every lead so nobody waits.

## Features

- BANT scoring with explanations
- Budget parsing (500k, 2m, NGN 1,500,000)
- Seniority detection from titles
- Urgency detection
- Drafted first replies per tier
- CSV export for your CRM

## Quick start

```bash
git clone https://github.com/Princewill106/lead-qualification-agent.git
cd lead-qualification-agent
python main.py --demo
```

No installs needed: it uses only the Python standard library. The demo runs fully offline using the sample data in this repo.

**Optional: plug in an LLM.** Copy `.env.example` to `.env` and add an Anthropic or OpenAI key. The project will then use the model for the language-heavy steps and fall back to its rule-based logic if a call fails.

Run the tests:

```bash
python -m unittest -v
```

## Sample output

```text
HOT   100  Samuel Okon        (whatsapp)
      {'budget': 'NGN 800,000', 'authority': 'head of', 'need': 'training, workflow, ai', 'timeline': 'urgent'}
      reply: Hi Samuel, thanks for reaching out. I can help with this. Are you free for a 20-minute call today or tomorrow?

HOT    95  Bola Adeniran      (website)
      {'budget': 'NGN 1,500,000', 'authority': 'founder', 'need': 'automate, whatsapp', 'timeline': 'urgent'}
      reply: Hi Bola, thanks for reaching out. I can help with this. Are you free for a 20-minute call today or tomorrow?

WARM   55  Daniel Ojo         (linkedin)
      {'budget': 'NGN 200,000', 'authority': 'manager', 'need': 'automation, crm', 'timeline': 'not soon'}
      reply: Hi Daniel, thanks for your message. Could you share a bit more about your timeline and the process you want to automate?

COLD   35  Halima Yusuf       (website)
      {'budget': 'not stated', 'authority': 'role unclear', 'need': 'chatbot', 'timeline': 'unspecified'}
      reply: Hi Halima, thanks for getting in touch! Here's a short guide on where AI automation saves businesses time. Happy to chat whenever you're ready.

COLD   33  Ifeoma Chukwu      (instagram)
      {'budget': 'not stated', 'authority': 'role unclear', 'need': 'training, ai', 'timeline': 'not soon'}
      reply: Hi Ifeoma, thanks for getting in touch! Here's a short guide on where AI automation saves businesses time. Happy to chat whenever you're ready.

Saved output/scored_leads.csv
```

## Use it in n8n (no code needed)

[`n8n-workflow.json`](n8n-workflow.json) is a ready-to-import n8n version of this project, built for n8n 1.x.

1. In n8n, open **Workflows → Import from File** and choose `n8n-workflow.json`.
2. Click **Test workflow**. It runs the full logic on the sample data built into the *Sample data* node, so you can see the results before connecting anything.
3. Open each output node and connect your accounts: Gmail (OAuth2), Google Sheets (OAuth2), Slack. For Google Sheets, pick your spreadsheet and sheet.
4. Adjust the settings at the top of the **Logic** node (thresholds, templates, contacts), then **Activate**.

**Flow:** **n8n Form** → **Logic** (Code node) → **Route** (Switch)

**Outputs:**
- Ping me: hot lead (Slack)
- Email hot lead
- Email warm lead
- Add cold lead to nurture sheet

The Logic node is a JavaScript port of the rules in `main.py`, so you can run the project in n8n without Python.

## Use it on your own data

Point `--input` at a JSON list of leads with `name`, `source` and `message`. Adjust `MIN_BUDGET` and keyword lists in `main.py` to your offer. Import `output/scored_leads.csv` into your CRM.

## Project structure

```text
n8n-workflow.json            Importable n8n workflow
.env.example                 Optional API key settings
.gitignore                   Git ignore rules
LICENSE                      MIT license
README.md                    This file
llm.py                       Optional LLM helper (offline fallback)
main.py                      Entry point and core logic
requirements.txt             Dependencies (stdlib only)
sample_leads.json            Sample input data for the demo
test_main.py                 Unit tests
```

## Who this is for

- Agencies and consultants
- Real estate teams
- Training providers selling cohorts

## Ideas to extend it

- [ ] Push hot leads to Slack/WhatsApp instantly
- [ ] HubSpot/Zoho CRM sync
- [ ] Learn weights from closed-won data
- [ ] Calendar link for hot leads

## About

Built by **Ogbu Ugochukwu Princewill**, AI Automation Lead and robotics engineer. I teach people and businesses to build with AI, not just talk about it. [LinkedIn](https://www.linkedin.com/in/ugochukwu-ogbu-653a0816a)

If this helped you, give it a ⭐ and share what you built with it.

## License

MIT — see [LICENSE](LICENSE).
