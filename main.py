from fastapi import FastAPI, Request, Form
from fasthtml.common import *
import os
from datetime import datetime
import pytz
from supabase import create_client, Client
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse

# Load environment variables
load_dotenv()

# Constants for input character limits and timestamp format
MAX_NAME_CHAR = 50
TIMESTAMP_FMT = "%Y-%m-%d %I:%M:%S %p CET"

# Initialize Supabase client
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def get_cet_time():
    cet_tz = pytz.timezone("CET")
    return datetime.now(cet_tz)

def get_questions():
    response = supabase.table("quiz").select("*").execute()
    return response.data

def submit_answers(name, answers):
    timestamp = get_cet_time().strftime(TIMESTAMP_FMT)
    score = calculate_score(answers)
    try:
        supabase.table("quiz_results").insert(
            {"name": name, "score": score, "timestamp": timestamp}
        ).execute()
    except Exception as e:
        return f"Error submitting answers: {str(e)}"
    return score

def calculate_score(answers):
    questions = get_questions()
    score = 0
    for question in questions:
        answer = answers.get(str(question['id']))
        if answer == question['correct_choice']:
            score += 1
    return score

def render_question(question):
    return Fieldset(
        Legend(question['question']),
        Input(type="radio", name=f"{question['id']}", value="A", required=True),
        Label(question['choice_a']),
        Br(),
        Input(type="radio", name=f"{question['id']}", value="B"),
        Label(question['choice_b']),
        Br(),
        Input(type="radio", name=f"{question['id']}", value="C"),
        Label(question['choice_c']),
        Br(),
        Input(type="radio", name=f"{question['id']}", value="D"),
        Label(question['choice_d']),
        Br(),
    )

app, rt = fast_app()

def render_quiz_form():
    questions = get_questions()
    return Form(
        Input(
            type="text",
            name="name",
            placeholder="Your Name",
            required=True,
            maxlength=MAX_NAME_CHAR,
        ),
        *[render_question(question) for question in questions],
        Button("Submit", type="submit"),
        method="post",
        hx_post="/submit-quiz",
        hx_target="#result",
        hx_swap="innerHTML",
    )

def render_content():
    return Div(
       
        P(Em("Test your knowledge!")),
        render_quiz_form(),
        Div(id="result"),
        Hr(),
       
    )

@rt("/", methods=["GET"])
def get():
    return Titled("Quiz Application 📝", render_content())

@rt("/submit-quiz", methods=["POST"])
async def post(request: Request):
    form_data = await request.form()
    name = form_data.get('name', '')
    answers = {key: value for key, value in form_data.items() if key != 'name'}
    score = submit_answers(name, answers)
    total = len(get_questions())
    
    # Redirect to the score page with score and total as query parameters
    return RedirectResponse(url=f"/score?score={score}&total={total}", status_code=303)

@rt("/score", methods=["GET"])
def display_score(request: Request):
    score = request.query_params.get("score", "0")
    total = request.query_params.get("total", "0")
    return Titled(
        "Quiz Score 🏆",
        Div(
            P(f"You scored {score} out of {total}"),
            A("Take the quiz again", href="/", hx_boost="true"),
        )
    )

serve()
