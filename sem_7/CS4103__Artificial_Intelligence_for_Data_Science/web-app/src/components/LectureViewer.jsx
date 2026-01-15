import React from 'react';
import './LectureViewer.css';

const LectureViewer = ({ lecture }) => {
    return (
        <div className="lecture-viewer">
            <h2>{lecture.title}</h2>
            <div className="lecture-meta">
                <span>Date: {lecture.date}</span>
            </div>
            <div className="topics-list">
                {lecture.topics.map((topic, index) => (
                    <div key={index} className="topic-card">
                        <h3>{topic.title}</h3>
                        <p>{topic.content}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default LectureViewer;
