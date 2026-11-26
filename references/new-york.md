# New York LLC reference

Facts as checked on 2026-11-17 (agent and Certificate of Change section re-checked 2026-11-20, filing methods and expedite fees 2026-11-26). Re-verify fees and forms on dos.ny.gov before filing.

## Public record

- Search: https://apps.dos.ny.gov/publicInquiry/ . Set Search By to Entity Name, tick "Limited Liability Company" in the entity list, then search.
- The entity page shows status, DOS ID, county, statement status, next statement due date, the address for service of process and the registered agent. The **Filing History** tab lists every document filed.
- A domestic LLC's first filing is "Articles of Organization" (LLC Law §203).
- The search page is backed by a JSON API that needs no sign-in (useful from a script):
  - `POST https://apps.dos.ny.gov/PublicInquiryWeb/api/PublicInquiry/GetComplexSearchMatchingEntities` with `{"searchValue":"<NAME>","searchByTypeIndicator":"EntityName","searchExpressionIndicator":"BeginsWith","entityStatusIndicator":"AllStatuses","entityTypeIndicator":["LimitedLiabilityCompany"],"listPaginationInfo":{"listStartRecord":1,"listEndRecord":50}}` returns the DOS ID.
  - `POST .../GetEntityRecordByID` with `{"SearchID":"<DOS ID>","EntityName":"<NAME>","AssumedNameFlag":"false"}` returns status, `sopAddress`, `registeredAgent` and `nextStatementDueDate`.
  - `GetFilingHistoryByID` with the same body returned a server error in Nov 2026; use the Filing History tab in the browser.

## Agent for service of process

- The Secretary of State is every NY LLC's statutory agent for service of process. It forwards papers to the "post office address" on file.
- A separate registered agent is optional in NY. Formation services often put their own name and address on both lines.
- To change either one, file a **Certificate of Change** (LLC Law §211-A). The fee is **$30**.

## Removing a formation service as agent (Certificate of Change, DOS-1359-f)

Use this when a provider (a formation service, LegalZoom and so on) is on the record and won't stop billing until it is off. a formation service told a NY client in Nov 2026 that it cannot turn off auto-renew while it is the registered agent on state records, and will adjust the subscription only once a Certificate of Change is filed and processed. Plan for that with every provider.

1. Read the record: note whether the provider is on the **service of process (SOP) address**, the **registered agent** line, or both. Formation services usually fill both.
2. Pick the new SOP address with the owner. NY needs no registered agent, so the cheapest fix is: change the SOP address to the owner (any post office address where they reliably get mail; it does not have to be a staffed street address) and revoke the agent. Trade-off: the address becomes public on the DOS record and is scraped by mailers, so some owners use a mail address or a cheaper commercial agent instead. If they keep an agent, it must have a NY street address (a PO box is not allowed for the agent).
3. Fill form **DOS-1359-f (Rev. 12/22)**, "Certificate of Change of [LLC] under Section 211-A", fillable PDF from https://dos.ny.gov/certificate-change-domestic-limited-liability-companies . It comes with the cover sheet DOS-2183-f. Fields:
   - FIRST: exact LLC name. SECOND: the filing date of the articles, exactly as on the record (the filing receipt's FILE DATE).
   - THIRD, tick "The post office address to which the Secretary of State shall mail a copy of any process ... is changed to read in its entirety as follows:" and write the new name/address (for example "The LLC, c/o Owner, street, city, NY zip").
   - THIRD, tick "The limited liability company hereby revokes the designation of its registered agent." (Or tick "changes the designation of its registered agent to:" and give the new agent's name and NY street address.)
   - Leave the county and email-service lines unless they change.
   - Signature by a member, manager or authorized person, with the capacity box ticked; then the filer's name and mailing address block, and the cover sheet's contact email (the filing receipt is emailed there).
   - PDF field names (for prefilling with pypdf): `Date1`, `Check Box2` + `Process Address` (SOP), `Check Box7` + `Changes  designation of registered agent to` (new agent), `Check Box9` (revoke agent), `Type or print name`, radio `Group2` (`/Choice1` member, `/Choice2` manager, `/Choice3` authorized person).
4. File and pay (re-checked on dos.ny.gov 2026-11-26). There is still **no online filing** for this certificate (online filing covers name-only amendments and the biennial statement). Two ways to send it:
   - **Fax (fastest, no stamps or checks):** DOS accepts documents for filing by fax at **(518) 474-1418** (https://dos.ny.gov/faxed-filingsother-service-requests). Fax filings must be paid by card on the **Credit Card/Debit Card Authorization, DOS-1515-f (Rev. 04/25)**, https://dos.ny.gov/system/files/documents/2025/07/1515-f-07-2025-update.pdf . Send the cover sheet, the certificate and the card form as one fax, **once only** (a resend can be filed and charged twice, and DOS won't confirm receipt by phone). The filing receipt goes to the cover sheet's email; anything else comes back by first-class mail.
   - **Mail:** to NYS Department of State, Division of Corporations, One Commerce Plaza, 99 Washington Avenue, Albany, NY 12231, with a check or money order payable to "Department of State", or the DOS-1515-f card form.
   - Fee **$30**. Optional expediting per document: $25 (24 hours), $75 (same day, received by 12 noon), $150 (2 hours, received by 2:30 PM), business days only, non-refundable even if the filing is rejected. Tick the level on DOS-1515-f (or pay it by a separate check); on mail, write "Expedited Processing" on the envelope. $30 + $25 = $55 is the usual "about $50" owners remember.
   - DOS-1515-f field names (pypdf): `Name of Corporation or Business Entity`, `FDC` (filing of document, `/Yes`), `FDC$1` (fee), `FDC-No` / `FDC-$25` / `FDC-$75` / `FDC-$150` (processing), `FDC$2` (expedite fee), `TOTAL`, `Email Address`. Card number, expiry, name on card, billing address, signature and date are the owner's to fill: never prefill them.
   - The signature on the certificate can be a drawn signature on the PDF (for example macOS Preview, Markup, Sign) when it is faxed; print and sign by hand for mail.
   - DOS is closed on state holidays (Thanksgiving and the Friday after it are both state holidays), so expedited clocks start the next business day.
5. Confirm it appears in Filing History and the entity page shows the new SOP address and no agent.
6. Send the provider the filing receipt from the owner's email (owner approves the text first), asking it to cancel the registered agent service and its auto-renew. Then check the next invoice.
7. Deadline: aim to file at least 8 weeks before the provider's renewal date.

A provider can also resign as agent on its own (Certificate of Resignation, LLC Law §302), but that is the provider's filing and leaves the SOP address pointing at it; don't rely on it.

## Deadlines after formation

| What | When | Basis | Fee | Notes |
|---|---|---|---|---|
| Operating agreement | Within 90 days of filing the articles | LLC Law §417 | none | Written agreement kept by the members. Not filed with the state. |
| Publication | Notices run once a week for 6 weeks in two newspapers (one daily, one weekly) named by the county clerk. The Certificate of Publication is due within 120 days of formation. | LLC Law §206 | $50 state filing fee plus newspaper costs, which vary by county ($1,000+ in New York County) | A late filing suspends the LLC's authority to do business until it is filed. The LLC still exists. Check Filing History for "Certificate of Publication". |
| Biennial statement | Every 2 years, in the calendar month of formation | LLC Law §301 | $9 | Filed online. The entity page shows "Next statement due date". |

## Taxes (confirm classification first)

- A NY LLC treated as a partnership, or a disregarded entity with NY-source income, may owe the annual LLC filing fee on Form IT-204-LL. The amount is based on NY-source gross income.
- An LLC taxed as an S or C corporation files corporate returns instead.
- Do not put tax dates on the calendar until the owner confirms how the LLC is taxed.

## Useful contacts

- NY DOS Division of Corporations: (518) 473-2492, Mon to Fri 8:45 AM to 4:30 PM ET.
