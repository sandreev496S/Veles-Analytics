# Veles Fiverr Report Pre-Delivery Checklist

Use this checklist for every client report. A report is not deliverable until all blocking items pass.

## 1. Order scope and identity

- [ ] Client ticker, legal company name, exchange, currency, industry, and requested report type are confirmed.
- [ ] The report date, market-data timestamp, and latest filing date are visible.
- [ ] The company is not confused with a similarly named issuer or foreign listing.
- [ ] The Fiverr package matches the delivered sections and revision scope.

## 2. Data integrity - blocking

- [ ] `validate_report_for_delivery(..., raise_on_error=True)` passes.
- [ ] No unsafe, unresolved, withheld, partial, or period-inconsistent metric appears as a number.
- [ ] Cash, debt, shares, share price, market cap, and enterprise value reconcile.
- [ ] The same metric agrees across the executive summary, dashboard, tables, charts, and valuation.
- [ ] Annual and quarterly periods are not mixed without explicit labeling.
- [ ] Units are consistent: dollars versus thousands, millions, or billions.
- [ ] Negative values, parentheses, percentages, and per-share values are presented correctly.

## 3. Source provenance - blocking

- [ ] Every core financial metric has a source name and period/as-of date.
- [ ] SEC filing form and filing date are shown or retained in the report data where applicable.
- [ ] Derived values are distinguishable from reported values and analyst assumptions.
- [ ] Any provider conflict is resolved, disclosed, or suppressed.
- [ ] No claim cites a source that does not support it.

## 4. Valuation - blocking when included

- [ ] Current share price in valuation matches the dashboard and market-data section.
- [ ] Net cash/debt used in equity-value reconciliation matches the validated balance sheet.
- [ ] Enterprise value plus net cash equals equity value, subject to clearly disclosed adjustments.
- [ ] Equity value divided by diluted shares equals implied value per share.
- [ ] Bull case is greater than or equal to base case, which is greater than or equal to bear case.
- [ ] WACC, terminal growth, forecast horizon, and scenario assumptions are labeled as assumptions.
- [ ] Sensitivity tables move in economically coherent directions.
- [ ] The valuation is labeled illustrative when evidence or assumptions do not support a firm target.

## 5. Narrative quality

- [ ] Every major conclusion is supported by report evidence.
- [ ] The executive summary accurately reflects the detailed sections.
- [ ] Risks are company-specific rather than generic filler.
- [ ] Catalysts include a credible event or decision point and avoid invented dates.
- [ ] The report distinguishes facts, calculations, assumptions, and analyst interpretation.
- [ ] Language is professional, neutral, and free of exaggerated certainty.
- [ ] AI-generated commentary contains no unsupported claims or fabricated citations.

## 6. Visual PDF inspection - blocking

- [ ] Render the PDF to images and inspect every page.
- [ ] No clipped text, overlapping objects, blank pages, black boxes, or broken glyphs.
- [ ] Tables fit within margins and repeat headers when needed.
- [ ] Charts have readable titles, axes, units, periods, and source notes.
- [ ] Figure references point to the correct charts.
- [ ] Table of contents entries and page numbers are correct.
- [ ] Cover information and confidentiality/disclaimer text are present.
- [ ] No internal paths, debug text, fixture labels, or client-private information leak into the report.

## 7. Commercial delivery

- [ ] File name is professional and includes company, report type, and date or version.
- [ ] Final PDF opens successfully on desktop and mobile viewers.
- [ ] Any promised Excel model or source appendix is included.
- [ ] The delivered report contains the agreed package only.
- [ ] The client-facing message states the data cutoff and key limitations.
- [ ] A clean archived copy of inputs, report JSON, PDF, and validation results is retained.

## Mandatory stop conditions

Do not deliver when any of the following is true:

- Reconciliation fails.
- A core metric has no reliable source or period.
- The valuation does not mathematically bridge to per-share value.
- The report contains contradictory values.
- The PDF has visual defects.
- A material claim cannot be supported.
