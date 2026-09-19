# ============================================================
# DARUKAA.EARTH CONVERSATION MANAGER
# ============================================================

class ConversationManager:
    """
    Maintains environmental context and conversation history
    across multiple user turns.
    """

    # --------------------------------------------------------
    # Initialization
    # --------------------------------------------------------

    def __init__(self):

        self.environmental_data = {}

        self.history = []

        self.required_context = [
            "soil_organic_carbon",
            "rainfall",
            "land_use"
        ]

    # --------------------------------------------------------
    # Add message
    # --------------------------------------------------------

    def add_message(
        self,
        role,
        content
    ):

        self.history.append(
            {
                "role": role,
                "content": content
            }
        )

    # --------------------------------------------------------
    # Update environmental context
    # --------------------------------------------------------

    def update_context(
        self,
        new_data
    ):
        """
        Merge newly extracted environmental information
        with previously known environmental information.

        Returns the complete updated context.
        """

        if not new_data:

            return self.environmental_data

        for key, value in new_data.items():

            if value is not None:

                self.environmental_data[key] = value

        return self.environmental_data

    # --------------------------------------------------------
    # Get current context
    # --------------------------------------------------------

    def get_context(self):

        return self.environmental_data

    # --------------------------------------------------------
    # Get missing required context
    # --------------------------------------------------------

    def get_missing_context(self):

        missing = []

        for key in self.required_context:

            if key not in self.environmental_data:

                missing.append(key)

            elif self.environmental_data[key] is None:

                missing.append(key)

        return missing

    # --------------------------------------------------------
    # Check whether enough context exists
    # --------------------------------------------------------

    def has_required_context(self):

        return len(
            self.get_missing_context()
        ) == 0

    # --------------------------------------------------------
    # Get conversation history
    # --------------------------------------------------------

    def get_history(self):

        return self.history

    # --------------------------------------------------------
    # Clear conversation
    # --------------------------------------------------------

    def clear(self):

        self.environmental_data = {}

        self.history = []


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    manager = ConversationManager()

    print("\n==========================================")
    print("Conversation Manager Test")
    print("==========================================")

    # First message
    first_data = {
        "soil_organic_carbon": 0.3,
        "rainfall": "low"
    }

    context = manager.update_context(
        first_data
    )

    print("\nAfter first message:")
    print(context)

    print("\nMissing:")
    print(
        manager.get_missing_context()
    )

    # Second message
    second_data = {
        "land_use": "monoculture",
        "crop": "wheat",
        "habitat_fragmentation": "high"
    }

    context = manager.update_context(
        second_data
    )

    print("\nAfter second message:")
    print(context)

    print("\nMissing:")
    print(
        manager.get_missing_context()
    )

    print("\nHas required context:")
    print(
        manager.has_required_context()
    )