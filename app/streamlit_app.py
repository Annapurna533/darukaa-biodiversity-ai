# ============================================================
# DARUKAA.EARTH
# BIODIVERSITY INTELLIGENCE SYSTEM
# ============================================================

import sys
from pathlib import Path

# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORTS
# ============================================================

import streamlit as st

from backend.pipeline import (
    run_pipeline,
    clear_pipeline_context
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Darukaa.Earth",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   MAIN PAGE
   ============================================================ */

.stApp {
    background-color: #f8fafc !important;
}


/* ============================================================
   GENERAL MARKDOWN TEXT
   ============================================================ */

[data-testid="stMarkdownContainer"] p {
    color: #334155 !important;
}

[data-testid="stMarkdownContainer"] li {
    color: #334155 !important;
}

[data-testid="stMarkdownContainer"] strong {
    color: #1e293b !important;
}

[data-testid="stMarkdownContainer"] b {
    color: #1e293b !important;
}


/* ============================================================
   HEADINGS
   ============================================================ */

[data-testid="stMarkdownContainer"] h1 {
    color: #14532d !important;
}

[data-testid="stMarkdownContainer"] h2 {
    color: #166534 !important;
}

[data-testid="stMarkdownContainer"] h3 {
    color: #166534 !important;
}

[data-testid="stMarkdownContainer"] h4 {
    color: #334155 !important;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

[data-testid="stSidebar"] {
    background-color: #f1f5f9 !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #334155 !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li {
    color: #334155 !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
    color: #14532d !important;
}


/* ============================================================
   HERO BADGE
   ============================================================ */

.hero-badge {
    display: inline-block;

    background-color: #dcfce7;

    color: #166534 !important;

    padding: 7px 14px;

    border-radius: 999px;

    font-size: 12px;

    font-weight: 800;

    margin-bottom: 12px;
}


/* ============================================================
   HERO DESCRIPTION
   ============================================================ */

.hero-description {
    color: #475569 !important;

    font-size: 17px !important;

    line-height: 1.7 !important;

    max-width: 900px;

    margin-bottom: 20px;
}


/* ============================================================
   ENVIRONMENTAL FINDINGS
   ============================================================ */

.finding-card {
    background-color: #ffffff !important;

    border-left: 5px solid #22c55e;

    border-radius: 10px;

    padding: 12px 16px;

    margin-bottom: 8px;

    color: #334155 !important;

    box-shadow:
        0 3px 12px rgba(15, 23, 42, 0.05);
}


/* ============================================================
   PATHWAY
   ============================================================ */

.pathway-card {
    background-color: #f0fdf4 !important;

    border: 1px solid #bbf7d0;

    border-radius: 10px;

    padding: 12px 16px;

    margin-bottom: 8px;

    color: #166534 !important;

    font-weight: 600;

    line-height: 1.5;
}


/* ============================================================
   RECOMMENDATION
   ============================================================ */

.recommendation-card {
    background-color: #ffffff !important;

    border: 1px solid #dbeafe;

    border-radius: 18px;

    padding: 20px;

    margin-bottom: 12px;

    box-shadow:
        0 7px 22px rgba(15, 23, 42, 0.06);
}


/* ============================================================
   RECOMMENDATION NUMBER
   ============================================================ */

.recommendation-number {
    display: inline-block;

    background-color: #dcfce7;

    color: #166534 !important;

    padding: 5px 10px;

    border-radius: 999px;

    font-size: 11px;

    font-weight: 800;
}


/* ============================================================
   RECOMMENDATION TITLE
   ============================================================ */

.recommendation-title {
    color: #0f172a !important;

    font-size: 20px;

    font-weight: 800;

    margin-top: 8px;

    margin-bottom: 10px;
}


/* ============================================================
   RECOMMENDATION TEXT
   ============================================================ */

.recommendation-text {
    color: #334155 !important;

    font-size: 15px;

    line-height: 1.6;
}


/* ============================================================
   SOURCE CARD
   ============================================================ */

.source-card {
    background-color: #ffffff !important;

    border: 1px solid #e2e8f0;

    border-radius: 12px;

    padding: 15px;

    margin-bottom: 10px;
}


/* ============================================================
   SOURCE TITLE
   ============================================================ */

.source-title {
    color: #0f172a !important;

    font-weight: 800;

    font-size: 15px;
}


/* ============================================================
   SOURCE META
   ============================================================ */

.source-meta {
    color: #64748b !important;

    font-size: 12px;

    margin-top: 5px;

    margin-bottom: 10px;
}


/* ============================================================
   EVIDENCE
   ============================================================ */

.evidence-text {
    color: #334155 !important;

    font-size: 14px;

    line-height: 1.6;
}


/* ============================================================
   TAGS
   ============================================================ */

.tag {
    display: inline-block;

    background-color: #eff6ff;

    color: #1d4ed8 !important;

    border: 1px solid #bfdbfe;

    border-radius: 999px;

    padding: 4px 9px;

    margin: 3px;

    font-size: 11px;

    font-weight: 700;
}


/* ============================================================
   ============================================================
   CHAT INPUT — IMPORTANT FIX
   ============================================================
   ============================================================ */

/* Chat input outer container */

[data-testid="stChatInput"] {
    background: transparent !important;
}


/* Main chat input wrapper */

[data-testid="stChatInput"] > div {
    background-color: #ffffff !important;

    border: 1px solid #cbd5e1 !important;

    border-radius: 16px !important;

    box-shadow:
        0 4px 15px rgba(15, 23, 42, 0.08) !important;
}


/* ============================================================
   ACTUAL TEXTAREA
   ============================================================ */

[data-testid="stChatInput"] textarea {
    background-color: #ffffff !important;

    color: #0f172a !important;

    -webkit-text-fill-color: #0f172a !important;

    caret-color: #166534 !important;

    opacity: 1 !important;

    visibility: visible !important;

    font-size: 16px !important;

    font-weight: 500 !important;
}


/* ============================================================
   TEXTAREA INNER ELEMENTS
   ============================================================ */

[data-testid="stChatInput"] textarea:focus {
    background-color: #ffffff !important;

    color: #0f172a !important;

    -webkit-text-fill-color: #0f172a !important;

    caret-color: #166534 !important;

    outline: none !important;
}


/* ============================================================
   PLACEHOLDER
   ============================================================ */

[data-testid="stChatInput"] textarea::placeholder {
    color: #64748b !important;

    -webkit-text-fill-color: #64748b !important;

    opacity: 1 !important;
}


/* ============================================================
   TEXT SELECTION
   ============================================================ */

[data-testid="stChatInput"] textarea::selection {
    background-color: #bbf7d0 !important;

    color: #0f172a !important;

    -webkit-text-fill-color: #0f172a !important;
}


/* ============================================================
   INPUT FOCUS
   ============================================================ */

[data-testid="stChatInput"] > div:focus-within {
    border: 2px solid #22c55e !important;

    box-shadow:
        0 0 0 3px rgba(34, 197, 94, 0.12) !important;
}


/* ============================================================
   CHAT MESSAGE TEXT
   ============================================================ */

[data-testid="stChatMessage"] p {
    color: #334155 !important;
}

[data-testid="stChatMessage"] li {
    color: #334155 !important;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton button {
    color: #334155 !important;

    border-radius: 10px !important;
}


/* ============================================================
   DIVIDER
   ============================================================ */

hr {
    border-color: #e2e8f0 !important;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "environmental_data" not in st.session_state:
    st.session_state.environmental_data = {}

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "# 🌿 Darukaa.Earth"
    )

    st.caption(
        "Biodiversity Intelligence System"
    )

    st.divider()

    st.markdown(
        "### 🧠 System Capabilities"
    )

    st.markdown(
        """
🌱 **Soil health analysis**

🌳 **Biodiversity assessment**

🌦️ **Climate reasoning**

🌾 **Land-use analysis**

🏞️ **Habitat connectivity**

🔬 **Scientific evidence retrieval**

🧩 **Multi-metric reasoning**

💡 **Actionable recommendations**
"""
    )

    st.divider()

    st.markdown(
        "### 📊 Supported Variables"
    )

    st.markdown(
        """
**Soil**

• Soil Organic Carbon  
• Soil pH  
• Soil Moisture  

**Climate**

• Rainfall  
• Temperature  
• Water Availability  

**Land**

• Land Use  
• Land Cover  
• Habitat Fragmentation  

**Biodiversity**

• Species Richness  
• Habitat Diversity  
• Habitat Connectivity  

**Human Impact**

• Pollution  
• Deforestation
"""
    )

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.session_state.environmental_data = {}

        st.session_state.last_result = None

        st.rerun()


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<span class="hero-badge">
AI • RAG • MULTI-METRIC REASONING
</span>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<h1 style="
    color: #14532d !important;
    font-size: 42px !important;
    font-weight: 800 !important;
    margin: 5px 0 8px 0 !important;
">
🌿 Darukaa.Earth
</h1>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<h2 style="
    color: #166534 !important;
    font-size: 27px !important;
    font-weight: 750 !important;
    margin: 0 0 12px 0 !important;
">
Biodiversity Intelligence System
</h2>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero-description">
Understand environmental conditions, connect multiple
ecological metrics, and generate evidence-backed
recommendations using RAG and environmental reasoning.
</div>
""",
    unsafe_allow_html=True,
)

st.divider()


# ============================================================
# READABLE NAMES
# ============================================================

def readable_name(value):

    mapping = {

        "soil_organic_carbon":
            "Soil Organic Carbon",

        "soil_ph":
            "Soil pH",

        "soil_moisture":
            "Soil Moisture",

        "soil_biodiversity":
            "Soil Biodiversity",

        "land_use":
            "Land Use",

        "land_cover":
            "Land Cover",

        "habitat_fragmentation":
            "Habitat Fragmentation",

        "habitat_diversity":
            "Habitat Diversity",

        "habitat_connectivity":
            "Habitat Connectivity",

        "species_richness":
            "Species Richness",

        "rainfall":
            "Rainfall",

        "temperature":
            "Temperature",

        "water_availability":
            "Water Availability",

        "pollution":
            "Pollution",

        "deforestation":
            "Deforestation",

        "vegetation condition":
            "Vegetation Condition",

        "species movement":
            "Species Movement",

        "crop":
            "Crop",
    }

    return mapping.get(
        str(value),
        str(value).replace(
            "_",
            " "
        ).title(),
    )


# ============================================================
# TAG DISPLAY
# ============================================================

def display_tags(values):

    if not values:
        return

    html = ""

    for value in values:

        html += (
            '<span class="tag">'
            + readable_name(value)
            + '</span>'
        )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


# ============================================================
# ENVIRONMENTAL CONTEXT
# ============================================================

def display_environmental_context(
    environmental_data
):

    if not environmental_data:
        return

    st.markdown(
        "## 🌍 Environmental Context"
    )

    items = list(
        environmental_data.items()
    )

    for start in range(
        0,
        len(items),
        4,
    ):

        row = items[
            start:start + 4
        ]

        columns = st.columns(4)

        for column, (
            key,
            value,
        ) in zip(
            columns,
            row,
        ):

            with column:

                st.metric(
                    label=readable_name(key),
                    value=str(value),
                )


# ============================================================
# REASONING
# ============================================================

def display_reasoning(reasoning):

    if not reasoning:
        return

    st.markdown(
        "## 🧠 Environmental Reasoning"
    )

    pressures = reasoning.get(
        "pressures",
        [],
    )

    interactions = reasoning.get(
        "interactions",
        [],
    )

    affected_metrics = reasoning.get(
        "affected_metrics",
        [],
    )

    findings = reasoning.get(
        "findings",
        [],
    )

    pressure_level = reasoning.get(
        "pressure_level",
        "Not assessed",
    )


    # ========================================================
    # SUMMARY
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Direct Pressures",
            len(pressures),
        )

    with col2:

        st.metric(
            "Interaction Pathways",
            len(interactions),
        )

    with col3:

        st.metric(
            "Affected Metrics",
            len(affected_metrics),
        )

    with col4:

        st.metric(
            "System Assessment",
            pressure_level,
        )


    # ========================================================
    # FINDINGS
    # ========================================================

    if findings:

        st.markdown(
            "### 🔎 Detected Environmental Pressures"
        )

        for finding in findings:

            st.markdown(
                f"""
<div class="finding-card">
{finding}
</div>
""",
                unsafe_allow_html=True,
            )


    # ========================================================
    # PATHWAYS
    # ========================================================

    if interactions:

        st.markdown(
            "### 🔗 Multi-Metric Interaction Pathways"
        )

        for index, interaction in enumerate(
            interactions,
            start=1,
        ):

            if isinstance(
                interaction,
                dict,
            ):

                pathway = interaction.get(
                    "pathway",
                    [],
                )

            else:

                pathway = interaction


            if isinstance(
                pathway,
                list,
            ):

                pathway_text = " → ".join(
                    str(item)
                    for item in pathway
                )

            else:

                pathway_text = str(pathway)


            st.markdown(
                f"""
<div class="pathway-card">
<b>{index}.</b> {pathway_text}
</div>
""",
                unsafe_allow_html=True,
            )


    # ========================================================
    # AFFECTED METRICS
    # ========================================================

    if affected_metrics:

        st.markdown(
            "### 📊 Affected Environmental Metrics"
        )

        display_tags(
            affected_metrics
        )


# ============================================================
# RECOMMENDATIONS
# ============================================================

def display_recommendations(
    recommendations
):

    if not recommendations:
        return

    st.markdown(
        "## 💡 Evidence-Backed Recommendations"
    )

    for index, recommendation in enumerate(
        recommendations,
        start=1,
    ):

        if not isinstance(
            recommendation,
            dict,
        ):
            st.write(recommendation)
            continue

        # ====================================================
        # DATA
        # ====================================================

        action = recommendation.get(
            "recommendation",
            recommendation.get(
                "action",
                "Recommended intervention",
            ),
        )

        why = recommendation.get(
            "why",
            recommendation.get(
                "scientific_reasoning",
                "This action is connected to "
                "the detected environmental pressures.",
            ),
        )

        metrics = recommendation.get(
            "metrics",
            recommendation.get(
                "impacted_metrics",
                [],
            ),
        )

        time_horizon = recommendation.get(
            "time_horizon",
            recommendation.get(
                "time",
                "Not specified",
            ),
        )

        confidence = recommendation.get(
            "confidence",
            "Not specified",
        )

        pathways = recommendation.get(
            "reasoning_pathways",
            [],
        )

        evidence = recommendation.get(
            "evidence",
            [],
        )

        # ====================================================
        # RECOMMENDATION
        # ====================================================

        st.markdown(
            f"### 🌱 Recommendation {index}"
        )

        st.markdown(
            f"**{action}**"
        )

        st.markdown(
            f"**Why:** {why}"
        )

        # ====================================================
        # DETAILS
        # ====================================================

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                "**⏳ Time Horizon**"
            )
            st.write(
                time_horizon
            )

        with col2:
            st.markdown(
                "**🎯 Confidence**"
            )
            st.write(
                confidence
            )

        with col3:
            st.markdown(
                "**📊 Impacted Metrics**"
            )
            display_tags(
                metrics
            )

        # ====================================================
        # REASONING PATHWAYS
        # ====================================================

        if pathways:

            with st.expander(
                "🧠 Why the system selected this action"
            ):

                st.markdown(
                    "#### Environmental reasoning"
                )

                for pathway in pathways:

                    if isinstance(
                        pathway,
                        list,
                    ):
                        pathway_text = " → ".join(
                            str(item)
                            for item in pathway
                        )
                    else:
                        pathway_text = str(pathway)

                    st.info(
                        pathway_text
                    )

                st.markdown(
                    "#### Interpretation"
                )

                st.write(
                    "The system connects detected "
                    "environmental pressures with their "
                    "effects across multiple ecological "
                    "metrics before selecting the action."
                )

        # ====================================================
        # SCIENTIFIC EVIDENCE
        # ====================================================

        if evidence:

            with st.expander(
                f"🔬 Scientific Evidence ({len(evidence)} sources)",
                expanded=True,
            ):

                for evidence_index, item in enumerate(
                    evidence,
                    start=1,
                ):

                    if not isinstance(
                        item,
                        dict,
                    ):
                        st.write(item)
                        continue

                    source = item.get(
                        "source",
                        "Unknown source",
                    )

                    organization = item.get(
                        "organization",
                        "",
                    )

                    year = item.get(
                        "year",
                        "n.d.",
                    )

                    topic = item.get(
                        "topic",
                        "",
                    )

                    source_type = item.get(
                        "source_type",
                        "",
                    )

                    passage = item.get(
                        "passage",
                        "",
                    )

                    url = item.get(
                        "url",
                        "",
                    )

                    st.markdown(
                        f"**📚 Evidence Source {evidence_index}: {source}**"
                    )

                    metadata_parts = [
                        str(value)
                        for value in [
                            organization,
                            year,
                            topic,
                            source_type,
                        ]
                        if value
                    ]

                    if metadata_parts:
                        st.caption(
                            " • ".join(
                                metadata_parts
                            )
                        )

                    if passage:

                        st.markdown(
                            "**Retrieved evidence:**"
                        )

                        st.info(
                            passage
                        )

                    if url:

                        st.markdown(
                            f"[🔗 View source]({url})"
                        )

                    if evidence_index < len(evidence):
                        st.divider()

        if index < len(recommendations):
            st.divider()



# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    role = message.get(
        "role",
        "assistant",
    )

    content = message.get(
        "content",
        "",
    )

    with st.chat_message(role):

        st.markdown(
            content
        )

        stored_result = message.get(
            "result"
        )

        if (
            role == "assistant"
            and stored_result
            and not stored_result.get(
                "needs_clarification",
                False,
            )
        ):

            display_environmental_context(
                stored_result.get(
                    "environmental_data",
                    {},
                )
            )

            display_reasoning(
                stored_result.get(
                    "reasoning",
                    {},
                )
            )

            display_recommendations(
                stored_result.get(
                    "recommendations",
                    [],
                )
            )


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "Describe the environmental conditions..."
)


# ============================================================
# PROCESS INPUT
# ============================================================

if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):

        st.markdown(
            user_input
        )

    with st.chat_message("assistant"):

        with st.spinner(
            "🌿 Analyzing environmental relationships..."
        ):

            try:

                result = run_pipeline(
                    user_input
                )

                st.session_state.last_result = result

                st.session_state.environmental_data = (
                    result.get(
                        "environmental_data",
                        {},
                    )
                )

                # =================================================
                # CLARIFICATION
                # =================================================

                if result.get(
                    "needs_clarification",
                    False,
                ):

                    response = result.get(
                        "response",
                        "I need more environmental information.",
                    )

                    st.markdown(
                        response
                    )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": response,
                        }
                    )

                # =================================================
                # COMPLETE ANALYSIS
                # =================================================

                else:

                    response = result.get(
                        "response",
                        "Environmental analysis completed.",
                    )

                    st.markdown(
                        response
                    )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": response,
                            "result": result,
                        }
                    )

                    display_environmental_context(
                        result.get(
                            "environmental_data",
                            {},
                        )
                    )

                    display_reasoning(
                        result.get(
                            "reasoning",
                            {},
                        )
                    )

                    display_recommendations(
                        result.get(
                            "recommendations",
                            [],
                        )
                    )

            except Exception as error:

                st.error(
                    "Something went wrong while "
                    "processing the environmental analysis."
                )

                st.exception(
                    error
                )
