#!/usr/bin/env python3
"""
Generate .vscode/settings.json from config/tools.yml
This script reads the tools configuration and creates Command Runner settings.
"""
import yaml
import json
import os
from pathlib import Path

# Get the workspace root (parent of scripts/)
WORKSPACE_ROOT = Path(__file__).parent.parent
CONFIG_FILE = WORKSPACE_ROOT / "config" / "tools.yml"
VSCODE_SETTINGS = WORKSPACE_ROOT / ".vscode" / "settings.json"


def load_config():
    """Load tools.yml configuration."""
    if not CONFIG_FILE.exists():
        print(f"Warning: {CONFIG_FILE} not found. Creating empty config.")
        return {}
    
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def generate_command_runner_settings(config):
    """Generate Command Runner settings from tools.yml."""
    commands = {}
    inputs = {}
    
    # Get workspace folder variable
    workspace_folder = config.get("workspace", {}).get("folder", "${workspaceFolder}")
    
    # Process each tool
    for tool_name, tool_config in config.items():
        if tool_name == "workspace":
            continue
        
        if not isinstance(tool_config, dict):
            continue
        
        command_template = tool_config.get("command", "")
        args = tool_config.get("args", {})
        
        # Replace {arg} placeholders with ${input:arg} for Command Runner
        command_parts = []
        input_args = []
        
        # Simple replacement: {a} -> ${input:a}
        command = command_template
        for arg_name, arg_config in args.items():
            if isinstance(arg_config, dict):
                arg_type = arg_config.get("type", "promptString")
                arg_desc = arg_config.get("description", arg_name)
                
                # Register input
                inputs[arg_name] = {
                    "type": "promptString" if arg_type == "number" else "promptString",
                    "description": arg_desc
                }
                
                # Replace placeholder in command
                command = command.replace(f"{{{arg_name}}}", f"${{input:{arg_name}}}")
        
        commands[tool_name] = command
    
    return {
        "command-runner.commands": commands,
        "command-runner.inputs": inputs
    }


def update_vscode_settings(new_settings):
    """Update .vscode/settings.json with Command Runner configuration."""
    # Create .vscode directory if it doesn't exist
    VSCODE_SETTINGS.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing settings if they exist
    existing_settings = {}
    if VSCODE_SETTINGS.exists():
        with open(VSCODE_SETTINGS, "r", encoding="utf-8") as f:
            try:
                existing_settings = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: {VSCODE_SETTINGS} exists but is not valid JSON. Overwriting.")
                existing_settings = {}
    
    # Merge new settings with existing ones
    merged_settings = {**existing_settings, **new_settings}
    
    # Write back to file
    with open(VSCODE_SETTINGS, "w", encoding="utf-8") as f:
        json.dump(merged_settings, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] Updated {VSCODE_SETTINGS}")
    print(f"  Added {len(new_settings.get('command-runner.commands', {}))} commands")


def main():
    """Main entry point."""
    print(f"Reading configuration from {CONFIG_FILE}...")
    config = load_config()
    
    if not config:
        print("No tools configuration found. Exiting.")
        return
    
    print(f"Generating Command Runner settings...")
    settings = generate_command_runner_settings(config)
    
    print(f"Updating {VSCODE_SETTINGS}...")
    update_vscode_settings(settings)
    
    print("Done!")


if __name__ == "__main__":
    main()

