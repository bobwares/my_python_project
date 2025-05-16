from langchain_core.language_models.fake import FakeListLLM

from langchain_poc.main import run, _build_llm

def test_translation():
    llm = FakeListLLM(responses=["Bonjour le monde !"])
    assert llm.invoke("ignored").content == "Bonjour le monde !"
