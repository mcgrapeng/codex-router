# Codex Router TUI Logo Design

## Goal

Show a large `codex router` logo on both the onboarding homepage and the first screen of a new chat session.

## Confirmed Direction

Use a static single-line ASCII wordmark for `CODEX ROUTER`. The logo should read as one brand mark when the terminal is wide enough. Narrow terminals must not clip the logo; they should fall back to compact text.

## Architecture

Add a small reusable TUI brand/logo module that owns the wordmark text and renders it as Ratatui lines. The onboarding welcome widget and the session header history cell will call this module instead of duplicating ASCII art.

## Components

- `codex-rs/tui/src/brand.rs`: provides the single-line wordmark, compact fallback, width checks, and conversion to `Line` values.
- `codex-rs/tui/src/onboarding/welcome.rs`: renders the brand wordmark on the homepage before the welcome copy.
- `codex-rs/tui/src/history_cell.rs`: adds the brand wordmark to the first session information cell.
- `codex-rs/tui/src/chatwidget/tests/status_and_layout.rs` and existing snapshots: verify the empty session homepage includes the logo.

## Behavior

- Wide terminals render a five-line ASCII `CODEX ROUTER` wordmark.
- Narrow terminals render `codex router` as compact text.
- Existing onboarding controls and session help text remain available.
- The implementation does not change sandbox or network environment handling.

## Testing

- Unit tests cover wide and narrow logo rendering.
- Onboarding welcome rendering tests assert the large logo appears on wide screens and falls back on narrow screens.
- ChatWidget snapshot coverage captures the empty session homepage logo.
