import util.json_reader as json_reader


def load(input_file_name) -> list[dict]:
    prompt_file = json_reader.read_json_file(input_file_name)
    return prompt_file


if __name__ == "__main__":
    file_name = "src/my_package/prompts.json"
    prompts = load(file_name)
    prompts.insert(0, {"title": "All", "category": "all"})
    for prompt in prompts:
        print(prompt.get("title") + ": " + prompt.get("category"))
