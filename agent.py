from crewai import Agent, LLM

from config import GROQ_API_KEY, MODEL_NAME

from tools import (
    save_student_memory,
    recall_student_memory,
    get_recent_memories,
    calculator
)


def create_study_tutor():

    groq_llm = LLM(
        model=f"groq/{MODEL_NAME}",
        api_key=GROQ_API_KEY,
        temperature=0.3
    )

    tutor = Agent(
        role="Study Tutor",

        goal=(
            "Help students understand academic concepts, "
            "answer questions, create useful explanations, "
            "and remember important information about their "
            "learning goals and preferences."
        ),

        backstory=(
            "You are an experienced and patient academic tutor. "
            "You explain difficult concepts in simple language. "
            "You use examples and analogies when useful. "
            "You adapt explanations to the student's level. "
            "You provide constructive feedback and encourage "
            "the student to learn rather than simply giving answers."
        ),

        llm=groq_llm,

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
