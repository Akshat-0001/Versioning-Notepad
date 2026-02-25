from flask import Blueprint, request, jsonify
from services import (
    create_note, update_note, revert_note, get_note_history, NoteServiceError
)
from models import Note, NoteVersion

api = Blueprint('api', __name__)

@api.errorhandler(NoteServiceError)
def handle_service_error(e):
    return jsonify({"error": str(e)}), 400

@api.route('/notes', methods=['POST'])
def handle_create_note():
    data = request.json
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({"error": "Title and content are required."}), 400
        
    note = create_note(data['title'], data['content'])
    return jsonify({
        "id": note.id,
        "title": note.title,
        "created_at": note.created_at.isoformat()
    }), 201

@api.route('/notes', methods=['GET'])
def list_notes():
    notes = Note.query.order_by(Note.created_at.desc()).all()
    result = []
    for note in notes:
        latest = note.versions[0] if note.versions else None
        latest_data = None
        if latest:
            latest_data = {
                "id": latest.id,
                "content": latest.content,
                "version_number": latest.version_number,
                "created_at": latest.created_at.isoformat()
            }
        
        result.append({
            "id": note.id,
            "title": note.title,
            "created_at": note.created_at.isoformat(),
            "latest_version": latest_data
        })
    return jsonify(result), 200

@api.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    note = Note.query.get_or_404(note_id)
    latest_version = note.versions[0] if note.versions else None
    
    if not latest_version:
        return jsonify({"error": "Note found but has no versions."}), 404

    return jsonify({
        "id": note.id,
        "title": note.title,
        "created_at": note.created_at.isoformat(),
        "latest_version": {
            "id": latest_version.id,
            "content": latest_version.content,
            "version_number": latest_version.version_number,
            "created_at": latest_version.created_at.isoformat()
        }
    }), 200

@api.route('/notes/<int:note_id>', methods=['PUT'])
def handle_update_note(note_id):
    data = request.json
    if not data or not data.get('content'):
        return jsonify({"error": "Content is required."}), 400
        
    version = update_note(note_id, data['content'])
    return jsonify({
        "id": version.id,
        "content": version.content,
        "version_number": version.version_number,
        "created_at": version.created_at.isoformat()
    }), 200

@api.route('/notes/<int:note_id>/history', methods=['GET'])
def get_history(note_id):
    history = get_note_history(note_id)
    result = [{
        "id": v.id,
        "content": v.content,
        "version_number": v.version_number,
        "created_at": v.created_at.isoformat()
    } for v in history]
    return jsonify(result), 200

@api.route('/notes/<int:note_id>/revert/<int:version_id>', methods=['POST'])
def handle_revert_note(note_id, version_id):
    version = revert_note(note_id, version_id)
    return jsonify({
        "id": version.id,
        "content": version.content,
        "version_number": version.version_number,
        "created_at": version.created_at.isoformat()
    }), 200
