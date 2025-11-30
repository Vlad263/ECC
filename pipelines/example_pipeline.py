
from agents.base_agent import BaseAgent

def run_example():
    """Temporary pipeline to verify imports and structure."""
    class EchoAgent(BaseAgent):
        def run(self, input_data):
            return f"[{self.name}] {input_data}"

    agent = EchoAgent("EchoAgent")
    result = agent.run("ECC structure OK.")
    print(result)
