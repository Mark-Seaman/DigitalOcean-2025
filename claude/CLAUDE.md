# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a minimal Python script that sends a prompt to the Claude API (claude-opus-4-6) and writes the response to a file.

## Usage

```bash
python run_prompt.py <output_file> <prompt>
# Example:
python run_prompt.py output.txt "Write a haiku about Python"
```

## Dependencies

- `anthropic` Python SDK
- `ANTHROPIC_API_KEY` environment variable must be set

## Architecture

`run_prompt.py` is a single-file CLI tool. It uses the Anthropic streaming API (`client.messages.stream`) but only returns the final message text, writing it to the specified output file.
