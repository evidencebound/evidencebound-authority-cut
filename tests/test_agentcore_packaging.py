import tomllib
from pathlib import Path


def test_agentcore_extra_pins_runtime_and_strands_dependencies():
    data = tomllib.loads((Path(__file__).parents[1] / "pyproject.toml").read_text())
    deps = data["project"]["optional-dependencies"]["agentcore"]
    assert "bedrock-agentcore==1.21.0" in deps
    assert "strands-agents==1.52.0" in deps
