# Fasthtml Quiz Application
## Overview

This is a FastAPI-based quiz application that allows users to take a quiz, submit their answers, and see their scores. The application uses Supabase for storing quiz questions and results and supports handling user input and rendering quiz questions dynamically.

## Features

- Dynamic quiz questions fetched from Supabase.
- User can submit answers and get a score.
- Score is saved to a Supabase database with a timestamp.
- Results page displays the score and allows the user to retake the quiz.

## Prerequisites

- Python 3.11 or later
- FastAPI
- `fasthtml`
- Supabase account
- PostgreSQL database (used by Supabase)
- `dotenv` for managing environment variables
- uvicorn(server)
  
### Install dependencies:
     pip install fastapi fasthtml supabase-python python-dotenv pytz

### Create a .env file in the root directory of the project with the following content:
    SUPABASE_URL=<your-supabase-url>
    SUPABASE_KEY=<your-supabase-key>
    
### Create tables in Supabase:

Ensure you have two tables created in your Supabase database(quiz,quiz_results):

quiz with columns: id, question, choice_a, choice_b, choice_c, choice_d, correct_choice.
quiz_results with columns: id, name, score, timestamp.

### ## deployment
[Click me to see the output](https://fasthtml-quiz-29bf.vercel.app/)
