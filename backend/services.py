import logging
from models import db, Note, NoteVersion

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NoteServiceError(Exception):
    pass

def create_note(title: str, content: str) -> Note:
    new_note = Note(title=title)
    db.session.add(new_note)
    db.session.flush()
    
    version = NoteVersion(
        note_id=new_note.id,
        content=content,
        version_number=1
    )
    db.session.add(version)
    db.session.commit()
    logger.info(f"Created note {new_note.id} with version 1")
    return new_note

def _get_latest_version(note_id: int) -> NoteVersion:
    return NoteVersion.query.filter_by(note_id=note_id).order_by(NoteVersion.version_number.desc()).first()

def update_note(note_id: int, content: str) -> NoteVersion:
    note = Note.query.get(note_id)
    if not note:
        raise NoteServiceError(f"Note with id {note_id} does not exist.")
        
    latest_version = _get_latest_version(note_id)
    if not latest_version:
        raise NoteServiceError(f"Note {note_id} has no versions. Invalid state.")
        
    next_version_number = latest_version.version_number + 1
    
    new_version = NoteVersion(
        note_id=note_id,
        content=content,
        version_number=next_version_number
    )
    db.session.add(new_version)
    db.session.commit()
    logger.info(f"Updated note {note_id} to version {next_version_number}")
    return new_version

def get_note_with_latest_version(note_id: int) -> Note:
    """Get note by ID."""
    note = Note.query.get(note_id)
    if not note:
        raise NoteServiceError(f"Note with id {note_id} does not exist.")
    return note

def get_all_notes() -> list[Note]:
    """Get all notes."""
    return Note.query.order_by(Note.created_at.desc()).all()

def get_note_history(note_id: int) -> list[NoteVersion]:
    """Get all versions of a note."""
    note = Note.query.get(note_id)
    if not note:
        raise NoteServiceError(f"Note with id {note_id} does not exist.")
    return NoteVersion.query.filter_by(note_id=note_id).order_by(NoteVersion.version_number.desc()).all()

def revert_note(note_id: int, target_version_id: int) -> NoteVersion:
    """Revert a note to a previous version by creating a new version with the old content."""
    note = Note.query.get(note_id)
    if not note:
        raise NoteServiceError(f"Note with id {note_id} does not exist.")
        
    target_version = NoteVersion.query.filter_by(id=target_version_id, note_id=note_id).first()
    if not target_version:
        raise NoteServiceError(f"Version {target_version_id} does not exist for note {note_id}.")
        
    latest_version = _get_latest_version(note_id)
    next_version_number = latest_version.version_number + 1
    
    new_version = NoteVersion(
        note_id=note_id,
        content=target_version.content,
        version_number=next_version_number
    )
    db.session.add(new_version)
    db.session.commit()
    logger.info(f"Reverted note {note_id} to version {target_version.version_number} (new version is {next_version_number})")
    return new_version
