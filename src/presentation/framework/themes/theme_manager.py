from __future__ import annotations

from PySide6.QtWidgets import QApplication

from presentation.framework.themes.theme import ThemeMode, ThemePalette


class ThemeManager:
    """Applies runtime QSS themes to the desktop application."""

    def __init__(self) -> None:
        self._current_mode = ThemeMode.DARK
        self._palettes = {
            ThemeMode.DARK: ThemePalette(
                mode=ThemeMode.DARK,
                background="#111827",
                surface="#1f2937",
                text="#f9fafb",
                primary="#38bdf8",
                danger="#f87171",
            ),
            ThemeMode.LIGHT: ThemePalette(
                mode=ThemeMode.LIGHT,
                background="#f8fafc",
                surface="#ffffff",
                text="#111827",
                primary="#0369a1",
                danger="#b91c1c",
            ),
            ThemeMode.HIGH_CONTRAST: ThemePalette(
                mode=ThemeMode.HIGH_CONTRAST,
                background="#000000",
                surface="#101010",
                text="#ffffff",
                primary="#ffff00",
                danger="#ff4040",
            ),
        }

    @property
    def current_mode(self) -> ThemeMode:
        """Return current theme mode."""
        return self._current_mode

    def apply(self, application: QApplication, mode: ThemeMode) -> None:
        """Apply a theme to the Qt application."""
        self._current_mode = mode
        palette = self._palettes[mode]
        application.setStyleSheet(self._build_qss(palette))

    def toggle_light_dark(self, application: QApplication) -> ThemeMode:
        """Toggle between light and dark themes."""
        next_mode = ThemeMode.LIGHT if self._current_mode == ThemeMode.DARK else ThemeMode.DARK
        self.apply(application, next_mode)
        return next_mode

    @staticmethod
    def _build_qss(palette: ThemePalette) -> str:
        return f"""
        QWidget {{
            background: {palette.background};
            color: {palette.text};
            font-family: Segoe UI, Arial;
            font-size: 10pt;
        }}
        QFrame#header, QFrame#sidebar, QFrame#statusBar, QFrame#card {{
            background: {palette.surface};
            border: 1px solid rgba(128, 128, 128, 0.22);
        }}
        QLabel#title {{
            font-size: 18pt;
            font-weight: 700;
        }}
        QLabel#subtitle {{
            color: {palette.primary};
            font-weight: 600;
        }}
        QPushButton {{
            background: {palette.surface};
            border: 1px solid rgba(128, 128, 128, 0.45);
            border-radius: 6px;
            padding: 8px 10px;
        }}
        QPushButton:hover {{
            border-color: {palette.primary};
        }}
        QPushButton#primaryButton {{
            background: {palette.primary};
            color: {palette.background};
            font-weight: 700;
        }}
        QLineEdit {{
            background: {palette.surface};
            border: 1px solid rgba(128, 128, 128, 0.45);
            border-radius: 6px;
            padding: 8px;
        }}
        """
