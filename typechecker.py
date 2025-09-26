import subprocess
import sys


def run_mypy_check():
    print("⏳ Starting type checking via mypy...\n")

    result = subprocess.run(["mypy", "."], capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ There is no error in the code.\n")
    else:
        print("❌ The following errors were detected during mypy validation:\n")
        print(result.stdout)
        print(result.stderr)
        sys.exit(1)


if __name__ == "__main__":
    run_mypy_check()