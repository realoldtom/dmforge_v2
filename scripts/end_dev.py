# scripts/end_dev.py
import subprocess
import sys


def run_check(command: list[str], description: str):
    print(f"🔍 Running: {description} ...")
    result = subprocess.run(command)
    if result.returncode != 0:
        print(f"❌ Failed: {description}")
        sys.exit(result.returncode)
    print(f"✅ Passed: {description}")


def main():
    if len(sys.argv) < 2:
        print("❌ ERROR: Commit message required.")
        print('Usage: python scripts/end_dev.py "feat: add spell filter"')
        sys.exit(1)

    msg = sys.argv[1]

    run_check(["poetry", "run", "pytest", "--cov", "--exitfirst"], "tests with coverage")
    run_check(["poetry", "run", "black", "."], "code formatting check")
    run_check(["poetry", "run", "ruff", "check", ".", "--fix"], "style linting")
    run_check(["git", "add", "."], "git stage all")
    run_check(["git", "commit", "-m", msg], "git commit")
    run_check(["git", "push"], "git push")


if __name__ == "__main__":
    main()
