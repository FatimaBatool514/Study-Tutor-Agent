from crewai import Agent, LLM

from config import GROQ_API_KEY, MODEL_NAME

from tools import (
    save_student_memory,
    recall_student_memory,
    get_recent_memories,
    calculator
)


def create_study_tutor():

    llm = LLM(
        model=f"groq/{MODEL_NAME}",
        api_key=GROQ_API_KEY,
        temperature=0.3
    )

    tutor = Agent(
        role="Study Tutor",

        goal=(
            "Help students understand academic concepts, "
            "answer questions, provide explanations, "
            "and remember useful information about "
            "their learning."
        ),

        backstory=(
            "You are a friendly and patient AI study tutor. "
            "You explain difficult concepts in simple language. "
            "You adapt explanations to the student's level. "
            "You use examples when helpful and encourage "
            "students to understand concepts."
        ),

        llm=llm,

        tools=[
            save_student_memory,
            recall_student_memory,
            get_recent_memories,
            calculator
        ],

        verbose=True,

        allow_delegation=False
    )

    return tutor
