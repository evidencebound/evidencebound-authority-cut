import importlib.util
import sys
import types
from pathlib import Path


def test_agentcore_entrypoint_wraps_existing_strands_proof(monkeypatch):
    class FakeApp:
        def entrypoint(self, fn):
            return fn

        def run(self):
            return None

    runtime_module = types.ModuleType("bedrock_agentcore.runtime")
    runtime_module.BedrockAgentCoreApp = FakeApp
    package = types.ModuleType("bedrock_agentcore")
    package.runtime = runtime_module
    monkeypatch.setitem(sys.modules, "bedrock_agentcore", package)
    monkeypatch.setitem(sys.modules, "bedrock_agentcore.runtime", runtime_module)

    live = types.ModuleType("authority_cut.live_proof")
    live.run_live_strands_proof = lambda: {
        "execution": "REAL_STRANDS_AGENT_LOOP_DETERMINISTIC_MODEL",
        "authority_mutation_tools": [],
        "agentcore": "UNVERIFIED",
    }
    monkeypatch.setitem(sys.modules, "authority_cut.live_proof", live)

    path = Path(__file__).parents[1] / "agentcore_main.py"
    spec = importlib.util.spec_from_file_location("authority_cut_agentcore_main", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    result = module.authority_cut_agentcore({"prompt": "judge-proof"})
    assert result["execution"] == "REAL_STRANDS_AGENT_LOOP_DETERMINISTIC_MODEL"
    assert result["authority_mutation_tools"] == []
    assert result["agentcore"] == "RUNTIME_ADAPTER_EXECUTED"
    assert result["agentcore_runtime_adapter"] == "BEDROCK_AGENTCORE_DIRECT_CODE"
