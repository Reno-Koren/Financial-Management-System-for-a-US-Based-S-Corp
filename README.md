# Cash Accounting Automation — Small Business Treasury Workflow

## Context

This project automates the full cash accounting workflow for a real 
US-based small business — a service and merchandise company generating 
~$250K in annual revenue. The business operates on a cash accounting 
basis: transactions are recorded when cash actually moves.

The goal was simple: the owner was spending 3 to 4 weeks per year 
processing bank statements manually, transaction by transaction, from 
memory. That time had a real opportunity cost. The objective was to 
bring that down while improving accuracy, auditability, and financial 
visibility.

---

## What the pipeline does

Takes raw PDF bank statements as input and produces:
- Categorized and verified transaction data in Excel
- A chart of accounts mapping ready for CPA transmission
- Monthly reporting on cash flow by category
- Visual dashboards on inflows, outflows and trends

**PDF bank statements → Local LLM → JSON → Python 
→ Excel + Reference file → Accounts mapping → Reporting**

---

## Why local

All financial data stays on a local server. Nothing is sent to 
external APIs. The LLM (Qwen 8B) runs via LM Studio on a local 
desktop and is accessible from a laptop via AnythingLLM — both 
on the same private network.

---

## Workflow

### Step 1 — PDF to JSON
The LLM reads each bank statement and structures every transaction 
into a standardized JSON format:
```json
{
  "Date": "",
  "Month": "",
  "Description": "",
  "Amount": "",
  "Account": "",
  "Category": ""
}
```

Processing time is roughly 10 to 15 minutes per statement. 
Slower than a pure script, but meaningfully more accurate on 
messy or inconsistent transaction descriptions.

### Step 2 — First checkpoint
Before moving forward:
- Total amount in JSON = Total amount on bank statement ✓
- Row count in JSON = Row count on bank statement ✓

If both pass, continue. If not, find and fix the discrepancy first.

### Step 3 — Excel reference file
Categorization is driven by a dedicated Excel reference file — 
not hardcoded lists in the script.

Structure: each column header is a category name. 
Each value in that column is a keyword to look for 
in the transaction description.

This replaced the original hardcoded Python approach for 
three practical reasons: easier to update without touching code, 
readable at 100+ terms, and conditional formatting instantly 
flags duplicate keywords across categories.

Column order matters: Python reads left to right, so less frequent 
categories whose keywords overlap with common ones are placed further 
left to ensure correct matching priority.

### Step 4 — Python categorization
The script cross-references each transaction description against 
the reference file and adds two columns:

- `Keyword_Source` — which keyword triggered the match
- `In/Out` — inflow or outflow

### Step 5 — Second checkpoint
- Any uncategorized transaction is flagged automatically
- Total amount verified again
- Row count verified again

Average uncategorized rate on last full year: ~6%. 
These are reviewed manually before proceeding.

This process runs 24 times per year — 2 bank accounts × 12 months.

### Step 6 — Chart of accounts mapping
Categories are mapped to a standard US chart of accounts structure, 
built by reverse-engineering the company's 2024 tax declaration — 
the same structure the CPA already works with.

Example: Software, Freight and Shipping → mapped under Utilities.

This step produces a file the CPA can work with directly, 
without reformatting or interpretation.

### Step 7 — Reporting
*(In progress — to be documented)*

Monthly reporting by category — Excel pivot tables and Power BI 
dashboards covering inflows, outflows and category trends across 
the full year.

---

## Results

| Metric | Before | After |
|--------|--------|-------|
| Processing time (full year) | 3–4 weeks | 8–15 hours |
| Transactions per year | ~1,800 | ~1,800 |
| Uncategorized rate | Unknown | ~6% flagged automatically |
| Checkpoints | None | 3 automated verification steps |
| CPA-ready output | Manual reformatting | Direct mapping to existing chart of accounts |
| Cash flow visibility | None | Monthly reporting + dashboards |

---

## Tech stack

| Tool | Role |
|------|------|
| Qwen 8B | PDF to JSON structuring |
| LM Studio | Local LLM hosting |
| AnythingLLM | Local LLM interface |
| Python | Categorization script |
| Excel + Power Query | Reference file + data loading |
| Power BI | Dashboard visualization |

---

## How this evolved

The first version used hardcoded keyword lists directly in the 
Python script. It worked but created real problems quickly: 
adding a new keyword meant editing code, duplicate detection 
was impossible, and with 100+ terms the script became unreadable. 
More importantly, I couldn't easily audit or improve something 
I hadn't fully written myself.

Moving keyword management to a separate Excel reference file 
solved all of that. Adding the local LLM replaced a brittle 
manual formatting step with something that handles inconsistent 
bank statement formats without special cases.

---

## Limitations

- LLM processing: 10–15 min per bank statement 
  (speed optimization is the main open question)
- ~6% uncategorized transactions require manual review
- 24 runs per year (2 accounts × 12 months) — 
  loop automation under exploration

---

## Data and privacy

This project was built on real financial data from a US-based 
small business. All raw data is excluded from this repository. 
Only code and anonymized structural examples are shared here.

---

## Status

✅ Full pipeline operational  
✅ 3 years of data processed and verified  
✅ Chart of accounts mapping complete  
🔄 Reporting section in progress  
🔄 LLM processing speed — optimization in progress
