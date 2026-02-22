import anthropic
import sys


def run_prompt(prompt: str, output_file: str) -> None:
    client = anthropic.Anthropic()

    print(f"Running prompt...")

    with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        result = stream.get_final_message().content[0].text

    with open(output_file, "w") as f:
        f.write(result)

    print(f"Output written to: {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python run_prompt.py <output_file> <prompt>")
        print('Example: python run_prompt.py output.txt "Write a haiku about Python"')
        sys.exit(1)

    output_file = sys.argv[1]
    prompt = " ".join(sys.argv[2:])

    run_prompt(prompt, output_file)
