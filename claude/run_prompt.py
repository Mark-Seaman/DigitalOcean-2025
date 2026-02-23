import subprocess
import sys


def run_prompt(prompt: str, output_file: str) -> None:
    print(f"Running prompt...")

    result = subprocess.run(
        ["claude", "-p", prompt],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)

    with open(output_file, "w") as f:
        f.write(result.stdout)

    print(f"Output written to: {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python run_prompt.py <output_file> <prompt>")
        print('Example: python run_prompt.py output.txt "Write a haiku about Python"')
        sys.exit(1)

    output_file = sys.argv[1]
    prompt = " ".join(sys.argv[2:])

    run_prompt(prompt, output_file)
