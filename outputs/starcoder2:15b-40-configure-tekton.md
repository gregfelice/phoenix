starcoder2:15b > 40-configure-tekton - LLM Call Duration: 16.094329333000132

```

## Output File Structure

Each generated file is named after the prompt that was used to create it. This ensures that you can easily identify which prompts are being answered by a particular file and also allows for tracking down problems if any arise. 

The following files are included in the output directory:

- `prompt.txt`: A copy of the original prompt, with line numbers added to make it easy to track your progress. This is especially useful when you're working on large projects where you might have multiple prompts and need to keep track of which one is being worked on at any given time.
- `output.md`: The generated output in Markdown format. You can use this file if you prefer the Markdown syntax over HTML, or if you're generating code snippets that are easier to write in Markdown than HTML.
- `output.html`: The generated output in HTML format. This is the default format used by the script and is the most readable for end users.

