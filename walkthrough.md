# Complete Video Walkthrough Script (10-15 Minutes)

**Before You Start (Checklist)**
- Since this project uses SQLite, you don't need Docker or Postgres. Just make sure your virtual environment is activated.
- Have your frontend and backend terminals running (`npm run dev` and `flask run`).
- Have VS Code open to `README.md` and your browser open to the local app (side-by-side or easily swappable).
- Take a deep breath. Speak slowly and confidently like an engineer giving a system demo to a coworker.

---

### [0:00 - 1:30] 1. Introduction & The "Why"
**(Show your screen with the app open on one side and `README.md` on the other)**

"Hi, I'm Akshat. Thank you for the opportunity to walk you through my submission for the Associate Software Engineer role at Better Software.

For this problem statement, I decided to build a 'Versioned Notes System'. It’s an inherently immutable notepad built with Python, Flask, SQLAlchemy, and React. 

The core idea is simple but strict: *Notes are never overwritten.* Whenever a user edits a note, a completely new version is appended instead of mutating the existing record. I chose this because it forces you to think deeply about data integrity, state management, and strict architectural boundaries.

Today I want to walk you through how I structured the system to prioritize correctness and safety over a massive feature count."

---

### [1:30 - 4:30] 2. Architecture & Clear Boundaries
**(Switch to VS Code. Open the `backend` folder structure. Specifically open `app.py`, `routes.py`, and `services.py`)**

"Let's start with the Backend structure. I deliberately separated this app into distinct layers to enforce clear boundaries.

If you look at `routes.py` **[highlight or point to routes.py]**, you’ll see it has almost zero logic. Its *only* responsibility is to parse incoming HTTP requests and return JSON. Instead of using complex validation libraries, I kept it extremely simple with basic API checks. This makes the system incredibly easy to read and maintain for any developer.

All of the actual business logic is totally isolated inside `services.py` **[open services.py]**. By centralizing the logic here, I guarantee that no matter what endpoint is called, the rules of the system—like immutability—cannot be bypassed.

Finally, the data layer is handled by `models.py` **[open models.py]**. I used SQLAlchemy as an ORM layer. This separation of concerns means the React frontend acts purely as a 'dumb client' consuming the API, while the Python backend strictly enforces the structure."

---

### [4:30 - 7:30] 3. Technical Decisions & Correctness
**(Open `services.py` again, specifically the `update_note` function)**

"For my technical decisions, my main goal was to make the system 'Correct' and 'Safe'. In an app like this, the biggest mistake would be accidentally overwriting an old note or messing up the numbered order of the versions.

To prevent that, I made a strict rule: The frontend is *never* allowed to decide the version number. The backend is completely in charge. If you look at the `update_note` function, when an edit comes in, the backend checks the database for the current version and simply forces the new version to be `latest_version + 1`. 

By locking this logic deep in the backend, it becomes impossible for the frontend to accidentally overwrite history, even if there's a bug in the UI code. 

And finally, to prove this is safe, I wrote a quick suite of automated tests that verify the version always goes up and nothing can ever get overwritten."

---

### [7:30 - 10:00] 4. AI Usage & Guidance (Antigravity)
**(Open `ai/rules.md`)**

"I want to touch on my AI usage, as it was a massive part of this workflow. I used Google's Antigravity system, but I didn't treat it like a generic code generator. I acted as the systems architect and used prompt engineering to strictly constrain it.

Before any code was written, I provided the AI with this `ai/rules.md` file. I explicitly mapped out invariants:
1. Immutability is the core concept.
2. It must *always* use the service layer—no business logic in the routes.
3. Version logic cannot be bypassed.

By guiding the AI upfront with these architectural boundaries, I prevented it from writing clever but fragile code. I critically reviewed every iteration, and when the AI tried to leak logic into the frontend, I was able to catch it and enforce the constraints I set."

---

### [10:00 - 12:00] 5. UI Structure & Demonstration
**(Switch back to the Browser showing the Frontend)**

"Let me quickly show you the frontend and the final result. I didn't focus on flashy animations or UI libraries; I focused on 'simplicity'. The UX rule I followed was 'One screen = one purpose'.

1. I built a clean list view here on the Home page. It's fully clickable and just shows the necessary metadata.
2. **[Click on a note]** When you open the Editor, it's distraction-free. The React components are completely modular. 
3. **[Make an edit, hit Save]** I'll make a quick update. It hits the API, the backend creates version 2.
4. **[Click into history]** Here on the history timeline, you can see the immutable audit trail.
5. **[Click Revert]** If I hit Revert on an older version, notice that it doesn't delete the timeline. It safely appends a *brand new* version to the end of the timeline containing the old content."

---

### [12:00 - 14:00] 6. Risks, Tradeoffs, & Conclusion
**(Switch back to VS Code `README.md` or just speak directly to the camera)**

"To wrap up, I want to address the weaknesses and tradeoffs I made to keep this system simple.

1. **Storage Tradeoff:** Currently, I'm storing the entire text chunk in the database for every single version. For simple notes, this is fine. But at scale, this is inefficient. If I were extending this, I would implement a diff-based storage system—similar to Git's packfiles—where we only store the delta between versions.
2. **Database:** I used SQLite for the sake of an easily runnable submission. In production, I would swap this to PostgreSQL to utilize stricter transaction isolation levels to prevent race conditions during high-concurrency edits.

Overall, by focusing on service-layer isolation, strict validation, and upfront AI constraint rules, I believe this system demonstrates clean boundaries and readable code. 

Thank you for your time, and I look forward to your feedback!"
