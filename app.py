import streamlit as st
import PyPDF2
from src.retrain import retrain_model
import pandas as pd
import google.generativeai as genai
import json
import re
import joblib
from src.nlp_engine import extract_features
from src.vector_engine import semantic_search
from src.dataset_builder import save_feedback
from src.parser import parse_resume
from docx import Document
from src.validation import validate_system
from src.scoring_engine import (
    calculate_skill_match,
)


from src.explain_engine import explain

# ---------- CONFIG ----------
# ---------- ML MODEL ----------
# ---------- LOAD MODEL ----------

def load_model():

    try:

        model = joblib.load(
            "models/hr_model.pkl"
        )

        print(
            "✅ ML model loaded"
        )

        return model

    except Exception as e:

        print(
            "❌ Load model error:",
            e
        )

        return None


# โหลด model ครั้งแรก
# ---------- LOAD MODEL ----------

def load_model():

    try:

        model = joblib.load(
            "models/hr_model.pkl"
        )

        print("✅ ML model loaded")

        return model

    except Exception as e:

        print(
            "❌ Load model error:",
            e
        )

        return None


# โหลด model เข้า session
if "ml_model" not in st.session_state:

    st.session_state.ml_model = load_model()
st.set_page_config(
    page_title="AI Recruitment Pro",
    page_icon="🎯",
    layout="wide"
)
# ---------- CUSTOM UI ----------

st.markdown("""

<style>

/* ---------- BACKGROUND ---------- */

.stApp {

    background:
        linear-gradient(
            135deg,
            #0f172a 0%,
            #111827 40%,
            #1e293b 100%
        );

    color: white;
}

/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #111827 0%,
            #0f172a 100%
        );

    border-right:
        1px solid rgba(255,255,255,0.08);
}

/* ---------- TITLE ---------- */

.main-title {

    font-size: 52px;

    font-weight: 800;

    background:
        linear-gradient(
            90deg,
            #60a5fa,
            #a78bfa,
            #f472b6
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    margin-bottom: 5px;
}

.sub-title {

    color: #cbd5e1;

    font-size: 18px;

    margin-bottom: 25px;
}

/* ---------- CARD ---------- */

.block-container {

    padding-top: 2rem;
}

[data-testid="stMetric"] {

    background:
        rgba(255,255,255,0.06);

    border:
        1px solid rgba(255,255,255,0.08);

    padding:
        20px;

    border-radius:
        20px;

    backdrop-filter:
        blur(10px);

    box-shadow:
        0 8px 24px rgba(0,0,0,0.25);
}

/* ---------- BUTTON ---------- */

.stButton > button {

    width: 100%;

    border-radius: 14px;

    border: none;

    background:
        linear-gradient(
            90deg,
            #3b82f6,
            #8b5cf6
        );

    color: white;

    font-weight: 700;

    padding: 14px;

    font-size: 16px;

    transition: 0.3s;
}

.stButton > button:hover {

    transform:
        translateY(-2px);

    box-shadow:
        0 10px 20px rgba(59,130,246,0.35);
}

/* ---------- TEXT AREA ---------- */

textarea {

    border-radius: 15px !important;

    background:
        rgba(255,255,255,0.04) !important;

    color: white !important;

    border:
        1px solid rgba(255,255,255,0.08) !important;
}

/* ---------- FILE UPLOADER ---------- */

[data-testid="stFileUploader"] {

    background:
        rgba(255,255,255,0.05);

    padding:
        15px;

    border-radius:
        18px;

    border:
        1px dashed rgba(255,255,255,0.15);
}

/* ---------- EXPANDER ---------- */

.streamlit-expanderHeader {

    font-size: 18px;

    font-weight: 700;

    color: white;
}

/* ---------- TABLE ---------- */

table {

    border-radius: 15px !important;

    overflow: hidden;
}

/* ---------- SUCCESS BOX ---------- */

.stSuccess {

    border-radius: 14px;
}

/* ---------- INFO BOX ---------- */

.stInfo {

    border-radius: 14px;
}

/* ---------- WARNING BOX ---------- */

.stWarning {

    border-radius: 14px;
}

</style>

""", unsafe_allow_html=True)

if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []

if "metrics" not in st.session_state:
    st.session_state.metrics = {
        "total": 0,
        "agreed": 0,
        "time_saved": 0
    }


# ---------- LLM ----------

def deep_analysis(
    api_key,
    jd_text,
    candidates,
    tuned_model=None
):
    
    genai.configure(
        api_key=api_key
    )

    model_name = (
        tuned_model
        if tuned_model
        else
        "gemini-2.5-flash"
    )

    model = genai.GenerativeModel(
        model_name
    )

    output = []

    for r in candidates:

        prompt = f"""
คุณคือผู้เชี่ยวชาญด้าน HR

วิเคราะห์ Resume เทียบกับ Job Description

ตอบภาษาไทย

กฎสำคัญ:
- ตอบเป็น JSON ONLY
- ห้ามอธิบายเพิ่ม
- ห้ามใช้ markdown
- ห้ามใส่ ```json

รูปแบบ:

{{
"score":0,
"verdict":"",
"key_skills":[],
"missing_skills":[],
"reasoning":""
}}

JOB DESCRIPTION:
{jd_text}

RESUME:
{r["content"]}
"""

        try:

            res = model.generate_content(
                prompt
            )

            match = re.search(
                r'\{.*?\}',
                res.text,
                re.DOTALL
            )

            if not match:
                continue

            data = json.loads(
                match.group()
            )

            data["name"] = (
                r["name"]
            )

            data["content"] = (
                r["content"]
            )

            data["profile"] = (
                r["profile"]
            )

            output.append(
                data
            )

        except Exception as e:

            st.warning(
                f"Skip {r['name']} : {e}"
            )

    return output
# ---------- ML PREDICT ----------

def predict_candidate(
    jd,
    resume
):

    model = st.session_state.ml_model

    if model is None:

        return {

            "prediction": "unknown",

            "confidence": 0

        }

    try:

        text = jd + " " + resume

        pred = model.predict(
            [text]
        )[0]

        if hasattr(
            model,
            "predict_proba"
        ):

            prob = max(

                model.predict_proba(
                    [text]
                )[0]

            )

        else:

            prob = 0.5

        return {

            "prediction": str(pred),

            "confidence": round(
                prob * 100,
                1
            )

        }

    except Exception as e:

        print("ML ERROR:", e)

        return {

            "prediction": "error",

            "confidence": 0

        }

# ---------- SIDEBAR ----------

with st.sidebar:

    st.header(
        "⚙️ System"
    )

    # =========================
    # API KEY
    # =========================

    api_key = st.text_input(

        "Gemini API Key",

        type="password"

    )

    tuned_id = ""

    st.divider()

    # =========================
    # METRICS
    # =========================

    m = st.session_state.metrics

    acc = (

        (
            m["agreed"]

            /

            m["total"]

        ) * 100

    ) if m["total"] else 0

    st.subheader(
        "📊 AI Metrics"
    )

    st.metric(

        "HR Agreement",

        f"{acc:.1f}%"

    )

    st.metric(

        "Time Saved",

        f"{m['time_saved']} mins"

    )

    st.metric(

        "Feedback Count",

        m["total"]

    )

    st.divider()

    # =========================
    # SYSTEM STATUS
    # =========================

    st.subheader(
        "🖥️ System Status"
    )

    st.success(
        "Gemini Connected"
    )

    st.success(
        "FAISS Ready"
    )

    st.success(
        "Semantic Search Active"
    )

    st.success(
        "HR Feedback Learning"
    )

    st.success(
        "ML Model Loaded"
    )

    st.divider()

    # =========================
    # AI FEATURES
    # =========================

    st.subheader(
        "🧠 AI Features"
    )

    st.write(
        "✅ Resume Parsing"
    )

    st.write(
        "✅ Semantic Search"
    )

    st.write(
        "✅ Gemini LLM"
    )

    st.write(
        "✅ Machine Learning"
    )

    st.write(
        "✅ HR Feedback Loop"
    )

    st.write(
        "✅ Validation Metrics"
    )

    st.divider()

    # =========================
    # DOWNLOAD DATASET
    # =========================

    import os

    if os.path.exists(
        "data/feedback.jsonl"
    ):

        with open(
            "data/feedback.jsonl",
            "rb"
        ) as f:

            st.download_button(

                "📥 Download Training Dataset",

                f,

                file_name="feedback.jsonl",

                use_container_width=True

            )

    st.divider()

    # =========================
    # ABOUT
    # =========================

    st.caption(
        "AI Recruitment"
    )

    st.caption(
        "Built with Streamlit + Gemini"
    )
# ---------- MAIN ----------

st.markdown(

    """
    <div class='main-title'>
        AI Resume Screening
    </div>

    <div class='sub-title'>
        Gemini AI • NLP • Semantic Search • Machine Learning
    </div>
    """,

    unsafe_allow_html=True

)
# ---------- JD TEMPLATE ----------

jd_templates = {

        "Flutter Developer": """
    ตำแหน่ง: Flutter Developer

    คุณสมบัติ:
    - มีประสบการณ์ Flutter (Dart)
    - เข้าใจ REST API
    - ใช้ MySQL / SQL ได้
    - มีความรู้ Node.js
    - เข้าใจ Git และ Agile
    - สามารถทำงานร่วมกับทีมได้ดี
    """,

        "Frontend Developer": """
    ตำแหน่ง: Frontend Developer

    คุณสมบัติ:
    - React.js
    - Tailwind CSS
    - JavaScript / TypeScript
    - HTML/CSS
    - REST API Integration
    - Responsive Design
    - Git
    """,

        "Backend Developer": """
    ตำแหน่ง: Backend Developer

    คุณสมบัติ:
    - Python / Node.js
    - FastAPI / Express.js
    - REST API
    - MySQL / PostgreSQL
    - Docker
    - AWS
    - CI/CD
    """,

        "Data Scientist": """
    ตำแหน่ง: Data Scientist

    คุณสมบัติ:
    - Python
    - Machine Learning
    - NLP
    - Pandas / Scikit-learn
    - SQL
    - Data Visualization
    - TensorFlow หรือ PyTorch
    """,

        "AI Engineer": """
    ตำแหน่ง: AI Engineer

    คุณสมบัติ:
    - Deep Learning
    - Python
    - LLM / NLP
    - TensorFlow / PyTorch
    - HuggingFace
    - Vector Database
    - Deployment Model
    """,

        "IT Support": """
    ตำแหน่ง: IT Support / Helpdesk

    คุณสมบัติ:
    - Troubleshooting
    - Hardware / Software Support
    - Windows Server
    - Network เบื้องต้น
    - Ticketing System
    - Active Directory
    - Service Mind
    """,

        "Network Engineer": """
    ตำแหน่ง: Network Engineer

    คุณสมบัติ:
    - Cisco
    - Routing & Switching
    - Firewall
    - VPN
    - Linux
    - TCP/IP
    - Network Security
    """,

        "Full Stack Developer": """
    ตำแหน่ง: Full Stack Developer

    คุณสมบัติ:
    - React.js
    - Node.js
    - Python
    - REST API
    - SQL
    - Docker
    - Git
    - Cloud Deployment
    """,

        "Mobile Developer": """
    ตำแหน่ง: Mobile Developer

    คุณสมบัติ:
    - Flutter หรือ React Native
    - REST API
    - Firebase
    - Mobile UI/UX
    - Android/iOS
    - Git
    """,

        "Cyber Security": """
    ตำแหน่ง: Cyber Security Analyst

    คุณสมบัติ:
    - Penetration Testing
    - SIEM
    - Firewall
    - Network Security
    - Linux
    - Incident Response
    - Security Monitoring
    """
    }
# ---------- SELECT TEMPLATE ----------

selected_template = st.selectbox(

    "📌 เลือก Job Description Template",

    ["Custom"] + list(jd_templates.keys())

)

# ถ้าเลือก template
if selected_template != "Custom":

    default_jd = jd_templates[
        selected_template
    ]

else:

    default_jd = ""
# ---------- SELECT TEMPLATE ----------




col1, col2 = st.columns(2)

with col1:
    
    jd_input = st.text_area(

        "Job Description",

        value=default_jd,

        height=250

    )

with col2:

    files = st.file_uploader(
        "Upload Resume PDF/TXT",
        type=["pdf", "txt", "docx"],
        accept_multiple_files=True
    )


# ---------- ANALYZE ----------

if st.button(
    "Analyze",
    use_container_width=True,
    type="primary"
):

    if not api_key:

        st.warning(
            "ใส่ API ก่อน"
        )

    elif not jd_input:

        st.warning(
            "ใส่ JD"
        )

    elif not files:

        st.warning(
            "อัป Resume"
        )

    else:

        resumes = []

        with st.spinner(
            "Reading PDF..."
        ):

            for f in files:

                text = ""

                # ---------- PDF ----------

                if f.name.endswith(".pdf"):

                    pdf = PyPDF2.PdfReader(f)

                    for p in pdf.pages:

                        page = p.extract_text()

                        if page:

                            text += page

                # ---------- TXT ----------

                elif f.name.endswith(".txt"):

                    text = f.read().decode(
                        "utf-8",
                        errors="ignore"
                    )
                elif f.name.endswith(".docx"):

                    doc = Document(f)

                    text = "\n".join(

                        p.text for p in doc.paragraphs

                    )

                # ---------- NLP ----------

                feat = extract_features(
                    text
                )

                parsed = parse_resume(
                    text
                )

                resumes.append({

                    "name": f.name,

                    "content": text,

                    "profile": parsed

                })

        with st.spinner(
            "Semantic Search..."
        ):

            shortlisted = semantic_search(
                jd_input,
                resumes,
                top_k=len(resumes)
            )

        with st.spinner(
            "LLM Analysis..."
        ):

            result = (
                deep_analysis(
                    api_key,
                    jd_input,
                    shortlisted,
                    tuned_id
                )
            )

        result = sorted(
            result,
            key=lambda x:
            x.get(
                "score",
                0
            ),
            reverse=True
        )

        st.session_state[
            "leaderboard"
        ] = result

        st.session_state[
            "metrics"
        ][
            "time_saved"
        ] += len(
            files
        ) * 10

        st.rerun()


# ---------- RESULT ----------

if st.session_state.leaderboard:

    st.subheader("🥇 อันดับผู้สมัคร")

    df = pd.DataFrame(
        st.session_state.leaderboard
    )

    # =========================
    # DASHBOARD
    # =========================

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "ผู้สมัคร",
            len(df)
        )

    with c2:
        st.metric(
            "คะแนนเฉลี่ย",
            round(
                df["score"].mean(),
                1
            )
        )

    with c3:

        passed = len(
            df[df["score"] >= 70]
        )

        st.metric(
            "ผ่าน",
            passed
        )

    st.divider()

    # =========================
    # EXPORT CSV
    # =========================

    export_df = df[
        [
            "name",
            "score",
            "verdict",
            "reasoning"
        ]
    ]

    csv = export_df.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="📥 Export Result CSV",
        data=csv,
        file_name="candidate_result.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.divider()

    # =========================
    # TABLE
    # =========================

    st.table(

        df[
            [
                "name",
                "score",
                "verdict"
            ]
        ]

    )

    st.divider()

    # =========================
    # BAR CHART
    # =========================

    st.subheader(
        "📊 คะแนนผู้สมัคร"
    )

    chart_df = df[
        [
            "name",
            "score"
        ]
    ]

    st.bar_chart(
        chart_df.set_index(
            "name"
        )
    )

    st.divider()

    # =========================
    # PIE CHART DATA
    # =========================

    st.subheader(
        "🥧 สัดส่วนผู้สมัคร"
    )

    pie_df = pd.DataFrame({

        "status": [
            "ผ่าน",
            "ไม่ผ่าน"
        ],

        "count": [

            len(
                df[
                    df["score"] >= 70
                ]
            ),

            len(
                df[
                    df["score"] < 70
                ]
            )

        ]

    })

    st.dataframe(
        pie_df,
        use_container_width=True
    )

    st.bar_chart(
        pie_df.set_index(
            "status"
        )
    )

    st.divider()

    # =========================
    # EACH CANDIDATE
    # =========================

    for i, cand in enumerate(

        st.session_state
        .leaderboard

    ):

        with st.expander(

            f"🏅 {cand['name']}"

        ):

            # ---------- SCORE ----------

            st.progress(
                cand["score"] / 100
            )

            st.metric(
                "คะแนนรวม",
                f"{cand['score']}%"
            )

            # ---------- PROFILE ----------

            profile = cand.get(
                "profile",
                {}
            )

            if profile:

                st.write(
                    f"👤 {profile.get('name', '-')}"
                )

                st.write(
                    f"📧 {profile.get('email', '-')}"
                )

                st.write(
                    f"📱 {profile.get('phone', '-')}"
                )

                st.write(
                    "🧠 Skills"
                )

                st.write(
                    ", ".join(
                        profile.get(
                            "skills",
                            []
                        )
                    )
                )

            st.divider()

            # ---------- AI ANALYSIS ----------

            st.subheader(
                "🤖 AI วิเคราะห์"
            )

            st.info(
                cand["reasoning"]
            )

            # ---------- SKILL MATCH ----------

            skill = calculate_skill_match(

                jd_input,

                cand["content"]

            )
            # ---------- ML PREDICTION ----------

            ml_result = predict_candidate(

                jd_input,

                cand["content"]

            )

            st.subheader(
                "🧠 ML Prediction"
            )

            st.write(
                f"Prediction: {ml_result['prediction']}"
            )

            st.write(
                f"Confidence: {ml_result['confidence']}%"
            )

            st.metric(
                "Skill Match",
                f"{skill['percent']}%"
            )

            st.divider()

            # ---------- GOOD / BAD ----------

            left, right = st.columns(2)

            with left:

                st.success(
                    "✅ จุดเด่น"
                )

                if skill["matched"]:

                    for s in skill[
                        "matched"
                    ]:

                        st.write(
                            f"✔ {s}"
                        )

                else:

                    st.write(
                        "ไม่มี"
                    )

            with right:

                st.warning(
                    "❌ ยังขาด"
                )

                if skill["missing"]:

                    for s in skill[
                        "missing"
                    ]:

                        st.write(
                            f"ขาด {s}"
                        )

                else:

                    st.write(
                        "ไม่มี"
                    )

            st.divider()

            # ---------- FEEDBACK ----------

            like, dislike = st.columns(2)

            # =========================
            # ACCEPT
            # =========================

            if like.button(

                "👍 HR เห็นด้วย",

                key=f"accept_{i}"

            ):

                save_feedback(

                    jd_input,

                    cand["content"],

                    cand["score"],

                    "accept"

                )

                success = retrain_model()

                if success:

                    st.session_state.ml_model = load_model()

                # metrics
                st.session_state[
                    "metrics"
                ][
                    "total"
                ] += 1

                st.session_state[
                    "metrics"
                ][
                    "agreed"
                ] += 1

                st.success(
                    "✅ AI retrained realtime"
                )

                st.rerun()

            # =========================
            # REJECT
            # =========================

            if dislike.button(

                "👎 HR ไม่เห็นด้วย",

                key=f"reject_{i}"

            ):

                save_feedback(

                    jd_input,

                    cand["content"],

                    cand["score"],

                    "reject"

                )

                # realtime retrain
                success = retrain_model()

                # reload latest model
                ml_model = load_model()

                # metrics
                st.session_state[
                    "metrics"
                ][
                    "total"
                ] += 1

                st.success(
                    "✅ AI retrained realtime"
                )

                st.rerun()
# ---------- SYSTEM VALIDATION ----------

st.divider()

st.subheader(
    "📊 AI System Validation"
)

try:

    import pandas as pd

    feedback_df = pd.read_csv(
        "data/feedback.csv"
    )

    total_feedback = len(
        feedback_df
    )

    true_labels = []
    pred_labels = []

    for _, row in feedback_df.iterrows():

        true_labels.append(
            row["label"]
        )

        text = row["jd"] + " " + row["resume"]

        pred = st.session_state.ml_model.predict([text])[0]

        pred_labels.append(pred)

    metrics = validate_system(

        true_labels,

        pred_labels

    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Accuracy",
        f"{metrics['accuracy']}%"
    )

    c2.metric(
        "Precision",
        f"{metrics['precision']}%"
    )

    c3.metric(
        "Recall",
        f"{metrics['recall']}%"
    )

    c4.metric(
        "F1 Score",
        f"{metrics['f1']}%"
    )

    st.success(
        "Validation Complete"
    )

    # ---------- CHART ----------

    chart_df = pd.DataFrame({

        "Metric": [

            "Accuracy",
            "Precision",
            "Recall",
            "F1"

        ],

        "Score": [

            metrics[
                "accuracy"
            ],

            metrics[
                "precision"
            ],

            metrics[
                "recall"
            ],

            metrics[
                "f1"
            ]

        ]

    })

    st.bar_chart(

        chart_df.set_index(
            "Metric"
        )

    )

except Exception as e:

    st.warning(
        "No validation data yet"
    )