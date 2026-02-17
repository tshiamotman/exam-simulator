"""
FastAPI backend for OmniStudio Exam System.
Provides REST API for exam delivery and result tracking.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List, Optional
import uvicorn

from models import (
    Question, ExamSession, StartExamRequest, SubmitAnswerRequest,
    ExamResult, ExamConfig, UserAnswer, Exam
)
from exam_engine import ExamEngine

# Initialize FastAPI app
app = FastAPI(
    title="OmniStudio Exam System API",
    description="REST API for certification exam simulation",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize exam engine
engine = ExamEngine()


@app.get("/")
async def root():
    """Serve the main exam interface."""
    return FileResponse("exam.html")


@app.get("/api/config")
async def get_config() -> ExamConfig:
    """
    Get system configuration.
    
    Returns:
        ExamConfig object with all settings
    """
    return engine.config


@app.get("/api/exams")
async def get_exams() -> List[dict]:
    """
    Get list of all available exams.
    
    Returns:
        List of exam dictionaries
    """
    exams = engine.get_exams()
    # Explicitly convert to dict to ensure proper serialization
    return [exam.dict() for exam in exams]


@app.get("/api/exams/{exam_id}")
async def get_exam(exam_id: str) -> Exam:
    """
    Get details for a specific exam.
    
    Args:
        exam_id: Exam identifier
    
    Returns:
        Exam object
    """
    exam = engine.get_exam(exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail=f"Exam {exam_id} not found")
    return exam


@app.get("/api/statistics")
async def get_statistics(exam_id: Optional[str] = None):
    """
    Get question bank statistics.
    
    Args:
        exam_id: Optional exam ID to get statistics for
    
    Returns:
        Statistics about available questions
    """
    return engine.get_statistics(exam_id)


@app.post("/api/exam/start")
async def start_exam(request: StartExamRequest) -> ExamSession:
    """
    Start a new exam session.
    
    Args:
        request: Exam configuration (exam_id, mode, topics, question count)
    
    Returns:
        ExamSession with questions and session ID
    """
    try:
        session = engine.create_exam_session(
            exam_id=request.exam_id,
            mode=request.mode,
            topics=request.topics,
            question_count=request.question_count
        )
        return session
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/exam/{session_id}")
async def get_session(session_id: str) -> ExamSession:
    """
    Get exam session details.
    
    Args:
        session_id: Unique session identifier
    
    Returns:
        ExamSession object
    """
    session = engine.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@app.get("/api/exam/{session_id}/question")
async def get_current_question(session_id: str) -> dict:
    """
    Get current question for a session.
    
    Args:
        session_id: Unique session identifier
    
    Returns:
        Current question with metadata
    """
    session = engine.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    question = engine.get_current_question(session_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Get user's answer if exists
    user_answer = engine.get_user_answer(session_id, question.id)
    
    # Get remaining time for timed exams
    remaining_time = engine.get_remaining_time(session_id)
    
    return {
        "question": question,
        "question_number": session.current_question_index + 1,
        "total_questions": len(session.questions),
        "user_answer": user_answer,
        "remaining_time_seconds": remaining_time,
        "is_expired": engine.is_session_expired(session_id)
    }


@app.post("/api/exam/{session_id}/answer")
async def submit_answer(session_id: str, request: SubmitAnswerRequest) -> dict:
    """
    Submit an answer for the current question.
    
    Args:
        session_id: Unique session identifier
        request: Answer submission data
    
    Returns:
        Success status
    """
    success = engine.submit_answer(
        session_id=session_id,
        question_id=request.question_id,
        selected_answers=request.selected_answers,
        bookmarked=request.bookmarked
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to submit answer")
    
    return {"success": True}


@app.post("/api/exam/{session_id}/navigate/{direction}")
async def navigate_question(session_id: str, direction: str) -> dict:
    """
    Navigate to next or previous question.
    
    Args:
        session_id: Unique session identifier
        direction: "next" or "previous"
    
    Returns:
        Updated question number
    """
    session = engine.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    current_index = session.current_question_index
    
    if direction == "next":
        new_index = min(current_index + 1, len(session.questions) - 1)
    elif direction == "previous":
        new_index = max(current_index - 1, 0)
    else:
        raise HTTPException(status_code=400, detail="Invalid direction")
    
    engine.navigate_to_question(session_id, new_index)
    
    return {
        "current_index": new_index,
        "question_number": new_index + 1
    }


@app.post("/api/exam/{session_id}/jump/{question_number}")
async def jump_to_question(session_id: str, question_number: int) -> dict:
    """
    Jump to a specific question number.
    
    Args:
        session_id: Unique session identifier
        question_number: Question number (1-based)
    
    Returns:
        Updated question index
    """
    session = engine.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Convert to 0-based index
    index = question_number - 1
    
    if not engine.navigate_to_question(session_id, index):
        raise HTTPException(status_code=400, detail="Invalid question number")
    
    return {"current_index": index}


@app.get("/api/exam/{session_id}/progress")
async def get_progress(session_id: str) -> dict:
    """
    Get exam progress summary.
    
    Args:
        session_id: Unique session identifier
    
    Returns:
        Progress statistics
    """
    session = engine.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    total = len(session.questions)
    answered = len(session.user_answers)
    bookmarked = sum(1 for a in session.user_answers if a.bookmarked)
    
    return {
        "total_questions": total,
        "answered": answered,
        "unanswered": total - answered,
        "bookmarked": bookmarked,
        "completion_percentage": round((answered / total * 100) if total > 0 else 0, 1)
    }


@app.post("/api/exam/{session_id}/submit")
async def submit_exam(session_id: str) -> ExamResult:
    """
    Submit exam for grading.
    
    Args:
        session_id: Unique session identifier
    
    Returns:
        ExamResult with complete scoring and analytics
    """
    result = engine.calculate_score(session_id)
    if not result:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return result


@app.get("/api/exam/{session_id}/review")
async def get_review_data(session_id: str) -> dict:
    """
    Get all questions with answers for review.
    
    Args:
        session_id: Unique session identifier
    
    Returns:
        All questions with user answers and correct answers
    """
    session = engine.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    review_data = []
    for i, question in enumerate(session.questions):
        user_answer = engine.get_user_answer(session_id, question.id)
        
        review_data.append({
            "question_number": i + 1,
            "question": question,
            "user_answer": user_answer,
            "is_correct": set(user_answer.selected_answers) == set(question.correct_answers) 
                         if user_answer else False
        })
    
    return {"questions": review_data}


if __name__ == "__main__":
    print("=" * 60)
    print("🎓 OmniStudio Exam System")
    print("=" * 60)
    print(f"Questions loaded: {len(engine.questions_bank)}")
    print(f"Exam duration: {engine.config.exam_duration_minutes} minutes")
    print(f"Passing score: {engine.config.passing_score_percentage}%")
    print(f"Questions per exam: {engine.config.questions_per_exam}")
    print("=" * 60)
    print("\n🚀 Starting server...")
    print("📱 Open http://localhost:8000 in your browser\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
