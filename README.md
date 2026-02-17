# OmniStudio Practice Exam System

A comprehensive exam simulation platform for Salesforce OmniStudio Developer Certification preparation.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Web UI)                        │
│  - React-based exam interface                               │
│  - Timer, navigation, progress tracking                     │
│  - Results visualization                                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ HTTP/JSON
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                Backend (FastAPI)                             │
│  - Question management                                       │
│  - Session handling                                          │
│  - Scoring engine                                            │
│  - Analytics                                                 │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ File I/O
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                Data Layer (JSON)                             │
│  - questions.json: Question bank                            │
│  - results.json: Historical results                         │
│  - config.json: System configuration                        │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```
omnistudio-exam/
├── backend/
│   ├── app.py                 # FastAPI application
│   ├── models.py              # Data models
│   ├── exam_engine.py         # Core exam logic
│   ├── scoring.py             # Scoring & analytics
│   └── requirements.txt       # Python dependencies
├── data/
│   ├── questions.json         # Question bank
│   ├── config.json            # Configuration
│   └── results/               # Exam results history
├── frontend/
│   └── exam.html              # Single-page application
├── docs/
│   ├── DESIGN.md              # Design decisions
│   └── API.md                 # API documentation
└── README.md
```

## Technology Stack

**Backend**: FastAPI
- Fast, modern Python web framework
- Automatic API documentation
- Easy to extend and maintain
- Built-in validation with Pydantic

**Frontend**: React (via CDN)
- Single HTML file - no build process needed
- Interactive UI with state management
- Professional exam experience

**Why Web App over CLI?**
1. **Better UX**: Visual timer, progress bars, color-coded results
2. **Rich Interactivity**: Navigate questions easily, bookmark, review flagged items
3. **Results Visualization**: Charts and graphs for performance analysis
4. **Accessibility**: Works on any device with a browser
5. **Scalable**: Easy to add features like question images, code syntax highlighting

## Features

### Exam Modes
- **Exam Mode**: Timed, no hints, full simulation
- **Study Mode**: Untimed, shows explanations, review mode

### Question Management
- Load from JSON
- Randomization
- Topic-based filtering
- Multi-select and single-select support

### Results & Analytics
- Real-time scoring
- Topic-based performance breakdown
- Historical tracking
- Weakness identification
- Exportable results

### User Experience
- Question bookmarking
- Previous/Next navigation
- Progress indicator
- Responsive design
- Keyboard shortcuts

## Quick Start

1. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

2. Run the server:
```bash
cd backend
python app.py
```

3. Open browser:
```
http://localhost:8000
```

## Configuration

Edit `data/config.json`:
```json
{
  "exam_duration_minutes": 90,
  "passing_score_percentage": 70,
  "questions_per_exam": 60,
  "allow_review": true
}
```

## Data Model

See `data/questions.json` for the question schema.

## Extension Ideas

- [ ] Question difficulty levels
- [ ] Adaptive testing (focus on weak areas)
- [ ] Multiple exam templates
- [ ] User authentication
- [ ] Progress tracking across sessions
- [ ] Export to PDF
- [ ] Mobile app
- [ ] Spaced repetition algorithm
