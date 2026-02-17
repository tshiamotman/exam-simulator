"""
Data models for the OmniStudio Exam System.
Using Pydantic for validation and serialization.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime
from enum import Enum


class QuestionType(str, Enum):
    """Type of question."""
    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"


class Topic(str, Enum):
    """OmniStudio certification topics."""
    DATA_RAPTORS = "DataRaptors"
    OMNISCRIPTS = "OmniScripts"
    INTEGRATION_PROCEDURES = "Integration Procedures"
    FLEX_CARDS = "FlexCards"
    OMNISTUDIO_CORE = "OmniStudio Core"


class Answer(BaseModel):
    """Individual answer option."""
    id: str = Field(..., description="Unique answer identifier (A, B, C, D, etc.)")
    text: str = Field(..., description="Answer text")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "A",
                "text": "Update Salesforce records"
            }
        }


class Question(BaseModel):
    """Exam question model."""
    id: str = Field(..., description="Unique question identifier")
    topic: Topic = Field(..., description="Question topic/category")
    question_text: str = Field(..., description="The question itself")
    answers: List[Answer] = Field(..., min_items=2, description="Answer options")
    correct_answers: List[str] = Field(..., min_items=1, description="Correct answer IDs")
    question_type: QuestionType = Field(..., description="Single or multiple choice")
    explanation: Optional[str] = Field(None, description="Explanation of correct answer")
    difficulty: Optional[Literal["easy", "medium", "hard"]] = Field("medium", description="Question difficulty")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "Q001",
                "topic": "DataRaptors",
                "question_text": "What is the primary purpose of a DataRaptor Extract?",
                "answers": [
                    {"id": "A", "text": "Update Salesforce records"},
                    {"id": "B", "text": "Read Salesforce data"},
                    {"id": "C", "text": "Orchestrate external services"},
                    {"id": "D", "text": "Render UI components"}
                ],
                "correct_answers": ["B"],
                "question_type": "single_choice",
                "explanation": "DataRaptor Extract is specifically designed to read and retrieve data from Salesforce.",
                "difficulty": "easy"
            }
        }


class UserAnswer(BaseModel):
    """User's answer to a question."""
    question_id: str
    selected_answers: List[str]
    time_spent_seconds: Optional[int] = None
    bookmarked: bool = False


class ExamSession(BaseModel):
    """Active exam session."""
    session_id: str
    mode: Literal["exam", "study"] = "exam"
    questions: List[Question]
    start_time: datetime
    duration_minutes: Optional[int] = None
    current_question_index: int = 0
    user_answers: List[UserAnswer] = []
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TopicPerformance(BaseModel):
    """Performance breakdown by topic."""
    topic: str
    total_questions: int
    correct_answers: int
    percentage: float
    is_weak_area: bool = False


class ExamResult(BaseModel):
    """Exam results and analytics."""
    session_id: str
    exam_mode: Literal["exam", "study"]
    total_questions: int
    correct_answers: int
    score_percentage: float
    passed: bool
    time_taken_minutes: Optional[int] = None
    completion_date: datetime
    topic_performance: List[TopicPerformance]
    weak_areas: List[str]
    question_details: List[dict]  # Detailed results per question
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ExamConfig(BaseModel):
    """System configuration."""
    exam_duration_minutes: int = 90
    passing_score_percentage: float = 70.0
    questions_per_exam: int = 60
    allow_review: bool = True
    randomize_questions: bool = True
    randomize_answers: bool = True
    show_explanations_in_study_mode: bool = True
    weak_area_threshold_percentage: float = 65.0


class Exam(BaseModel):
    """Available exam."""
    id: str = Field(..., description="Unique exam identifier")
    name: str = Field(..., description="Exam name")
    description: str = Field(..., description="Exam description")
    questions_file: str = Field(..., description="Path to questions JSON file")
    duration_minutes: int = Field(..., description="Exam duration in minutes")
    passing_score: float = Field(..., description="Required passing score percentage")
    total_questions: int = Field(..., description="Total number of questions in exam")
    topics: Optional[List[str]] = Field(None, description="Topics covered in exam")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "omnistudio-dev",
                "name": "OmniStudio Developer Certification",
                "description": "Comprehensive exam for OmniStudio Developer Certification",
                "questions_file": "data/questions.json",
                "duration_minutes": 90,
                "passing_score": 70.0,
                "total_questions": 60,
                "topics": ["DataRaptors", "OmniScripts", "Integration Procedures"]
            }
        }


class StartExamRequest(BaseModel):
    """Request to start a new exam."""
    exam_id: str = Field(..., description="ID of the exam to start")
    mode: Literal["exam", "study"] = "exam"
    topics: Optional[List[str]] = None
    question_count: Optional[int] = None


class SubmitAnswerRequest(BaseModel):
    """Submit an answer for a question."""
    session_id: str
    question_id: str
    selected_answers: List[str]
    bookmarked: bool = False
