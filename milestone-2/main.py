import os
import sys
import types
from importlib import import_module


def _load_run_research():
    """Load the workflow entry point whether this file runs as a module or script."""
    if __package__:
        from .graph import run_research

        return run_research

    package_name = "milestone_2_runtime"
    package_dir = os.path.dirname(__file__)

    if package_name not in sys.modules:
        package_module = types.ModuleType(package_name)
        package_module.__path__ = [package_dir]
        sys.modules[package_name] = package_module

    return import_module(f"{package_name}.graph").run_research


run_research = _load_run_research()

def main():
    """
    Entry Point for the Agentic AI Research Assistant.
    """
    print("\n" + "="*60)
    print("AGENTIC AI RESEARCH ASSISTANT")
    print("="*60)
    
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("\nEnter your research topic: ").strip()
    
    if not query:
        print("❌ Error: No query provided.")
        return

    try:
        final_state = run_research(query)
    
        report = final_state.get("final_report", "No report generated.")
        
        print("\n" + "✅"*25)
        print("FINAL RESEARCH REPORT GENERATED")
        print("✅"*25 + "\n")
        
        print(report)
        
        print("\n" + "="*60)
        print("🛤️  EXECUTION SUMMARY")
        print("="*60)
        for i, step in enumerate(final_state.get("steps", [])):
            print(f"[{i+1}] {step}")
        print("="*60)

    except Exception as e:
        print(f"\n❌ A critical error occurred: {e}")

if __name__ == "__main__":
    main()
