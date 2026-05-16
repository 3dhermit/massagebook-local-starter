# MassageBook Starter - Local Practice Management App

A starter Python desktop application replicating core features of MassageBook and Mindbody for massage therapists and wellness practitioners.

## Features (Starter Version)
- Local SQLite database (offline-first)
- Client management (add, view, search)
- Basic appointment scheduling with conflict detection
- Simple SOAP notes entry
- One-click database backup/export
- User authentication (basic)
- Calendar-style schedule view (table-based for simplicity)
- Reports export (CSV)

## Planned / Extensible
- Full PyQt calendar with drag-drop
- Email/SMS reminders
- Payment tracking
- Multi-staff support
- Embedded client booking portal
- Packaging to .exe with PyInstaller

## Tech Stack
- **GUI**: PySide6 (Qt for Python)
- **Database**: SQLite + SQLAlchemy ORM
- **Packaging**: PyInstaller (for .exe)
- Python 3.10+

## Setup Instructions

1. Clone or download this repository.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## Database
- Default database file: `data/massagebook.db`
- Backup: Use the "Backup Database" button in the app (copies the .db file with timestamp).
- To inspect: Use any SQLite browser or `sqlite3 data/massagebook.db`

## Building to .exe (Windows)
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=app.ico main.py
```
The executable will be in the `dist/` folder.

## Project Structure
```
massagebook_starter/
├── main.py                 # Application entry point
├── requirements.txt
├── README.md
├── .gitignore
├── database/
│   ├── __init__.py
│   ├── models.py           # SQLAlchemy models
│   ├── db.py               # Database session and utilities
├── ui/
│   ├── __init__.py
│   ├── main_window.py      # Main dashboard
│   ├── client_dialog.py    # Add/Edit client
│   ├── appointment_dialog.py
├── core/
│   ├── scheduler.py        # Booking logic
│   ├── auth.py             # Simple authentication
├── utils/
│   ├── export.py           # CSV/PDF export and backup
│   ├── reports.py
├── data/                   # SQLite database lives here
└── LICENSE
```

## Next Steps / Customization
- Extend the calendar view using QCalendarWidget or a custom table.
- Add rich text for SOAP notes.
- Integrate Twilio for SMS or smtplib for email.
- Add role-based access for multi-therapist practices.
- Package with PyInstaller for distribution.

This starter provides a solid foundation. Expand it according to your specific workflow needs.

For full production use, consider adding encryption for sensitive data and proper input validation.

## License
MIT License (placeholder) - Customize as needed.