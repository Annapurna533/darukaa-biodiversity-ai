from conversation import ConversationManager


manager = ConversationManager()


# ---------------------------------------------------------
# FIRST USER MESSAGE
# ---------------------------------------------------------

user_message = (
    "My farm has low rainfall and soil organic carbon "
    "is 0.3%."
)

manager.add_message(
    "user",
    user_message
)


# Simulated extraction
new_data = {
    "soil_organic_carbon": 0.3,
    "rainfall": "low"
}

manager.update_context(new_data)


print("\n")
print("=" * 70)
print("DARUKAA.EARTH CONVERSATION TEST")
print("=" * 70)


print("\nCurrent environmental memory:")

for key, value in manager.get_context().items():
    print(f"- {key}: {value}")


# ---------------------------------------------------------
# CHECK MISSING INFORMATION
# ---------------------------------------------------------

question = manager.clarification_question()


if question:

    print("\nClarifying question:")
    print(question)

else:

    print(
        "\nAll required environmental information "
        "is available."
    )


# ---------------------------------------------------------
# SECOND USER MESSAGE
# ---------------------------------------------------------

second_message = (
    "I grow only wheat."
)

manager.add_message(
    "user",
    second_message
)


new_data = {
    "land_use": "monoculture",
    "crop": "wheat"
}

manager.update_context(new_data)


print("\n")
print("UPDATED ENVIRONMENTAL MEMORY")
print("-" * 70)

for key, value in manager.get_context().items():
    print(f"- {key}: {value}")


question = manager.clarification_question()


if question:

    print("\nStill missing:")
    print(question)

else:

    print(
        "\nAll required environmental information "
        "is now available."
    )