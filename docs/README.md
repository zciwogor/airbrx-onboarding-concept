# Airbrx product docs hub

Live page: https://zciwogor.github.io/airbrx-onboarding-concept/docs/

Drafts for the Airbrx founders. Not for prospects.

## How it fits together

- `index.html`: the viewer. Left pane lists the docs, right pane shows the selected one with Download PDF, Print, Comment and History.
- `manifest.json`: the doc list, each with its version, update date and PDF path.
- `content/*.html`: the document bodies, exported from Claude Docs.
- `img/`: diagram snapshots used in the docs.
- `pdf/`: prebuilt PDFs. Rebuild with `python3 docs/tools/build_pdfs.py` after any content change.
- `revisions.json`: the revision log, newest first. Add an entry for every change and bump the version in `manifest.json`.
- `comments.json`: comments approved for display. The page has no backend: the comment form emails Adam, and reviewed comments get added here as `{"doc": "pricing", "name": "...", "date": "2026-11-05", "section": "Plan lineup", "text": "..."}`.

## Updating a doc

1. Replace `content/<id>.html` with the new body.
2. Bump `version` and `updated` for that doc in `manifest.json`.
3. Add a line to `revisions.json`.
4. Run `python3 docs/tools/build_pdfs.py`, then commit.
