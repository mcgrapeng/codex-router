# Codex Router TUI Logo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Render a large single-line `CODEX ROUTER` logo on the onboarding homepage and new-session homepage.

**Architecture:** Add a small `brand` module that owns the wordmark and fallback rendering. Wire that shared module into `WelcomeWidget` and `SessionHeaderHistoryCell` so both surfaces render identical branding without duplicating ASCII art.

**Tech Stack:** Rust, Ratatui `Line`/`Span`, existing `HistoryCell` rendering, `insta` snapshots.

---

### Task 1: Shared Brand Logo Module

**Files:**
- Create: `codex-rs/tui/src/brand.rs`
- Modify: `codex-rs/tui/src/lib.rs`

- [ ] **Step 1: Write failing tests**

Add tests in `brand.rs` for wide and narrow rendering:

```rust
#[test]
fn wordmark_uses_ascii_logo_when_width_allows() {
    let lines = codex_router_logo_lines(/*width*/ 80);
    let rendered = lines_to_plain_text(&lines);
    assert!(rendered.contains("____ ___  ____"));
    assert_eq!(lines.len(), 5);
}

#[test]
fn wordmark_falls_back_when_width_is_too_narrow() {
    let lines = codex_router_logo_lines(/*width*/ 40);
    let rendered = lines_to_plain_text(&lines);
    assert_eq!(rendered, vec!["codex router"]);
}
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cargo test -p codex-tui brand::tests`

Expected: FAIL because `brand` and `codex_router_logo_lines` do not exist yet.

- [ ] **Step 3: Implement the module**

Create `brand.rs` with constants for the five-line wordmark, a width check using `UnicodeWidthStr`, and `codex_router_logo_lines(width: u16) -> Vec<Line<'static>>`.

- [ ] **Step 4: Register the module**

Add `mod brand;` to `codex-rs/tui/src/lib.rs`.

- [ ] **Step 5: Run tests to verify pass**

Run: `cargo test -p codex-tui brand::tests`

Expected: PASS.

### Task 2: Onboarding Homepage

**Files:**
- Modify: `codex-rs/tui/src/onboarding/welcome.rs`

- [ ] **Step 1: Write failing tests**

Update existing welcome tests so a wide render asserts the large logo appears and a narrow render asserts compact fallback text appears.

- [ ] **Step 2: Run tests to verify they fail**

Run: `cargo test -p codex-tui onboarding::welcome::tests`

Expected: FAIL because welcome still renders the old animation-first UI.

- [ ] **Step 3: Implement welcome logo rendering**

Use `crate::brand::codex_router_logo_lines(layout_area.width)` before the welcome copy. Remove the old welcome animation from this screen so the homepage matches the selected static wordmark direction.

- [ ] **Step 4: Run tests to verify pass**

Run: `cargo test -p codex-tui onboarding::welcome::tests`

Expected: PASS.

### Task 3: New Session Homepage

**Files:**
- Modify: `codex-rs/tui/src/history_cell.rs`
- Modify snapshots under `codex-rs/tui/src/chatwidget/snapshots/`

- [ ] **Step 1: Write failing test**

Add or update a ChatWidget empty-session snapshot to assert the first screen includes the `CODEX ROUTER` wordmark.

- [ ] **Step 2: Run test to verify it fails**

Run: `cargo test -p codex-tui chatwidget::tests::status_and_layout::ui_snapshots_small_heights_idle`

Expected: FAIL if the snapshot expects the logo and the code has not yet rendered it.

- [ ] **Step 3: Implement session header logo**

Insert `crate::brand::codex_router_logo_lines(inner_width)` at the top of `SessionHeaderHistoryCell::display_lines`, followed by a blank line and the existing session title/model/directory lines.

- [ ] **Step 4: Run focused snapshots**

Run: `cargo test -p codex-tui chatwidget::tests::status_and_layout::chatwidget_tall`

Expected: PASS after accepting intentional snapshot changes.

### Task 4: Formatting and Focused Verification

**Files:**
- Rust files changed above

- [ ] **Step 1: Format**

Run: `just fmt` from `codex-rs`.

- [ ] **Step 2: Run project tests**

Run: `cargo test -p codex-tui` from `codex-rs`.

- [ ] **Step 3: Run lints**

Run: `just fix -p codex-tui` from `codex-rs`.

- [ ] **Step 4: Re-check pending snapshots**

Run: `cargo insta pending-snapshots -p codex-tui` from `codex-rs`.

Expected: no unintended pending snapshots remain.
