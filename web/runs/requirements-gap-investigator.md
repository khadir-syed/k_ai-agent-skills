Date: 2026-09-26
Tool: Codex CLI 0.154.0
Model: gpt-5.6-sol
Example: skills/product/requirements-gap-investigator/examples/vague-export-request.md

## Investigation status

**Gaps identified — not clear enough to draft requirements.**

The request establishes demand for some form of export, but not the user problem, scope, output, access model, supported platforms, or measurable outcome.

## Request framing

| Item | Evidence status | Finding |
|---|---|---|
| Request | **Stated** | Sales lead: “Can we get an export on the reports page? Customers keep asking.” |
| Ticket scope | **Stated** | PM: “Export button for reports page.” |
| Requester | **Stated** | Sales initiated the request. |
| Customer demand | **Reported** | Sales says customers are asking, but no customer examples, volume, use cases, or source conversations are available. |
| Problem being solved | **Unknown** | It is unclear what customers need exported or what they intend to do with it. |
| Deadline or dependency | **Unknown** | None is mentioned. |
| Other stakeholders | **Unknown** | No report owner, security/compliance owner, mobile owner, or affected customer segment is identified. |

## Gaps and unresolved questions

| Area | Evidence status | What must be established |
|---|---|---|
| Export subject | **Unknown** | Current report, selected rows, filtered results, chart, underlying records, every report, or a bulk export? |
| Reports covered | **Unknown** | One specific report, a report type, or the entire reports page? |
| Customer use case | **Unknown** | Offline analysis, sharing, audit evidence, importing elsewhere, printing, or data backup? |
| File format | **Unknown** | CSV, XLSX, PDF, image, or another format? |
| Applied state | **Unknown** | Whether filters, sorting, date range, visible columns, grouping, and timezone affect the export. |
| Permissions | **Unknown** | Whether export follows view permissions or requires a separate permission; whether sensitive fields must be omitted. |
| Data volume | **Unknown** | Typical and maximum row counts, synchronous versus background generation, timeout behavior, and file-size limits. |
| Platform | **Unknown** | Web only, mobile web, or native mobile apps. |
| Delivery behavior | **Unknown** | Immediate download, emailed link, notification, or export history. |
| Edge cases | **Unknown** | Empty reports, partially available data, failed exports, concurrent requests, and stale data. |
| Security/compliance | **Unknown** | Audit logging, retention, download-link expiry, data residency, spreadsheet-injection protection, or regulated-data restrictions. |
| Existing behavior | **Unknown** | Whether another export mechanism exists and would be supplemented or replaced. |
| Success criteria | **Unknown** | No adoption, completion, reliability, performance, or customer-outcome measure is defined. |
| Explicit exclusions | **Unknown** | Nothing has been declared out of scope. |

## Plausible interpretations

1. **Export the currently displayed table**

   - **Supporting evidence:** **Inferred** from “button on the reports page.”
   - Must confirm: whether the export reflects current filters, sorting, columns, pagination, and permissions.

2. **Download a presentation-ready report**

   - **Supporting evidence:** **Inferred** from the word “report.”
   - Must confirm: PDF versus image, inclusion of charts and branding, and whether the output must match the screen.

3. **Extract underlying data for further analysis**

   - **Supporting evidence:** **Inferred** from common customer export workflows; no supplied evidence confirms it.
   - Must confirm: CSV/XLSX format, raw versus aggregated data, field definitions, volume limits, and sensitive-data controls.

4. **Export multiple reports or a complete reporting dataset**

   - **Supporting evidence:** **Inferred** from the plural “reports page.”
   - Must confirm: selection behavior, packaging, asynchronous processing, and scale constraints.

These interpretations have materially different security, performance, and implementation implications, so none should be selected silently.

## Confirm before drafting

Ask the **Sales lead**:

- Which customers asked, and what were they trying to accomplish after exporting?
- Can they provide two or three representative customer statements or examples?
- Is this connected to a sale, renewal, commitment, or deadline?

Ask the **PM/report owner**:

- Which report or reports are in scope?
- Should the export represent the visible presentation or the underlying data?
- Which formats and platforms are required?
- What is explicitly out of scope, and how will success be measured?

Confirm with the **security/data owner**:

- Whether existing view permissions are sufficient for downloads.
- Whether sensitive fields, auditing, retention, or regulatory controls apply.

Confirm with the **engineering/reporting owner**:

- Expected data volumes, generation limits, existing export infrastructure, and failure-handling constraints.

No PRD, specification, user story, or product decision has been drafted.