# Vulnix Project Guidelines

## Code Style
- **Python**: Strict typing, modular architecture, and rich terminal output.
- **TUI (Textual)**: Use Textual components, reactive paradigms, and external `.tcss` for styling (exemplified by `tui/styles.tcss` and `tui/screens/` widgets).
- **Documentation**: Provide clear module-level docstrings, especially for integrations to the database (`database/connection.py`) and UI widgets (`tui/widgets/`).

## Architecture
- **TUI Layer**: Powers the visualization of the swarm. Separation of concerns is maintained with sub-modules for screens, modals, and widgets (`tui/`).
- **Agent/Skill Engine**: Under `agents/` and `skills/`. Business logic and vulnerabilities payloads are loaded dynamically from `skills/`. Ensure rule boundaries (such as `failure_patterns.yaml` and `ports.yaml`) are consulted for contextual logic.
- **Persistence**: SQLite forms the persistence backend, managed via `database/connection.py` defaulting to `~/.vulnix/`.

## Build and Run
- Create a virtual environment (`python -m venv .venv` and source it).
- Install dependencies: `pip install -r requirements.txt`.
- Run the TUI application: `python main.py`.

## Conventions
- **Safety First (Strict RoE)**: Vulnix is a security orchestrator. Never generate destructive database commands (e.g., `DROP`, `DELETE`), billion laughs DoS payloads against live systems, or pivot into unauthorized segments in code or documentation. PoC generation should strictly adhere to `exploit/SKILL.md`.
- **Textual Paradigms**: Do not block the main asyncio loop. Long-running security scans or agent computations MUST be dispatched to background workers.
- **Modularity**: UI components must remain decoupled from the scanner agents. Agent logs should route through `events` in the database, while the UI pulls asynchronously using `events.tail`.
