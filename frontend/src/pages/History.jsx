import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getNoteHistory, revertNote, getNote } from '../api';

function History() {
    const { id } = useParams();
    const navigate = useNavigate();

    const [note, setNote] = useState(null);
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [reverting, setReverting] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        Promise.all([getNote(id), getNoteHistory(id)])
            .then(([noteRes, historyRes]) => {
                setNote(noteRes.data);
                setHistory(historyRes.data);
                setLoading(false);
            })
            .catch(err => {
                console.error(err);
                setError('Failed to load note history.');
                setLoading(false);
            });
    }, [id]);

    const handleRevert = (versionId) => {
        if (!window.confirm('Are you sure you want to revert to this version?')) return;

        setReverting(true);
        setError(null);

        revertNote(id, versionId)
            .then(() => {
                navigate(`/note/${id}`);
            })
            .catch(err => {
                console.error(err);
                setError(err.response?.data?.error || 'Failed to revert note.');
                setReverting(false);
            });
    };

    if (loading) return <p className="meta-text text-center mt-4">Loading history...</p>;
    if (error) return <div className="error">{error}</div>;

    return (
        <div>
            <div className="editor-header">
                <button type="button" className="link-button" onClick={() => navigate(`/note/${id}`)}>
                    ← Back to Note
                </button>
                <h1 className="editor-title">History: {note?.title}</h1>
            </div>

            <div className="history-timeline">
                {history.map((version, index) => {
                    const isLatest = index === 0;
                    return (
                        <div key={version.id} className="history-item">
                            <div className="history-meta">
                                <span className="history-version">Version {version.version_number} {isLatest && '(current)'}</span>
                                <span className="history-date">{new Date(version.created_at).toLocaleString()}</span>
                            </div>

                            <div className="history-content">
                                {version.content}
                            </div>

                            {!isLatest && (
                                <button
                                    onClick={() => handleRevert(version.id)}
                                    className="link-button"
                                    disabled={reverting}
                                >
                                    [ Revert ]
                                </button>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
}

export default History;
