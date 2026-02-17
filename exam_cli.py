"""
CLI Version of OmniStudio Exam System
Simple terminal-based interface for the exam
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import sys

# Color codes for terminal
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def clear_screen():
    """Clear terminal screen."""
    print('\033[2J\033[H', end='')

def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(70)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.END}\n")

def print_question(question: Dict, number: int, total: int):
    """Print a formatted question."""
    clear_screen()
    
    # Topic badge
    topic = question['topic']
    print(f"{Colors.YELLOW}Topic: {topic}{Colors.END}")
    print(f"{Colors.CYAN}Question {number}/{total}{Colors.END}\n")
    
    # Question text
    print(f"{Colors.BOLD}{question['question_text']}{Colors.END}\n")
    
    # Hint for multiple choice
    if question['question_type'] == 'multiple_choice':
        print(f"{Colors.YELLOW}ℹ️  Select all that apply (comma-separated){Colors.END}\n")
    
    # Answer options
    for answer in question['answers']:
        print(f"  {Colors.BOLD}{answer['id']}{Colors.END}) {answer['text']}")
    
    print()

def get_user_input(question: Dict, current_answer: List[str] = None) -> List[str]:
    """Get user's answer input."""
    if current_answer:
        print(f"{Colors.GREEN}Current answer: {', '.join(current_answer)}{Colors.END}")
    
    prompt = "Your answer (or 'n' for next, 'p' for previous, 'q' to quit): "
    user_input = input(prompt).strip().upper()
    
    # Navigation commands
    if user_input in ['N', 'P', 'Q']:
        return [user_input]
    
    # Parse answers
    if question['question_type'] == 'single_choice':
        if user_input and user_input[0] in [a['id'] for a in question['answers']]:
            return [user_input[0]]
        else:
            print(f"{Colors.RED}Invalid answer. Please try again.{Colors.END}")
            time.sleep(1)
            return get_user_input(question, current_answer)
    else:
        # Multiple choice - comma separated
        answers = [a.strip() for a in user_input.split(',')]
        valid_ids = [a['id'] for a in question['answers']]
        
        if all(ans in valid_ids for ans in answers):
            return answers
        else:
            print(f"{Colors.RED}Invalid answer(s). Please try again.{Colors.END}")
            time.sleep(1)
            return get_user_input(question, current_answer)

def calculate_results(questions: List[Dict], user_answers: Dict) -> Dict:
    """Calculate exam results."""
    total = len(questions)
    correct = 0
    topic_stats = {}
    question_details = []
    
    for question in questions:
        q_id = question['id']
        user_ans = set(user_answers.get(q_id, []))
        correct_ans = set(question['correct_answers'])
        
        is_correct = user_ans == correct_ans
        if is_correct:
            correct += 1
        
        # Topic stats
        topic = question['topic']
        if topic not in topic_stats:
            topic_stats[topic] = {'total': 0, 'correct': 0}
        topic_stats[topic]['total'] += 1
        if is_correct:
            topic_stats[topic]['correct'] += 1
        
        # Question details
        question_details.append({
            'question': question['question_text'],
            'topic': topic,
            'user_answers': list(user_ans),
            'correct_answers': list(correct_ans),
            'is_correct': is_correct
        })
    
    # Calculate percentages
    score_pct = (correct / total * 100) if total > 0 else 0
    
    topic_performance = []
    weak_areas = []
    for topic, stats in topic_stats.items():
        pct = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
        topic_performance.append({
            'topic': topic,
            'total': stats['total'],
            'correct': stats['correct'],
            'percentage': pct
        })
        if pct < 65:
            weak_areas.append(topic)
    
    # Sort by percentage
    topic_performance.sort(key=lambda x: x['percentage'])
    
    return {
        'total': total,
        'correct': correct,
        'score_percentage': score_pct,
        'passed': score_pct >= 70,
        'topic_performance': topic_performance,
        'weak_areas': weak_areas,
        'question_details': question_details
    }

def display_results(results: Dict):
    """Display exam results."""
    clear_screen()
    print_header("EXAM RESULTS")
    
    # Score
    score = results['score_percentage']
    passed = results['passed']
    
    if passed:
        print(f"{Colors.GREEN}{Colors.BOLD}{'PASSED!'.center(70)}{Colors.END}")
    else:
        print(f"{Colors.RED}{Colors.BOLD}{'FAILED'.center(70)}{Colors.END}")
    
    print(f"\n{Colors.BOLD}Score: {score:.1f}%{Colors.END}")
    print(f"Correct: {results['correct']} / {results['total']}\n")
    
    # Topic performance
    print(f"{Colors.BOLD}Performance by Topic:{Colors.END}\n")
    for topic_perf in results['topic_performance']:
        topic = topic_perf['topic']
        pct = topic_perf['percentage']
        correct = topic_perf['correct']
        total = topic_perf['total']
        
        # Color based on performance
        if pct >= 80:
            color = Colors.GREEN
        elif pct >= 65:
            color = Colors.YELLOW
        else:
            color = Colors.RED
        
        weak_badge = " ⚠️  FOCUS AREA" if topic in results['weak_areas'] else ""
        print(f"  {topic:30s} {color}{pct:5.1f}%{Colors.END} ({correct}/{total}){weak_badge}")
    
    # Weak areas
    if results['weak_areas']:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}Recommended Focus Areas:{Colors.END}")
        for area in results['weak_areas']:
            print(f"  • {area}")
    
    print()

def load_exams() -> Dict:
    """Load available exams from JSON file."""
    exams_file = Path("data/exams.json")
    try:
        with open(exams_file, 'r') as f:
            data = json.load(f)
            return {exam['id']: exam for exam in data.get('exams', [])}
    except Exception as e:
        print(f"{Colors.RED}Error loading exams: {e}{Colors.END}")
        return {}

def select_exam(exams: Dict) -> Optional[Dict]:
    """Display exam selection menu and return selected exam."""
    if not exams:
        print(f"{Colors.RED}No exams available.{Colors.END}")
        return None
    
    clear_screen()
    print_header("SELECT AN EXAM")
    
    exam_list = list(exams.values())
    for i, exam in enumerate(exam_list, 1):
        print(f"{Colors.CYAN}{i}){Colors.END} {exam['name']}")
        print(f"   {exam['description']}")
        print(f"   Questions: {exam['total_questions']} | Duration: {exam['duration_minutes']} min")
        print()
    
    print(f"{Colors.CYAN}0){Colors.END} Exit")
    print()
    
    while True:
        try:
            choice = input(f"{Colors.YELLOW}Select exam (0-{len(exam_list)}): {Colors.END}").strip()
            choice_num = int(choice)
            
            if choice_num == 0:
                return None
            elif 1 <= choice_num <= len(exam_list):
                return exam_list[choice_num - 1]
            else:
                print(f"{Colors.RED}Invalid selection. Try again.{Colors.END}")
        except ValueError:
            print(f"{Colors.RED}Please enter a valid number.{Colors.END}")

def run_exam():
    """Run the CLI exam."""
    # Load exams
    exams = load_exams()
    if not exams:
        return
    
    # Select exam
    selected_exam = select_exam(exams)
    if not selected_exam:
        print(f"{Colors.YELLOW}No exam selected. Exiting.{Colors.END}")
        return
    
    # Load questions for selected exam
    questions_file = Path(selected_exam['questions_file'])
    try:
        with open(questions_file, 'r') as f:
            data = json.load(f)
            questions = data['questions']
    except Exception as e:
        print(f"{Colors.RED}Error loading questions: {e}{Colors.END}")
        return
    
    # Welcome screen
    clear_screen()
    print_header(selected_exam['name'].upper())
    print(f"{Colors.CYAN}{selected_exam['description']}{Colors.END}\n")
    print(f"Total Questions: {len(questions)}")
    print(f"Duration: {selected_exam['duration_minutes']} minutes")
    print(f"Passing Score: {selected_exam['passing_score']}%")
    print(f"\nControls:")
    print(f"  • Enter answer letter(s)")
    print(f"  • 'n' = next question")
    print(f"  • 'p' = previous question")
    print(f"  • 'q' = quit exam\n")
    
    input("Press Enter to start...")
    
    # Exam state
    current_index = 0
    user_answers = {}
    start_time = time.time()
    
    # Main exam loop
    while True:
        question = questions[current_index]
        q_id = question['id']
        current_answer = user_answers.get(q_id, [])
        
        print_question(question, current_index + 1, len(questions))
        answer = get_user_input(question, current_answer)
        
        # Handle navigation
        if answer[0] == 'Q':
            if input("Are you sure you want to quit? (y/n): ").lower() == 'y':
                break
            continue
        elif answer[0] == 'N':
            if current_index < len(questions) - 1:
                current_index += 1
            else:
                print(f"{Colors.YELLOW}This is the last question.{Colors.END}")
                time.sleep(1)
            continue
        elif answer[0] == 'P':
            if current_index > 0:
                current_index -= 1
            else:
                print(f"{Colors.YELLOW}This is the first question.{Colors.END}")
                time.sleep(1)
            continue
        
        # Save answer
        user_answers[q_id] = answer
        
        # Auto-advance to next question
        if current_index < len(questions) - 1:
            current_index += 1
        else:
            # Last question - ask to submit
            if input(f"\n{Colors.YELLOW}Last question answered. Submit exam? (y/n): {Colors.END}").lower() == 'y':
                break
    
    # Calculate results
    elapsed_time = (time.time() - start_time) / 60
    results = calculate_results(questions, user_answers)
    
    # Display results
    display_results(results)
    
    # Save results
    results_dir = Path("data/results")
    results_dir.mkdir(exist_ok=True)
    
    result_file = results_dir / f"cli_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    results['exam_id'] = selected_exam['id']
    results['exam_name'] = selected_exam['name']
    results['time_taken_minutes'] = int(elapsed_time)
    results['completion_date'] = datetime.now().isoformat()
    
    with open(result_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"{Colors.GREEN}Results saved to: {result_file}{Colors.END}\n")

if __name__ == "__main__":
    try:
        run_exam()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Exam interrupted.{Colors.END}")
        sys.exit(0)
