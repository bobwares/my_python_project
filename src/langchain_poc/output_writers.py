# LangChain PoC - Output Writers
# Package: langchain_poc
# File: output_writers.py
# Version: 2.0.21
# Author: Bobwares
# Date: May 15, 2025
# Description: Output writer functions for LangChain PoC. Provides function to write
#              JSON output to files based on the output_ext specified in the job
#              definition. SQL output is handled directly in main.py by writing raw LLM
#              response. Version 2.0.21 removes write_sql_output as .sql output is now
#              written directly in main.py.

from typing import Any
import json


def _sql_escape(value: Any) -> str:
    """Escape SQL string values by doubling single quotes or return 'NULL' for None."""
    if value is None:
        return "NULL"
    escaped = str(value).replace("'", "''")
    return "'" + escaped + "'"


def write_json_output(output_path: str, data: Any, output_ext: str) -> None:
    """Write JSON output to a file."""
    with open(output_path, "w", encoding="utf-8") as file:
        if output_ext.lower() == ".json":
            json.dump({"response": data}, file, ensure_ascii=False, indent=2)
        else:
            file.write(json.dumps(data, ensure_ascii=False, indent=2))