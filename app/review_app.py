import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────────────
RESULTS_FILE = "data/synthetic_results.csv"
REVIEWED_FILE = "data/reviewed_labels.csv"
LABELS = ["PME", "T", "RNF", "NA"]

# ── Page setup ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="OccuMap — Human Review Queue",
    page_icon="🔍",
    layout="wide"
)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_results():
    df = pd.read_csv(RESULTS_FILE)
    df['llm_label'] = df['llm_label'].fillna('NA')
    df['rule_based_label'] = df['rule_based_label'].fillna('NONE')
    return df

def load_reviewed():
    if os.path.exists(REVIEWED_FILE):
        return pd.read_csv(REVIEWED_FILE)
    return pd.DataFrame(columns=[
        "original_title", "llm_label", "final_label",
        "override_reason", "reviewed_by", "reviewed_at"
    ])

def save_review(original_title, llm_label, final_label,
                override_reason, reviewed_by):
    reviewed_df = load_reviewed()
    reviewed_df = reviewed_df[
        reviewed_df['original_title'] != original_title
    ]
    new_row = pd.DataFrame([{
        "original_title": original_title,
        "llm_label": llm_label,
        "final_label": final_label,
        "override_reason": override_reason if final_label != llm_label else "",
        "reviewed_by": reviewed_by,
        "reviewed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    reviewed_df = pd.concat([reviewed_df, new_row], ignore_index=True)
    reviewed_df.to_csv(REVIEWED_FILE, index=False)

# ── Label styling ─────────────────────────────────────────────────────────────
LABEL_EMOJI = {"PME": "🔵", "T": "🟡", "RNF": "🟠", "NA": "⚪"}
STATUS_EMOJI = {"NEEDS_REVIEW": "🔎", "DISAGREE": "⚠️"}

# ── Main ──────────────────────────────────────────────────────────────────────
st.title("🔍 OccuMap — Human Review Queue")
st.caption("Review low-confidence and disputed occupation classifications")

results_df = load_results()
reviewed_df = load_reviewed()
reviewed_map = dict(zip(reviewed_df['original_title'], reviewed_df['final_label']))

review_queue = results_df[
    results_df['validation_status'].isin(['NEEDS_REVIEW', 'DISAGREE'])
].copy().reset_index(drop=True)

reviewed_count = sum(1 for t in review_queue['original_title'] if t in reviewed_map)
pending_count = len(review_queue) - reviewed_count

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Queue Status")
    st.metric("Total for review", len(review_queue))
    st.metric("Reviewed", reviewed_count)
    st.metric("Pending", pending_count)
    st.divider()
    reviewed_by = st.text_input("Your initials", value="SL")
    st.divider()
    status_filter = st.multiselect(
        "Filter by status",
        options=["NEEDS_REVIEW", "DISAGREE"],
        default=["DISAGREE", "NEEDS_REVIEW"]
    )
    st.divider()
    st.caption(f"Prompt version: {results_df['prompt_version'].iloc[0]}")

# Apply filter
filtered_queue = review_queue.copy()
if status_filter:
    filtered_queue = filtered_queue[
        filtered_queue['validation_status'].isin(status_filter)
    ].reset_index(drop=True)

# ── Queue ─────────────────────────────────────────────────────────────────────
if pending_count == 0:
    st.success("✅ All records reviewed.")
    st.balloons()
else:
    st.markdown(f"**{pending_count} records pending · {reviewed_count} reviewed**")

st.divider()

# Column headers
h1, h2, h3, h4 = st.columns([2, 1, 4, 2])
h1.markdown("**Original Title**")
h2.markdown("**LLM Label**")
h3.markdown("**Reasoning**")
h4.markdown("**Decision**")
st.divider()

# One row per record
for i, row in filtered_queue.iterrows():
    title = row['original_title']
    is_reviewed = title in reviewed_map

    if is_reviewed:
        # ── Collapsed reviewed row ────────────────────────────────────────
        final = reviewed_map[title]
        emoji = LABEL_EMOJI.get(final, "⚫")
        col1, col2 = st.columns([10, 2])
        with col1:
            st.markdown(
                f"<span style='color: gray; font-size: 0.85em;'>"
                f"{emoji} &nbsp; {title} &nbsp;→&nbsp; {final} &nbsp;&nbsp; ✅ Reviewed"
                f"</span>",
                unsafe_allow_html=True
            )
        st.divider()

    else:
        # ── Full pending row ──────────────────────────────────────────────
        col1, col2, col3, col4 = st.columns([2, 1, 4, 2])

        with col1:
            status_icon = STATUS_EMOJI.get(row['validation_status'], "")
            st.markdown(f"{status_icon} **{title}**")
            st.caption(f"SSOC {row['llm_ssoc_code']} · {row['llm_ssoc_occupation_title']}")

        with col2:
            emoji = LABEL_EMOJI.get(row['llm_label'], "⚫")
            st.markdown(f"{emoji} **{row['llm_label']}**")
            st.caption(f"{row['llm_confidence']:.0%} · {int(row['llm_votes'])}/3")

        with col3:
            st.caption(row['llm_reasoning'])

        with col4:
            if st.button("✅ Accept", key=f"accept_{i}", use_container_width=True):
                save_review(title, row['llm_label'], row['llm_label'], "", reviewed_by)
                st.cache_data.clear()
                st.rerun()

            with st.expander("✏️ Override"):
                override_label = st.selectbox(
                    "Correct label",
                    options=LABELS,
                    index=LABELS.index(row['llm_label'])
                    if row['llm_label'] in LABELS else 0,
                    key=f"select_{i}"
                )
                override_reason = st.text_input(
                    "Reason",
                    placeholder="Why are you overriding?",
                    key=f"reason_{i}"
                )
                if st.button("Confirm", key=f"confirm_{i}",
                             use_container_width=True):
                    if not override_reason:
                        st.error("Please provide a reason.")
                    else:
                        save_review(
                            title, row['llm_label'],
                            override_label, override_reason, reviewed_by
                        )
                        st.cache_data.clear()
                        st.rerun()

        st.divider()

# ── Reviewed records table ────────────────────────────────────────────────────
reviewed_df = load_reviewed()
if len(reviewed_df) > 0:
    st.divider()
    with st.expander(f"📋 Reviewed records ({len(reviewed_df)})"):
        st.dataframe(reviewed_df, use_container_width=True)