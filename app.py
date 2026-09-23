import streamlit as st

from memory import (
    create_database,
    get_memories
)

from agent import create_study_tutor

from ui import (
    load_custom_css,
    render_header,
    render_metric_cards,
    render_sidebar
)


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Study Tutor AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# LOAD UI
# ==================================================

load_custom_css()


# ==================================================
# DATABASE
# ==================================================

create_database()


# ==================================================
# SESSION STATE
# ==================================================

if "tutor" not in st.session_state:

    st.session_state.tutor = create_study_tutor()


if "messages" not in st.session_state:

    st.session_state.messages = []


# ==================================================
# HEADER
# ==================================================

render_header()


# ==================================================
# SIDEBAR
# ==================================================

settings = render_sidebar()


subject = settings["subject"]

level = settings["level"]

learning_mode = settings["learning_mode"]


# ==================================================
# METRICS
# ==================================================

render_metric_cards()


st.markdown("<br>", unsafe_allow_html=True)


# ==================================================
# MEMORY PANEL
# ==================================================

if settings["show_memories"]:

    st.markdown(
        """
        <div class="glass-card">

            <div class="card-title">
                🧠 Your Study Memory
            </div>

            <div class="card-description">
                Information remembered by your Study Tutor.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    memories = get_memories()

    if memories:

        for memory in memories:

            st.info(memory)

    else:

        st.info(
            "Your Study Tutor has not saved any memories yet."
        )


# ==================================================
# CHAT HEADER
# ==================================================

st.markdown(
    """
    <div class="glass-card">

        <div class="card-title">
            💬 Chat with your Study Tutor
        </div>

        <div class="card-description">
            Ask questions, request explanations,
            practice concepts, or prepare for exams.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# DISPLAY CHAT HISTORY
# ==================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ==================================================
# CHAT INPUT
# ==================================================

user_input = st.chat_input(
    "Ask your Study Tutor anything..."
)


# ==================================================
# PROCESS USER MESSAGE
# ==================================================

if user_input:

    # ----------------------------------------------
    # Display user message
    # ----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):

        st.markdown(user_input)


    # ----------------------------------------------
    # Create Tutor Prompt
    # ----------------------------------------------

    prompt = f"""
You are Study Tutor AI.

Student information:

Subject:
{subject}

Learning Level:
{level}

Learning Mode:
{learning_mode}

Student message:
{user_input}

Your responsibilities:

1. Explain concepts clearly.
2. Adapt your explanation to the student's level.
3. Use examples when appropriate.
4. Ask a short follow-up question when it
   would improve learning.
5. Use the memory tools when useful.
6. Remember important student goals,
   preferences, and learning context.
7. Use the calculator when mathematical
   calculations are required.
8. Never invent facts.
9. Encourage understanding instead of
   simply giving answers.
10. Keep responses structured and readable.
"""


    # ----------------------------------------------
    # Generate AI response
    # ----------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🧠 Study Tutor is thinking..."
        ):

            try:

                result = (
                    st.session_state
                    .tutor
                    .kickoff(prompt)
                )

                answer = result.raw

                st.markdown(answer)

            except Exception as error:

                answer = (
                    "I encountered an error while "
                    "processing your question."
                )

                st.error(
                    f"{answer}\n\n{error}"
                )


    # ----------------------------------------------
    # Save assistant response
    # ----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
