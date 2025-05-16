LangChain Proof of Concept (PoC)
This project is a proof-of-concept for batch text processing using LangChain and OpenAI's language models. It processes job definitions from JSON configuration files, combines input files, and generates output in .json, .sql, or .md formats. The project supports flexible output file names and logs debug information for prompts and LLM responses.

Version: 2.0.28
Author: Bobwares
Date: May 16, 2025

Features

Load job configurations from jobs/job-{name}.json.
Combine multiple input files into a single prompt.
Support for .json (parsed JSON), .sql (raw SQL), and .md (raw Markdown) output.
Custom output file names via output_file in job config.
Debug logging of prompts and LLM responses with escaped newlines.
Single LLM call per job for efficiency.
CLI interface: poetry run lc-demo --job <name>.

Prerequisites

Python: 3.11 or higher
Poetry: For dependency management (install via pip install poetry or follow Poetry's installation guide)
OpenAI API Key: Obtain from OpenAI
Git: For cloning the repository

Installation

Clone the Repository (if applicable):
git clone <repository-url>
cd my_python_project

Or use the existing project directory:
cd /Users/bobware/projects/my_python_project


Install Dependencies:
poetry install


Set Up Environment Variables:Create or update /Users/bobware/projects/my_python_project/.env:
echo "OPENAI_API_KEY=your_key_here" > .env
echo "TEMPLATE_DIR=/Users/bobware/projects/my_python_project/prompt_templates" >> .env

Replace your_key_here with your OpenAI API key.

Verify Setup:
cat .env
poetry run python -c "import langchain; print(langchain.__version__)"

Expected output: 0.3.0 (or similar).


Usage
Run the PoC using the CLI command:
poetry run lc-demo --job <job-name>

The --job argument specifies the job configuration file (jobs/job-<job-name>.json).
Available Jobs
Run one of the following commands to execute a job:

Generate Test Data:
poetry run lc-demo --job generate-test-data


Purpose: Generates test data in JSON format based on input files.
Output: Typically a .json file (e.g., output/test_data.json).
Example Use Case: Creating sample data for testing applications.


SQL Generator:
poetry run lc-demo --job sql-generator


Purpose: Generates SQL statements (e.g., CREATE TABLE or INSERT) or Markdown documents with SQL code blocks from a JSON schema.
Output: .sql (e.g., output/customer_table.sql) or .md (e.g., output/customer_table.md).
Example Use Case: Creating database schemas or documenting SQL queries.


Domain-Driven Design:
poetry run lc-demo --job domain-driven-design


Purpose: Generates Markdown documentation for domain-driven design (DDD) concepts, such as domain models or aggregates.
Output: Typically a .md file (e.g., output/ddd_documentation.md).
Example Use Case: Documenting software architecture for DDD-based projects.



Example Output
For poetry run lc-demo --job sql-generator with output_ext: ".md":

Stdout:```sql
CREATE TABLE Customer (
id INTEGER,
name VARCHAR,
email VARCHAR
);




Output File: output/customer_table.md (same as stdout).
Debug Log (stderr, redirected to debug.log):poetry run lc-demo --job sql-generator 2> debug.log
cat debug.log

Example content:DEBUG:langchain_poc: Prompt sent to LLM: Given a JSON schema in {...}, generate a Markdown document with a SQL CREATE TABLE statement...
DEBUG:langchain_poc: Raw LLM response: ```sql\nCREATE TABLE Customer (\n    id INTEGER,\n    name VARCHAR,\n    email VARCHAR\n);\n```



File Structure
my_python_project/
├── src/
│   └── langchain_poc/
│       ├── __init__.py
│       ├── main.py          # Main script (version 2.0.28)
│       └── output_writers.py  # Output utilities (version 2.0.21)
├── jobs/
│   ├── job-generate-test-data.json
│   ├── job-sql-generator.json
│   └── job-domain-driven-design.json
├── inputs/
│   └── customer-schema.json  # Example input
├── prompt_templates/
│   └── prompt-sql-generator.md  # Example prompt
├── output/
│   ├── customer_table.md
│   ├── test_data.json
│   └── ddd_documentation.md
├── .env                    # Environment variables
├── pyproject.toml          # Poetry configuration
└── README.md               # This file

Job Configuration
Each job file (jobs/job-<name>.json) must include:

template: Prompt template file (e.g., prompt-sql-generator.md).
input: List of input files (e.g., ["customer-schema.json"]).
output_ext: Output extension (.json, .sql, or .md).
output_file: Output file name (e.g., customer_table.md, must match output_ext).
model: OpenAI model (e.g., gpt-4o-mini).
temperature: LLM temperature (0 to 2).

Example (jobs/job-sql-generator.json):
{
"template": "prompt-sql-generator.md",
"input": ["customer-schema.json"],
"output_ext": ".md",
"output_file": "customer_table.md",
"model": "gpt-4o-mini",
"temperature": 0.7
}

Troubleshooting

Error: "Job file does not exist":
Ensure the job file exists in jobs/ (e.g., job-sql-generator.json).
Check the --job argument matches the file name (sql-generator for job-sql-generator.json).


Error: "Invalid JSON in LLM response":
For .json output, verify the LLM response is valid JSON.
Check the prompt in prompt_templates/ to ensure it requests JSON output.


Error: "OPENAI_API_KEY not set":
Verify .env contains a valid OPENAI_API_KEY.
Run cat .env to check.


No output file:
Check output/ directory for the specified output_file.
Ensure output_ext matches output_file extension.


Debugging:
Redirect stderr to a file:poetry run lc-demo --job sql-generator 2> debug.log
cat debug.log


Inspect logs for prompt and LLM response.



Contributing
This is a proof-of-concept. To contribute:

Fork the repository (if applicable).
Create a branch: git checkout -b feature/your-feature.
Commit changes: git commit -m "Add your feature".
Push and create a pull request.
