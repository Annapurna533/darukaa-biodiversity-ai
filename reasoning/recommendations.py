# reasoning/recommendations.py

"""
Darukaa.Earth
Evidence-Backed Environmental Recommendation Engine

Flow:

Environmental Data
        ↓
Reasoning Engine
        ↓
Recommendation Rules
        ↓
Knowledge Graph Pathways
        ↓
RAG Evidence Retrieval
        ↓
Evidence-Backed Recommendation
"""

from reasoning.engine import analyze_environment
from rag.retrieve import retrieve_evidence
from knowledge_graph.graph import find_path, format_path


# ============================================================
# DISPLAY NAMES
# ============================================================

METRIC_NAMES = {
    "soil_organic_carbon": "Soil Organic Carbon",
    "soil_moisture": "Soil Moisture",
    "soil_biodiversity": "Soil Biodiversity",
    "rainfall": "Rainfall",
    "water_availability": "Water Availability",
    "habitat_diversity": "Habitat Diversity",
    "species_richness": "Species Richness",
    "land_use": "Land Use",
    "habitat_fragmentation": "Habitat Fragmentation",
    "habitat_connectivity": "Habitat Connectivity",
    "vegetation condition": "Vegetation Condition",
    "pollution": "Pollution",
    "deforestation": "Deforestation",
    "soil_quality": "Soil Quality",
    "water_quality": "Water Quality",
}


def display_metric(metric):
    return METRIC_NAMES.get(
        metric,
        metric.replace("_", " ").title()
    )


# ============================================================
# KNOWLEDGE GRAPH TARGETS
# ============================================================

RECOMMENDATION_GRAPH_TARGETS = {

    "cover_crop": [
        "soil_biodiversity_pressure",
        "vegetation_stress",
        "species_richness_pressure",
    ],

    "intercropping": [
        "habitat_diversity_pressure",
        "species_richness_pressure",
        "soil_biodiversity_pressure",
    ],

    "agroforestry": [
        "habitat_diversity_pressure",
        "reduced_connectivity",
        "species_richness_pressure",
    ],

    "corridor": [
        "reduced_connectivity",
        "species_richness_pressure",
        "habitat_diversity_pressure",
    ],

    "restoration": [
        "habitat_diversity_pressure",
        "reduced_connectivity",
        "species_richness_pressure",
    ],

    "pollution_reduction": [
        "organism_stress",
        "water_quality_pressure",
        "soil_quality_pressure",
        "species_richness_pressure",
    ],
}


# ============================================================
# GRAPH PATHWAY RETRIEVAL
# ============================================================

def get_graph_pathways(
    pressures,
    recommendation_type
):
    """
    Find explicit Knowledge Graph pathways relevant
    to the recommendation.
    """

    targets = RECOMMENDATION_GRAPH_TARGETS.get(
        recommendation_type,
        []
    )

    pathways = []

    seen = set()

    for pressure in pressures:

        for target in targets:

            path = find_path(
                pressure,
                target
            )

            if not path:
                continue

            formatted = format_path(
                path
            )

            if formatted in seen:
                continue

            seen.add(
                formatted
            )

            pathways.append({

                "source_pressure":
                    pressure,

                "target":
                    target,

                "path":
                    path,

                "formatted_path":
                    formatted,
            })


    return pathways


# ============================================================
# RECOMMENDATION-SPECIFIC PATHWAYS
# ============================================================

RECOMMENDATION_SPECIFIC_PATHWAYS = {
    "cover_crop": [
        ("low_soil_organic_carbon", "soil_biodiversity_pressure"),
        ("low_soil_organic_carbon", "vegetation_stress"),
        ("low_rainfall", "soil_biodiversity_pressure"),
    ],

    "intercropping": [
        ("monoculture", "habitat_diversity_pressure"),
        ("monoculture", "species_richness_pressure"),
        ("monoculture", "soil_biodiversity_pressure"),
    ],

    "agroforestry": [
        ("monoculture", "habitat_diversity_pressure"),
        ("monoculture", "species_richness_pressure"),
        ("low_soil_organic_carbon", "habitat_diversity_pressure"),
    ],

    "corridor": [
        ("habitat_fragmentation", "reduced_connectivity"),
        ("habitat_fragmentation", "species_richness_pressure"),
        ("habitat_fragmentation", "habitat_diversity_pressure"),
    ],

    "restoration": [
        ("high_deforestation", "reduced_connectivity"),
        ("high_deforestation", "species_richness_pressure"),
        ("high_deforestation", "habitat_diversity_pressure"),
    ],

    "pollution_reduction": [
        ("high_pollution", "organism_stress"),
        ("high_pollution", "water_quality_pressure"),
        ("high_pollution", "soil_quality_pressure"),
        ("high_pollution", "species_richness_pressure"),
    ],
}


def get_recommendation_pathways(pressures, recommendation_type):
    """
    Return only Knowledge Graph pathways that directly support
    the selected recommendation.
    """

    pathway_rules = RECOMMENDATION_SPECIFIC_PATHWAYS.get(
        recommendation_type,
        []
    )

    pathways = []
    seen = set()

    for source_pressure, target in pathway_rules:

        if source_pressure not in pressures:
            continue

        path = find_path(
            source_pressure,
            target
        )

        if not path:
            continue

        formatted = format_path(path)

        if formatted in seen:
            continue

        seen.add(formatted)

        pathways.append({
            "source_pressure": source_pressure,
            "target": target,
            "path": path,
            "formatted_path": formatted,
        })

    return pathways


# ============================================================
# RECOMMENDATION BUILDER
# ============================================================

def _make_recommendation(
    action,
    why,
    metrics,
    time_horizon,
    confidence,
    recommendation_type,
    pressures,
    reasoning_pathways=None
):

    # --------------------------------------------------------
    # Knowledge Graph reasoning
    # --------------------------------------------------------

    graph_pathways = get_recommendation_pathways(
        pressures,
        recommendation_type
    )


    # --------------------------------------------------------
    # RAG evidence
    # --------------------------------------------------------

    evidence = retrieve_evidence(
        recommendation=action,
        metrics=metrics,
        pathways=(
            reasoning_pathways or []
        ),
        top_k=3
    )


    # --------------------------------------------------------
    # Human-readable graph pathways
    # --------------------------------------------------------

    graph_reasoning = [

        item[
            "formatted_path"
        ]

        for item in graph_pathways

    ]


    # --------------------------------------------------------
    # Evidence source summary
    # --------------------------------------------------------

    evidence_sources = []

    for item in evidence:

        source = {
            "source_id":
                item.get(
                    "source_id"
                ),

            "source":
                item.get(
                    "source"
                ),

            "organization":
                item.get(
                    "organization"
                ),

            "year":
                item.get(
                    "year"
                ),

            "topic":
                item.get(
                    "topic"
                ),

            "source_type":
                item.get(
                    "source_type"
                ),

            "url":
                item.get(
                    "url"
                ),

            "passage":
                item.get(
                    "passage"
                ),

            "relevance_score":
                item.get(
                    "relevance_score"
                ),
        }

        evidence_sources.append(
            source
        )


    # --------------------------------------------------------
    # Final recommendation object
    # --------------------------------------------------------

    return {

        "action":
            action,

        "why":
            why,

        "metrics":
            [
                display_metric(
                    metric
                )

                for metric in metrics
            ],

        "time_horizon":
            time_horizon,

        "confidence":
            confidence,

        "recommendation_type":
            recommendation_type,

        "reasoning_pathways":
            [
                item["formatted_path"]
                for item in graph_pathways
            ] or reasoning_pathways or [],

        "knowledge_graph_pathways":
            graph_reasoning,

        "knowledge_graph_details":
            graph_pathways,

        "evidence":
            evidence_sources,

        "evidence_count":
            len(
                evidence_sources
            ),

        "grounding": {

            "knowledge_graph":
                len(
                    graph_pathways
                ) > 0,

            "rag_evidence":
                len(
                    evidence_sources
                ) > 0,

            "scientific_grounding":
                (
                    len(
                        graph_pathways
                    ) > 0
                    and
                    len(
                        evidence_sources
                    ) > 0
                ),
        },
    }


# ============================================================
# MAIN RECOMMENDATION ENGINE
# ============================================================

def generate_recommendations(
    environmental_data,
    reasoning_result=None
):
    """
    Generate evidence-backed environmental
    recommendations.
    """

    # --------------------------------------------------------
    # Run reasoning engine if needed
    # --------------------------------------------------------

    if reasoning_result is None:

        reasoning_result = analyze_environment(
            environmental_data
        )


    pressures = reasoning_result.get(
        "pressures",
        []
    )


    interactions = reasoning_result.get(
        "interactions",
        []
    )


    # --------------------------------------------------------
    # Existing reasoning pathways
    # --------------------------------------------------------

    reasoning_pathways = reasoning_result.get(
        "interaction_explanations",
        []
    )


    recommendations = []


    # ========================================================
    # RULE 1
    # LOW SOC + LOW RAINFALL
    # ========================================================

    if (
        "low_soil_organic_carbon" in pressures
        and
        "low_rainfall" in pressures
    ):

        recommendations.append(

            _make_recommendation(

                action=(
                    "Introduce suitable "
                    "legume-based cover crops."
                ),

                why=(
                    "Cover crops can add organic "
                    "inputs to the soil and support "
                    "soil biological activity. Under "
                    "low-rainfall conditions, maintaining "
                    "soil cover can also support soil "
                    "moisture-related functions. The "
                    "specific species should be selected "
                    "according to local climate, soil "
                    "and crop conditions."
                ),

                metrics=[
                    "soil_organic_carbon",
                    "soil_moisture",
                    "soil_biodiversity",
                ],

                time_horizon=(
                    "Medium term: "
                    "approximately 2–3 years"
                ),

                confidence="Medium",

                recommendation_type="cover_crop",

                pressures=pressures,

                reasoning_pathways=(
                    reasoning_pathways
                ),
            )
        )


    # ========================================================
    # RULE 2
    # MONOCULTURE + LOW RAINFALL
    # ========================================================

    if (
        "monoculture" in pressures
        and
        "low_rainfall" in pressures
    ):

        recommendations.append(

            _make_recommendation(

                action=(
                    "Introduce suitable "
                    "crop intercropping."
                ),

                why=(
                    "Diversifying crop structure can "
                    "increase vegetation and resource "
                    "diversity compared with a uniform "
                    "monoculture. This can create more "
                    "varied habitat conditions and may "
                    "support biodiversity while "
                    "distributing resource demand "
                    "across crops. Crop combinations "
                    "should be selected for local water "
                    "availability and compatibility."
                ),

                metrics=[
                    "habitat_diversity",
                    "species_richness",
                    "soil_biodiversity",
                ],

                time_horizon=(
                    "Short to medium term: "
                    "1–3 years"
                ),

                confidence="Medium",

                recommendation_type="intercropping",

                pressures=pressures,

                reasoning_pathways=(
                    reasoning_pathways
                ),
            )
        )


    # ========================================================
    # RULE 3
    # MONOCULTURE + LOW SOC
    # ========================================================

    if (
        "monoculture" in pressures
        and
        "low_soil_organic_carbon" in pressures
    ):

        recommendations.append(

            _make_recommendation(

                action=(
                    "Evaluate suitable agroforestry "
                    "strips or native vegetation zones."
                ),

                why=(
                    "Introducing trees or native "
                    "vegetation within suitable parts "
                    "of an agricultural landscape can "
                    "increase structural and habitat "
                    "diversity. Vegetation inputs can "
                    "also contribute to soil-related "
                    "functions. Species and spacing "
                    "should be adapted to local water "
                    "availability, soils and agricultural "
                    "objectives."
                ),

                metrics=[
                    "habitat_diversity",
                    "habitat_connectivity",
                    "species_richness",
                    "soil_organic_carbon",
                ],

                time_horizon=(
                    "Long term: "
                    "approximately 3–5+ years"
                ),

                confidence="Medium",

                recommendation_type="agroforestry",

                pressures=pressures,

                reasoning_pathways=(
                    reasoning_pathways
                ),
            )
        )


    # ========================================================
    # RULE 4
    # HABITAT FRAGMENTATION
    # ========================================================

    if (
        "habitat_fragmentation"
        in pressures
    ):

        recommendations.append(

            _make_recommendation(

                action=(
                    "Maintain or establish connected "
                    "native vegetation corridors "
                    "where feasible."
                ),

                why=(
                    "Connected vegetation can reduce "
                    "the isolation of habitat patches "
                    "and provide routes or stepping-stone "
                    "habitat for species movement. "
                    "Maintaining connectivity can "
                    "therefore support landscape-level "
                    "biodiversity functions."
                ),

                metrics=[
                    "habitat_connectivity",
                    "habitat_diversity",
                    "species_richness",
                ],

                time_horizon=(
                    "Medium to long term: "
                    "2–5+ years"
                ),

                confidence="Medium",

                recommendation_type="corridor",

                pressures=pressures,

                reasoning_pathways=(
                    reasoning_pathways
                ),
            )
        )


    # ========================================================
    # RULE 5
    # DEFORESTATION
    # ========================================================

    if (
        "high_deforestation"
        in pressures
    ):

        recommendations.append(

            _make_recommendation(

                action=(
                    "Prioritize native vegetation "
                    "restoration in suitable "
                    "degraded areas."
                ),

                why=(
                    "Restoring suitable native "
                    "vegetation can recover habitat "
                    "structure and improve landscape "
                    "connectivity. Restoration planning "
                    "should consider local species, "
                    "soil conditions, water availability "
                    "and surrounding land use."
                ),

                metrics=[
                    "habitat_connectivity",
                    "habitat_diversity",
                    "species_richness",
                ],

                time_horizon=(
                    "Long term: "
                    "approximately 3–5+ years"
                ),

                confidence="Medium",

                recommendation_type="restoration",

                pressures=pressures,

                reasoning_pathways=(
                    reasoning_pathways
                ),
            )
        )


    # ========================================================
    # RULE 6
    # POLLUTION
    # ========================================================

    if (
        "high_pollution"
        in pressures
    ):

        recommendations.append(

            _make_recommendation(

                action=(
                    "Identify and reduce the "
                    "dominant local pollution source."
                ),

                why=(
                    "Reducing the dominant pollution "
                    "source can decrease environmental "
                    "stress on organisms and reduce "
                    "pressure on soil or water quality. "
                    "The intervention should be selected "
                    "after identifying the specific "
                    "pollutant and pathway."
                ),

                metrics=[
                    "pollution",
                    "species_richness",
                ],

                time_horizon=(
                    "Months to approximately "
                    "2 years"
                ),

                confidence="Medium",

                recommendation_type=(
                    "pollution_reduction"
                ),

                pressures=pressures,

                reasoning_pathways=(
                    reasoning_pathways
                ),
            )
        )


    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    unique = []

    seen_actions = set()


    for recommendation in recommendations:

        action = recommendation[
            "action"
        ]

        if action in seen_actions:

            continue

        seen_actions.add(
            action
        )

        unique.append(
            recommendation
        )


    return unique


# ============================================================
# COMPATIBILITY CLASS
# ============================================================

class RecommendationEngine:
    """
    Compatibility wrapper used by backend.pipeline.py.
    """

    def __init__(self):

        pass


    def generate(
        self,
        environmental_data,
        reasoning_result=None
    ):

        return generate_recommendations(
            environmental_data,
            reasoning_result
        )


    def generate_recommendations(
        self,
        environmental_data,
        reasoning_result=None
    ):

        return generate_recommendations(
            environmental_data,
            reasoning_result
        )


    def get_recommendations(
        self,
        environmental_data,
        reasoning_result=None
    ):

        return generate_recommendations(
            environmental_data,
            reasoning_result
        )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_data = {

        "soil_organic_carbon":
            0.3,

        "rainfall":
            "low",

        "land_use":
            "monoculture",

        "crop":
            "wheat",

        "habitat_fragmentation":
            "high",
    }


    print()
    print("=" * 70)
    print(
        "DARUKAA INTEGRATED RECOMMENDATION ENGINE TEST"
    )
    print("=" * 70)


    # --------------------------------------------------------
    # Reasoning
    # --------------------------------------------------------

    reasoning = analyze_environment(
        test_data
    )


    print()
    print("PRESSURES")
    print("-" * 70)

    for pressure in reasoning[
        "pressures"
    ]:

        print(
            "-",
            pressure
        )


    # --------------------------------------------------------
    # Recommendations
    # --------------------------------------------------------

    print()
    print("GENERATING RECOMMENDATIONS...")
    print("-" * 70)


    recommendations = generate_recommendations(
        test_data,
        reasoning
    )


    print()
    print(
        "Number of recommendations:",
        len(recommendations)
    )


    # --------------------------------------------------------
    # Display recommendations
    # --------------------------------------------------------

    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):

        print()
        print(
            f"RECOMMENDATION {index}"
        )

        print(
            "Action:",
            recommendation[
                "action"
            ]
        )

        print(
            "Why:",
            recommendation[
                "why"
            ]
        )

        print(
            "Metrics:",
            recommendation[
                "metrics"
            ]
        )

        print(
            "Time:",
            recommendation[
                "time_horizon"
            ]
        )

        print(
            "Confidence:",
            recommendation[
                "confidence"
            ]
        )


        print()
        print(
            "Knowledge Graph Pathways:"
        )

        graph_paths = recommendation.get(
            "knowledge_graph_pathways",
            []
        )

        if graph_paths:

            for path in graph_paths:

                print(
                    "  →",
                    path
                )

        else:

            print(
                "  → No matching graph pathway"
            )


        print()
        print(
            "RAG Evidence:"
        )

        evidence = recommendation.get(
            "evidence",
            []
        )

        if evidence:

            for source in evidence:

                print(
                    "  →",
                    source.get(
                        "organization"
                    ),
                    "-",
                    source.get(
                        "source"
                    )
                )

        else:

            print(
                "  → No evidence retrieved"
            )


        print()
        print(
            "Grounding:"
        )

        print(
            "  Knowledge Graph:",
            recommendation[
                "grounding"
            ][
                "knowledge_graph"
            ]
        )

        print(
            "  RAG Evidence:",
            recommendation[
                "grounding"
            ][
                "rag_evidence"
            ]
        )

        print(
            "  Scientific Grounding:",
            recommendation[
                "grounding"
            ][
                "scientific_grounding"
            ]
        )


    print()
    print("=" * 70)
    print(
        "INTEGRATED RECOMMENDATION TEST COMPLETED"
    )
    print("=" * 70)