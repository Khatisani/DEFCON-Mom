import streamlit as st
from models import (
    ChoreStatus,
    ForgivenessStatus,
    InfractionRecency,
    InfractionSeverity,
    MomEnergy,
    RecentFriction,
    AcademicStanding,
    CrowdFactor,
    LogisticsPlan,
)

from trust_engine import evaluate_plan

st.set_page_config(page_title="DEFCON: Mom", layout="centered")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;700;800&family=Gaegu:wght@700&display=swap');

    /* Kill default Streamlit top bar */
    header[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {
        display: none !important;
    }


    .stApp {
        background-color: #FFD1DC !important;
        background-image: radial-gradient(#FF85A2 18%, transparent 18%) !important;
        background-size: 24px 24px !important;
        font-family: 'Fredoka', cursive, sans-serif !important;
        color: #1A1A1A !important;
    }


    .block-container {
        padding-top: 1.5rem !important;
        max-width: 580px !important;
    }


    .comic-title {
        font-family: 'Fredoka', cursive !important;
        font-size: 3.2rem;
        font-weight: 800;
        text-align: center;
        color: #FF2E7E;
        -webkit-text-stroke: 3px #1A1A1A;
        text-shadow: 4px 4px 0px #1A1A1A;
        margin-bottom: 20px;
        letter-spacing: 1px;
    }


    .comic-card {
        border-radius: 24px;
        padding: 24px;
        text-align: center;
        border: 4px solid #1A1A1A;
        box-shadow: 6px 6px 0px #1A1A1A;
        margin-bottom: 24px;
    }

    .comic-green {
        background-color: #A3F7BF;
    }
    .comic-yellow {
        background-color: #FFF385;
    }
    .comic-red {
        background-color: #FF6B8B;
        color: white;
    }

    .big-score {
        font-size: 4.8rem;
        font-weight: 800;
        line-height: 1;
        margin: 4px 0 10px 0;
        -webkit-text-stroke: 2px #1A1A1A;
        text-shadow: 3px 3px 0px #1A1A1A;
        color: #FFFFFF;
    }

    .comic-verdict {
        font-size: 1.35rem;
        font-weight: 700;
        line-height: 1.3;
        margin: 0;
    }


    [data-testid="stForm"] {
        background-color: #FFFFFF !important;
        border: 4px solid #1A1A1A !important;
        border-radius: 28px !important;
        box-shadow: 7px 7px 0px #1A1A1A !important;
        padding: 24px !important;
    }


    label, .stRadio label p, .stTextInput label p {
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        color: #1A1A1A !important;
    }


    .stTextInput input {
        border: 3px solid #1A1A1A !important;
        border-radius: 16px !important;
        background-color: #FFF5F8 !important;
        color: #1A1A1A !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        box-shadow: 3px 3px 0px #1A1A1A !important;
        padding: 12px !important;
    }
    .stTextInput input:focus {
        border-color: #FF2E7E !important;
        background-color: #FFFFFF !important;
    }


    div[role="radiogroup"] {
        gap: 8px !important;
    }
    div[role="radiogroup"] label {
        background: #FFF5F8;
        border: 2px solid #1A1A1A;
        border-radius: 12px;
        padding: 6px 14px;
        box-shadow: 2px 2px 0px #1A1A1A;
        transition: 0.1s transform ease;
    }
    div[role="radiogroup"] label:hover {
        transform: translate(-1px, -1px);
        box-shadow: 3px 3px 0px #1A1A1A;
    }


    .stButton > button {
        background-color: #FF2E7E !important;
        color: #FFFFFF !important;
        border: 4px solid #1A1A1A !important;
        border-radius: 20px !important;
        font-size: 1.4rem !important;
        font-weight: 800 !important;
        padding: 12px 30px !important;
        box-shadow: 5px 5px 0px #1A1A1A !important;
        width: 100% !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        cursor: pointer !important;
    }
    .stButton > button:hover {
        background-color: #E01E68 !important;
        transform: translate(-2px, -2px) !important;
        box-shadow: 7px 7px 0px #1A1A1A !important;
    }
    .stButton > button:active {
        transform: translate(2px, 2px) !important;
        box-shadow: 2px 2px 0px #1A1A1A !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


if "assessment" not in st.session_state:
    st.session_state.assessment = None

st.markdown('<div class="comic-title">DEFCON: MOM</div>', unsafe_allow_html=True)

if st.session_state.assessment:
    res = st.session_state.assessment
    st.markdown(
        f"""
        <div class="comic-card {res.card_class}">
            <div class="big-score">{res.score}%</div>
            <div class="comic-verdict">{res.verdict}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with st.form("quick_check_form"):
    plan = st.text_input("What are you trying to do?", placeholder="Sneak snacks, go out with friends...")

    recency = st.radio(
        "When did she last catch you?",
        [
            ("Today or yesterday", InfractionRecency.TODAY_OR_YESTERDAY),
            ("This past week", InfractionRecency.PAST_WEEK),
            ("Two weeks ago", InfractionRecency.TWO_WEEKS_CLEAN),
            ("A whole month clean", InfractionRecency.ONE_MONTH_CLEAN),
        ],
        format_func=lambda x: x[0],
    )

    severity = st.radio(
        "How bad was it?",
        [
            ("Nothing, record is clean", InfractionSeverity.NONE),
            ("Mild: small attitude or forgotten chore", InfractionSeverity.MILD),
            ("Medium: came home late or told a lie", InfractionSeverity.MEDIUM),
            ("Severe: absolute disaster", InfractionSeverity.NUCLEAR),
        ],
        format_func=lambda x: x[0],
    )

    forgiveness = st.radio(
        "Her mood towards you right now?",
        [
            ("Silent treatment and heavy sighs", ForgivenessStatus.ACTIVE_COLD_WAR),
            ("Talking, but suspicious", ForgivenessStatus.CAUTIOUS_TRUCE),
            ("Totally back to normal", ForgivenessStatus.FULL_AMNESTY),
        ],
        format_func=lambda x: x[0],
    )

    energy = st.radio(
        "What is she doing right now?",
        [
            ("Relaxing / having tea or coffee", MomEnergy.CHILLING),
            ("Busy / rushing / stressed out", MomEnergy.STRESSED),
        ],
        format_func=lambda x: x[0],
    )

    friction = st.radio(
        "Did you two argue in the last 24 hours?",
        [
            ("No, peace in the house", RecentFriction.NO_ARGUMENT),
            ("Yes, we clashed recently", RecentFriction.ARGUED_RECENTLY),
        ],
        format_func=lambda x: x[0],
    )

    chores = st.radio(
        "What is the chore situation?",
        [
            ("Room is clean and chores are done", ChoreStatus.CHORES_DONE),
            ("Chores are undone", ChoreStatus.CHORES_UNDONE),
        ],
        format_func=lambda x: x[0],
    )

    submitted = st.form_submit_button("Calculate Risk")
    if submitted:
        if not plan.strip():
            st.error("Write down what you want to do first.")
        else:
            assessment = evaluate_plan(
                plan=plan.strip(),
                recency=recency[1],
                severity=severity[1],
                forgiveness=forgiveness[1],
                energy=energy[1],
                friction=friction[1],
                chores=chores[1],
            )
            st.session_state.assessment = assessment
            st.rerun()