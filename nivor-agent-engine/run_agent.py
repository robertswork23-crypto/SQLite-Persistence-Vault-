"""Example runner for the sanitized Nivor workflow.

This script demonstrates how to load the provided JSON workflow, validate
that no secrets are hardcoded, and print a summary. It does not implement
an execution runtime for the full agent engine — use it as a starting point.

Usage:
    python run_agent.py --workflow nivor-agent-engine/nivor-workflow.json

"""

import json
import os
import argparse
from pathlib import Path


def load_workflow(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_for_hardcoded_secrets(workflow: dict) -> list:
    issues = []
    # Simple scan: look for string values that look like API keys or local URLs
    def scan(obj, path=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                scan(v, f"{path}/{k}")
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                scan(item, f"{path}[{i}]")
        elif isinstance(obj, str):
            if "sk-" in obj or "api_key" in path.lower() and obj.strip() and not obj.startswith("${"):
                issues.append((path, obj))
            if "http://localhost" in obj or "127.0.0.1" in obj:
                issues.append((path, obj))

    scan(workflow)
    return issues


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow", default="nivor-agent-engine/nivor-workflow.json", help="Path to the workflow JSON")
    args = parser.parse_args()

    workflow_path = Path(args.workflow)
    if not workflow_path.exists():
        print(f"Workflow file not found: {workflow_path}")
        raise SystemExit(1)

    wf = load_workflow(workflow_path)
    print(f"Loaded workflow: {wf.get('name')} (version: {wf.get('version')})")

    issues = check_for_hardcoded_secrets(wf)
    if issues:
        print("Potential hardcoded secrets or local URLs found in the workflow:\n")
        for p, v in issues:
            print(f" - {p}: {v}")
        print("\nPlease remove hardcoded secrets and use environment variables or secret managers before running in production.")
    else:
        print("No obvious hardcoded secrets detected. Ensure environment variables are set before running the agent.")

    # Example: show nodes and pipelines
    nodes = wf.get("nodes", [])
    pipelines = wf.get("pipelines", {})
    print(f"\nNodes ({len(nodes)}):")
    for n in nodes:
        nid = n.get("id")
        ntype = n.get("type")
        provider = n.get("provider")
        print(f" - {nid}: type={ntype}, provider={provider}")

    print("\nPipelines:")
    for pname, steps in pipelines.items():
        print(f" - {pname}: {steps}")

    print("\nRunner example complete. Integrate this workflow into your Nivor runtime to execute the pipelines.")
