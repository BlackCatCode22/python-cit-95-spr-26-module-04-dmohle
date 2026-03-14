# dH 2/23/26
# create_python_chpts_7_8_9_quiz.py
# dH 2/23/26
# Dennis Mohle, Professor
# Creates a 20-question (1 point each) Canvas quiz for Python Chapters 7, 8, and 9

import time
import sys
import requests

# ----------------------------
# CONFIGURATION
# ----------------------------
# API_KEY = Hide This API Key ! Hide This API Key ! Hide This API Key !v "5496~YI8KNJaAT2qkVQTvmkhp2eJhhs2eYdhVnkBkzGOJBN03R0HsL9zrZjryuvvdXbCC"
BASE_URL = "https://scccd.instructure.com/api/v1"
COURSE_ID = "135559"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

# ----------------------------
# QUIZ SETTINGS
# ----------------------------
quiz_payload = {
    "quiz": {
        "title": "Python Quiz: Chapters 7, 8, & 9",
        "description": "20 multiple-choice questions (1 point each) covering Files, Lists, and Dictionaries.",
        "quiz_type": "assignment",
        "allowed_attempts": 3,
        "scoring_policy": "keep_highest",
        "shuffle_answers": True,
        "published": True,
    }
}

# ----------------------------
# QUESTIONS (1 point each)
# Based on Python for Everybody: Chapters 7 (Files), 8 (Lists), and 9 (Dictionaries)
# ----------------------------
questions = [
    # ---- Chapter 7: Files ----
    {"q": "Which built-in function is used to open a file in Python and returns a file handle?", "a": [("open()", 100), ("file()", 0), ("read()", 0), ("access()", 0)]},
    {"q": "What character represents a newline in Python strings?", "a": [("\\n", 100), ("\\nl", 0), ("\\next", 0), ("\\w", 0)]},
    {"q": "What happens if you try to open a file that does not exist for reading?", "a": [("The program stops with a traceback error", 100), ("The program creates the file", 0), ("The program returns None", 0), ("The program continues silently", 0)]},
    {"q": "When iterating through a file handle with a for loop, what is each 'element' processed?", "a": [("A line of text", 100), ("A single character", 0), ("A single word", 0), ("The entire file content", 0)]},
    {"q": "Which method is used to read the entire contents of a file into a single string?", "a": [("read()", 100), ("all()", 0), ("get_text()", 0), ("input()", 0)]},
    {"q": "What is the primary purpose of the 'rstrip()' method when processing file lines?", "a": [("To remove whitespace and the newline character from the right side", 100), ("To reverse the string", 0), ("To count the characters", 0), ("To split the line into words", 0)]},

    # ---- Chapter 8: Lists ----
    {"q": "In Python, which characters are used to define a list?", "a": [("Square brackets [ ]", 100), ("Parentheses ( )", 0), ("Curly braces { }", 0), ("Angle brackets < >", 0)]},
    {"q": "Lists are 'mutable'. What does this mean?", "a": [("You can change the elements within a list", 100), ("The list cannot be changed once created", 0), ("The list can only hold integers", 0), ("The list is hidden from view", 0)]},
    {"q": "Which method is used to add a new element to the end of a list?", "a": [("append()", 100), ("add()", 0), ("plus()", 0), ("extend()", 0)]},
    {"q": "What does the 'range(n)' function return?", "a": [("A list of indices from 0 to n-1", 100), ("A list of numbers from 1 to n", 0), ("The length of a list", 0), ("A random number", 0)]},
    {"q": "Which list method reorders the items in the list alphabetically or numerically?", "a": [("sort()", 100), ("order()", 0), ("arrange()", 0), ("organize()", 0)]},
    {"q": "Which string method breaks a string into a list of words?", "a": [("split()", 100), ("break()", 0), ("divide()", 0), ("listify()", 0)]},
    {"q": "What is the slice [1:3] of the list [10, 20, 30, 40]?", "a": [("[20, 30]", 100), ("[10, 20]", 0), ("[20, 30, 40]", 0), ("[30, 40]", 0)]},

    # ---- Chapter 9: Dictionaries ----
    {"q": "What is the primary difference between a list and a dictionary?", "a": [("Lists use integer indices; dictionaries use keys (often strings)", 100), ("Lists are faster", 0), ("Dictionaries are immutable", 0), ("Lists use curly braces", 0)]},
    {"q": "Which characters are used to define a dictionary?", "a": [("Curly braces { }", 100), ("Square brackets [ ]", 0), ("Parentheses ( )", 0), ("Double quotes \" \"", 0)]},
    {"q": "What happens if you try to access a key that is not in the dictionary?", "a": [("It causes a KeyError", 100), ("It returns 0", 0), ("It returns None", 0), ("The program adds the key", 0)]},
    {"q": "Which dictionary method allows you to provide a default value if a key is not found?", "a": [("get()", 100), ("fetch()", 0), ("find()", 0), ("check()", 0)]},
    {"q": "What is the term for a collection of key-value pairs in a dictionary?", "a": [("Items", 100), ("Elements", 0), ("Indices", 0), ("Lists", 0)]},
    {"q": "When used in a for loop, what does a dictionary iterate over by default?", "a": [("The keys", 100), ("The values", 0), ("The items", 0), ("The length", 0)]},
    {"q": "Which keyword is used to check if a key exists in a dictionary?", "a": [("in", 100), ("exists", 0), ("has", 0), ("find", 0)]},
]

def request_or_die(method: str, url: str, **kwargs) -> requests.Response:
    try:
        resp = requests.request(method, url, timeout=30, **kwargs)
    except requests.RequestException as e:
        print(f"NETWORK ERROR calling {url}: {e}")
        sys.exit(1)

    if resp.status_code not in (200, 201):
        print(f"HTTP {resp.status_code} ERROR calling {url}")
        try:
            print(resp.json())
        except Exception:
            print(resp.text)
        sys.exit(1)

    return resp

def run() -> None:
    # 1) Create quiz
    quiz_url = f"{BASE_URL}/courses/{COURSE_ID}/quizzes"
    res = request_or_die("POST", quiz_url, headers=headers, json=quiz_payload)

    quiz_id = res.json().get("id")
    if not quiz_id:
        print("ERROR: Quiz created but no quiz ID returned.")
        sys.exit(1)

    print(f"Created Python Quiz ID: {quiz_id}")

    # 2) Add questions
    q_url = f"{BASE_URL}/courses/{COURSE_ID}/quizzes/{quiz_id}/questions"

    for i, item in enumerate(questions, start=1):
        q_data = {
            "question": {
                "question_name": f"Q{i}",
                "question_text": item["q"],
                "question_type": "multiple_choice_question",
                "points_possible": 1,
                "answers": [{"answer_text": t, "answer_weight": w} for (t, w) in item["a"]],
            }
        }
        request_or_die("POST", q_url, headers=headers, json=q_data)
        print(f"Added Q{i}")
        time.sleep(0.2)

    print(f"\n✅ Python Quiz (Ch 7-9) successfully added to Course {COURSE_ID}!")

if __name__ == "__main__":
    run()
