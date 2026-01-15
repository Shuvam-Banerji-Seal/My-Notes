import React, { useState } from 'react';
import './Quiz.css';

const Quiz = ({ quizData }) => {
    const [currentQuestion, setCurrentQuestion] = useState(0);
    const [score, setScore] = useState(0);
    const [showScore, setShowScore] = useState(false);

    const handleAnswerOptionClick = (selectedOption) => {
        if (selectedOption === quizData[currentQuestion].correctAnswer) {
            setScore(score + 1);
        }

        const nextQuestion = currentQuestion + 1;
        if (nextQuestion < quizData.length) {
            setCurrentQuestion(nextQuestion);
        } else {
            setShowScore(true);
        }
    };

    const resetQuiz = () => {
        setCurrentQuestion(0);
        setScore(0);
        setShowScore(false);
    };

    return (
        <div className="quiz-container">
            {showScore ? (
                <div className="score-section">
                    You scored {score} out of {quizData.length}
                    <button onClick={resetQuiz} className="reset-button">Restart Quiz</button>
                </div>
            ) : (
                <>
                    <div className="question-section">
                        <div className="question-count">
                            <span>Question {currentQuestion + 1}</span>/{quizData.length}
                        </div>
                        <div className="question-text">{quizData[currentQuestion].question}</div>
                    </div>
                    <div className="answer-section">
                        {quizData[currentQuestion].options.map((option, index) => (
                            <button
                                key={index}
                                className="answer-button"
                                onClick={() => handleAnswerOptionClick(option)}
                            >
                                {option}
                            </button>
                        ))}
                    </div>
                </>
            )}
        </div>
    );
};

export default Quiz;
