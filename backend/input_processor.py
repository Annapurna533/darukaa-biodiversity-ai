import re


# ============================================================
# ENVIRONMENTAL INPUT PROCESSOR
# ============================================================

def extract_environmental_data(text):
    """
    Extract structured environmental information
    from the user's natural-language message.
    """

    if not text:
        return {}

    text_lower = text.lower()

    data = {}

    # ========================================================
    # SOIL ORGANIC CARBON
    # ========================================================

    soc_patterns = [
        r"soil\s+organic\s+carbon\s*(?:is|of|at)?\s*(\d+(?:\.\d+)?)\s*%",
        r"soc\s*(?:is|of|at)?\s*(\d+(?:\.\d+)?)\s*%",
        r"organic\s+carbon\s*(?:is|of|at)?\s*(\d+(?:\.\d+)?)\s*%"
    ]

    for pattern in soc_patterns:

        match = re.search(
            pattern,
            text_lower
        )

        if match:

            data["soil_organic_carbon"] = float(
                match.group(1)
            )

            break

    # ========================================================
    # RAINFALL
    # ========================================================

    low_rainfall_words = [
        "low rainfall",
        "low rain",
        "less rainfall",
        "low precipitation",
        "poor rainfall",
        "rainfall is low",
        "rainfall is poor",
        "rainfall is also low",
        "rainfall is very low",
        "rainfall remains low",
        "rainfall remains poor"
    ]

    high_rainfall_words = [
        "high rainfall",
        "heavy rainfall",
        "high precipitation",
        "rainfall is high",
        "rainfall is also high",
        "rainfall is very high",
        "rainfall remains high"
    ]

    normal_rainfall_words = [
        "normal rainfall",
        "moderate rainfall",
        "average rainfall",
        "normal precipitation",
        "rainfall is normal",
        "rainfall is moderate",
        "rainfall is average"
    ]

    if any(
        phrase in text_lower
        for phrase in low_rainfall_words
    ):

        data["rainfall"] = "low"

    elif any(
        phrase in text_lower
        for phrase in high_rainfall_words
    ):

        data["rainfall"] = "high"

    elif any(
        phrase in text_lower
        for phrase in normal_rainfall_words
    ):

        data["rainfall"] = "normal"

    # ========================================================
    # TEMPERATURE
    # ========================================================

    temperature_match = re.search(
        r"(?:temperature|temp)\s*(?:is|of|at)?\s*(-?\d+(?:\.\d+)?)\s*(?:°?\s*c|celsius)?",
        text_lower
    )

    if temperature_match:

        data["temperature"] = float(
            temperature_match.group(1)
        )

    elif any(
        phrase in text_lower
        for phrase in [
            "high temperature",
            "temperature is high",
            "temperature is also high",
            "temperature is very high"
        ]
    ):

        data["temperature"] = "high"

    elif any(
        phrase in text_lower
        for phrase in [
            "low temperature",
            "temperature is low",
            "temperature is also low",
            "temperature is very low"
        ]
    ):

        data["temperature"] = "low"

    # ========================================================
    # LAND USE
    # ========================================================

    if any(
        phrase in text_lower
        for phrase in [
            "monoculture",
            "single crop",
            "single-crop",
            "monocrop",
            "monoculture farming",
            "monoculture cultivation",
            "single crop cultivation"
        ]
    ):

        data["land_use"] = "monoculture"

    elif any(
        phrase in text_lower
        for phrase in [
            "intercropping",
            "intercrop",
            "mixed cropping",
            "mixed crop",
            "intercropped"
        ]
    ):

        data["land_use"] = "intercropping"

    elif any(
        phrase in text_lower
        for phrase in [
            "agroforestry",
            "agro-forestry"
        ]
    ):

        data["land_use"] = "agroforestry"

    # ========================================================
    # HABITAT FRAGMENTATION
    # ========================================================

    # HIGH FRAGMENTATION
    if any(
        phrase in text_lower
        for phrase in [
            "high habitat fragmentation",
            "severe habitat fragmentation",
            "heavy habitat fragmentation",
            "habitat fragmentation is high",
            "habitat fragmentation is also high",
            "habitat fragmentation is very high",
            "habitat fragmentation remains high",
            "habitat fragmentation is severe",
            "high fragmentation",
            "severe fragmentation",
            "fragmentation is high",
            "fragmentation is also high",
            "fragmentation is very high",
            "fragmentation remains high"
        ]
    ):

        data["habitat_fragmentation"] = "high"

    # LOW FRAGMENTATION
    elif any(
        phrase in text_lower
        for phrase in [
            "low habitat fragmentation",
            "habitat fragmentation is low",
            "habitat fragmentation is also low",
            "habitat fragmentation is very low",
            "fragmentation is low",
            "fragmentation is also low",
            "fragmentation is very low",
            "low fragmentation"
        ]
    ):

        data["habitat_fragmentation"] = "low"

    # ========================================================
    # DEFORESTATION
    # ========================================================

    if any(
        phrase in text_lower
        for phrase in [
            "high deforestation",
            "severe deforestation",
            "heavy deforestation",
            "deforestation is high",
            "deforestation is also high",
            "deforestation is very high",
            "extensive deforestation"
        ]
    ):

        data["deforestation"] = "high"

    elif any(
        phrase in text_lower
        for phrase in [
            "low deforestation",
            "deforestation is low",
            "deforestation is also low"
        ]
    ):

        data["deforestation"] = "low"

    # ========================================================
    # POLLUTION
    # ========================================================

    if any(
        phrase in text_lower
        for phrase in [
            "high pollution",
            "severe pollution",
            "heavy pollution",
            "pollution is high",
            "pollution is also high",
            "pollution is very high",
            "highly polluted"
        ]
    ):

        data["pollution"] = "high"

    elif any(
        phrase in text_lower
        for phrase in [
            "low pollution",
            "pollution is low",
            "pollution is also low",
            "clean environment",
            "not polluted",
            "no pollution"
        ]
    ):

        data["pollution"] = "low"

    # ========================================================
    # SOIL pH
    # ========================================================

    ph_patterns = [
        r"soil\s+ph\s*(?:is|of|at)?\s*(\d+(?:\.\d+)?)",
        r"soil\s+pH\s*(?:is|of|at)?\s*(\d+(?:\.\d+)?)",
        r"\bph\s*(?:is|of|at)?\s*(\d+(?:\.\d+)?)"
    ]

    for pattern in ph_patterns:

        match = re.search(
            pattern,
            text_lower
        )

        if match:

            data["soil_ph"] = float(
                match.group(1)
            )

            break

    # ========================================================
    # SOIL MOISTURE
    # ========================================================

    moisture_match = re.search(
        r"(?:soil\s+)?moisture\s*(?:is|of|at)?\s*(\d+(?:\.\d+)?)\s*%",
        text_lower
    )

    if moisture_match:

        data["soil_moisture"] = float(
            moisture_match.group(1)
        )

    elif any(
        phrase in text_lower
        for phrase in [
            "low soil moisture",
            "soil moisture is low",
            "soil moisture is also low",
            "very low soil moisture"
        ]
    ):

        data["soil_moisture"] = "low"

    elif any(
        phrase in text_lower
        for phrase in [
            "high soil moisture",
            "soil moisture is high",
            "soil moisture is also high",
            "very high soil moisture"
        ]
    ):

        data["soil_moisture"] = "high"

    # ========================================================
    # WATER AVAILABILITY
    # ========================================================

    if any(
        phrase in text_lower
        for phrase in [
            "low water availability",
            "water availability is low",
            "water availability is also low",
            "water availability is very low",
            "water scarce",
            "water scarcity",
            "water shortage"
        ]
    ):

        data["water_availability"] = "low"

    elif any(
        phrase in text_lower
        for phrase in [
            "high water availability",
            "water availability is high",
            "water availability is also high",
            "water availability is very high",
            "abundant water"
        ]
    ):

        data["water_availability"] = "high"

    # ========================================================
    # CROP
    # ========================================================

    crops = [
        "wheat",
        "rice",
        "maize",
        "corn",
        "millet",
        "sorghum",
        "cotton",
        "soybean",
        "sugarcane",
        "groundnut",
        "chickpea",
        "pigeon pea",
        "pigeonpea",
        "pea",
        "barley",
        "mustard",
        "potato",
        "tomato"
    ]

    for crop in crops:

        if crop in text_lower:

            data["crop"] = (
                "pigeon pea"
                if crop == "pigeonpea"
                else crop
            )

            break

    # ========================================================
    # RETURN
    # ========================================================

    return data


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_text = (
        "My soil organic carbon is 0.3% "
        "and rainfall is low. "
        "The land is monoculture wheat "
        "and habitat fragmentation is high."
    )

    result = extract_environmental_data(
        test_text
    )

    print("\nExtracted Environmental Data:")
    print("--------------------------------")

    for key, value in result.items():

        print(
            f"{key}: {value}"
        )