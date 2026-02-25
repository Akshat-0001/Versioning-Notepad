import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getNotes } from '../api';

function Home() {
    const [notes, setNotes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        getNotes()
            .then(res => {
                setNotes(res.data);
                setLoading(false);
            })
            .catch(err => {
                console.error(err);
                setError('Failed to load notes.');
                setLoading(false);
            });
    }, []);

    if (loading) return <p className="meta-text text-center mt-4">Loading notes...</p>;
    if (error) return <div className="error">{error}</div>;

    return (
        <div>
            <div className="header-actions">
                <h1>All Notes</h1>
            </div>

            {notes.length === 0 ? (
                <div className="empty-state">
                    <p className="meta-text">No notes yet.</p>
                    <button onClick={() => navigate('/new')} className="button">Create First Note</button>
                </div>
            ) : (
                <ul className="clean-list">
                    {notes.map(note => (
                        <li key={note.id} className="list-item" onClick={() => navigate(`/note/${note.id}`)}>
                            <h2 className="item-title">{note.title}</h2>

                            {note.latest_version && (
                                <p className="item-preview">
                                    {note.latest_version.content}
                                </p>
                            )}

                            <div className="item-meta">
                                <span>v{note.latest_version?.version_number || 0}</span>
                                <span> • </span>
                                <span>updated {note.latest_version ? new Date(note.latest_version.created_at).toLocaleString() : 'Never'}</span>
                            </div>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default Home;
