# Cash Accounting Automation — Small Business Treasury Workflow

## Problem

Small businesses with significant revenue ($250K+ annually) often handle 
bookkeeping manually — a time-consuming process prone to errors and with 
high opportunity cost. This project automates the cash accounting workflow 
for a real US-based small business operating on a cash accounting basis 
(transactions recorded when cash moves).

**Before this project:**
- Owner processed bank statements manually, transaction by transaction, from memory
- Full yearly reconciliation took 3–4 weeks
- No structured visibility on cash flow (what goes where and when)
- Data then transmitted to CPA for tax filing

---

## Solution

A local, privacy-first automated pipeline that transforms raw bank statements 
into categorized, verified financial data — without sending sensitive data 
to external cloud services.

**PDF bank statement → Local LLM → JSON → Python categorization 
→ Excel → Power BI dashboard**

---

## Workflow

### Step 1 — PDF to JSON (Local LLM)
Bank statements are processed by a local LLM (Qwen 8B) hosted via 
LM Studio on a local server, accessible via AnythingLLM on a separate 
device. The LLM structures each transaction into a standardized JSON format:
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

**Why local?** All financial data stays on-premise. 
No sensitive data transmitted to external APIs.

### Step 2 — First Checkpoint
Before proceeding:
- Total amount in bank statement = Total amount in Excel ✓
- Row count in bank statement = Row count in Excel ✓

If both checks pass → proceed. If not → identify and fix the discrepancy.

### Step 3 — Excel Data Reference
A structured Excel reference file maps keywords to categories.
Each column header = one category. Each value in the column = 
a keyword to find in the transaction description.

**Advantages over hardcoded Python lists:**
- Flexible — add/modify keywords without touching code
- Visual — conditional formatting highlights duplicates instantly
- Readable — 100+ terms manageable in a spreadsheet, not in a script
- Ordered — left-to-right priority handles recurring keyword conflicts

### Step 4 — Python Categorization Script
The script cross-references each transaction description against 
the Excel reference file and adds two columns:

- `Keyword_Source` — which keyword triggered the category
- `In/Out` — cash inflow or outflow

### Step 5 — Final Checkpoints
- Uncategorized transactions flagged automatically (6% average on last full year)
- Total amount verified again
- Row count verified again

### Step 6 — Power BI Dashboard
Structured data loaded into Power BI for visual cash flow analysis:
- Monthly breakdown by category
- Inflow vs outflow tracking
- Trend visualization across accounts

---

## Results

| Metric | Before | After |
|--------|--------|-------|
| Processing time (full year) | 3–4 weeks | 8–15 hours |
| Transactions processed | ~1,800/year | ~1,800/year |
| Uncategorized rate | Variable/unknown | ~6% (flagged automatically) |
| Data loss risk | Manual, unverified | 3 automated checkpoints |
| Cash flow visibility | None | Real-time Power BI dashboard |

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Qwen 8B (local) | PDF to JSON structuring |
| LM Studio | Local LLM hosting |
| AnythingLLM | Local LLM interface |
| Python | Categorization script |
| Excel + Power Query | Data reference + loading |
| Power BI | Dashboard visualization |

---

## Iteration History

**V1 — Pure Python**
Keyword lists hardcoded directly in the script.

Issues encountered:
- Inflexible — adding keywords required modifying code
- No duplicate detection
- No checkpoints
- Poor readability at 100+ terms
- Difficult to audit or improve without strong Python knowledge

**V2 — Current System**
Keyword management moved to Excel reference file.
Local LLM replaces manual PDF parsing.
Three automated checkpoints added throughout the pipeline.

---

## Known Limitations & Next Steps

- LLM processing time: 10–15 min per bank statement 
  (optimization in progress)
- 6% uncategorized transaction rate on edge cases 
  (manual review required)
- Process repeated 24 times per year (2 accounts × 12 months) 
  — partial automation of this loop under exploration

---

## Data & Privacy

All data used in this project belongs to a real US-based small business.
Raw financial data is excluded from this repository (.gitignore).
Only anonymized examples and code logic are shared publicly.

---

## Status

✅ Year 1 complete — fully processed and verified  
✅ Year 2 complete  
✅ Year 3 complete  
🔄 Optimization in progress
