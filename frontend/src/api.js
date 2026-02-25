import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

export const getNotes = () => axios.get(`${API_URL}/notes`);
export const getNote = (id) => axios.get(`${API_URL}/notes/${id}`);
export const createNote = (title, content) =>
    axios.post(`${API_URL}/notes`, { title, content });
export const updateNote = (id, content) =>
    axios.put(`${API_URL}/notes/${id}`, { content });
export const getNoteHistory = (id) => axios.get(`${API_URL}/notes/${id}/history`);
export const revertNote = (id, versionId) =>
    axios.post(`${API_URL}/notes/${id}/revert/${versionId}`);
