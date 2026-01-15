import React, { useState } from 'react';
import { lectures } from './data/lectures';
import LectureViewer from './components/LectureViewer';
import Flashcard from './components/Flashcard';
import Quiz from './components/Quiz';
import './App.css';

function App() {
  const [currentLectureId, setCurrentLectureId] = useState(42);
  const [activeTab, setActiveTab] = useState('content');

  const currentLecture = lectures.find(l => l.id === currentLectureId);

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>AI for Data Science - Learning Portal</h1>
        <nav>
          <button
            className={activeTab === 'content' ? 'active' : ''}
            onClick={() => setActiveTab('content')}
          >
            Lecture Content
          </button>
          <button
            className={activeTab === 'flashcards' ? 'active' : ''}
            onClick={() => setActiveTab('flashcards')}
          >
            Flashcards
          </button>
          <button
            className={activeTab === 'quiz' ? 'active' : ''}
            onClick={() => setActiveTab('quiz')}
          >
            Quiz
          </button>
        </nav>
      </header>

      <main className="app-content">
        {activeTab === 'content' && (
          <LectureViewer lecture={currentLecture} />
        )}

        {activeTab === 'flashcards' && (
          <div className="flashcard-container">
            <h2>Flashcards: {currentLecture.title}</h2>
            <div className="flashcards-grid">
              {currentLecture.flashcards.map((card, index) => (
                <Flashcard key={index} flashcard={card} />
              ))}
            </div>
          </div>
        )}

        {activeTab === 'quiz' && (
          <div className="quiz-view">
            <h2>Quiz: {currentLecture.title}</h2>
            <Quiz quizData={currentLecture.quiz} />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
