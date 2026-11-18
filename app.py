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

# ---------- Remember the current screen ----------
# session_state keeps its values between clicks. We start on "topics".
if "screen" not in st.session_state:
    st.session_state.screen = "topics"

# Topics that are ready to use. To enable a topic, add its name here.
ACTIVE_TOPICS = ["Ratio & Proportion"]

def go_to(screen_name):
    """Change the current screen."""
    st.session_state.screen = screen_name

def open_lesson(topic):
    """Remember which topic was clicked, then show the lesson screen."""
    st.session_state.topic = topic
    st.session_state.screen = "lesson"


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


# ---------- Screen 2: Lesson (placeholder) ----------
def show_lesson():
    st.markdown('<div class="eyebrow">Lesson</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="title">{st.session_state.topic}</div>', unsafe_allow_html=True)
    st.markdown('<hr class="rule">', unsafe_allow_html=True)

    st.write("Lesson content will appear here.")

    st.button("← Back to topics", on_click=go_to, args=("topics",), key="back")


# ---------- Show the right screen ----------
if st.session_state.screen == "topics":
    show_topics()
elif st.session_state.screen == "lesson":
    show_lesson()
