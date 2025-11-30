
from core.config import load_env
from pipelines.example_pipeline import run_example

def main():
    print("\n🔷 ECC LAUNCHING 🔷")
    load_env()
    run_example()
    print("System online. Agents will be attached here.\n")

if __name__ == "__main__":
    main()

