"""Public judge service for Authority Cut.

The live endpoint executes the real Strands Agent loop using a deterministic custom
Model provider. It is intentionally credential-free and does not claim Bedrock or
AgentCore execution.
"""
from __future__ import annotations

from dataclasses import asdict

from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse

from .evaluate import run_evaluation
from .live_proof import run_live_strands_proof
from .strands_app import STRANDS_TOOL_NAMES

app = FastAPI(title="Authority Cut — Live Strands Judge Surface", version="1.0.0")


@app.get("/health")
def health() -> dict[str, object]:
    return {
        "status": "READY",
        "control_kernel": "PASS",
        "live_strands_agent_loop": "AVAILABLE",
        "live_model_provider": "DETERMINISTIC_CUSTOM",
        "foundation_model": "UNVERIFIED",
        "agentcore": "UNVERIFIED",
        "authority_boundary": "EXTERNAL_HUMAN_ONLY",
        "model_callable_tools": list(STRANDS_TOOL_NAMES),
        "authority_mutation_tools": [],
    }


@app.get("/api/evaluation")
def evaluation() -> dict:
    return asdict(run_evaluation())


@app.get("/api/tool-boundary")
def tool_boundary() -> dict[str, object]:
    return {
        "model_callable_tools": list(STRANDS_TOOL_NAMES),
        "authority_mutation_tools": [],
        "principal_actions": ["approve", "revoke"],
        "principal_channel": "EXTERNAL_HUMAN_API",
    }


@app.post("/api/strands-proof")
def strands_proof() -> dict[str, object]:
    return run_live_strands_proof()


@app.get("/favicon.ico", include_in_schema=False)
@app.get("/favicon.png", include_in_schema=False)
def favicon() -> Response:
    return Response(status_code=204)


HTML = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Authority Cut — Live Strands Judge Surface</title><style>:root{--bg:#f4f6fa;--panel:#fff;--ink:#111827;--muted:#64748b;--line:#dde4ee;--deep:#0f172a;--ok:#087a4b;--warn:#a25d00;--accent:#3156d3}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 Inter,system-ui,-apple-system,sans-serif}.w{max-width:1120px;margin:auto;padding:42px 22px 72px}.p{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:24px;box-shadow:0 8px 28px #1111}.hero{display:grid;grid-template-columns:1.4fr .8fr;gap:18px}.k{font-size:12px;font-weight:850;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}h1{font-size:46px;line-height:1;margin:8px 0 14px;letter-spacing:-.05em}.muted{color:var(--muted)}.badges{display:flex;gap:7px;flex-wrap:wrap;margin:18px 0}.b{border-radius:999px;padding:6px 10px;font-size:12px;font-weight:850;background:#e9f7f0;color:var(--ok)}.b.w{background:#fff3df;color:var(--warn)}button{border:0;border-radius:11px;background:var(--deep);color:#fff;padding:12px 16px;font-weight:800;cursor:pointer}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:16px}.n{font-size:32px;font-weight:900;letter-spacing:-.04em}.code{white-space:pre-wrap;background:#0c1320;color:#dce7ff;border-radius:14px;padding:18px;max-height:650px;overflow:auto;font:12px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace}.section{margin-top:16px}.callout{border-left:4px solid var(--accent);background:#eef2ff;padding:14px 16px;border-radius:0 12px 12px 0}.ok{color:var(--ok)}@media(max-width:780px){.hero,.grid{grid-template-columns:1fr}h1{font-size:36px}}</style></head><body><main class="w"><section class="hero"><div class="p"><div class="k">AWS Agents for Humans · Professional Agents</div><h1>Authority Cut</h1><p class="muted">Routine vendor-onboarding work runs autonomously. The agent surfaces only the smallest policy-valid human authority set needed for protected effects, and a later correction rolls back reversible downstream work without erasing unrelated safe work.</p><div class="badges"><span class="b">CONTROL KERNEL · PASS</span><span class="b">REAL STRANDS LOOP · LIVE</span><span class="b">MODEL CANNOT APPROVE ITSELF</span><span class="b w">FOUNDATION MODEL · UNVERIFIED</span><span class="b w">AGENTCORE · UNVERIFIED</span></div><button id="run" onclick="runProof()">Run live Strands judge path</button></div><div class="p"><div class="k">Fixed workflow</div><div class="n">5 safe</div><p class="muted">actions before human attention</p><div class="n">7 → 3</div><p class="muted">protected-effect prompts compressed to semantic authorities</p><div class="n">6 rollback</div><p class="muted">reversible descendants after correction</p></div></section><section class="grid"><div class="p"><div class="k">Human boundary</div><h2>External principal only</h2><p>The Strands tool schema contains execute-safe, inspect-cut, and execute-authorized tools. Approve and revoke do not exist in the model tool set.</p></div><div class="p"><div class="k">Irreversible boundary</div><h2>First funds stays separate</h2><p>Funds transmission cannot become ready until the remittance preview receipt exists, and is never executed in the public proof.</p></div><div class="p"><div class="k">Correction semantics</div><h2>Preserve safe work</h2><p>Revoking vendor-risk compensates six reversible protected effects while five safe actions remain executed.</p></div></section><section class="section p"><div class="callout"><strong>Truth boundary.</strong> This page runs the real Strands SDK Agent/tool loop with a deterministic custom Model provider. It proves live Strands orchestration and authority separation. It does not claim Bedrock foundation-model or AgentCore execution.</div></section><section class="section p"><h2>Live execution ledger</h2><pre id="out" class="code">Select “Run live Strands judge path”.</pre></section></main><script>async function runProof(){const b=document.getElementById('run'),o=document.getElementById('out');b.disabled=true;b.textContent='Running real Strands loop…';o.textContent='Executing safe work → authority cut → external human grants → authorized resume → correction propagation…';try{const r=await fetch('/api/strands-proof',{method:'POST'});const d=await r.json();if(!r.ok)throw new Error(JSON.stringify(d));o.textContent=JSON.stringify(d,null,2);b.textContent='Run again';}catch(e){o.textContent='FAIL-CLOSED: '+e;b.textContent='Retry';}finally{b.disabled=false}}</script></body></html>'''


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return HTML
