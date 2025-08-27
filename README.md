# Account Projection Module

This repository contains a custom Odoo module that introduces basic
models to manage financial projections. Projections represent expected
cash movements that may later be linked to real accounting documents.

The module currently includes:

* `account.projection` to record projected amounts and track their
  realization. Each projection must be linked to an account for
  traceability in reports and when matching real documents.
* `account.projection.realization` to link projections with
  `account.move` records for partial or full realization.
* Categorization via `account.projection.category`.
* Configurable projection report (`account.projection.report`) to choose
  which accounts appear in the exported XLSX report.
* Suggestion of related projections when creating accounting entries and
  a wizard to link them on the fly.
* XLSX report exporting projected vs. realized amounts per account based
  on configurable selections.

The module serves as a foundation for a broader cashflow projection
feature set.
