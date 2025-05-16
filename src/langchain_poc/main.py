# LangChain PoC - Minimal Chat Example
# Package: langchain_poc
# File: main.py
# Version: 2.0.28
# Author: Bobwares
# Date: May 16, 2025
# Description: A proof-of-concept for LangChain using OpenAI to process text via batch
#              processing. Loads job definitions from jobs/job-{name}.json, specified
#              via required --job CLI argument. Job files define template, input (array of
#              file names), output extension (.json, .sql, or .md), output file name, model,
#              and temperature. Combines all input files into a single string, appends to the
#              prompt, and makes one LLM call per job. Writes responses to the output/
#              directory (using specified output file name) and raw response to stdout. For
#              .sql and .md output, writes raw LLM response directly; for .json, writes parsed
#              JSON. Version 2.0.28 adds .md as a valid output extension.

from __future__ import annotations

import os
import json
import sys
import argparse
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import AIMessage
from langchain_poc.output_writers import write_json_output

# Configure logger
logger = logging.getLogger("langchain_poc")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

load_dotenv()


def _escape_for_logging(text: str) -> str:
    """Escape newlines in text for logging, showing \\n explicitly."""
    return repr(text)[1:-1]  # Strip quotes from repr


def _build_llm(model: str, temperature: float) -> ChatOpenAI:
    """Return a configured ChatOpenAI runnable."""
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=os.getenv("OPENAI_API_KEY"),
    )


def _load_template(template_name: str) -> str | None:
    """Load the prompt template from a file."""
    template_dir = os.getenv("TEMPLATE_DIR", os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "prompt_templates"))
    if not template_dir:
        logger.error("TEMPLATE_DIR not set in .env and no default directory provided.")
        return None

    template_path = os.path.join(template_dir, template_name)
    if not os.path.exists(template_path):
        logger.error("Template file %s does not exist.", template_path)
        return None

    try:
        with open(template_path, "r", encoding="utf-8") as file:
            template_content = file.read()
            if not template_content.strip():
                logger.error("%s is empty.", template_name)
                return None
            return template_content
    except Exception as e:
        logger.error("Error reading file %s: %s", template_path, e)
        return None


def _load_inputs(input_files: list[str]) -> str | None:
    """Combine input files from the inputs/ directory into a single string."""
    input_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "inputs")
    input_contents = []
    for input_file in input_files:
        input_path = os.path.join(input_dir, input_file)
        if not os.path.exists(input_path):
            logger.error("Input file %s does not exist.", input_path)
            continue
        try:
            with open(input_path, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content:
                    logger.error("Input file %s is empty.", input_path)
                    continue
                input_contents.append(content)
        except Exception as e:
            logger.error("Error reading input file %s: %s", input_path, e)
            continue

    if not input_contents:
        logger.error("No valid input files to process.")
        return None
    return "\n".join(input_contents)


def _load_job(job_name: str) -> dict | None:
    """Load the job definition from jobs/job-{name}.json."""
    jobs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "jobs")
    job_path = os.path.join(jobs_dir, f"job-{job_name}.json")
    if not os.path.exists(job_path):
        logger.error("Job file %s does not exist.", job_path)
        return None

    try:
        with open(job_path, "r", encoding="utf-8") as file:
            job_config = json.load(file)
            required_fields = ["template", "input", "output_ext", "output_file", "model", "temperature"]
            missing_fields = [field for field in required_fields if field not in job_config]
            if missing_fields:
                logger.error("Job file %s missing required fields: %s.", job_path, ", ".join(missing_fields))
                return None
            if not isinstance(job_config["input"], list) or not job_config["input"] or not all(isinstance(f, str) for f in job_config["input"]):
                logger.error("'input' in %s must be a non-empty list of file names.", job_path)
                return None
            if not isinstance(job_config["temperature"], (int, float)) or job_config["temperature"] < 0 or job_config["temperature"] > 2:
                logger.error("Invalid temperature in %s. Must be a number between 0 and 2.", job_path)
                return None
            if job_config["output_ext"] not in [".json", ".sql", ".md"]:
                logger.error("Invalid output_ext in %s. Must be .json, .sql, or .md.", job_path)
                return None
            if not isinstance(job_config["output_file"], str) or not job_config["output_file"]:
                logger.error("output_file in %s must be a non-empty string.", job_path)
                return None
            if not job_config["output_file"].endswith(job_config["output_ext"]):
                logger.error("output_file %s in %s must end with output_ext %s.", job_config["output_file"], job_path, job_config["output_ext"])
                return None
            if ".." in job_config["output_file"] or os.path.isabs(job_config["output_file"]):
                logger.error("output_file %s in %s contains invalid path characters.", job_config["output_file"], job_path)
                return None
            return job_config
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON in %s: %s", job_path, e)
        return None
    except Exception as e:
        logger.error("Error reading %s: %s", job_path, e)
        return None


def run(template_name: str, input_files: list[str], output_ext: str, output_file: str, model: str, temperature: float) -> None:
    """Entry-point for the PoC with single LLM call per job."""
    llm = _build_llm(model, temperature)

    template_content = _load_template(template_name)
    if template_content is None:
        logger.error("Cannot proceed without a valid prompt template.")
        return

    try:
        prompt = ChatPromptTemplate.from_template(template_content)
    except Exception as e:
        logger.error("Error creating prompt template: %s", e)
        return

    chain = prompt | llm

    # Set up output directory
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Combine inputs
    combined_input = _load_inputs(input_files)
    if combined_input is None:
        return

    try:
        # Format and log the prompt with combined input
        formatted_prompt = prompt.format(text=combined_input)
        logger.debug("Prompt sent to LLM: %s", formatted_prompt)

        response: AIMessage = chain.invoke({"text": combined_input})
        # Log raw LLM response with escaped newlines
        logger.debug("Raw LLM response: %s", _escape_for_logging(response.content))
        # Output raw response to stdout
        print(response.content)

        # Write to output file
        output_path = os.path.join(output_dir, output_file)
        if output_ext.lower() == ".json":
            # Parse LLM response as JSON for .json output
            try:
                parsed_response = json.loads(response.content)
            except json.JSONDecodeError as e:
                logger.error("Invalid JSON in LLM response: %s", e)
                return
            write_json_output(output_path, parsed_response, output_ext)
        else:
            # For .sql or .md output, write raw response directly
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(response.content)
                if not response.content.endswith("\n"):
                    file.write("\n")
    except Exception as e:
        logger.error("Error during invocation: %s", e)


def main() -> None:
    """Parse CLI arguments and run the PoC."""
    parser = argparse.ArgumentParser(description="LangChain Job-based PoC")
    parser.add_argument(
        "--job",
        required=True,
        help="Name of the job (loads jobs/job-{name}.json)"
    )
    args = parser.parse_args()

    job_config = _load_job(args.job)
    if job_config is None:
        logger.error("Cannot proceed without a valid job configuration.")
        return

    run(
        template_name=job_config["template"],
        input_files=job_config["input"],
        output_ext=job_config["output_ext"],
        output_file=job_config["output_file"],
        model=job_config["model"],
        temperature=job_config["temperature"],
    )


if __name__ == "__main__":
    main()