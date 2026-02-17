"""
Core exam engine logic for the OmniStudio Exam System.
Handles question selection, session management, and business rules.
"""

import json
import random
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from pathlib import Path
import uuid

from models import (
    Question, ExamSession, UserAnswer, ExamConfig,
    Topic, QuestionType, ExamResult, TopicPerformance, Exam
)


class ExamEngine:
    """Core exam engine that manages exam sessions and question delivery."""
    
    def __init__(self, exams_file: str = "data/exams.json",
                 config_file: str = "data/config.json"):
        """
        Initialize the exam engine.
        
        Args:
            exams_file: Path to exams JSON file
            config_file: Path to configuration JSON file
        """
        self.exams_file = Path(exams_file)
        self.config_file = Path(config_file)
        self.exams: Dict[str, Exam] = {}
        self.questions_bank: List[Question] = {}  # Will be keyed by exam_id
        self.config: ExamConfig = ExamConfig()
        self.active_sessions: Dict[str, ExamSession] = {}
        
        self._load_exams()
        self._load_config()
    
    def _load_exams(self):
        """Load exams from JSON file."""
        try:
            with open(self.exams_file, 'r') as f:
                data = json.load(f)
                for exam_data in data.get('exams', []):
                    exam = Exam(**exam_data)
                    self.exams[exam.id] = exam
            print(f"Loaded {len(self.exams)} exams from {self.exams_file}")
        except Exception as e:
            print(f"Error loading exams: {e}")
            self.exams = {}
    
    def _load_questions_for_exam(self, exam_id: str) -> List[Question]:
        """Load questions from a specific exam's questions file."""
        if exam_id not in self.exams:
            print(f"Exam {exam_id} not found")
            return []
        
        exam = self.exams[exam_id]
        questions_file = Path(exam.questions_file)
        
        try:
            with open(questions_file, 'r') as f:
                data = json.load(f)
                questions = [Question(**q) for q in data.get('questions', [])]
            print(f"Loaded {len(questions)} questions from {questions_file}")
            return questions
        except Exception as e:
            print(f"Error loading questions from {questions_file}: {e}")
            return []
    
    def _load_config(self):
        """Load configuration from JSON file."""
        try:
            with open(self.config_file, 'r') as f:
                data = json.load(f)
                self.config = ExamConfig(**data)
            print(f"Loaded configuration: {self.config.dict()}")
        except Exception as e:
            print(f"Error loading config: {e}, using defaults")
            self.config = ExamConfig()
    
    def get_exams(self) -> List[Exam]:
        """Get list of all available exams."""
        return list(self.exams.values())
    
    def get_exam(self, exam_id: str) -> Optional[Exam]:
        """Get exam details by ID."""
        return self.exams.get(exam_id)
    
    def create_exam_session(self, exam_id: str, mode: str = "exam", 
                           topics: Optional[List[str]] = None,
                           question_count: Optional[int] = None) -> ExamSession:
        """
        Create a new exam session.
        
        Args:
            exam_id: ID of the exam to take
            mode: "exam" or "study"
            topics: Optional list of topics to filter by
            question_count: Optional number of questions (defaults to exam config)
        
        Returns:
            ExamSession object
        """
        # Load exam config
        exam = self.get_exam(exam_id)
        if not exam:
            raise ValueError(f"Exam {exam_id} not found")
        
        # Load questions for this exam
        available_questions = self._load_questions_for_exam(exam_id)
        if not available_questions:
            raise ValueError(f"No questions found for exam {exam_id}")
        
        # Filter questions by topic if specified
        if topics:
            available_questions = [
                q for q in available_questions 
                if q.topic in topics
            ]
        
        # Determine number of questions
        num_questions = question_count or exam.total_questions
        num_questions = min(num_questions, len(available_questions))
        
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        
        # Select and optionally randomize questions
        selected_questions = random.sample(available_questions, num_questions) \
            if self.config.randomize_questions \
            else available_questions[:num_questions]
        
        # Optionally randomize answer order for each question
        if self.config.randomize_answers:
            for question in selected_questions:
                random.shuffle(question.answers)
        
        # Create session
        session = ExamSession(
            session_id=session_id,
            mode=mode,
            questions=selected_questions,
            start_time=datetime.now(),
            duration_minutes=exam.duration_minutes if mode == "exam" else None,
            current_question_index=0,
            user_answers=[]
        )
        
        self.active_sessions[session_id] = session
        return session

    
    def get_session(self, session_id: str) -> Optional[ExamSession]:
        """Get an active exam session."""
        return self.active_sessions.get(session_id)
    
    def submit_answer(self, session_id: str, question_id: str, 
                     selected_answers: List[str], bookmarked: bool = False) -> bool:
        """
        Submit an answer for a question.
        
        Args:
            session_id: Exam session ID
            question_id: Question ID
            selected_answers: List of selected answer IDs
            bookmarked: Whether question is bookmarked
        
        Returns:
            True if submission successful
        """
        session = self.active_sessions.get(session_id)
        if not session:
            return False
        
        # Remove existing answer for this question if any
        session.user_answers = [
            a for a in session.user_answers 
            if a.question_id != question_id
        ]
        
        # Add new answer
        user_answer = UserAnswer(
            question_id=question_id,
            selected_answers=selected_answers,
            bookmarked=bookmarked
        )
        session.user_answers.append(user_answer)
        
        return True
    
    def navigate_to_question(self, session_id: str, index: int) -> bool:
        """Navigate to a specific question by index."""
        session = self.active_sessions.get(session_id)
        if not session:
            return False
        
        if 0 <= index < len(session.questions):
            session.current_question_index = index
            return True
        return False
    
    def get_current_question(self, session_id: str) -> Optional[Question]:
        """Get the current question for a session."""
        session = self.active_sessions.get(session_id)
        if not session:
            return None
        
        if 0 <= session.current_question_index < len(session.questions):
            return session.questions[session.current_question_index]
        return None
    
    def get_user_answer(self, session_id: str, question_id: str) -> Optional[UserAnswer]:
        """Get user's answer for a specific question."""
        session = self.active_sessions.get(session_id)
        if not session:
            return None
        
        for answer in session.user_answers:
            if answer.question_id == question_id:
                return answer
        return None
    
    def is_session_expired(self, session_id: str) -> bool:
        """Check if exam session has expired (for timed exams)."""
        session = self.active_sessions.get(session_id)
        if not session or not session.duration_minutes:
            return False
        
        elapsed = datetime.now() - session.start_time
        max_duration = timedelta(minutes=session.duration_minutes)
        return elapsed > max_duration
    
    def get_remaining_time(self, session_id: str) -> Optional[int]:
        """Get remaining time in seconds for a timed exam."""
        session = self.active_sessions.get(session_id)
        if not session or not session.duration_minutes:
            return None
        
        elapsed = datetime.now() - session.start_time
        max_duration = timedelta(minutes=session.duration_minutes)
        remaining = max_duration - elapsed
        
        return max(0, int(remaining.total_seconds()))
    
    def calculate_score(self, session_id: str) -> Optional[ExamResult]:
        """
        Calculate exam score and generate detailed results.
        
        Args:
            session_id: Exam session ID
        
        Returns:
            ExamResult object with complete analytics
        """
        session = self.active_sessions.get(session_id)
        if not session:
            return None
        
        total_questions = len(session.questions)
        correct_count = 0
        topic_stats: Dict[str, Dict] = {}
        question_details = []
        
        # Calculate score and gather statistics
        for question in session.questions:
            # Get user's answer
            user_answer = self.get_user_answer(session_id, question.id)
            selected = set(user_answer.selected_answers) if user_answer else set()
            correct = set(question.correct_answers)
            
            # Check if answer is correct
            is_correct = selected == correct
            if is_correct:
                correct_count += 1
            
            # Track topic performance
            topic = question.topic
            if topic not in topic_stats:
                topic_stats[topic] = {"total": 0, "correct": 0}
            topic_stats[topic]["total"] += 1
            if is_correct:
                topic_stats[topic]["correct"] += 1
            
            # Store question details
            question_details.append({
                "question_id": question.id,
                "question_text": question.question_text,
                "topic": topic,
                "user_answers": list(selected),
                "correct_answers": list(correct),
                "is_correct": is_correct,
                "explanation": question.explanation,
                "bookmarked": user_answer.bookmarked if user_answer else False
            })
        
        # Calculate overall score
        score_percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
        passed = score_percentage >= self.config.passing_score_percentage
        
        # Calculate topic performance
        topic_performance = []
        weak_areas = []
        
        for topic, stats in topic_stats.items():
            percentage = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
            is_weak = percentage < self.config.weak_area_threshold_percentage
            
            topic_performance.append(TopicPerformance(
                topic=topic,
                total_questions=stats["total"],
                correct_answers=stats["correct"],
                percentage=round(percentage, 1),
                is_weak_area=is_weak
            ))
            
            if is_weak:
                weak_areas.append(topic)
        
        # Sort by percentage (lowest first for weak areas)
        topic_performance.sort(key=lambda x: x.percentage)
        
        # Calculate time taken
        time_taken = (datetime.now() - session.start_time).total_seconds() / 60
        
        # Create result object
        result = ExamResult(
            session_id=session_id,
            exam_mode=session.mode,
            total_questions=total_questions,
            correct_answers=correct_count,
            score_percentage=round(score_percentage, 1),
            passed=passed,
            time_taken_minutes=int(time_taken),
            completion_date=datetime.now(),
            topic_performance=topic_performance,
            weak_areas=weak_areas,
            question_details=question_details
        )
        
        # Save result to file
        self._save_result(result)
        
        return result
    
    def _save_result(self, result: ExamResult):
        """Save exam result to file for historical tracking."""
        results_dir = Path("../data/results")
        results_dir.mkdir(exist_ok=True)
        
        filename = results_dir / f"result_{result.session_id}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(result.dict(), f, indent=2, default=str)
            print(f"Saved result to {filename}")
        except Exception as e:
            print(f"Error saving result: {e}")
    
    def get_statistics(self, exam_id: Optional[str] = None) -> Dict:
        """
        Get statistics from question bank.
        
        Args:
            exam_id: Optional exam ID to get statistics for. If not provided, returns stats for all exams.
        
        Returns:
            Dictionary with statistics
        """
        if exam_id:
            # Get statistics for a specific exam
            questions = self._load_questions_for_exam(exam_id)
            total = len(questions)
            by_topic = {}
            by_difficulty = {"easy": 0, "medium": 0, "hard": 0}
            
            for q in questions:
                # Count by topic
                topic = q.topic
                by_topic[topic] = by_topic.get(topic, 0) + 1
                
                # Count by difficulty
                if q.difficulty:
                    by_difficulty[q.difficulty] += 1
            
            return {
                "exam_id": exam_id,
                "total_questions": total,
                "by_topic": by_topic,
                "by_difficulty": by_difficulty
            }
        else:
            # Get statistics for all exams
            all_stats = {}
            for exam_id in self.exams.keys():
                all_stats[exam_id] = self.get_statistics(exam_id)
            return {
                "by_exam": all_stats,
                "total_exams": len(all_stats)
            }

