# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a minimal Python script that sends a prompt to the Claude CLI and writes the response to a file.

## Usage

```bash
python run_prompt.py <output_file> <prompt>
# Example:
python run_prompt.py output.txt "Write a haiku about Python"
```

## Dependencies

- Claude Code CLI (`claude`) must be installed and logged in — no separate API key needed

## Architecture

`run_prompt.py` is a single-file CLI tool. It shells out to `claude -p <prompt>` and writes the output to the specified file. Must be run from a regular terminal, not from within a Claude Code session.
