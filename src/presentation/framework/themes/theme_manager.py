from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QApplication

from presentation.framework.themes.qss_loader import QssLoader
from presentation.framework.themes.theme import Theme, ThemeMode, ThemePalette


class ThemeManager:
    """Applies runtime QSS themes to the desktop application."""

    def __init__(
        self, styles_root: Path | None = None, qss_loader: QssLoader | None = None
    ) -> None:
        self._current_mode = ThemeMode.DARK
        self._styles_root = styles_root or Path("resources") / "styles"
        self._qss_loader = qss_loader or QssLoader()
        self._themes = {
            ThemeMode.DARK: Theme("dark", "Dark", self._styles_root / "dark.qss"),
            ThemeMode.LIGHT: Theme("light", "Light", self._styles_root / "light.qss"),
            ThemeMode.HIGH_CONTRAST: Theme(
                "high_contrast",
                "Alto Contraste",
                self._styles_root / "high_contrast.qss",
            ),
        }
        self._palettes = {
            ThemeMode.DARK: ThemePalette(
                mode=ThemeMode.DARK,
                background="#182015",
                surface="#242f1d",
                text="#f4f1df",
                primary="#c8b568",
                danger="#b85445",
            ),
            ThemeMode.LIGHT: ThemePalette(
                mode=ThemeMode.LIGHT,
                background="#eef0e2",
                surface="#f7f5e9",
                text="#1e2718",
                primary="#5f6f35",
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
        theme = self._themes[mode]
        stylesheet = self._qss_loader.load(theme.qss_path)
        if not stylesheet:
            stylesheet = self._build_qss(self._palettes[mode])
        application.setStyleSheet(stylesheet)

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
