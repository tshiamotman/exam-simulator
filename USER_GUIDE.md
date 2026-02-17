# User Guide: OmniStudio Practice Exam System

## Getting Started

### Installation

1. **Install Python dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Verify installation:**
```bash
python -c "import fastapi, uvicorn, pydantic; print('Dependencies OK')"
```

### Running the Application

```bash
cd backend
python app.py
```

You should see:
```
============================================================
🎓 OmniStudio Exam System
============================================================
Questions loaded: 15
Exam duration: 90 minutes
Passing score: 70.0%
Questions per exam: 15
============================================================

🚀 Starting server...
📱 Open http://localhost:8000 in your browser
```

Open your browser to `http://localhost:8000`

---

## Using the Exam System

### 1. Start Screen

When you first open the application, you'll see two modes:

#### **Exam Mode** 🎯
- Timed simulation (90 minutes default)
- No hints or explanations during the exam
- Simulates real certification exam conditions
- Results shown only at the end

**Best for:** 
- Final practice before certification
- Assessing readiness
- Building test-taking stamina

#### **Study Mode** 📚
- Untimed practice
- Immediate feedback available
- Detailed explanations for learning
- Can review answers anytime

**Best for:**
- Learning new topics
- Understanding concepts deeply
- Identifying knowledge gaps
- Building confidence

Select your mode and click "Start".

---

### 2. Taking the Exam

#### Question Display

Each question shows:
- **Topic badge**: The certification topic (DataRaptors, OmniScripts, etc.)
- **Question counter**: Current question number / Total questions
- **Question text**: The actual question
- **Answer options**: Labeled A, B, C, D, etc.

**Single Choice Questions:**
- Select one answer only
- Previously selected answer is replaced

**Multiple Choice Questions:**
- Yellow info box: "ℹ️ Select all that apply"
- Can select multiple answers
- Click to toggle selection

#### Timer (Exam Mode Only)

Top right corner shows remaining time:
- **Normal**: Blue display (10+ minutes remaining)
- **Warning**: Orange display (5-10 minutes remaining)
- **Critical**: Red pulsing display (<5 minutes remaining)

#### Question Navigator (Left Panel)

Quick overview of all questions:
- **Gray**: Unanswered
- **Green**: Answered
- **Blue**: Current question
- **Star (★)**: Bookmarked question

Click any number to jump directly to that question.

---

### 3. Navigation

#### Forward/Backward
- **Next →**: Move to next question
- **← Previous**: Move to previous question

#### Jump Navigation
- Click any question number in the navigator
- Jump instantly to that question

#### Progress Bar
Bottom of screen shows:
- Completion percentage
- Questions answered vs. total

---

### 4. Answering Questions

1. **Read the question carefully**
2. **Check if it's single or multiple choice**
3. **Click your answer(s)**
   - Selected answers highlight in blue
   - Click again to deselect (multiple choice)
4. **Move to next question or review**

**Tips:**
- You can change answers anytime before submitting
- Use the navigator to review all questions
- Bookmark difficult questions for later review

---

### 5. Submitting the Exam

When ready to finish:

1. Click **"Submit Exam"** button (red, bottom right)
2. Confirm submission in the dialog
3. Wait for results calculation

**Before submitting, verify:**
- All questions answered (check progress bar)
- Review bookmarked questions
- Double-check any uncertain answers

---

### 6. Results Screen

#### Score Display

Large percentage shows your score:
- **Green "✓ PASSED"**: Score ≥ 70%
- **Red "✗ FAILED"**: Score < 70%

Details include:
- Correct answers / Total questions
- Time taken (exam mode)

#### Performance Chart

Bar chart shows performance by topic:
- **Green bars**: Strong performance (≥65%)
- **Orange bars**: Weak areas (<65%)

#### Topic Breakdown

Detailed list showing for each topic:
- Number correct / total questions
- Percentage score
- "Focus Area" badge for weak topics

#### Recommended Study Areas

List of topics needing improvement:
- Based on < 65% threshold
- Prioritized by weakness severity

#### Question Review

Click on any topic to see:
- Your answers vs. correct answers
- Question explanations
- Topics to study

---

## Configuration

Edit `data/config.json` to customize:

```json
{
  "exam_duration_minutes": 90,        // Time limit for exam mode
  "passing_score_percentage": 70.0,   // Minimum to pass
  "questions_per_exam": 15,           // Questions per session
  "allow_review": true,               // Enable review mode
  "randomize_questions": true,        // Shuffle questions
  "randomize_answers": true,          // Shuffle answer order
  "show_explanations_in_study_mode": true,  // Study mode hints
  "weak_area_threshold_percentage": 65.0    // Weak area cutoff
}
```

**After changing config, restart the server.**

---

## Managing Questions

### Adding New Questions

1. Open `data/questions.json`
2. Add new question following this template:

```json
{
  "id": "Q999",
  "topic": "DataRaptors",
  "question_text": "Your question here?",
  "answers": [
    {"id": "A", "text": "Option A"},
    {"id": "B", "text": "Option B"},
    {"id": "C", "text": "Option C"},
    {"id": "D", "text": "Option D"}
  ],
  "correct_answers": ["B"],
  "question_type": "single_choice",
  "explanation": "Explanation of why B is correct...",
  "difficulty": "medium"
}
```

### Question Fields

- **id**: Unique identifier (e.g., "Q999")
- **topic**: One of:
  - "DataRaptors"
  - "OmniScripts"
  - "Integration Procedures"
  - "FlexCards"
  - "OmniStudio Core"
- **question_text**: The question itself
- **answers**: Array of 2-10 answer objects
  - Each has `id` (A, B, C...) and `text`
- **correct_answers**: Array of correct answer IDs
  - Single choice: `["B"]`
  - Multiple choice: `["A", "C", "D"]`
- **question_type**: 
  - `"single_choice"` or `"multiple_choice"`
- **explanation**: Why the answer is correct
- **difficulty**: `"easy"`, `"medium"`, or `"hard"`

### Validation

After adding questions, validate JSON:
```bash
python -c "import json; json.load(open('../data/questions.json'))"
```

If valid: No output
If invalid: Error message with line number

---

## Tips for Effective Study

### First Time Users
1. Start with **Study Mode** to learn
2. Take notes on weak topics
3. Review explanations carefully
4. Practice until comfortable

### Before Certification
1. Take full **Exam Mode** tests
2. Simulate real conditions (quiet space, no interruptions)
3. Time yourself strictly
4. Review weak areas after each attempt
5. Retake until consistently passing

### Tracking Progress
- Results saved in `data/results/`
- Each exam creates a JSON file
- Compare scores over time
- Focus on improving weak topics

---

## Troubleshooting

### Server won't start

**Error: "Port already in use"**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
# Then restart
python app.py
```

**Error: "Module not found"**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Questions not loading

**Check file path:**
```bash
# From backend directory
ls ../data/questions.json
```

**Validate JSON:**
```bash
python -c "import json; print(len(json.load(open('../data/questions.json'))['questions']))"
```

### Timer not working

- Clear browser cache
- Hard refresh (Ctrl+Shift+R / Cmd+Shift+R)
- Check browser console for errors

### Results not displaying

- Ensure you answered at least one question
- Check browser console for errors
- Verify session ID is valid

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| → | Next question |
| ← | Previous question |
| 1-9 | Jump to question 1-9 |
| Space | Select/deselect current focused answer |
| Enter | Submit exam (when focused on button) |

---

## Best Practices

### During Exam
1. **Read all questions carefully**
2. **Note the question type** (single vs multiple choice)
3. **Eliminate obviously wrong answers first**
4. **Bookmark uncertain questions**
5. **Don't spend too long on one question**
6. **Review all questions before submitting**

### For Study
1. **Focus on weak topics** identified in results
2. **Read all explanations**, even for correct answers
3. **Take breaks** between practice sessions
4. **Vary between exam and study mode**
5. **Track improvement over time**

### Question Management
1. **Use realistic questions** from official sources
2. **Update regularly** as platform changes
3. **Verify correct answers** before adding
4. **Write clear explanations**
5. **Balance difficulty levels**

---

## Advanced Features

### Custom Exam Sessions

Edit start request to customize:
```javascript
fetch('http://localhost:8000/api/exam/start', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    mode: 'exam',
    topics: ['DataRaptors', 'Integration Procedures'],  // Only these topics
    question_count: 20  // Custom question count
  })
})
```

### Exporting Results

Results auto-saved to `data/results/result_{session_id}.json`

To export all results:
```bash
cd data/results
# Combine all results
cat *.json > all_results.json
```

---

## Getting Help

### Common Questions

**Q: Can I pause the exam?**
A: No, exam mode simulates real conditions. Use study mode for untimed practice.

**Q: How many times can I retake?**
A: Unlimited. Each session is independent.

**Q: Are questions reused?**
A: Yes, questions are randomly selected from the bank each time.

**Q: Can I review answers before submitting?**
A: Yes, navigate freely and change answers until you submit.

**Q: What happens if time runs out?**
A: Exam auto-submits. Only answered questions are graded.

### Support

- Check logs in terminal where server is running
- Review browser console (F12) for frontend errors
- Verify file paths and permissions
- Ensure Python 3.8+ installed

---

## Next Steps

1. ✅ Complete this guide
2. 📝 Take your first practice exam
3. 📊 Review results and identify weak areas
4. 📚 Study weak topics
5. 🔄 Retake until consistently passing
6. 🎓 Schedule your certification exam!

Good luck with your OmniStudio Developer Certification! 🚀
