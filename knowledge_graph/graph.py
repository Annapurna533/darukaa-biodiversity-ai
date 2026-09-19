# knowledge_graph/graph.py

"""
Darukaa.Earth
Environmental Knowledge Graph

This module represents relationships between:

Environmental conditions
        ↓
Ecosystem processes
        ↓
Environmental pressures
        ↓
Biodiversity impacts

The graph is used as an explicit reasoning layer alongside RAG.
"""


# ============================================================
# ENVIRONMENTAL KNOWLEDGE GRAPH
# ============================================================

KNOWLEDGE_GRAPH = {

    # ========================================================
    # SOIL
    # ========================================================

    "low_soil_organic_carbon": {

        "name": "Low Soil Organic Carbon",

        "category": "soil",

        "leads_to": [
            "reduced_soil_function",
            "soil_biodiversity_pressure",
            "reduced_water_related_soil_function",
        ],
    },


    "reduced_soil_function": {

        "name": "Reduced Soil Function",

        "category": "soil",

        "leads_to": [
            "soil_moisture_pressure",
            "soil_biodiversity_pressure",
        ],
    },


    "reduced_water_related_soil_function": {

        "name": "Reduced Water-Related Soil Function",

        "category": "soil",

        "leads_to": [
            "soil_moisture_pressure",
            "low_water_availability",
        ],
    },


    "soil_moisture_pressure": {

        "name": "Soil Moisture Pressure",

        "category": "soil",

        "leads_to": [
            "vegetation_stress",
            "water_availability_pressure",
            "soil_biodiversity_pressure",
        ],
    },


    "soil_biodiversity_pressure": {

        "name": "Soil Biodiversity Pressure",

        "category": "soil",

        "leads_to": [
            "biodiversity_pressure",
        ],
    },


    # ========================================================
    # CLIMATE / WATER
    # ========================================================

    "low_rainfall": {

        "name": "Low Rainfall",

        "category": "climate",

        "leads_to": [
            "low_water_availability",
            "vegetation_stress",
            "species_stress",
        ],
    },


    "low_water_availability": {

        "name": "Low Water Availability",

        "category": "climate",

        "leads_to": [
            "vegetation_stress",
            "species_stress",
        ],
    },


    "water_availability_pressure": {

        "name": "Water Availability Pressure",

        "category": "climate",

        "leads_to": [
            "vegetation_stress",
            "species_stress",
        ],
    },


    "vegetation_stress": {

        "name": "Vegetation Stress",

        "category": "biodiversity",

        "leads_to": [
            "habitat_diversity_pressure",
            "species_richness_pressure",
        ],
    },


    "species_stress": {

        "name": "Species Stress",

        "category": "biodiversity",

        "leads_to": [
            "species_richness_pressure",
        ],
    },


    # ========================================================
    # LAND USE / MONOCULTURE
    # ========================================================

    "monoculture": {

        "name": "Monoculture",

        "category": "land_use",

        "leads_to": [
            "low_vegetation_diversity",
            "uniform_habitat",
            "lower_habitat_diversity",
        ],
    },


    "low_vegetation_diversity": {

        "name": "Low Vegetation Diversity",

        "category": "biodiversity",

        "leads_to": [
            "lower_habitat_diversity",
            "biodiversity_pressure",
        ],
    },


    "uniform_habitat": {

        "name": "Uniform Habitat",

        "category": "biodiversity",

        "leads_to": [
            "lower_habitat_diversity",
            "biodiversity_pressure",
        ],
    },


    "lower_habitat_diversity": {

        "name": "Lower Habitat Diversity",

        "category": "biodiversity",

        "leads_to": [
            "species_richness_pressure",
        ],
    },


    # ========================================================
    # HABITAT FRAGMENTATION
    # ========================================================

    "habitat_fragmentation": {

        "name": "Habitat Fragmentation",

        "category": "land_use",

        "leads_to": [
            "reduced_connectivity",
            "restricted_species_movement",
            "species_richness_pressure",
        ],
    },


    "reduced_connectivity": {

        "name": "Reduced Habitat Connectivity",

        "category": "biodiversity",

        "leads_to": [
            "restricted_species_movement",
            "species_richness_pressure",
        ],
    },


    "restricted_species_movement": {

        "name": "Restricted Species Movement",

        "category": "biodiversity",

        "leads_to": [
            "species_richness_pressure",
        ],
    },


    # ========================================================
    # DEFORESTATION
    # ========================================================

    "high_deforestation": {

        "name": "High Deforestation",

        "category": "human_impact",

        "leads_to": [
            "habitat_loss",
            "habitat_fragmentation",
            "biodiversity_pressure",
        ],
    },


    "habitat_loss": {

        "name": "Habitat Loss",

        "category": "biodiversity",

        "leads_to": [
            "habitat_fragmentation",
            "species_richness_pressure",
        ],
    },


    # ========================================================
    # POLLUTION
    # ========================================================

    "high_pollution": {

        "name": "High Pollution",

        "category": "human_impact",

        "leads_to": [
            "organism_stress",
            "water_quality_pressure",
            "soil_quality_pressure",
            "biodiversity_pressure",
        ],
    },


    "organism_stress": {

        "name": "Organism Stress",

        "category": "biodiversity",

        "leads_to": [
            "species_richness_pressure",
        ],
    },


    "water_quality_pressure": {

        "name": "Water Quality Pressure",

        "category": "human_impact",

        "leads_to": [
            "organism_stress",
            "species_richness_pressure",
        ],
    },


    "soil_quality_pressure": {

        "name": "Soil Quality Pressure",

        "category": "soil",

        "leads_to": [
            "soil_biodiversity_pressure",
            "organism_stress",
        ],
    },


    # ========================================================
    # BIODIVERSITY
    # ========================================================

    "biodiversity_pressure": {

        "name": "Biodiversity Pressure",

        "category": "biodiversity",

        "leads_to": [
            "species_richness_pressure",
            "habitat_diversity_pressure",
        ],
    },


    "species_richness_pressure": {

        "name": "Species Richness Pressure",

        "category": "biodiversity",

        "leads_to": [],
    },


    "habitat_diversity_pressure": {

        "name": "Habitat Diversity Pressure",

        "category": "biodiversity",

        "leads_to": [],
    },
}


# ============================================================
# GET NODE
# ============================================================

def get_node(node):
    """
    Return information about a graph node.
    """

    return KNOWLEDGE_GRAPH.get(node)


# ============================================================
# CHECK NODE
# ============================================================

def node_exists(node):
    """
    Check whether a node exists in the graph.
    """

    return node in KNOWLEDGE_GRAPH


# ============================================================
# GET NEIGHBORS
# ============================================================

def get_neighbors(node):
    """
    Return nodes directly connected to a node.
    """

    node_data = get_node(node)

    if not node_data:
        return []

    return node_data.get(
        "leads_to",
        []
    )


# ============================================================
# FIND PATH
# ============================================================

def find_path(
    start,
    target,
    max_depth=8
):
    """
    Find the shortest reasoning path between two nodes.

    Breadth-first search is used.
    """

    if not node_exists(start):
        return []

    if not node_exists(target):
        return []

    if start == target:
        return [start]

    queue = [
        [start]
    ]

    visited = {
        start
    }

    while queue:

        path = queue.pop(0)

        current = path[-1]

        if current == target:
            return path

        if len(path) >= max_depth:
            continue

        for neighbor in get_neighbors(
            current
        ):

            if neighbor in visited:
                continue

            visited.add(
                neighbor
            )

            new_path = (
                path +
                [neighbor]
            )

            queue.append(
                new_path
            )

    return []


# ============================================================
# FIND PATHS TO MULTIPLE TARGETS
# ============================================================

def find_paths_to_targets(
    start,
    targets,
    max_depth=8
):
    """
    Find paths from one starting condition to
    multiple environmental targets.
    """

    results = {}

    for target in targets:

        path = find_path(
            start,
            target,
            max_depth
        )

        if path:

            results[target] = path

    return results


# ============================================================
# FORMAT PATH
# ============================================================

def format_path(path):
    """
    Convert graph node IDs into human-readable
    environmental reasoning.
    """

    if not path:
        return ""

    names = []

    for node in path:

        node_data = get_node(node)

        if node_data:

            name = node_data.get(
                "name",
                node
            )

        else:

            name = node.replace(
                "_",
                " "
            ).title()

        names.append(name)

    return " → ".join(
        names
    )


# ============================================================
# ANALYZE SINGLE PRESSURE
# ============================================================

def analyze_pressure(
    pressure,
    max_depth=8
):
    """
    Analyze how one environmental pressure can
    propagate through the knowledge graph.
    """

    if not node_exists(
        pressure
    ):

        return {
            "pressure": pressure,
            "exists": False,
            "paths": {},
        }


    targets = [

        "species_richness_pressure",

        "habitat_diversity_pressure",

        "reduced_connectivity",

        "soil_biodiversity_pressure",

        "vegetation_stress",

        "low_water_availability",
    ]


    paths = find_paths_to_targets(
        pressure,
        targets,
        max_depth
    )


    return {

        "pressure":
            pressure,

        "exists":
            True,

        "paths":
            paths,
    }


# ============================================================
# ANALYZE MULTIPLE PRESSURES
# ============================================================

def analyze_multiple_pressures(
    pressures,
    max_depth=8
):
    """
    Analyze multiple environmental pressures.
    """

    results = []

    for pressure in pressures:

        results.append(
            analyze_pressure(
                pressure,
                max_depth
            )
        )

    return results


# ============================================================
# GET ALL NODES
# ============================================================

def get_all_nodes():
    """
    Return all graph node IDs.
    """

    return list(
        KNOWLEDGE_GRAPH.keys()
    )


# ============================================================
# GET GRAPH SUMMARY
# ============================================================

def get_graph_summary():
    """
    Return basic graph statistics.
    """

    node_count = len(
        KNOWLEDGE_GRAPH
    )

    relationship_count = 0

    categories = set()

    for node_data in KNOWLEDGE_GRAPH.values():

        relationship_count += len(
            node_data.get(
                "leads_to",
                []
            )
        )

        category = node_data.get(
            "category"
        )

        if category:

            categories.add(
                category
            )

    return {

        "nodes":
            node_count,

        "relationships":
            relationship_count,

        "categories":
            sorted(categories),
    }


# ============================================================
# TEST ONE PATH
# ============================================================

def test_path(
    start,
    target
):
    """
    Print a graph pathway.
    """

    path = find_path(
        start,
        target
    )

    if path:

        print(
            format_path(path)
        )

    else:

        print(
            "No path found."
        )


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print(
        "DARUKAA.EARTH ENVIRONMENTAL KNOWLEDGE GRAPH"
    )
    print("=" * 70)


    # --------------------------------------------------------
    # GRAPH SUMMARY
    # --------------------------------------------------------

    summary = get_graph_summary()

    print()
    print("GRAPH SUMMARY")
    print("-" * 70)

    print(
        "Nodes:",
        summary["nodes"]
    )

    print(
        "Relationships:",
        summary["relationships"]
    )

    print(
        "Categories:",
        summary["categories"]
    )


    # --------------------------------------------------------
    # PATH 1
    # LOW SOC → SPECIES RICHNESS
    # --------------------------------------------------------

    print()
    print("PATH 1 - LOW SOC → SPECIES RICHNESS")
    print("-" * 70)

    test_path(
        "low_soil_organic_carbon",
        "species_richness_pressure"
    )


    # --------------------------------------------------------
    # PATH 2
    # MONOCULTURE → SPECIES RICHNESS
    # --------------------------------------------------------

    print()
    print("PATH 2 - MONOCULTURE → SPECIES RICHNESS")
    print("-" * 70)

    test_path(
        "monoculture",
        "species_richness_pressure"
    )


    # --------------------------------------------------------
    # PATH 3
    # FRAGMENTATION → SPECIES RICHNESS
    # --------------------------------------------------------

    print()
    print(
        "PATH 3 - HABITAT FRAGMENTATION → SPECIES RICHNESS"
    )
    print("-" * 70)

    test_path(
        "habitat_fragmentation",
        "species_richness_pressure"
    )


    # --------------------------------------------------------
    # PATH 4
    # LOW RAINFALL → SPECIES RICHNESS
    # --------------------------------------------------------

    print()
    print(
        "PATH 4 - LOW RAINFALL → SPECIES RICHNESS"
    )
    print("-" * 70)

    test_path(
        "low_rainfall",
        "species_richness_pressure"
    )


    # --------------------------------------------------------
    # PATH 5
    # LOW SOC → SOIL BIODIVERSITY
    # --------------------------------------------------------

    print()
    print(
        "PATH 5 - LOW SOC → SOIL BIODIVERSITY"
    )
    print("-" * 70)

    test_path(
        "low_soil_organic_carbon",
        "soil_biodiversity_pressure"
    )


    # --------------------------------------------------------
    # MULTI-PRESSURE TEST
    # --------------------------------------------------------

    print()
    print(
        "MULTI-PRESSURE ANALYSIS"
    )
    print("-" * 70)


    pressures = [

        "low_soil_organic_carbon",

        "low_rainfall",

        "monoculture",

        "habitat_fragmentation",
    ]


    results = analyze_multiple_pressures(
        pressures
    )


    for result in results:

        print()
        print(
            "Pressure:",
            result["pressure"]
        )

        paths = result.get(
            "paths",
            {}
        )

        if not paths:

            print(
                "  No target paths found."
            )

            continue


        for target, path in paths.items():

            print(
                f"  {target}: "
                f"{format_path(path)}"
            )


    print()
    print("=" * 70)
    print(
        "KNOWLEDGE GRAPH TEST COMPLETED"
    )
    print("=" * 70)