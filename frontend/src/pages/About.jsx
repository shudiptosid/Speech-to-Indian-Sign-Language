export default function About() {
    const pipelineSteps = [
        {
            num: 1,
            title: 'Speech-to-Text',
            description: 'Audio is captured via the browser microphone and converted to text using the Web Speech API.',
            tech: ['Web Speech API', 'Chrome'],
        },
        {
            num: 2,
            title: 'NLP Processing',
            description: 'English text is tokenized, lemmatized, and reordered to ISL grammar (Subject-Object-Verb). Stop words are removed.',
            tech: ['NLTK', 'Python'],
        },
        {
            num: 3,
            title: 'Sign Mapping',
            description: 'Each processed token is mapped to ISL hand gesture images. Unknown words are spelled out letter by letter.',
            tech: ['Dictionary Lookup', 'Dataset'],
        },
        {
            num: 4,
            title: 'CNN Classification',
            description: 'A Convolutional Neural Network trained on 42,000+ images classifies hand gestures into A-Z and 1-9.',
            tech: ['TensorFlow', 'Keras', 'Conv2D'],
        },
    ];

    return (
        <div className="main-container about-page">
            <h1>About <span className="gradient-text">ISL Generator</span></h1>
            <p className="subtitle">Understanding the AI pipeline behind speech-to-sign translation</p>

            {/* Pipeline */}
            <section className="pipeline-section">
                <h2>How It Works</h2>
                <div className="pipeline-cards">
                    {pipelineSteps.map((step) => (
                        <div className="pipeline-card" key={step.num}>
                            <div className="step-num">{step.num}</div>
                            <h3>{step.title}</h3>
                            <p>{step.description}</p>
                            <div>{step.tech.map((t) => <span className="tech-tag" key={t}>{t}</span>)}</div>
                        </div>
                    ))}
                </div>
            </section>

            {/* CNN Architecture */}
            <section className="pipeline-section">
                <h2>CNN Architecture</h2>
                <div className="glass-card">
                    <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem', fontSize: '0.9rem' }}>
                        The model uses three convolutional blocks to extract spatial features from hand gesture images,
                        followed by dense layers for classification into 35 classes.
                    </p>
                    <div style={{
                        fontFamily: "'JetBrains Mono', monospace",
                        fontSize: '0.8rem',
                        color: 'var(--accent)',
                        lineHeight: 1.9,
                        padding: '1rem',
                        background: 'var(--bg-tertiary)',
                        borderRadius: 'var(--radius-md)',
                        border: '1px solid var(--border)',
                    }}>
                        <div>Input (64 x 64 x 1 grayscale)</div>
                        <div style={{ color: 'var(--text-muted)' }}>&nbsp;&nbsp;&darr;</div>
                        <div>Conv2D(32) &rarr; BatchNorm &rarr; MaxPool &rarr; Dropout</div>
                        <div style={{ color: 'var(--text-muted)' }}>&nbsp;&nbsp;&darr;</div>
                        <div>Conv2D(64) &rarr; BatchNorm &rarr; MaxPool &rarr; Dropout</div>
                        <div style={{ color: 'var(--text-muted)' }}>&nbsp;&nbsp;&darr;</div>
                        <div>Conv2D(128) &rarr; BatchNorm &rarr; MaxPool &rarr; Dropout</div>
                        <div style={{ color: 'var(--text-muted)' }}>&nbsp;&nbsp;&darr;</div>
                        <div>Flatten &rarr; Dense(256) &rarr; BatchNorm &rarr; Dropout</div>
                        <div style={{ color: 'var(--text-muted)' }}>&nbsp;&nbsp;&darr;</div>
                        <div>Dense(35, softmax) &rarr; [A-Z, 1-9]</div>
                    </div>
                </div>
            </section>

            {/* ISL Grammar */}
            <section className="pipeline-section">
                <h2>ISL Grammar Rules</h2>
                <div className="glass-card">
                    <ul style={{
                        color: 'var(--text-secondary)',
                        lineHeight: 2.1,
                        paddingLeft: '0',
                        listStyleType: 'none',
                        fontSize: '0.9rem',
                    }}>
                        <li>Uses <strong style={{ color: 'var(--accent)' }}>SOV</strong> (Subject-Object-Verb) word order</li>
                        <li>Drops helper words: &ldquo;is&rdquo;, &ldquo;am&rdquo;, &ldquo;are&rdquo;, &ldquo;the&rdquo;, &ldquo;a&rdquo;</li>
                        <li>WH-question words move to the end of the sentence</li>
                        <li style={{ marginTop: '0.5rem' }}>
                            <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Example: </span>
                            <span style={{ color: 'var(--danger)' }}>&ldquo;What is your name?&rdquo;</span>
                            <span style={{ color: 'var(--text-muted)', margin: '0 8px' }}>&rarr;</span>
                            <span style={{ color: 'var(--success)' }}>&ldquo;your name what&rdquo;</span>
                        </li>
                    </ul>
                </div>
            </section>

            {/* Datasets */}
            <section className="pipeline-section">
                <h2>Datasets</h2>
                <div className="dataset-grid">
                    <div className="dataset-card">
                        <h3>33 Classes — Indian ISL</h3>
                        <div className="dataset-stat"><span className="label">Classes</span><span className="value">35 (A-Z + 1-9)</span></div>
                        <div className="dataset-stat"><span className="label">Images / class</span><span className="value">~1,200</span></div>
                        <div className="dataset-stat"><span className="label">Total</span><span className="value">~42,000</span></div>
                        <div className="dataset-stat"><span className="label">Purpose</span><span className="value">CNN Training</span></div>
                    </div>
                    <div className="dataset-card">
                        <h3>ISL General Gestures</h3>
                        <div className="dataset-stat"><span className="label">Classes</span><span className="value">33 (a-z + 0-9)</span></div>
                        <div className="dataset-stat"><span className="label">Images / class</span><span className="value">~300</span></div>
                        <div className="dataset-stat"><span className="label">Total</span><span className="value">~9,900</span></div>
                        <div className="dataset-stat"><span className="label">Purpose</span><span className="value">Display Output</span></div>
                    </div>
                </div>
            </section>

            {/* Tech Stack */}
            <section className="pipeline-section">
                <h2>Technology Stack</h2>
                <div className="pipeline-cards">
                    <div className="pipeline-card">
                        <h3>Frontend</h3>
                        <span className="tech-tag">React</span>
                        <span className="tech-tag">Vite</span>
                        <span className="tech-tag">Web Speech API</span>
                    </div>
                    <div className="pipeline-card">
                        <h3>Backend</h3>
                        <span className="tech-tag">Flask</span>
                        <span className="tech-tag">Python</span>
                        <span className="tech-tag">NLTK</span>
                    </div>
                    <div className="pipeline-card">
                        <h3>AI / ML</h3>
                        <span className="tech-tag">TensorFlow</span>
                        <span className="tech-tag">Keras</span>
                        <span className="tech-tag">CNN</span>
                    </div>
                    <div className="pipeline-card">
                        <h3>Data</h3>
                        <span className="tech-tag">42K+ Images</span>
                        <span className="tech-tag">35 Classes</span>
                    </div>
                </div>
            </section>
        </div>
    );
}
