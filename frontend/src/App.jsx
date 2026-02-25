import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import NoteEditor from './pages/NoteEditor';
import History from './pages/History';
import './index.css';

function App() {
    return (
        <BrowserRouter>
            <div className="container">
                <header className="main-header">
                    <Link to="/" className="logo-link">Versioned Notes</Link>
                    <Link to="/new" className="button header-button">New Note</Link>
                </header>
                <main>
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/new" element={<NoteEditor />} />
                        <Route path="/note/:id" element={<NoteEditor />} />
                        <Route path="/note/:id/history" element={<History />} />
                    </Routes>
                </main>
            </div>
        </BrowserRouter>
    );
}

export default App;
