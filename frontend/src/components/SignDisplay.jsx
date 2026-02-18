import { useState, useEffect, useRef, useCallback } from 'react';

const API_URL = 'http://localhost:5000';

/* SVG Icon Components */
const PlayIcon = () => <svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z" /></svg>;
const PauseIcon = () => <svg viewBox="0 0 24 24" fill="currentColor"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" /></svg>;
const PrevIcon = () => <svg viewBox="0 0 24 24" fill="currentColor"><path d="M6 6h2v12H6zm3.5 6l8.5 6V6z" /></svg>;
const NextIcon = () => <svg viewBox="0 0 24 24" fill="currentColor"><path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z" /></svg>;
const ReplayIcon = () => <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 5V1L7 6l5 5V7c3.31 0 6 2.69 6 6s-2.69 6-6 6-6-2.69-6-6H4c0 4.42 3.58 8 8 8s8-3.58 8-8-3.58-8-8-8z" /></svg>;
const HandIcon = () => <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12.5 2c-.28 0-.5.22-.5.5V11l-2.41-2.41c-.2-.2-.51-.2-.71 0l-.36.36c-.2.2-.2.51 0 .71L12 13.17l3.48-3.48c.2-.2.2-.51 0-.71l-.36-.36c-.2-.2-.51-.2-.71 0L12 11V2.5c0-.28-.22-.5-.5-.5zM3 14v7c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2v-7H3zm9 5c-1.66 0-3-1.34-3-3h2c0 .55.45 1 1 1s1-.45 1-1h2c0 1.66-1.34 3-3 3z" /></svg>;

export default function SignDisplay({ data }) {
    const [currentIndex, setCurrentIndex] = useState(0);
    const [isPlaying, setIsPlaying] = useState(false);
    const [speed, setSpeed] = useState(1000);
    const intervalRef = useRef(null);

    const signs = data?.signs || [];
    const currentSign = signs[currentIndex];

    const play = useCallback(() => setIsPlaying(true), []);

    const pause = useCallback(() => {
        setIsPlaying(false);
        if (intervalRef.current) { clearInterval(intervalRef.current); intervalRef.current = null; }
    }, []);

    const goToSign = useCallback((index) => setCurrentIndex(index), []);

    const nextSign = useCallback(() => {
        setCurrentIndex(prev => {
            if (prev >= signs.length - 1) { setIsPlaying(false); return prev; }
            let next = prev + 1;
            while (next < signs.length && signs[next].type === 'space') next++;
            return next >= signs.length ? prev : next;
        });
    }, [signs]);

    const prevSign = useCallback(() => {
        setCurrentIndex(prev => {
            if (prev <= 0) return 0;
            let next = prev - 1;
            while (next > 0 && signs[next].type === 'space') next--;
            return next;
        });
    }, [signs]);

    const replay = useCallback(() => {
        pause();
        setCurrentIndex(0);
        setTimeout(() => play(), 300);
    }, [pause, play]);

    useEffect(() => {
        if (isPlaying && signs.length > 0) {
            intervalRef.current = setInterval(() => {
                setCurrentIndex(prev => {
                    let next = prev + 1;
                    while (next < signs.length && signs[next].type === 'space') next++;
                    if (next >= signs.length) { setIsPlaying(false); clearInterval(intervalRef.current); return prev; }
                    return next;
                });
            }, speed);
        }
        return () => { if (intervalRef.current) clearInterval(intervalRef.current); };
    }, [isPlaying, speed, signs]);

    useEffect(() => { setCurrentIndex(0); setIsPlaying(false); }, [data]);
    useEffect(() => {
        if (data && signs.length > 0) {
            const t = setTimeout(() => play(), 500);
            return () => clearTimeout(t);
        }
    }, [data]);

    if (!data || signs.length === 0) {
        return (
            <div className="sign-display-section">
                <div className="empty-state">
                    <div className="icon"><HandIcon /></div>
                    <p>Enter text or speak to see the Indian Sign Language translation</p>
                </div>
            </div>
        );
    }

    return (
        <div className="sign-display-section">
            <h2>ISL Translation</h2>

            <div className="nlp-info">
                <div className="nlp-info-item">
                    <span className="nlp-info-label">Input</span>
                    <span className="nlp-info-value">{data.original_text}</span>
                </div>
                <div className="nlp-info-item">
                    <span className="nlp-info-label">ISL Order</span>
                    <span className="nlp-info-value">{data.isl_tokens?.join(' → ')}</span>
                </div>
                <div className="nlp-info-item">
                    <span className="nlp-info-label">Signs</span>
                    <span className="nlp-info-value">{data.total_signs}</span>
                </div>
            </div>

            <div className="glass-card">
                <div className="sign-player">
                    <div className="sign-player-image-container">
                        {currentSign && currentSign.image_url ? (
                            <img
                                src={`${API_URL}${currentSign.image_url}`}
                                alt={`ISL sign for ${currentSign.label}`}
                                key={currentSign.label + currentIndex}
                            />
                        ) : (
                            <div className="placeholder"><HandIcon /></div>
                        )}
                    </div>

                    {currentSign && (
                        <>
                            <div className="sign-player-label">{currentSign.label}</div>
                            <div className="sign-player-word">
                                {currentSign.type === 'letter' ? `Spelling: "${currentSign.original}"` : currentSign.original}
                            </div>
                        </>
                    )}

                    <div className="player-controls">
                        <button className="control-btn" onClick={prevSign} title="Previous"><PrevIcon /></button>
                        <button className="control-btn play-btn" onClick={isPlaying ? pause : play} title={isPlaying ? 'Pause' : 'Play'}>
                            {isPlaying ? <PauseIcon /> : <PlayIcon />}
                        </button>
                        <button className="control-btn" onClick={nextSign} title="Next"><NextIcon /></button>
                        <button className="control-btn" onClick={replay} title="Replay"><ReplayIcon /></button>
                        <select className="speed-select" value={speed} onChange={(e) => setSpeed(Number(e.target.value))}>
                            <option value={2000}>0.5x</option>
                            <option value={1000}>1x</option>
                            <option value={600}>1.5x</option>
                            <option value={400}>2x</option>
                        </select>
                    </div>
                </div>

                <div className="sign-timeline">
                    {signs.map((sign, idx) => {
                        if (sign.type === 'space') return <span key={idx} className="sign-chip space">|</span>;
                        return (
                            <span key={idx} className={`sign-chip ${idx === currentIndex ? 'active' : ''}`} onClick={() => goToSign(idx)}>
                                {sign.label}
                            </span>
                        );
                    })}
                </div>
            </div>
        </div>
    );
}
