use ratatui::style::Stylize;
use ratatui::text::Line;

pub(crate) const CODEX_ROUTER_LOGO_WIDTH: usize = 66;

const CODEX_ROUTER_LOGO: [&str; 5] = [
    "   ______          __              ____             __",
    "  / ____/___  ____/ /__  _  __    / __ \\____  __  __/ /____  _____",
    " / /   / __ \\/ __  / _ \\| |/_/   / /_/ / __ \\/ / / / __/ _ \\/ ___/",
    "/ /___/ /_/ / /_/ /  __/>  <    / _, _/ /_/ / /_/ / /_/  __/ /",
    "\\____/\\____/\\__,_/\\___/_/|_|   /_/ |_|\\____/\\__,_/\\__/\\___/_/",
];

pub(crate) fn codex_router_logo_lines(width: u16) -> Vec<Line<'static>> {
    if width as usize >= CODEX_ROUTER_LOGO_WIDTH {
        CODEX_ROUTER_LOGO
            .iter()
            .map(|line| (*line).magenta().bold().into())
            .collect()
    } else {
        vec!["codex router".magenta().bold().into()]
    }
}

pub(crate) fn codex_router_context_line() -> Line<'static> {
    vec![
        "coder".cyan(),
        " | ".dim(),
        "~/.codexrouter".into(),
        " | ".dim(),
        "isolated config".green(),
    ]
    .into()
}

#[cfg(test)]
mod tests {
    use pretty_assertions::assert_eq;
    use ratatui::text::Line;
    use unicode_width::UnicodeWidthStr;

    use super::*;

    fn lines_to_plain_text(lines: &[Line<'_>]) -> Vec<String> {
        lines
            .iter()
            .map(|line| {
                line.spans
                    .iter()
                    .map(|span| span.content.as_ref())
                    .collect()
            })
            .collect()
    }

    #[test]
    fn wordmark_uses_large_ascii_logo_when_width_allows() {
        let lines = codex_router_logo_lines(/*width*/ 80);
        let rendered = lines_to_plain_text(&lines);

        assert_eq!(
            rendered,
            vec![
                "   ______          __              ____             __",
                "  / ____/___  ____/ /__  _  __    / __ \\____  __  __/ /____  _____",
                " / /   / __ \\/ __  / _ \\| |/_/   / /_/ / __ \\/ / / / __/ _ \\/ ___/",
                "/ /___/ /_/ / /_/ /  __/>  <    / _, _/ /_/ / /_/ / /_/  __/ /",
                "\\____/\\____/\\__,_/\\___/_/|_|   /_/ |_|\\____/\\__,_/\\__/\\___/_/",
            ]
        );
    }

    #[test]
    fn wordmark_falls_back_when_width_is_too_narrow() {
        let lines = codex_router_logo_lines(/*width*/ 40);
        let rendered = lines_to_plain_text(&lines);

        assert_eq!(rendered, vec!["codex router"]);
    }

    #[test]
    fn context_line_labels_command_home_and_isolation() {
        let rendered = lines_to_plain_text(&[codex_router_context_line()]);

        assert_eq!(rendered, vec!["coder | ~/.codexrouter | isolated config"]);
    }

    #[test]
    fn logo_width_constant_matches_wordmark() {
        let logo_width = CODEX_ROUTER_LOGO
            .iter()
            .map(|line| UnicodeWidthStr::width(*line))
            .max()
            .unwrap_or(0);

        assert_eq!(logo_width, CODEX_ROUTER_LOGO_WIDTH);
    }
}
