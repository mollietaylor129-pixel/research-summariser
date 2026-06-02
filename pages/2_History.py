import streamlit as st

st.set_page_config(page_title="History", page_icon="📋", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f0f4f8; }
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
    .content-box {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #1d6ff2;
        margin-top: 0.5rem;
        color: #1a1a2e;
        box-shadow: 0 2px 12px rgba(29,111,242,0.08);
        white-space: pre-wrap;
    }
    .stExpander {
        background-color: #ffffff;
        border-radius: 10px;
        border: 1px solid #c8d6e5;
        margin-bottom: 0.5rem;
    }
    .section-header {
        background-color: #1d6ff2;
        color: #ffffff !important;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        margin: 1.5rem 0 0.75rem 0;
        font-size: 1.1rem;
    }
    .empty-note {
        color: #888;
        font-style: italic;
        padding: 0.5rem 0;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f4f8;
        border-radius: 8px;
        padding: 0.4rem 1rem;
        font-weight: 500;
        color: #1d6ff2 !important;
        border: 1px solid #c8d6e5;
        font-size: 13px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1d6ff2 !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-box">
        <h1>📋 History</h1>
        <p>All your generated content organised by client and category</p>
    </div>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

history = st.session_state.history

client_items = [i for i in history if i.get("section") == "Clients"]
social_items = [i for i in history if i.get("section") == "Social Media"]
personal_items = [i for i in history if i.get("section") == "Personal"]

# ---- CLIENTS ----
st.markdown('<div class="section-header">👥 Clients</div>', unsafe_allow_html=True)

# Build clients dict — same name = same client
clients_dict = {}
for item in client_items:
    name = item.get("client_name", "Unknown").strip().lower().title()
    if name not in clients_dict:
        clients_dict[name] = {
            "Generate full week workout plan": [],
            "Draft client check-in message": [],
            "Create nutrition advice email": [],
            "Write progress summary": []
        }
    mode = item.get("mode", "Unknown")
    if mode in clients_dict[name]:
        clients_dict[name][mode].append(item)

if not clients_dict:
    with st.expander("👤 No clients yet"):
        st.markdown('<p class="empty-note">Generate some client content first and it will appear here.</p>', unsafe_allow_html=True)
else:
    for client_name_key, modes in clients_dict.items():
        total = sum(len(v) for v in modes.values())
        with st.expander(f"👤 {client_name_key} — {total} items"):
            t1, t2, t3, t4 = st.tabs([
                "🏋️ Workout Plans",
                "💬 Check-ins",
                "🥗 Nutrition",
                "📈 Progress"
            ])
            mode_tabs = {
                "Generate full week workout plan": t1,
                "Draft client check-in message": t2,
                "Create nutrition advice email": t3,
                "Write progress summary": t4
            }
            for mode, tab in mode_tabs.items():
                with tab:
                    items = modes.get(mode, [])
                    if not items:
                        st.markdown('<p class="empty-note">Nothing generated yet for this category.</p>', unsafe_allow_html=True)
                    else:
                        for i, item in enumerate(reversed(items)):
                            st.markdown(f'<div class="content-box">{item["result"]}</div>', unsafe_allow_html=True)
                            st.download_button(
                                label="📥 Download",
                                data=item['result'],
                                file_name=f"{client_name_key}_{mode.lower().replace(' ', '_')}_{i}.txt",
                                mime="text/plain",
                                key=f"hist_client_{client_name_key}_{mode}_{i}"
                            )
                            if i < len(items) - 1:
                                st.divider()

# ---- SOCIAL MEDIA ----
st.markdown('<div class="section-header">📱 Social Media</div>', unsafe_allow_html=True)

social_modes = {
    "Write Instagram caption": [],
    "Write transformation post": [],
    "Write motivational quote post": []
}
for item in social_items:
    mode = item.get("mode", "Unknown")
    if mode in social_modes:
        social_modes[mode].append(item)

social_tab1, social_tab2, social_tab3 = st.tabs([
    "📸 Instagram Captions",
    "🔄 Transformation Posts",
    "💪 Motivational Quotes"
])

social_mode_tabs = {
    "Write Instagram caption": social_tab1,
    "Write transformation post": social_tab2,
    "Write motivational quote post": social_tab3
}

for mode, tab in social_mode_tabs.items():
    with tab:
        items = social_modes.get(mode, [])
        if not items:
            st.markdown('<p class="empty-note">Nothing generated yet for this category.</p>', unsafe_allow_html=True)
        else:
            for i, item in enumerate(reversed(items)):
                st.markdown(f'<div class="content-box">{item["result"]}</div>', unsafe_allow_html=True)
                st.download_button(
                    label="📥 Download",
                    data=item['result'],
                    file_name=f"social_{mode.lower().replace(' ', '_')}_{i}.txt",
                    mime="text/plain",
                    key=f"hist_social_{mode}_{i}"
                )
                if i < len(items) - 1:
                    st.divider()

# ---- PERSONAL ----
st.markdown('<div class="section-header">👤 Personal</div>', unsafe_allow_html=True)

personal_modes = {
    "Write PT bio": [],
    "Write DM template": [],
    "Write pricing package description": []
}
for item in personal_items:
    mode = item.get("mode", "Unknown")
    if mode in personal_modes:
        personal_modes[mode].append(item)

pers_tab1, pers_tab2, pers_tab3 = st.tabs([
    "📝 PT Bio",
    "💬 DM Templates",
    "💰 Pricing Packages"
])

personal_mode_tabs = {
    "Write PT bio": pers_tab1,
    "Write DM template": pers_tab2,
    "Write pricing package description": pers_tab3
}

for mode, tab in personal_mode_tabs.items():
    with tab:
        items = personal_modes.get(mode, [])
        if not items:
            st.markdown('<p class="empty-note">Nothing generated yet for this category.</p>', unsafe_allow_html=True)
        else:
            for i, item in enumerate(reversed(items)):
                st.markdown(f'<div class="content-box">{item["result"]}</div>', unsafe_allow_html=True)
                st.download_button(
                    label="📥 Download",
                    data=item['result'],
                    file_name=f"personal_{mode.lower().replace(' ', '_')}_{i}.txt",
                    mime="text/plain",
                    key=f"hist_personal_{mode}_{i}"
                )
                if i < len(items) - 1:
                    st.divider()

# Clear history
st.divider()
if st.button("🗑️ Clear all history", type="secondary"):
    st.session_state.history = []
    st.rerun()