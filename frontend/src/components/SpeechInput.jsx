import { useState, useRef } from 'react';

const API_URL = 'http://localhost:5000';

const MicIcon = () => (
    <svg viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm-1-9c0-.55.45-1 1-1s1 .45 1 1v6c0 .55-.45 1-1 1s-1-.45-1-1V5zm6 6c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
    </svg>
);

const StopIcon = () => (
    <svg viewBox="0 0 24 24" fill="currentColor">
        <path d="M6 6h12v12H6z" />
    </svg>
);

export default function SpeechInput({ onResult, onLoading }) {
    const [text, setText] = useState('');
    const [isRecording, setIsRecording] = useState(false);
    const recognitionRef = useRef(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!text.trim()) return;

        onLoading(true);
        try {
            const res = await fetch(`${API_URL}/api/process-text`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text.trim() }),
            });
            const data = await res.json();
            onResult(data);
        } catch (err) {
            console.error('API Error:', err);
            alert('Could not connect to backend. Make sure the Flask server is running on port 5000.');
        } finally {
            onLoading(false);
        }
    };

    const toggleRecording = () => {
        if (isRecording) {
            if (recognitionRef.current) recognitionRef.current.stop();
            setIsRecording(false);
        } else {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {
                alert('Speech recognition is not supported in this browser. Please use Chrome.');
                return;
            }
            const recognition = new SpeechRecognition();
            recognition.lang = 'en-US';
            recognition.interimResults = true;
            recognition.continuous = false;
            recognition.onresult = (event) => {
                const transcript = Array.from(event.results).map(r => r[0].transcript).join('');
                setText(transcript);
            };
            recognition.onend = () => setIsRecording(false);
            recognition.onerror = () => setIsRecording(false);
            recognitionRef.current = recognition;
            recognition.start();
            setIsRecording(true);
        }
    };

    return (
        <div className="input-section">
            <h2>Input</h2>
            <form onSubmit={handleSubmit}>
                <div className="input-row">
                    <button
                        type="button"
                        className={`btn-mic ${isRecording ? 'recording' : ''}`}
                        onClick={toggleRecording}
                        title={isRecording ? 'Stop recording' : 'Start recording'}
                    >
                        {isRecording ? <StopIcon /> : <MicIcon />}
                    </button>
                    <input
                        type="text"
                        className="text-input"
                        placeholder="Type a sentence, e.g. What is your name?"
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        id="speech-input"
                    />
                    <button type="submit" className="btn btn-primary" id="translate-btn">
                        Translate
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z" /></svg>
                    </button>
                </div>
            </form>
        </div>
    );
}
