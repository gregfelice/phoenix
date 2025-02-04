# Phoenix 

## Goal & Premise
- Subjectively evaluate LLM's ability to generate decent code.
- Inspect the different LLM outputs to hopefully gain insights into which is best for coding assistance at the current time.
- See how well an LLM independently executes against an imperfect directive -- to what extent can it work without coaching?

## Assumptions
- As an experienced coder, I should be able to review code and gauge its general quality.
- We'll use a one-shot approach, meaning we will not coach the LLM towards a better answer.
- We do not check for hallucinations or validations other than the human code review.
- We won't assume that a larger LLM is neccessarily better.
- We only ask the LLLMs to output [Ansible](https://www.redhat.com/en/ansible-collaborative) code.
  - Ansible is a popular open-source scripting language that automates application deployment, cloud provisioning, intra-service orchestration, and other IT tools.
  - We suspect asking for Ansible code generation will be more interesting than, say, python code, as it is not prioritized in any LLM coding performance benchmark tests that we know of, and requires the LLM to think about heterogeneous systems as well as the code itself.
- We'll run the tests on an Apple M3 Pro with 36GB RAM, and the LLM will be able to make use of the GPU.
  
## Approach
- Feed different LLMs the exact same prompt, asking them to write Ansible code that will automate common infrastructure installation and configuration tasks.
  - We used these [prompts](https://github.com/gregfelice/phoenix/tree/main/prompts_source).
- Act as a human code reviewer, and review the code, and rank it.
  - Is it total garbage? (1 star)
  - Does it just express concepts, but get the coding piece totally wrong, or show no code at all? (2 stars)
  - Does it generate some syntactically correct, but low quality code (3 stars)
  - Does it generate very high quality code that would most likely run if copy-pasted? (4 stars)
  - Does it generate insightful, mature code? Does it think in terms of reuse? Does it make use of more elegant language constructs to avoid code duplication? (5 stars)
- Share results in a [Google Sheet](https://docs.google.com/spreadsheets/d/12fIvSKlh3IiYsdJRcnnOU0iBIIqPxPLCQsqV8UOUqhI/view) with Subjective Rankings, Pivot tables.

## What Did I Observe and Learn?
See [output files](https://github.com/gregfelice/phoenix/tree/main/outputs)

**Best in Show:**
- Deepseek 14b and Deepseek 32b

**Honorable Mentions**
- Qwen 7b & 14b, Gemma 27b

**Observations**
- Deepseek
  - I observed Deepseek 14b and 32b giving the best outputs. I interpereteted 32b's results as showing an ability to think ahead and play out scenarios in a way that improved its outputs.
  - I observed Deepseek 7b making lots of language mistakes, often mixing Mandarin and English. This is a problem the Deepseek R1 paper talks about.
  - Deepseek 1.5b outputs were unintelligible.
- Qwen
  - Qwen wrote intelligible, well laid out code at 7b, unlike Deepseek.
- Gemma
  - At 27b, Gemma wrote clean and usable code, but sometimes made less elegant choices that caused unneeded repetition.
- CodeLlama
  - CodeLlamma 7b and 13b wrote poorly constructed, clumsy code, and often seemed to miss the key point expressed in the prompt.
- Starcoder
  - Starcoder output was garbage. I don't know if this was a misconfiguration or bug, but I threw out results from scoring.
- Wizard Vicuna Uncensored
  - Thrown into the evaulation for fun. Not designed for coding. Its outputs were unusable for any coding task.
 
**Next activities**
  - One-shot code generation with variations on prompts
  - Structured data outputting / conversion of outputs to executable files
  - Tool integration: CI/CD systems
  - Testing Feedback Loops: Can linters and test runner outputs fed back into LLMs improve results?


<img width="1526" alt="image" src="https://github.com/user-attachments/assets/61b06a5b-1538-4a2d-a39a-30e235213113" />
