ENVIRONMENTAL_METRICS = {
    "soil": [
        "soil_organic_carbon",
        "soil_ph",
        "soil_moisture"
    ],

    "land_use": [
        "land_use",
        "land_cover",
        "habitat_fragmentation"
    ],

    "biodiversity": [
        "species_richness",
        "habitat_diversity",
        "habitat_connectivity"
    ],

    "climate": [
        "temperature",
        "rainfall",
        "water_availability"
    ],

    "human_impact": [
        "pollution",
        "deforestation"
    ]
}


# ---------------------------------------------------------
# ENVIRONMENTAL RELATIONSHIPS
# ---------------------------------------------------------

METRIC_RELATIONSHIPS = {

    "low_soil_organic_carbon": {
        "effects": [
            "reduced_soil_function",
            "reduced_water_related_soil_function",
            "soil_biodiversity_pressure"
        ],
        "affected_metrics": [
            "soil_organic_carbon",
            "soil_moisture",
            "soil_biodiversity"
        ]
    },

    "low_rainfall": {
        "effects": [
            "low_water_availability",
            "vegetation_stress",
            "species_stress"
        ],
        "affected_metrics": [
            "rainfall",
            "water_availability",
            "habitat_diversity",
            "species_richness"
        ]
    },

    "monoculture": {
        "effects": [
            "uniform_habitat",
            "lower_habitat_diversity",
            "biodiversity_pressure"
        ],
        "affected_metrics": [
            "land_use",
            "habitat_diversity",
            "species_richness"
        ]
    },

    "habitat_fragmentation": {
        "effects": [
            "reduced_connectivity",
            "restricted_species_movement",
            "biodiversity_pressure"
        ],
        "affected_metrics": [
            "habitat_fragmentation",
            "habitat_connectivity",
            "species_richness"
        ]
    },

    "high_deforestation": {
        "effects": [
            "habitat_loss",
            "habitat_fragmentation",
            "biodiversity_pressure"
        ],
        "affected_metrics": [
            "deforestation",
            "habitat_fragmentation",
            "habitat_connectivity",
            "species_richness"
        ]
    },

    "high_pollution": {
        "effects": [
            "organism_stress",
            "soil_or_water_quality_pressure",
            "biodiversity_pressure"
        ],
        "affected_metrics": [
            "pollution",
            "soil_quality",
            "water_quality",
            "species_richness"
        ]
    }
}


# ---------------------------------------------------------
# MULTI-METRIC INTERACTIONS
# ---------------------------------------------------------

MULTI_METRIC_INTERACTIONS = [

    {
        "conditions": [
            "low_soil_organic_carbon",
            "low_rainfall"
        ],
        "pathway": [
            "low SOC",
            "soil-function pressure",
            "water-related soil pressure",
            "low water availability",
            "vegetation stress"
        ],
        "affected_metrics": [
            "soil_organic_carbon",
            "soil_moisture",
            "rainfall",
            "water_availability",
            "vegetation condition"
        ]
    },

    {
        "conditions": [
            "low_soil_organic_carbon",
            "monoculture"
        ],
        "pathway": [
            "low SOC",
            "soil-function pressure",
            "monoculture",
            "reduced vegetation diversity",
            "habitat diversity pressure"
        ],
        "affected_metrics": [
            "soil_organic_carbon",
            "soil_biodiversity",
            "land_use",
            "habitat_diversity",
            "species_richness"
        ]
    },

    {
        "conditions": [
            "low_rainfall",
            "monoculture"
        ],
        "pathway": [
            "low rainfall",
            "water availability pressure",
            "monoculture",
            "limited vegetation diversity",
            "biodiversity pressure"
        ],
        "affected_metrics": [
            "rainfall",
            "water_availability",
            "land_use",
            "habitat_diversity",
            "species_richness"
        ]
    },

    {
        "conditions": [
            "monoculture",
            "habitat_fragmentation"
        ],
        "pathway": [
            "monoculture",
            "low vegetation diversity",
            "fragmented habitat",
            "reduced connectivity",
            "biodiversity pressure"
        ],
        "affected_metrics": [
            "land_use",
            "habitat_diversity",
            "habitat_fragmentation",
            "habitat_connectivity",
            "species_richness"
        ]
    },

    {
        "conditions": [
            "low_rainfall",
            "habitat_fragmentation"
        ],
        "pathway": [
            "low rainfall",
            "vegetation stress",
            "fragmented habitat",
            "reduced connectivity",
            "species stress"
        ],
        "affected_metrics": [
            "rainfall",
            "water_availability",
            "habitat_fragmentation",
            "habitat_connectivity",
            "species_richness"
        ]
    },

    {
        "conditions": [
            "high_deforestation",
            "habitat_fragmentation"
        ],
        "pathway": [
            "deforestation",
            "habitat loss",
            "habitat fragmentation",
            "reduced connectivity",
            "biodiversity pressure"
        ],
        "affected_metrics": [
            "deforestation",
            "habitat_fragmentation",
            "habitat_connectivity",
            "species_richness"
        ]
    }
]