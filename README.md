# Versioned Notes System

A simple, Git-like notes application where notes are immutable. Every time a note is updated or reverted, a new version is created. 

## Architecture

This project is separated into a Python/Flask backend and a React frontend.

The backend strictly follows a layered architecture to keep complexity low and logic isolated:
- **Routes:** Handle only HTTP parsing and request/response formatting.
- **Services:** Contain 100% of the business logic. Rules like "version numbers must strictly increment by 1" and "updates cannot overwrite existing versions" are enforced here.
- **Models:** Describe the database schema.

## Why Immutability?

Immutability gives us a reliable audit trail (like Git). Instead of mutating an existing note, we append a new version. This means you can always view the history of a note or revert to any previous state without losing the intermediate history (a revert simply creates a *new* version with the old content).

## Tradeoffs

- **Storage:** We store a full copy of the note text for every edit. For a simple system, this is perfectly fine and avoids the complexity of storing diffs (like Operational Transformation or Git's packfiles). Python's `difflib` can be used on the fly to generate diffs when viewing history.
- **Database:** Using SQLite for simplicity and portability. In a high-concurrency production setting, Postgres with strict transaction isolation would be preferred.

## How to Run Locally

### Backend
1. Navigate to the `backend` directory.
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `.\venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Run the server: `flask run --debug` (runs on port 5000)

### Frontend
1. Navigate to the `frontend` directory.
2. Install dependencies: `npm install`
3. Start the dev server: `npm run dev`
