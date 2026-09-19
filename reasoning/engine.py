
# reasoning/engine.py

"""
Darukaa.Earth
Environmental Multi-Metric Reasoning Engine

Flow:

Environmental Data
        ↓
Pressure Detection
        ↓
Multi-Metric Interaction Detection
        ↓
Environmental Knowledge Graph
        ↓
Graph Reasoning Paths
        ↓
Affected Metrics
        ↓
Structured Reasoning Result
"""

from knowledge_graph.graph import (
    find_path,
    format_path,
)


# ============================================================
# ENVIRONMENTAL METRICS
# ============================================================

ENVIRONMENTAL_METRICS = {
    "soil": [
        "soil_organic_carbon",
        "soil_ph",
        "soil_moisture",
    ],

    "land_use": [
        "land_use",
        "land_cover",
        "habitat_fragmentation",
    ],

    "biodiversity": [
        "species_richness",
        "habitat_diversity",
        "habitat_connectivity",
    ],

    "climate": [
        "temperature",
        "rainfall",
        "water_availability",
    ],

    "human_impact": [
        "pollution",
        "deforestation",
    ],
}


# ============================================================
# DIRECT RELATIONSHIPS
# ============================================================

METRIC_RELATIONSHIPS = {

    "low_soil_organic_carbon": {
        "effects": [
            "reduced_soil_function",
            "reduced_water_related_soil_function",
            "soil_biodiversity_pressure",
        ],

        "affected_metrics": [
            "soil_organic_carbon",
            "soil_moisture",
            "soil_biodiversity",
        ],
    },

    "low_rainfall": {
        "effects": [
            "low_water_availability",
            "vegetation_stress",
            "species_stress",
        ],

        "affected_metrics": [
            "rainfall",
            "water_availability",
            "habitat_diversity",
            "species_richness",
        ],
    },

    "monoculture": {
        "effects": [
            "uniform_habitat",
            "lower_habitat_diversity",
            "biodiversity_pressure",
        ],

        "affected_metrics": [
            "land_use",
            "habitat_diversity",
            "species_richness",
        ],
    },

    "habitat_fragmentation": {
        "effects": [
            "reduced_connectivity",
            "restricted_species_movement",
            "biodiversity_pressure",
        ],

        "affected_metrics": [
            "habitat_fragmentation",
            "habitat_connectivity",
            "species_richness",
        ],
    },

    "high_deforestation": {
        "effects": [
            "habitat_loss",
            "habitat_fragmentation",
            "biodiversity_pressure",
        ],

        "affected_metrics": [
            "deforestation",
            "habitat_fragmentation",
            "habitat_connectivity",
            "species_richness",
        ],
    },

    "high_pollution": {
        "effects": [
            "organism_stress",
            "soil_or_water_quality_pressure",
            "biodiversity_pressure",
        ],

        "affected_metrics": [
            "pollution",
            "soil_quality",
            "water_quality",
            "species_richness",
        ],
    },
}


# ============================================================
# MULTI-METRIC INTERACTIONS
# ============================================================

MULTI_METRIC_INTERACTIONS = [

    {
        "conditions": [
            "low_soil_organic_carbon",
            "low_rainfall",
        ],

        "pathway": [
            "low SOC",
            "soil-function pressure",
            "water-related soil pressure",
            "low water availability",
            "vegetation stress",
        ],

        "affected_metrics": [
            "soil_organic_carbon",
            "soil_moisture",
            "rainfall",
            "water_availability",
            "vegetation condition",
        ],
    },

    {
        "conditions": [
            "low_soil_organic_carbon",
            "monoculture",
        ],

        "pathway": [
            "low SOC",
            "soil-function pressure",
            "monoculture",
            "reduced vegetation diversity",
            "habitat diversity pressure",
        ],

        "affected_metrics": [
            "soil_organic_carbon",
            "soil_biodiversity",
            "land_use",
            "habitat_diversity",
            "species_richness",
        ],
    },

    {
        "conditions": [
            "low_rainfall",
            "monoculture",
        ],

        "pathway": [
            "low rainfall",
            "water availability pressure",
            "monoculture",
            "limited vegetation diversity",
            "biodiversity pressure",
        ],

        "affected_metrics": [
            "rainfall",
            "water_availability",
            "land_use",
            "habitat_diversity",
            "species_richness",
        ],
    },

    {
        "conditions": [
            "monoculture",
            "habitat_fragmentation",
        ],

        "pathway": [
            "monoculture",
            "low vegetation diversity",
            "fragmented habitat",
            "reduced connectivity",
            "biodiversity pressure",
        ],

        "affected_metrics": [
            "land_use",
            "habitat_diversity",
            "habitat_fragmentation",
            "habitat_connectivity",
            "species_richness",
        ],
    },

    {
        "conditions": [
            "low_rainfall",
            "habitat_fragmentation",
        ],

        "pathway": [
            "low rainfall",
            "vegetation stress",
            "fragmented habitat",
            "reduced connectivity",
            "species stress",
        ],

        "affected_metrics": [
            "rainfall",
            "water_availability",
            "habitat_fragmentation",
            "habitat_connectivity",
            "species_richness",
        ],
    },

    {
        "conditions": [
            "high_deforestation",
            "habitat_fragmentation",
        ],

        "pathway": [
            "deforestation",
            "habitat loss",
            "habitat fragmentation",
            "reduced connectivity",
            "species richness pressure",
        ],

        "affected_metrics": [
            "deforestation",
            "habitat_fragmentation",
            "habitat_connectivity",
            "species_richness",
        ],
    },
]


# ============================================================
# PRESSURE DETECTION
# ============================================================

def detect_pressures(environmental_data):

    pressures = []

    if not isinstance(
        environmental_data,
        dict
    ):
        return pressures


    # --------------------------------------------------------
    # SOIL ORGANIC CARBON
    # --------------------------------------------------------

    soc = environmental_data.get(
        "soil_organic_carbon"
    )

    if soc is not None:

        try:

            soc = float(soc)

            if soc < 1.0:

                pressures.append(
                    "low_soil_organic_carbon"
                )

        except (
            ValueError,
            TypeError
        ):

            pass


    # --------------------------------------------------------
    # RAINFALL
    # --------------------------------------------------------

    rainfall = environmental_data.get(
        "rainfall"
    )

    if isinstance(
        rainfall,
        str
    ):

        if rainfall.lower().strip() == "low":

            pressures.append(
                "low_rainfall"
            )


    # --------------------------------------------------------
    # LAND USE
    # --------------------------------------------------------

    land_use = environmental_data.get(
        "land_use"
    )

    if isinstance(
        land_use,
        str
    ):

        if land_use.lower().strip() == "monoculture":

            pressures.append(
                "monoculture"
            )


    # --------------------------------------------------------
    # HABITAT FRAGMENTATION
    # --------------------------------------------------------

    fragmentation = environmental_data.get(
        "habitat_fragmentation"
    )

    if isinstance(
        fragmentation,
        str
    ):

        if fragmentation.lower().strip() == "high":

            pressures.append(
                "habitat_fragmentation"
            )


    # --------------------------------------------------------
    # DEFORESTATION
    # --------------------------------------------------------

    deforestation = environmental_data.get(
        "deforestation"
    )

    if isinstance(
        deforestation,
        str
    ):

        if deforestation.lower().strip() == "high":

            pressures.append(
                "high_deforestation"
            )


    # --------------------------------------------------------
    # POLLUTION
    # --------------------------------------------------------

    pollution = environmental_data.get(
        "pollution"
    )

    if isinstance(
        pollution,
        str
    ):

        if pollution.lower().strip() == "high":

            pressures.append(
                "high_pollution"
            )


    return pressures


# ============================================================
# MULTI-METRIC INTERACTIONS
# ============================================================

def find_multi_metric_interactions(
    pressures
):

    pressure_set = set(
        pressures or []
    )

    interactions = []

    for interaction in MULTI_METRIC_INTERACTIONS:

        conditions = set(
            interaction["conditions"]
        )

        if conditions.issubset(
            pressure_set
        ):

            interactions.append({

                "conditions":
                    interaction[
                        "conditions"
                    ],

                "pathway":
                    interaction[
                        "pathway"
                    ],

                "affected_metrics":
                    interaction[
                        "affected_metrics"
                    ],
            })


    return interactions


# ============================================================
# BUILD IMPACTS
# ============================================================

def build_impacts(
    pressures,
    interactions
):

    impacts = []

    affected_metrics = []


    # --------------------------------------------------------
    # DIRECT IMPACTS
    # --------------------------------------------------------

    for pressure in pressures:

        relationship = (
            METRIC_RELATIONSHIPS.get(
                pressure
            )
        )

        if relationship is None:

            continue


        for effect in relationship[
            "effects"
        ]:

            if effect not in impacts:

                impacts.append(
                    effect
                )


        for metric in relationship[
            "affected_metrics"
        ]:

            if metric not in affected_metrics:

                affected_metrics.append(
                    metric
                )


    # --------------------------------------------------------
    # INTERACTION IMPACTS
    # --------------------------------------------------------

    for interaction in interactions:

        for step in interaction[
            "pathway"
        ]:

            if step not in impacts:

                impacts.append(
                    step
                )


        for metric in interaction[
            "affected_metrics"
        ]:

            if metric not in affected_metrics:

                affected_metrics.append(
                    metric
                )


    return (
        impacts,
        affected_metrics
    )


# ============================================================
# KNOWLEDGE GRAPH REASONING
# ============================================================

def build_graph_reasoning(
    pressures
):
    """
    Use the Environmental Knowledge Graph to find
    explicit causal/reasoning pathways.
    """

    graph_paths = []

    targets = [

        "species_richness_pressure",

        "habitat_diversity_pressure",

        "reduced_connectivity",

        "soil_biodiversity_pressure",

        "vegetation_stress",

        "low_water_availability",
    ]


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


            graph_paths.append({

                "source":
                    pressure,

                "target":
                    target,

                "path":
                    path,

                "formatted_path":
                    formatted,
            })


    # --------------------------------------------------------
    # Remove duplicate formatted paths
    # --------------------------------------------------------

    unique_paths = []

    seen = set()

    for item in graph_paths:

        formatted = item[
            "formatted_path"
        ]

        if formatted in seen:

            continue

        seen.add(
            formatted
        )

        unique_paths.append(
            item
        )


    return unique_paths


# ============================================================
# ADD GRAPH METRICS
# ============================================================

def add_graph_metrics(
    affected_metrics,
    graph_paths
):
    """
    Add biodiversity/process metrics inferred through
    knowledge graph pathways.
    """

    metrics = list(
        affected_metrics
    )


    metric_mapping = {

        "species_richness_pressure":
            "species_richness",

        "habitat_diversity_pressure":
            "habitat_diversity",

        "reduced_connectivity":
            "habitat_connectivity",

        "soil_biodiversity_pressure":
            "soil_biodiversity",

        "vegetation_stress":
            "vegetation condition",

        "low_water_availability":
            "water_availability",
    }


    for graph_path in graph_paths:

        target = graph_path[
            "target"
        ]

        metric = metric_mapping.get(
            target
        )

        if metric and metric not in metrics:

            metrics.append(
                metric
            )


    return metrics


# ============================================================
# PRESSURE SCORE
# ============================================================

def calculate_pressure_level(
    pressures,
    interactions
):

    direct_score = len(
        pressures or []
    )

    interaction_score = (
        len(
            interactions or []
        ) * 2
    )

    total_score = (
        direct_score +
        interaction_score
    )


    if total_score <= 2:

        level = "Low"

    elif total_score <= 5:

        level = "Moderate"

    elif total_score <= 8:

        level = "High"

    else:

        level = "Very High"


    return {

        "score":
            total_score,

        "level":
            level,
    }


# ============================================================
# FINDINGS
# ============================================================

def build_findings(
    pressures
):

    names = {

        "low_soil_organic_carbon":
            "Soil organic carbon is low.",

        "low_rainfall":
            "Rainfall availability is low.",

        "monoculture":
            "The land-use pattern is monoculture.",

        "habitat_fragmentation":
            "Habitat fragmentation is high.",

        "high_deforestation":
            "Deforestation pressure is high.",

        "high_pollution":
            "Pollution pressure is high.",
    }


    findings = []


    for pressure in pressures:

        findings.append(
            names.get(
                pressure,
                pressure.replace(
                    "_",
                    " "
                ).capitalize()
            )
        )


    return findings


# ============================================================
# MAIN ENVIRONMENTAL ANALYSIS
# ============================================================

def analyze_environment(
    environmental_data
):
    """
    Complete environmental reasoning pipeline.

    1. Detect pressures
    2. Detect multi-metric interactions
    3. Build impacts
    4. Query knowledge graph
    5. Add graph-derived metrics
    6. Calculate pressure assessment
    """

    if not isinstance(
        environmental_data,
        dict
    ):

        environmental_data = {}


    # --------------------------------------------------------
    # STEP 1
    # Detect environmental pressures
    # --------------------------------------------------------

    pressures = detect_pressures(
        environmental_data
    )


    # --------------------------------------------------------
    # STEP 2
    # Multi-metric interactions
    # --------------------------------------------------------

    interactions = (
        find_multi_metric_interactions(
            pressures
        )
    )


    # --------------------------------------------------------
    # STEP 3
    # Direct + interaction impacts
    # --------------------------------------------------------

    impacts, affected_metrics = (
        build_impacts(
            pressures,
            interactions
        )
    )


    # --------------------------------------------------------
    # STEP 4
    # KNOWLEDGE GRAPH
    # --------------------------------------------------------

    graph_paths = (
        build_graph_reasoning(
            pressures
        )
    )


    # --------------------------------------------------------
    # STEP 5
    # Add graph-derived metrics
    # --------------------------------------------------------

    affected_metrics = (
        add_graph_metrics(
            affected_metrics,
            graph_paths
        )
    )


    # --------------------------------------------------------
    # STEP 6
    # Pressure assessment
    # --------------------------------------------------------

    pressure = (
        calculate_pressure_level(
            pressures,
            interactions
        )
    )


    # --------------------------------------------------------
    # STEP 7
    # Findings
    # --------------------------------------------------------

    findings = build_findings(
        pressures
    )


    # --------------------------------------------------------
    # STEP 8
    # Readable interaction pathways
    # --------------------------------------------------------

    interaction_explanations = []


    for interaction in interactions:

        pathway = interaction.get(
            "pathway",
            []
        )

        if pathway:

            interaction_explanations.append(
                " → ".join(
                    pathway
                )
            )


    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    return {

        "environmental_data":
            environmental_data,

        "findings":
            findings,

        "pressures":
            pressures,

        "impacts":
            impacts,

        "affected_metrics":
            affected_metrics,

        "interactions":
            interactions,

        "interaction_explanations":
            interaction_explanations,

        "graph_paths":
            graph_paths,

        "graph_reasoning":
            [
                item[
                    "formatted_path"
                ]

                for item in graph_paths
            ],

        "pressure_score":
            pressure[
                "score"
            ],

        "pressure_level":
            pressure[
                "level"
            ],
    }


# ============================================================
# COMPATIBILITY CLASS
# ============================================================

class EnvironmentalReasoningEngine:
    """
    Compatibility wrapper used by backend.pipeline.py.
    """

    def __init__(self):

        pass


    def analyze(
        self,
        environmental_data
    ):

        return analyze_environment(
            environmental_data
        )


    def analyze_environment(
        self,
        environmental_data
    ):

        return analyze_environment(
            environmental_data
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
        "DARUKAA.EARTH INTEGRATED REASONING TEST"
    )
    print("=" * 70)


    result = analyze_environment(
        test_data
    )


    print()
    print("PRESSURES")
    print("-" * 70)

    for pressure in result[
        "pressures"
    ]:

        print(
            "-",
            pressure
        )


    print()
    print("AFFECTED METRICS")
    print("-" * 70)

    for metric in result[
        "affected_metrics"
    ]:

        print(
            "-",
            metric
        )


    print()
    print("KNOWLEDGE GRAPH PATHS")
    print("-" * 70)

    for pathway in result[
        "graph_reasoning"
    ]:

        print(
            "-",
            pathway
        )


    print()
    print("MULTI-METRIC INTERACTIONS")
    print("-" * 70)

    for pathway in result[
        "interaction_explanations"
    ]:

        print(
            "-",
            pathway
        )


    print()
    print("PRESSURE SCORE")
    print("-" * 70)

    print(
        result[
            "pressure_score"
        ]
    )


    print()
    print("PRESSURE LEVEL")
    print("-" * 70)

    print(
        result[
            "pressure_level"
        ]
    )


    print()
    print("=" * 70)
    print(
        "INTEGRATED REASONING TEST COMPLETED"
    )
    print("=" * 70)
