#!/usr/bin/env python3
"""Development helper script."""
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False


def main():
    """Main development workflow."""
    print("🚀 Starting development workflow...")
    
    # Ensure we're in a git repository
    if not Path(".git").exists():
        print("Initializing git repository...")
        run_command("git init", "Git initialization")
        run_command("git add .", "Adding files to git")
        run_command(
            'git commit -m "Initial commit"', "Initial git commit"
        )
    
    # Install/update pre-commit hooks
    run_command("pre-commit install", "Installing pre-commit hooks")
    
    # Run code formatting
    run_command("black src tests", "Code formatting with black")
    run_command("isort src tests", "Import sorting with isort")
    
    # Run linting
    run_command("flake8 src tests --max-line-length=88", "Linting")
    
    # Run tests
    run_command("pytest tests/ -v", "Running tests")
    
    print("\n🎉 Development setup complete!")
    print("You can now run: python -m src.main")


if __name__ == "__main__":
    main()
