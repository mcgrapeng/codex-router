use crate::onboarding::onboarding_screen::KeyboardHandler;
use crate::onboarding::onboarding_screen::StepStateProvider;
use crate::tui::FrameRequester;
use crossterm::event::KeyEvent;
use ratatui::buffer::Buffer;
use ratatui::layout::Rect;
use ratatui::prelude::Widget;
use ratatui::style::Stylize;
use ratatui::text::Line;
use ratatui::widgets::Clear;
use ratatui::widgets::Paragraph;
use ratatui::widgets::WidgetRef;
use ratatui::widgets::Wrap;
use std::cell::Cell;

use super::onboarding_screen::StepState;

pub(crate) struct WelcomeWidget {
    pub is_logged_in: bool,
    layout_area: Cell<Option<Rect>>,
}

impl KeyboardHandler for WelcomeWidget {
    fn handle_key_event(&mut self, _key_event: KeyEvent) {}
}

impl WelcomeWidget {
    pub(crate) fn new(
        is_logged_in: bool,
        _request_frame: FrameRequester,
        _animations_enabled: bool,
    ) -> Self {
        Self {
            is_logged_in,
            layout_area: Cell::new(None),
        }
    }

    pub(crate) fn update_layout_area(&self, area: Rect) {
        self.layout_area.set(Some(area));
    }

    pub(crate) fn set_animations_suppressed(&self, _suppressed: bool) {}
}

impl WidgetRef for &WelcomeWidget {
    fn render_ref(&self, area: Rect, buf: &mut Buffer) {
        Clear.render(area, buf);

        let layout_area = self.layout_area.get().unwrap_or(area);
        let mut lines: Vec<Line> = crate::brand::codex_router_logo_lines(layout_area.width);
        lines.push("".into());
        lines.push(Line::from(vec![
            "  ".into(),
            "Welcome to ".into(),
            "codex router".bold(),
        ]));

        Paragraph::new(lines)
            .wrap(Wrap { trim: false })
            .render(area, buf);
    }
}

impl StepStateProvider for WelcomeWidget {
    fn get_step_state(&self) -> StepState {
        match self.is_logged_in {
            true => StepState::Hidden,
            false => StepState::Complete,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use pretty_assertions::assert_eq;
    use ratatui::buffer::Buffer;
    use ratatui::layout::Rect;

    fn row_containing(buf: &Buffer, needle: &str) -> Option<u16> {
        (0..buf.area.height).find(|&y| {
            let mut row = String::new();
            for x in 0..buf.area.width {
                row.push_str(buf[(x, y)].symbol());
            }
            row.contains(needle)
        })
    }

    #[test]
    fn welcome_renders_logo_on_first_draw() {
        let widget = WelcomeWidget::new(
            /*is_logged_in*/ false,
            FrameRequester::test_dummy(),
            /*animations_enabled*/ true,
        );
        let area = Rect::new(0, 0, crate::brand::CODEX_ROUTER_LOGO_WIDTH as u16, 12);
        let mut buf = Buffer::empty(area);
        (&widget).render(area, &mut buf);

        let logo_row = row_containing(&buf, "____ ___  ____");
        let welcome_row = row_containing(&buf, "Welcome");
        assert_eq!(logo_row, Some(0));
        assert_eq!(welcome_row, Some(6));
    }

    #[test]
    fn welcome_uses_compact_logo_below_width_breakpoint() {
        let widget = WelcomeWidget::new(
            /*is_logged_in*/ false,
            FrameRequester::test_dummy(),
            /*animations_enabled*/ true,
        );
        let area = Rect::new(0, 0, crate::brand::CODEX_ROUTER_LOGO_WIDTH as u16 - 1, 6);
        let mut buf = Buffer::empty(area);
        (&widget).render(area, &mut buf);

        let logo_row = row_containing(&buf, "codex router");
        let welcome_row = row_containing(&buf, "Welcome");
        assert_eq!(logo_row, Some(0));
        assert_eq!(welcome_row, Some(2));
    }
}
