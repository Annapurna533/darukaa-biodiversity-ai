# ============================================================
# DARUKAA.EARTH
# BIODIVERSITY INTELLIGENCE SYSTEM
# BACKEND PIPELINE
# ============================================================

from backend.input_processor import extract_environmental_data
from backend.conversation import ConversationManager
from reasoning.engine import EnvironmentalReasoningEngine
from reasoning.recommendations import RecommendationEngine


# ============================================================
# GLOBAL COMPONENTS
# ============================================================

conversation_manager = ConversationManager()

reasoning_engine = EnvironmentalReasoningEngine()

recommendation_engine = RecommendationEngine()


# ============================================================
# CLEAR BACKEND CONTEXT
# ============================================================

def clear_pipeline_context():
    """
    Clear all backend conversation and environmental context.

    This is called by the Streamlit Clear Conversation button.
    It ensures that old environmental variables such as
    pollution or water availability do not carry over into
    a completely new analysis.
    """

    conversation_manager.clear()


# ============================================================
# GET CURRENT BACKEND CONTEXT
# ============================================================

def get_pipeline_context():
    """
    Return the current backend environmental context.

    Useful for debugging and testing.
    """

    return conversation_manager.get_context()


# ============================================================
# REQUIRED CONTEXT
# ============================================================

REQUIRED_CONTEXT = [
    "soil_organic_carbon",
    "rainfall",
    "land_use"
]


# ============================================================
# FIND MISSING CONTEXT
# ============================================================

def find_missing_context(context):
    """
    Determine which required environmental variables
    are still missing.
    """

    missing = []

    for key in REQUIRED_CONTEXT:

        if key not in context:
            missing.append(key)

        elif context[key] is None:
            missing.append(key)

    return missing


# ============================================================
# MAIN PIPELINE
# ============================================================

def run_pipeline(user_message):
    """
    Complete Darukaa.Earth intelligence pipeline.

    User message
            ↓
    Input processing
            ↓
    Conversation context
            ↓
    Missing-context detection
            ↓
    Environmental reasoning
            ↓
    Recommendation generation
            ↓
    RAG scientific evidence
            ↓
    Final response
    """

    # --------------------------------------------------------
    # Validate input
    # --------------------------------------------------------

    if not user_message or not str(user_message).strip():

        return {
            "needs_clarification": True,

            "response": (
                "Please describe the environmental conditions "
                "you want me to analyze."
            ),

            "environmental_data":
                conversation_manager.get_context(),

            "reasoning": None,

            "recommendations": []
        }

    user_message = str(user_message).strip()

    # --------------------------------------------------------
    # 1. Store user message
    # --------------------------------------------------------

    conversation_manager.add_message(
        "user",
        user_message
    )

    # --------------------------------------------------------
    # 2. Extract environmental data
    # --------------------------------------------------------

    extracted_data = extract_environmental_data(
        user_message
    )

    # --------------------------------------------------------
    # 3. Update conversation context
    # --------------------------------------------------------

    context = conversation_manager.update_context(
        extracted_data
    )

    # --------------------------------------------------------
    # 4. Find missing required context
    # --------------------------------------------------------

    missing_context = find_missing_context(
        context
    )

    # --------------------------------------------------------
    # 5. Ask clarification if necessary
    # --------------------------------------------------------

    if missing_context:

        missing_names = [
            key.replace("_", " ").title()
            for key in missing_context
        ]

        if len(missing_names) == 1:

            clarification = (
                "I need one more piece of environmental "
                "information before I can perform the "
                "multi-metric analysis: **"
                + missing_names[0]
                + "**."
            )

        else:

            clarification = (
                "I need a little more environmental "
                "information before I can perform the "
                "multi-metric analysis.\n\n"
                "Please provide: **"
                + ", ".join(missing_names)
                + "**."
            )

        conversation_manager.add_message(
            "assistant",
            clarification
        )

        return {
            "needs_clarification": True,

            "response": clarification,

            "environmental_data": context,

            "reasoning": None,

            "recommendations": []
        }

    # --------------------------------------------------------
    # 6. Run environmental reasoning
    # --------------------------------------------------------

    reasoning_result = reasoning_engine.analyze(
        context
    )

    # --------------------------------------------------------
    # 7. Generate recommendations
    # --------------------------------------------------------

    recommendations = recommendation_engine.generate(
        context,
        reasoning_result
    )

    # --------------------------------------------------------
    # 8. Build conversational response
    # --------------------------------------------------------

    response = build_response(
        context,
        reasoning_result,
        recommendations
    )

    # --------------------------------------------------------
    # 9. Store assistant response
    # --------------------------------------------------------

    conversation_manager.add_message(
        "assistant",
        response
    )

    # --------------------------------------------------------
    # 10. Return result
    # --------------------------------------------------------

    return {
        "needs_clarification": False,

        "response": response,

        "environmental_data": context,

        "reasoning": reasoning_result,

        "recommendations": recommendations
    }


# ============================================================
# RESPONSE BUILDER
# ============================================================

def build_response(
    environmental_data,
    reasoning,
    recommendations
):
    """
    Build the conversational summary.

    Detailed reasoning, pathways and scientific evidence
    are displayed separately by Streamlit.
    """

    pressure_level = reasoning.get(
        "pressure_level",
        "Not assessed"
    )

    affected_metrics = reasoning.get(
        "affected_metrics",
        []
    )

    response = (
        f"Based on the available environmental data, "
        f"the system identified a **{pressure_level} "
        f"system-assessed environmental pressure level** "
        f"using multi-metric relationships."
    )

    if affected_metrics:

        readable_metrics = []

        for metric in affected_metrics:

            readable_metrics.append(
                str(metric).replace(
                    "_",
                    " "
                )
            )

        response += (
            "\n\nThe analysis connects pressures across "
            "multiple environmental dimensions, including "
            + ", ".join(readable_metrics)
            + "."
        )

    if recommendations:

        response += (
            f"\n\nThe system generated "
            f"**{len(recommendations)} evidence-backed "
            f"recommendations** based on these relationships."
        )

    return response


# ============================================================
# COMMAND-LINE TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("==============================================")
    print("DARUKAA.EARTH BIODIVERSITY INTELLIGENCE")
    print("==============================================")

    # ========================================================
    # TEST 1
    # ========================================================

    print()
    print("Test 1: Missing context")
    print("----------------------------------------------")

    clear_pipeline_context()

    result = run_pipeline(
        "My soil organic carbon is 0.3% and rainfall is low."
    )

    print()
    print("Response:")
    print(result["response"])

    print()
    print("Environmental Data:")
    print(result["environmental_data"])

    # ========================================================
    # TEST 2
    # ========================================================

    print()
    print("==============================================")
    print()
    print("Test 2: Multi-turn context")
    print("----------------------------------------------")

    result = run_pipeline(
        "The land is monoculture wheat and "
        "habitat fragmentation is high."
    )

    print()
    print("Response:")
    print(result["response"])

    print()
    print("Environmental Data:")

    for key, value in result[
        "environmental_data"
    ].items():

        print(
            f"  {key}: {value}"
        )

    # ========================================================
    # TEST 3
    # ========================================================

    print()
    print("==============================================")
    print()
    print("Test 3: Clear context")
    print("----------------------------------------------")

    clear_pipeline_context()

    result = run_pipeline(
        "Soil organic carbon is 0.3%, "
        "rainfall is low, "
        "and the land is monoculture wheat."
    )

    print()
    print("Environmental Data After Clear:")

    for key, value in result[
        "environmental_data"
    ].items():

        print(
            f"  {key}: {value}"
        )

    # ========================================================
    # TEST 4
    # ========================================================

    print()
    print("==============================================")
    print()
    print("Test 4: Fresh context verification")
    print("----------------------------------------------")

    clear_pipeline_context()

    result = run_pipeline(
        "Soil organic carbon is 0.3%, "
        "rainfall is low, "
        "and the land is monoculture wheat cultivation. "
        "Habitat fragmentation is also high."
    )

    print()
    print("Environmental Data:")

    for key, value in result[
        "environmental_data"
    ].items():

        print(
            f"  {key}: {value}"
        )

    print()
    print("Reasoning:")

    if result["reasoning"]:
        print(
            result["reasoning"]
        )

    print()
    print("Recommendations:")

    for index, recommendation in enumerate(
        result["recommendations"],
        start=1
    ):

        print(
            f"\n{index}. "
            + recommendation.get(
                "recommendation",
                "Recommendation"
            )
        )

        print(
            "   Time horizon: "
            + str(
                recommendation.get(
                    "time_horizon",
                    "Not specified"
                )
            )
        )

        print(
            "   Confidence: "
            + str(
                recommendation.get(
                    "confidence",
                    "Not specified"
                )
            )
        )

        print(
            "   Metrics: "
            + str(
                recommendation.get(
                    "metrics",
                    []
                )
            )
        )