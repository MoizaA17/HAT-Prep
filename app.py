import json
import time
from pathlib import Path

import streamlit as st

# ---------- Page setup ----------
st.set_page_config(page_title="HAT Prep", page_icon="◦", layout="centered")

# ---------- Styling (a little CSS for the minimal, elegant look) ----------
st.markdown(
    """
    <style>
    /* Hide Streamlit's default menu, header and footer */
    #MainMenu, header, footer {visibility: hidden;}

    /* Narrow, centered page with generous breathing room */
    .block-container {max-width: 760px; padding-top: 6rem;}

    /* Small spaced-out label above the title */
    .eyebrow {
        font-size: 0.95rem; letter-spacing: 0.25em; text-transform: uppercase;
        color: #fcf7f7; margin-bottom: 0.5rem;
    }

    /* Big serif title */
    .title {
        font-family: Georgia, 'Times New Roman', serif;
        font-size: 3.6rem; font-weight: 400; line-height: 1.15;
        color: #fcfbf7; margin: 0 0 0.75rem 0;
    }

    /* Soft grey subtitle */
    .subtitle {color: #fcfbf7; font-size: 1.2rem; margin-bottom: 2.5rem;}

    /* Thin divider line */
    .rule {border: none; border-top: 1px solid #e6e6e6; margin: 0 0 2rem 0;}

    /* Buttons: clean outlined rectangles */
    .stButton > button {
        width: 100%; text-align: left; padding: 1rem 1.25rem;
        background: #ffffff; color: #1c1c1c;
        border: 1px solid #dcdcdc; border-radius: 10px;
        font-size: 1rem; transition: all 0.2s ease;
    }
    .stButton > button:hover:enabled {
        border-color: #1c1c1c; background: #fafafa;
    }

    /* Disabled ("coming soon") buttons look faded */
    .stButton > button:disabled {
        background: #fafafa; color: #b5b5b5; border-color: #eeeeee;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Where the lesson files live ----------
# __file__ is this app.py. Its parent is the folder app.py sits in, so the
# path works no matter which folder you run "streamlit run" from.
BASE_DIR = Path(__file__).parent
LESSON_DIR = BASE_DIR / "data" / "lessons"      #HAT-Prep/data/lessons
QUESTION_DIR = BASE_DIR / "data"      # HAT-Prep/data


# ---------- Remember the current screen ----------
# session_state keeps its values between clicks. We start on "topics".
if "screen" not in st.session_state:
    st.session_state.screen = "topics"

# Topics that are ready to use. To enable a topic, add its name here.
ACTIVE_TOPICS = ["Ratio & Proportion"]

def go_to(screen_name):
    """Change the current screen."""
    st.session_state.screen = screen_name
    #Every time we open the test, start with "not submitted yet"
    if screen_name == "test":
        st.session_state.submitted = False
    # Delete any old start times and results from earlier tries
        for key in list(st.session_state.keys()):
            if key.startswith("start_") or key.startswith("seconds_"):
                del st.session_state[key]

def open_lesson(topic):
    """Remember which topic was clicked, then show the lesson screen."""
    st.session_state.topic = topic
    st.session_state.screen = "lesson"

def load_lesson(topic):
    """Read the lesson file for a topic. Returns None if the file is missing."""
    # "Ratio & Proportion" -> "ratio_proportion"
    file_name = topic.lower().replace(" & ", "_").replace(" ", "_") + ".md"
    lesson_path = LESSON_DIR / file_name
    if not lesson_path.exists():
        return None
    return lesson_path.read_text(encoding="utf-8")


def load_questions(topic):
    """Read the question file for a topic. Returns None if the file is missing."""
    # "Ratio & Proportion" -> "questions_ratio_proportion.json"
    file_name = "questions_" + topic.lower().replace(" & ", "_").replace(" ", "_") + ".json"
    question_path = QUESTION_DIR / file_name
    if not question_path.exists():
        return None
    text = question_path.read_text(encoding="utf-8")
    data = json.loads(text)          # turn the text into a Python list
    # Some files are a plain list, some wrap it as {"questions": [...]}
    if isinstance(data, dict):
        data = data["questions"]
    return data


# ---------- Screen 1: Topic picker ----------
def show_topics():
    st.markdown('<div class="eyebrow">HAT-I · Quantitative Reasoning</div>', unsafe_allow_html=True)
    st.markdown('<div class="title">Choose a topic</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Learn it, time yourself, find your gaps.</div>', unsafe_allow_html=True)
    st.markdown('<hr class="rule">', unsafe_allow_html=True)


    # All topics in one list (Ratio & Proportion is the only active one)
    topics = ["Ratio & Proportion", "Percentages", "Algebra", "Averages", "Profit & Loss", "Geometry"]

    # Go through the list 3 topics at a time (one row = 3 topics)
    for row_start in range(0, len(topics), 3):
        columns = st.columns(3)  # make 3 side-by-side columns for this row

        # Put one topic in each column
        for column, name in zip(columns, topics[row_start:row_start + 3]):
            with column:
                if name in ACTIVE_TOPICS:
                    # Active topic: clickable
                    st.button(name, on_click=open_lesson, args=(name,),
                              key=name, use_container_width=True)
                else:
                    # Not ready yet: disabled
                    st.button(f"{name} · coming soon", disabled=True,
                              key=name, use_container_width=True)


# ---------- Screen 2: Lesson ----------
def show_lesson():
    st.markdown('<div class="eyebrow">Lesson</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="title">{st.session_state.topic}</div>', unsafe_allow_html=True)

    # Load the lesson file and show it (or a warning if the file is missing)
    lesson_text = load_lesson(st.session_state.topic)
    if lesson_text is None:
        st.warning("Lesson file not found. Check the data/lessons folder.")
    else:
        st.markdown(lesson_text)

    
    st.markdown('<hr class="rule">', unsafe_allow_html=True)

    # Buttons below the lesson
    # Buttons below the lesson: Back on the left, Start test on the right
    left, middle, right = st.columns([1, 2, 1])

    with left:
        st.button("← Back to Topics", on_click=go_to, args=("topics",),
                  key="back", use_container_width=True)

    with right:
        st.button("Start Test", on_click=go_to, args=("test",),
                  key="start_test", use_container_width=True)

# ---------- Screen 3: Test ----------
def save_answer(question_id):
    """Runs when Submit is clicked. Stops the stopwatch and saves the seconds."""
    start_time = st.session_state[f"start_{question_id}"]
    seconds_taken = round(time.time() - start_time)      # whole seconds
    st.session_state[f"seconds_{question_id}"] = seconds_taken
    st.session_state.submitted = True

def show_test():
    st.markdown('<div class="eyebrow">Test</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="title">{st.session_state.topic}</div>', unsafe_allow_html=True)
    st.markdown('<hr class="rule">', unsafe_allow_html=True)

    questions = load_questions(st.session_state.topic)

    if not questions:
        st.warning("Question file not found. Check the data folder.")
    else:
        question = questions[0]          # still only the first question
        total = len(questions)
        question_id = question["id"]
        submitted = st.session_state.get("submitted", False)

        # --- Start the stopwatch ONCE ---
        # Streamlit re-runs this whole function on every click.
        # "if not in session_state" makes sure we only save the time
        # the very first time, so later re-runs don't reset it.
        start_key = f"start_{question_id}"
        if start_key not in st.session_state:
            st.session_state[start_key] = time.time()

        st.markdown(f"**Question 1 of {total}**")
        st.write(question["question"])

        chosen_option = st.radio(
            "Choose your answer",
            question["options"],
            index=None,
            key=f"answer_{question_id}",
            label_visibility="collapsed",
            disabled=submitted,
        )

        st.markdown("**How sure are you?**")
        confidence = st.radio(
            "How sure are you?",
            ["Sure", "Not sure"],
            index=None,
            horizontal=True,
            key=f"confidence_{question_id}",
            label_visibility="collapsed",
            disabled=submitted,
        )

        not_ready = chosen_option is None or confidence is None
        st.button("Submit", on_click=save_answer, args=(question_id,),
                  key="submit", disabled=not_ready or submitted)

        # After Submit: show saved message and the time line
        if submitted:
            st.success("Answer saved.")
            seconds_taken = st.session_state[f"seconds_{question_id}"]
            target = question.get("target_seconds", 72)   # 72 if the file has none
            st.caption(f"Time: {seconds_taken}s (target {target}s)")

    st.markdown('<hr class="rule">', unsafe_allow_html=True)
    st.button("← Back to lesson", on_click=go_to, args=("lesson",), key="back_to_lesson")

    
# ---------- Show the right screen ----------
if st.session_state.screen == "topics":
    show_topics()
elif st.session_state.screen == "lesson":
    show_lesson()
elif st.session_state.screen == "test":
    show_test()
