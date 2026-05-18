# vmkit-test-minimal

A **VMKit test fixture** for the simplest possible happy path: a single-file
Python HTTP server with no database, no cache, no extra deps beyond the
stdlib. Used by VMKit's end-to-end test suite to verify that:

1. The repo scanner detects Python (via `pyproject.toml`) and finds **no
   accessories** — `accessories_needed: []`. Catches the "we wrongly
   pulled in postgres because the scanner imagined a dep" class of bug.
2. The Kamal generator emits a config WITHOUT an `accessories:` block.
3. The minimal Dockerfile builds and the container boots; `/health`
   returns 200 immediately.

This is the baseline reference for "what does a one-page service look
like" — every other test repo can be compared against this for what they
add on top.

## What the app does

`http.server` extension that responds 200 with `ok` on `/health` and a
hello string on `/`. No async, no framework, no deps.
