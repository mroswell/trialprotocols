# trialprotocols.com — COVID-19 Vaccine Trial Protocol Amendment Histories

A compiled, verbatim record of how the protocols for ten pivotal COVID-19 vaccine clinical trials evolved over time — assembled from public sources and presented side-by-side with the source documents.

Live site: **https://trialprotocols.com/**

## Trials covered

| Trial | NCT | Sponsor |
|-------|-----|---------|
| C4591001 | NCT04368728 | Pfizer / BioNTech (pivotal Phase 1/2/3, adults 16+ then 12+) |
| C4591007 | NCT04816643 | Pfizer / BioNTech (pediatric, 6 months to <12 years) |
| C4591015 | NCT04754594 | Pfizer / BioNTech (maternal immunization — terminated Oct 2021) |
| C4591020 | NCT04760132 | Pfizer / BioNTech (Phase 4 healthcare-worker effectiveness) |
| C4591024 | NCT04895982 | Pfizer / BioNTech (immunocompromised ≥2 yr — no primary publication issued) |
| mRNA-1273-P201 | NCT04405076 | ModernaTX (Phase 2 dose-confirmation) |
| mRNA-1273-P301 (COVE) | NCT04470427 | ModernaTX (pivotal Phase 3 efficacy) |
| D8110C00001 | NCT04516746 | AstraZeneca (pivotal Phase 3, AZD1222 / Vaxzevria) |
| ENSEMBLE (VAC31518COV3001) | NCT04505722 | Janssen / J&J (Phase 3, single-dose Ad26.COV2.S) |
| ENSEMBLE 2 (VAC31518COV3009) | NCT04614948 | Janssen / J&J (Phase 3, two-dose Ad26.COV2.S) |

## Sources

Each trial's report cites — and links to — every source PDF used to build it:

- **PHMPT FOIA release** (`phmpt.org`) — five trials (C4591001 partial, C4591007, C4591015, C4591020, Moderna P201).
- **clinicaltrials.gov** — five trials' latest protocol versions (C4591001 Amendment 20, Moderna P301 Amendment 10, AZ Amendment 6, J&J ENSEMBLE Amendment 7, J&J ENSEMBLE 2 Amendment 7).
- **NEJM 2020–2022 protocol supplements** — original baselines and selected amendments for C4591001 (Polack), J&J ENSEMBLE (Sadoff), and AstraZeneca D8110C00001 (Falsey). The site uses `#page=N` deep-links to navigate inside these multi-version supplements.
- **AstraZeneca clinical-trial S3 bucket** (`s3.amazonaws.com/ctr-med-7111`) — AZ Amendments 2 and 4.
- **Wayback Machine snapshots of jnj.com** — J&J ENSEMBLE Amendments 1 and 3, ENSEMBLE 2 Amendment 3.
- **Internet Archive item `covid-19-vaccine-control-group-files`** — Moderna P301 Amendment 6.
- **clinicaltrials.gov via the Wayback Machine** — Pfizer C4591024 (the only retained copy of Amendment 5).

## Methodology

Two PDF parsers, depending on sponsor template:

- **Pfizer-template PDFs** (C4591001, C4591007, C4591015, C4591020) — text-based parsing of the "Protocol Amendment Summary of Changes Table" that prefixes the document. Bullet rationale text is split on the U+F0B7 Wingdings glyph that Pfizer's protocol template uses for bullets.
- **Moderna/AstraZeneca/Janssen/Pfizer-C4591024-template PDFs** — PyMuPDF (`fitz`) table-detection to extract:
  - the front-matter DOCUMENT HISTORY date list,
  - the per-amendment Section / Description / Brief Rationale change-tables,
  - regex parsing of the Appendix N: Protocol Amendment History section for prior-amendment rationale prose.

Both parsers normalize bullet characters (Wingdings U+F0B7, standard U+2022, dingbat variants) into proper HTML `<ul>` lists so cells with multiple sub-points render cleanly.

## Caveats

- Text is extracted from PDFs via PyMuPDF. Multi-column layouts may occasionally misorder or drop a stray character; spot-check any cell that surprises you against the source PDF (every report links to its source).
- NEJM `#page=N` deep-links use the PDF-viewer page number. Some viewers (notably Safari on macOS) ignore the fragment and open at page 1 — scroll to the indicated page if needed.
- C4591024 (Pfizer immunocompromised) is marked "Completed" on ClinicalTrials.gov as of 23 July 2023, but no peer-reviewed primary publication of its results has been issued. The trial enrolled fewer participants than originally targeted before recruitment was stopped.
- C4591015 (Pfizer maternal) was terminated on 25 October 2021 with ~349 of the planned 4,000 participants enrolled, because the placebo-controlled design became unethical once COVID-19 vaccines were universally recommended for pregnant individuals.

## Generator

This repository (`mroswell/trialprotocols`) holds only the built HTML output. The Python generator scripts live in the [mroswell/phmpt-index](https://github.com/mroswell/phmpt-index) repository, under `scripts/`:

- `make_*_amendment_history_html.py` — one per trial.
- `make_amendment_histories_index.py` — the landing page.
- `make_missing_pdfs_foia_request_docx.py` — auto-generates a FOIA request for any amendments still not findable in public sources.
- `_amendment_history_pfizer.py` / `_amendment_history_moderna.py` — the two shared parser/renderer modules.

## License

[CC BY 4.0](LICENSE). Copyright © 2026 Marjorie Roswell.

The CC license applies to this site's compilation, extraction, and presentation of the records. Underlying protocol documents remain works of their respective sponsors and are linked or excerpted under the terms of their original public-record availability.

## Compiled by

Marjorie Roswell.
