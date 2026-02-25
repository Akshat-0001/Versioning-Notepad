import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from app import create_app
from models import db, Note, NoteVersion
from services import create_note, update_note, revert_note, NoteServiceError

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def run_app(app):
    with app.app_context():
        yield app

def test_create_note(run_app):
    note = create_note("Test", "Content")
    assert note.id is not None
    assert len(note.versions) == 1
    version = note.versions[0]
    assert version.version_number == 1
    assert version.content == "Content"

def test_update_note(run_app):
    note = create_note("Test", "Content")
    new_version = update_note(note.id, "New Content")
    
    assert new_version.version_number == 2
    assert new_version.content == "New Content"

def test_revert_note(run_app):
    note = create_note("Test", "Content 1")
    version1_id = note.versions[0].id
    
    update_note(note.id, "Content 2")
    
    revert_version = revert_note(note.id, version1_id)
    
    assert revert_version.version_number == 3
    assert revert_version.content == "Content 1"

def test_invalid_update_nonexistent_note(run_app):
    with pytest.raises(NoteServiceError) as exc:
        update_note(999, "Content")
    assert "does not exist" in str(exc.value)

def test_invalid_revert_wrong_version(run_app):
    note = create_note("Test", "Content 1")
    with pytest.raises(NoteServiceError) as exc:
        revert_note(note.id, 999)
    assert "does not exist" in str(exc.value)


