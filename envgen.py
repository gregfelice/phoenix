"""

Module Name: envgen.py

Description: generate environments using an LLM

load granular prompt files to handle different facets of the setup
feed prompts into LLM, get back as structured JSON
process JSON into source code and config files, store in dirs

Author: Greg Felice
Email: gregfelice@pipelinestrategypartners.com
Website: http://www.pipelinestrategypartners.com

Created: YYYY-MM-DD  (Date of creation)
Last Modified: YYYY-MM-DD (Date of last modification)

License: MIT

see https://github.com/ollama/ollama-python/tree/main/examples

@todo add more LLMs
@todo check for existence of output files - skip to next run if file exists

"""

from ollama import chat
import os
import time

ppath = "./prompts"
opath = "./outputs"

models = {
    "gemma2 27b": "gemma2:27b",
    "qwen2.5 coder 7b": "qwen2.5-coder:latest",
    "qwen2.5 coder 14b": "qwen2.5-coder:14b",
    "codellama 7b": "codellama:latest",
    "codellama 13b": "codellama:13b",
    "starcoder2 3b": "starcoder2:latest",
    "starcoder2 7b": "starcoder2:7b",
    "starcoder2 15b": "starcoder2:15b",
    "wizard vicuna uncensored latest": "wizard-vicuna-uncensored:latest",
    "deepseek r1 1.5b": "deepseek-r1:1.5b",
    "deepseek r1 7b": "deepseek-r1:latest",
    "deepseek r1 14b": "deepseek-r1:14b",
    "deepseek-r1 32b": "deepseek-r1:32b",
    "llama2 uncensored latest": "llama2-uncensored:latest",
    "llama3.2 latest": "llama3.2:latest",
}

temperature = 0.7

hints = """
also note that i will have then following machines already existing.
use this information where it helps you define your responses.

hostname: weywot - macos, development laptop
hostname: yerbouti - debian, generic host
hostname: waza - debian, will be used as the main server for testing, production, database server.
"""


def get_files(dir_path):
    """
    Gets all filenames (excluding dirs) in a given directory.
    """
    try:
        files = [
            f for f in os.listdir(dir_path)
            if os.path.isfile(os.path.join(dir_path, f))
        ]
        return files
    except FileNotFoundError:
        print(f"Error: Directory '{dir_path}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def run_gen(model, prompt_name, prompt):
    """
    runs a model, feeding in a prompt.
    outputs the response to a file based on the argument name.
    """

    output_filename = f"{opath}/{model}-{prompt_name}.md"
    if os.path.exists(output_filename):
        print("output file exists. skipping LLM call.")
        return

    prompts = f"{prompt}\n\n{hints}"

    start_time = time.perf_counter()
    response = chat(model=model,
                    messages=[
                        {'role': 'user',
                         'content': prompts},
                    ],
                    options={'temperature': temperature}
                    )

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print(response.message.content)

    output_file_header = (f"{model} > {prompt_name} - "
                          f"LLM Call Duration: {elapsed_time}")

    with open(output_filename, 'w') as f:
        f.write(output_file_header)
        f.write(os.linesep)
        f.write(response.message.content)


def load_text(fpath):
    """Loads text from a file."""
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            return f.read()
    except (FileNotFoundError, UnicodeDecodeError, Exception) as e:
        print(f"Error: {e}")
        return None


def run():
    """run all models against all prompt files"""

    for model in models:
        pfile_names = get_files(ppath)
        for pname in pfile_names:
            fqpath = ppath + "/" + pname
            prompt = load_text(fqpath)
            print(f"processing {pname} with {model}")
            run_gen(models[model], pname, prompt)


if __name__ == "__main__":
    run()
