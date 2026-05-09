# Adaptix: AI Behavior Learning Tool

Adaptix is an open-source tool designed to observe, analyze, and learn from a user's computer habits. It captures screen activity and system metadata, processing it through an AI (Gemini) to build a "behavioral profile".

## User Review Required

> [!IMPORTANT]
> **Privacy & Security**: All screen captures are stored locally and only processed via the user's personal Gemini API key.
> **Desktop App**: Based on user request, this will be a standalone Python application, not a web app.

## Proposed Changes

### [Desktop App (Python)]
A premium local application built with CustomTkinter.

#### [NEW] [main.py](file:///d:/adaptix/adaptix/main.py)
- **UI Engine**: CustomTkinter for a sleek, dark-mode dashboard.
- **Settings**: Local storage of Gemini API keys.
- **Activity Log**: Real-time display of what the AI is "seeing".

### [The Collector]
#### [NEW] [collector.py](file:///d:/adaptix/adaptix/collector.py)
- **Vision**: Uses `pyautogui` to capture screenshots.
- **Context**: Uses `pywin32` to identify the active application.
- **Processing**: Sends data to Gemini 2.0 Flash for "habit analysis".

## Verification Plan

### Automated Tests
- Test screenshot capture logic.
- Verify active window detection.

### Manual Verification
- Run `main.py` and ensure the UI opens on D:.
- Enter API key and verify AI insights.
