import React, { useState } from 'react';
import './Flashcard.css';

const Flashcard = ({ flashcard }) => {
    const [flipped, setFlipped] = useState(false);

    return (
        <div
            className={`flashcard ${flipped ? 'flipped' : ''}`}
            onClick={() => setFlipped(!flipped)}
        >
            <div className="front">
                {flashcard.question}
                <div className="hint">Click to flip</div>
            </div>
            <div className="back">
                {flashcard.answer}
            </div>
        </div>
    );
};

export default Flashcard;
