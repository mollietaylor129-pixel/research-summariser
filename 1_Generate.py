import anthropic
import streamlit as st

api_client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

st.set_page_config(page_title="PT Assistant", page_icon="💪", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f0f4f8; }
    .stButton>button {
        background-color: #1d6ff2;
        color: #ffffff;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        width: 100%;
        font-size: 16px;
    }
    .stButton>button:hover { background-color: #1558c9; }
    .stTextArea>div>textarea {
        border-color: #c8d6e5;
        border-radius: 8px;
        background-color: #ffffff !important;
        color: #1a1a2e;
    }
    .stTextInput>div>input {
        border-color: #c8d6e5;
        border-radius: 8px;
        background-color: #ffffff !important;
        color: #1a1a2e;
    }
    .stSelectbox>div>div {
        background-color: #ffffff !important;
        border-color: #c8d6e5;
        border-radius: 8px;
    }
    .output-box {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #1d6ff2;
        margin-top: 1rem;
        color: #1a1a2e;
        box-shadow: 0 2px 12px rgba(29,111,242,0.08);
        white-space: pre-wrap;
    }
    .header-box {
        background: linear-gradient(135deg, #1d6ff2 0%, #5b9cf6 100%);
        padding: 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(29,111,242,0.2);
    }
    .header-box h1 { color: #ffffff !important; margin: 0; font-size: 2.2rem; }
    .header-box p { color: #e8f0fe; margin: 0.5rem 0 0 0; font-size: 1.1rem; }
    label { color: #1a1a2e !important; font-weight: 500; }
    .stExpander {
        background-color: #ffffff !important;
        border-radius: 10px !important;
        border: 1px solid #c8d6e5 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        color: #1d6ff2 !important;
        border: 1px solid #c8d6e5;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1d6ff2 !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []
if "last_generation" not in st.session_state:
    st.session_state.last_generation = None

st.markdown("""
    <div class="header-box">
        <h1>💪 PT Assistant</h1>
        <p>AI-powered content and planning tools for personal trainers</p>
    </div>
""", unsafe_allow_html=True)

def build_prompt(mode, extra, client_name="", client_age="", client_goal="",
                 client_level="", client_equipment="", client_notes=""):
    client_info = f"Client: {client_name}, Age: {client_age}, Goal: {client_goal}, Level: {client_level}, Equipment: {client_equipment}, Notes: {client_notes}." if client_name else ""

    human_instruction = """Important: Write in a natural, human tone. Do not use bullet points with dashes.
    Do not use bold headers with hashtags. Write in flowing paragraphs or numbered lists only.
    Avoid phrases like 'certainly', 'absolutely', 'of course', 'great question', or any AI-sounding language.
    Sound like an experienced personal trainer talking to a colleague, not a robot writing a report."""

    prompts = {
        "Generate full week workout plan": f"""You are an expert personal trainer. Create a detailed, structured 7-day workout plan for this client.
        For each day include: day name, focus area, warm up, main exercises with sets/reps/rest times, cool down, and coaching tips.
        Make sure all 7 days are fully written out. Include rest days where appropriate.
        {client_info} Extra details: {extra} {human_instruction}""",

        "Draft client check-in message": f"""You are a personal trainer writing a warm, motivating WhatsApp check-in message to a client.
        Keep it personal, encouraging, ask about their progress, and remind them of their goal.
        Sound human and friendly, not robotic. {client_info} Extra details: {extra} {human_instruction}""",

        "Create nutrition advice email": f"""You are a personal trainer writing a practical nutrition advice email to a client.
        Keep it simple, actionable, and tailored to their specific goal. Include meal timing tips, what to eat and avoid,
        and one easy recipe idea. {client_info} Extra details: {extra} {human_instruction}""",

        "Write progress summary": f"""You are a personal trainer writing a progress summary for a client after a period of training.
        Highlight achievements, improvements, and set motivating goals for the next phase.
        {client_info} Extra details: {extra} {human_instruction}""",

        "Write Instagram caption": f"""You are a social media expert for personal trainers.
        Write an engaging Instagram caption for a personal trainer to post.
        Make it motivational, authentic, use emojis naturally, and include 10 relevant hashtags at the end.
        Extra details: {extra} {human_instruction}""",

        "Write transformation post": f"""You are a personal trainer writing a compelling transformation story post for Instagram.
        Make it inspiring and authentic, focus on the client's journey, hard work, and mindset shift, not just physical changes.
        Include a call to action at the end. {client_info} Extra details: {extra} {human_instruction}""",

        "Write motivational quote post": f"""You are a personal trainer writing a short, punchy motivational quote post for Instagram.
        Make it original, real, and something a PT would actually say. Add 5 relevant hashtags.
        Extra details: {extra} {human_instruction}""",

        "Write PT bio": f"""You are helping a personal trainer write a compelling professional bio for their Instagram or website.
        Make it confident, warm, and specific. Include their specialty, who they help, and a call to action.
        Extra details: {extra} {human_instruction}""",

        "Write DM template": f"""You are helping a personal trainer write a natural, friendly DM template to send to potential new clients on Instagram.
        It should feel genuine not salesy. Include a hook, a question, and a soft call to action.
        Extra details: {extra} {human_instruction}""",

        "Write pricing package description": f"""You are helping a personal trainer write compelling descriptions for their training packages.
        Make them sound valuable and results-focused. Write 3 tiers: starter, standard, and premium.
        Extra details: {extra} {human_instruction}""",
    }

    return prompts[mode]

def generate_and_store(mode, section, extra, client_name="", client_age="", client_goal="",
                       client_level="", client_equipment="", client_notes=""):
    prompt = build_prompt(mode, extra, client_name, client_age, client_goal,
                         client_level, client_equipment, client_notes)
    full_result = ""

    stream_placeholder = st.empty()
    with api_client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            full_result += text
            stream_placeholder.markdown(f'<div class="output-box">{full_result}▌</div>', unsafe_allow_html=True)
    stream_placeholder.empty()

    st.session_state.history.append({
        "mode": mode,
        "result": full_result,
        "section": section,
        "client_name": client_name.strip().lower() if client_name else ""
    })

    st.session_state.last_generation = {
        "mode": mode,
        "section": section,
        "extra": extra,
        "client_name": client_name,
        "client_age": client_age,
        "client_goal": client_goal,
        "client_level": client_level,
        "client_equipment": client_equipment,
        "client_notes": client_notes
    }

# Tabs
tab1, tab2, tab3 = st.tabs(["👥 Clients", "📱 Social Media", "👤 Personal"])

with tab1:
    st.subheader("👥 Client Tools")
    with st.expander("👤 Client Details", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            client_name = st.text_input("Client name", placeholder="e.g. Sarah", key="c_name")
            client_age = st.text_input("Age", placeholder="e.g. 28", key="c_age")
            client_goal = st.selectbox("Primary goal", [
                "Weight loss", "Muscle gain", "Improve fitness", "Train for an event", "General health"
            ], key="c_goal")
        with col2:
            client_level = st.selectbox("Fitness level", [
                "Complete beginner", "Some experience", "Intermediate", "Advanced"
            ], key="c_level")
            client_equipment = st.selectbox("Equipment available", [
                "Gym (full equipment)", "Home (dumbbells only)", "Home (no equipment)", "Outdoor"
            ], key="c_equip")
            client_notes = st.text_input("Any injuries or notes", placeholder="e.g. bad knees", key="c_notes")

    with st.expander("✏️ What do you want to create?", expanded=True):
        client_mode = st.selectbox("Select what to create", [
            "Generate full week workout plan",
            "Draft client check-in message",
            "Create nutrition advice email",
            "Write progress summary"
        ], key="client_mode", label_visibility="collapsed")
        client_extra = st.text_area("Any extra details", height=100,
                                     placeholder="Add anything specific...", key="client_extra")

    if st.button("⚡ Generate", type="primary", key="client_generate"):
        if client_name:
            st.divider()
            generate_and_store(client_mode, "Clients", client_extra, client_name,
                             client_age, client_goal, client_level, client_equipment, client_notes)
        else:
            st.warning("Please enter a client name first!")

with tab2:
    st.subheader("📱 Social Media Tools")
    with st.expander("✏️ What do you want to create?", expanded=True):
        social_mode = st.selectbox("Select what to create", [
            "Write Instagram caption",
            "Write transformation post",
            "Write motivational quote post"
        ], key="social_mode", label_visibility="collapsed")
        social_extra = st.text_area("What's the post about?", height=120,
                                     placeholder="e.g. client just hit their first pull up, morning workout motivation...",
                                     key="social_extra")

    if st.button("⚡ Generate", type="primary", key="social_generate"):
        if social_extra:
            st.divider()
            generate_and_store(social_mode, "Social Media", social_extra)
        else:
            st.warning("Please add some details about the post first!")

with tab3:
    st.subheader("👤 Personal Tools")
    with st.expander("✏️ What do you want to create?", expanded=True):
        personal_mode = st.selectbox("Select what to create", [
            "Write PT bio",
            "Write DM template",
            "Write pricing package description"
        ], key="personal_mode", label_visibility="collapsed")
        personal_extra = st.text_area("Tell us about yourself", height=120,
                                       placeholder="e.g. specialise in weight loss for busy mums, based in London, 5 years experience...",
                                       key="personal_extra")

    if st.button("⚡ Generate", type="primary", key="personal_generate"):
        if personal_extra:
            st.divider()
            generate_and_store(personal_mode, "Personal", personal_extra)
        else:
            st.warning("Please add some details first!")

# Show latest output
if st.session_state.last_generation and st.session_state.history:
    latest = st.session_state.history[-1]
    st.divider()
    label = f"✅ {latest['mode']}"
    if latest.get('client_name'):
        label += f" for {latest['client_name'].title()}"
    st.subheader(label)
    st.markdown(f'<div class="output-box">{latest["result"]}</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.download_button(
            label="📥 Download",
            data=latest["result"],
            file_name=f"{latest['mode'].lower().replace(' ', '_')}.txt",
            mime="text/plain",
            key="persistent_download"
        )
    with col2:
        if st.button("🗑️ Clear output", key="clear_output"):
            st.session_state.last_generation = None
            st.rerun()