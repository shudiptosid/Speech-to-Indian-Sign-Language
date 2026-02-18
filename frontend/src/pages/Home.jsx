import { useState } from 'react';
import SpeechInput from '../components/SpeechInput';
import SignDisplay from '../components/SignDisplay';

export default function Home() {
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    return (
        <>
            <section className="hero">
                <div className="hero-badge">
                    <span className="dot"></span>
                    CNN-Powered ISL Translation
                </div>
                <h1>
                    Speech to <span className="gradient-text">Indian Sign Language</span>
                </h1>
                <p>
                    Convert spoken or typed English into Indian Sign Language gestures
                    using NLP processing and CNN-based classification.
                </p>
            </section>

            <div className="main-container">
                <SpeechInput onResult={setResult} onLoading={setLoading} />

                {loading && (
                    <div className="loading-spinner">
                        <div className="spinner"></div>
                        <span>Processing with NLP pipeline...</span>
                    </div>
                )}

                <SignDisplay data={result} />
            </div>
        </>
    );
}
