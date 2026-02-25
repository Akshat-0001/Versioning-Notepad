import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { createNote, updateNote, getNote } from '../api';

function NoteEditor() {
    const { id } = useParams();
    const navigate = useNavigate();
    const isEditing = !!id;

    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');

    const [loading, setLoading] = useState(isEditing);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (isEditing) {
            getNote(id)
                .then(res => {
                    setTitle(res.data.title);
                    if (res.data.latest_version) {
                        setContent(res.data.latest_version.content);
                    }
                    setLoading(false);
                })
                .catch(err => {
                    console.error(err);
                    setError('Failed to load note.');
                    setLoading(false);
                });
        }
    }, [id, isEditing]);

    const handleSubmit = (e) => {
        e.preventDefault();
        setSaving(true);
        setError(null);

        const request = isEditing
            ? updateNote(id, content)
            : createNote(title, content);

        request
            .then(() => {
                navigate('/');
            })
            .catch(err => {
                console.error(err);
                setError(err.response?.data?.error || 'Failed to save note.');
                setSaving(false);
            });
    };

    if (loading) return <p className="meta-text text-center mt-4">Loading editor...</p>;

    return (
        <div className="editor-container">
            <div className="editor-header">
                <button type="button" className="link-button" onClick={() => navigate('/')}>
                    ← Back
                </button>
                {isEditing ? (
                    <h1 className="editor-title">{title}</h1>
                ) : (
                    <input
                        className="title-input"
                        type="text"
                        value={title}
                        onChange={e => setTitle(e.target.value)}
                        required
                        placeholder="Note Title"
                    />
                )}
            </div>

            {error && <div className="error">{error}</div>}

            <form onSubmit={handleSubmit} className="editor-form">
                <textarea
                    className="content-textarea"
                    value={content}
                    onChange={e => setContent(e.target.value)}
                    required
                    placeholder="Start writing..."
                />

                <div className="editor-actions">
                    <button type="submit" className="button" disabled={saving || !content.trim() || !title.trim()}>
                        {saving ? 'Saving...' : 'Save'}
                    </button>
                    {isEditing && (
                        <Link to={`/note/${id}/history`} className="link-button">
                            View History
                        </Link>
                    )}
                </div>
            </form>
        </div>
    );
}

export default NoteEditor;
