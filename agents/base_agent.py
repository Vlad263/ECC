
class BaseAgent:
    """Generic agent template for ECC. Every agent will extend this."""

    def __init__(self, name: str):
        self.name = name

    def run(self, input_data):
        """Entry method all agents must implement."""
        raise NotImplementedError("run() must be implemented by the agent.")
