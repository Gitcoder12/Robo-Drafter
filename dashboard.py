import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random
from datetime import datetime

st.set_page_config(
    page_title="RoboDrafter: Evolutionary Config Optimizer",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    .stApp {
        background: linear-gradient(180deg, #0b0f19 0%, #111827 100%);
        color: #e5e7eb;
    }
    h1, h2, h3 {
        color: #22d3ee !important;
        font-family: 'Segoe UI', sans-serif;
    }
    .stMetric {
        background: rgba(34, 211, 238, 0.06);
        border: 1px solid rgba(34, 211, 238, 0.25);
        border-radius: 10px;
        padding: 14px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Session State
# -----------------------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = [
        {"Generation": 0, "Best Score": 0.42, "Mutation Type": "initial"}
    ]
    st.session_state.generation = 0
    st.session_state.best_score = 0.42
    st.session_state.last_mutation = "initial"

MUTATION_TYPES = [
    "policy_tweak",
    "param_noise",
    "strategy_swap",
    "config_replace",
    "aggressive_mutate",
    "conservative_refine",
]

def evolve_generation():
    st.session_state.generation += 1

    # Simulate evolutionary improvement with diminishing returns + noise
    current = st.session_state.best_score
    improvement = random.uniform(0.01, 0.08) * (1.0 - current)  # harder to improve near 1.0
    noise = random.uniform(-0.015, 0.025)
    new_score = min(0.99, max(0.0, current + improvement + noise))

    mutation = random.choice(MUTATION_TYPES)

    st.session_state.best_score = new_score
    st.session_state.last_mutation = mutation

    st.session_state.history.append(
        {
            "Generation": st.session_state.generation,
            "Best Score": round(new_score, 4),
            "Mutation Type": mutation,
        }
    )

# -----------------------------------------------------------------------------
# UI
# -----------------------------------------------------------------------------
st.title("RoboDrafter: Evolutionary Config Optimizer")
st.caption("Adaptive robotic agent that upgrades policies on success and mutates strategy on failure.")

# Metrics
m1, m2, m3 = st.columns(3)
m1.metric("Current Generation", st.session_state.generation)
m2.metric("Best Fitness Score", f"{st.session_state.best_score:.4f}")
m3.metric("Last Mutation", st.session_state.last_mutation)

st.divider()

col_btn, col_info = st.columns([1, 3])
with col_btn:
    if st.button(" Evolve Next Generation", type="primary", use_container_width=True):
        evolve_generation()
        st.rerun()

with col_info:
    st.info(
        "Simulates the **Policy → Evaluator → Mutator** loop. "
        "Each click advances one generation and records fitness + mutation type."
    )

# Chart
st.subheader("Fitness Over Generations")

df = pd.DataFrame(st.session_state.history)

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=df["Generation"],
        y=df["Best Score"],
        mode="lines+markers",
        name="Best Fitness",
        line=dict(color="#22d3ee", width=3),
        marker=dict(size=8, color="#22d3ee"),
    )
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=420,
    xaxis_title="Generation",
    yaxis_title="Fitness Score",
    yaxis=dict(range=[0, 1.05]),
    margin=dict(l=40, r=40, t=30, b=40),
    font=dict(color="#e5e7eb"),
)

st.plotly_chart(fig, use_container_width=True)

# History table
st.subheader("Evolution History")
st.dataframe(
    df.sort_values("Generation", ascending=False),
    use_container_width=True,
    hide_index=True,
)

st.divider()
st.caption(f"RoboDrafter · {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} · Research prototype")
