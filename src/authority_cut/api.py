from __future__ import annotations

from dataclasses import asdict

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from .engine import ControlPlane
from .evaluate import run_evaluation
from .runtime import get_plane

app = FastAPI(title="Authority Cut", version="0.1.0")


def plane(reset: bool = False) -> ControlPlane:
    return get_plane(reset=reset)


def snapshot(p: ControlPlane) -> dict:
    return {
        "status": {k: v.value for k, v in p.state.status.items()},
        "decision_surface": p.decision_surface(),
        "receipts": p.state.receipts,
    }


class DecisionRequest(BaseModel):
    approved: bool
    rationale: str


class CorrectionRequest(BaseModel):
    reason: str


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "READY",
        "control_kernel": "READY",
        "strands_runtime": "UNVERIFIED",
        "agentcore": "UNVERIFIED",
        "authority_boundary": "EXTERNAL_HUMAN_ONLY",
    }


@app.get("/api/evaluation")
def evaluation() -> dict:
    return asdict(run_evaluation())


@app.post("/api/reset")
def reset() -> dict:
    return snapshot(plane(reset=True))


@app.post("/api/run-safe")
def run_safe() -> dict:
    p = plane()
    p.execute_autonomous()
    return snapshot(p)


@app.get("/api/state")
def state() -> dict:
    return snapshot(plane())


@app.post("/api/decisions/{bundle_id}")
def decide(bundle_id: str, body: DecisionRequest) -> dict:
    p = plane()
    if bundle_id not in p.graph.bundles:
        raise HTTPException(status_code=404, detail="unknown decision bundle")
    try:
        p.decide(bundle_id, body.approved, body.rationale)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    p.execute_authorized()
    return snapshot(p)


@app.post("/api/corrections/{bundle_id}")
def correct(bundle_id: str, body: CorrectionRequest) -> dict:
    p = plane()
    try:
        affected = p.revoke_bundle(bundle_id, body.reason)
    except KeyError as exc:
        raise HTTPException(status_code=409, detail="bundle has no prior decision") from exc
    out = snapshot(p)
    out["affected"] = sorted(affected)
    return out


HTML = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Authority Cut — EvidenceBound</title><style>:root{color-scheme:light;--ink:#111827;--muted:#64748b;--line:#e2e8f0;--soft:#f8fafc;--deep:#0f172a;--ok:#166534;--warn:#92400e;--bad:#991b1b}*{box-sizing:border-box}body{margin:0;background:#f1f5f9;color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{max-width:1180px;margin:0 auto;padding:40px 24px 72px}.hero{background:white;border:1px solid var(--line);border-radius:20px;padding:28px;box-shadow:0 18px 50px rgba(15,23,42,.06)}h1{font-size:clamp(2rem,5vw,4.1rem);letter-spacing:-.055em;line-height:.95;margin:12px 0 18px}.eyebrow{text-transform:uppercase;letter-spacing:.14em;font-size:.75rem;font-weight:800;color:var(--muted)}.lede{max-width:830px;font-size:1.05rem;line-height:1.65;color:#334155}.badges{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0}.badge{border:1px solid var(--line);border-radius:999px;padding:7px 10px;font-size:.72rem;font-weight:800;background:var(--soft)}.ready{color:var(--ok)}.unverified{color:var(--warn)}.boundary{color:#1e3a8a}.grid{display:grid;grid-template-columns:repeat(12,1fr);gap:16px;margin-top:16px}.card{background:white;border:1px solid var(--line);border-radius:16px;padding:20px}.span8{grid-column:span 8}.span4{grid-column:span 4}.span12{grid-column:span 12}h2{margin:0 0 12px;font-size:1rem}.metric{font-size:2.25rem;font-weight:850;letter-spacing:-.05em}.small{font-size:.82rem;color:var(--muted);line-height:1.5}.controls{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}button{border:1px solid var(--deep);background:var(--deep);color:white;border-radius:10px;padding:10px 13px;font-weight:750;cursor:pointer}button.secondary{background:white;color:var(--deep);border-color:var(--line)}button.danger{background:white;color:var(--bad);border-color:#fecaca}pre{margin:0;background:#0b1220;color:#dbeafe;padding:18px;border-radius:12px;min-height:280px;max-height:620px;overflow:auto;font:12px/1.55 ui-monospace,SFMono-Regular,Menlo,monospace}.surface{display:grid;gap:8px}.decision{border:1px solid var(--line);border-radius:12px;padding:12px;background:var(--soft)}.decision strong{display:block}.state-row{display:flex;justify-content:space-between;gap:16px;border-top:1px solid var(--line);padding:8px 0;font:12px ui-monospace,SFMono-Regular,Menlo,monospace}.state-row:first-child{border-top:0}.status{font-weight:800}.EXECUTED{color:var(--ok)}.BLOCKED,.INVALIDATED,.ROLLED_BACK{color:var(--warn)}.note{padding:12px 14px;border-left:3px solid #94a3b8;background:var(--soft);border-radius:8px;line-height:1.5}.architecture{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;white-space:pre-wrap;line-height:1.7;color:#334155}@media(max-width:850px){.span8,.span4{grid-column:span 12}.grid{gap:12px}main{padding:20px 14px 56px}}</style></head><body><main><section class="hero"><div class="eyebrow">EvidenceBound · Agents for Humans candidate</div><h1>Authority Cut</h1><p class="lede">A professional-agent control plane that compresses seven protected vendor-onboarding effects into three policy-defined human authorities, executes routine work without interruption, and propagates a later human correction through already-executed reversible descendants.</p><div class="badges"><span class="badge ready">CONTROL KERNEL READY</span><span class="badge unverified">STRANDS RUNTIME UNVERIFIED</span><span class="badge unverified">AGENTCORE UNVERIFIED</span><span class="badge boundary">MODEL CANNOT APPROVE ITSELF</span></div><div class="note"><strong>Truth boundary.</strong> This local surface exercises the deterministic competition-period control kernel. Strands source integration exists, but a real Strands runtime and AgentCore deployment are not claimed until externally verified.</div></section><section class="grid"><div class="card span8"><h2>Controlled judge path</h2><p class="small">Safe work runs first. Human authority enters only through these external API actions; approve/revoke are deliberately absent from the model-callable Strands toolset.</p><div class="controls"><button class="secondary" onclick="post('/api/reset')">Reset</button><button onclick="post('/api/run-safe')">1 · Run five safe actions</button><button onclick="decision('vendor-risk')">2 · Human approves vendor-risk</button><button onclick="decision('payment-release')">3 · Human approves payment-release</button><button class="danger" onclick="correct()">4 · Human revokes vendor-risk</button></div></div><div class="card span4"><h2>Irreversible boundary</h2><div class="metric">3</div><div class="small">semantic authority decisions for 7 protected effects in this controlled workflow.</div><p class="small"><strong>First-funds remains a distinct irreversible authority.</strong> It cannot be approved until the remittance preview prerequisite actually exists.</p></div><div class="card span4"><h2>Attention compression</h2><div class="metric">57.14%</div><div class="small">fewer approval prompts than a per-protected-effect baseline in this fixed workflow (7 → 3). Not a general productivity claim.</div></div><div class="card span4"><h2>Autonomous safe work</h2><div class="metric">5</div><div class="small">routine actions complete before human authority is required.</div></div><div class="card span4"><h2>Correction recovery</h2><div class="metric">6</div><div class="small">reversible protected effects executed in the controlled path and rolled back after vendor-risk authority is revoked; irreversible transfer stays separately gated.</div></div><div class="card span4"><h2>Authority Cut</h2><div id="surface" class="surface"><div class="small">Run the workflow to inspect the current decision surface.</div></div></div><div class="card span4"><h2>Action state</h2><div id="states"><div class="small">No controlled run yet.</div></div></div><div class="card span4"><h2>Architecture boundary</h2><div class="architecture">Professional goal
  ↓
Strands agent (UNVERIFIED here)
  ↓ safe/authorized tools only
Shared ControlPlane
  ↙             ↘
Authority Cut    Receipts
  ↑
External human API
approve / revoke</div></div><div class="card span12"><h2>Evidence ledger</h2><pre id="out">Not run. Select Reset or run the controlled path.</pre></div></section></main><script>const out=document.getElementById('out'),states=document.getElementById('states'),surface=document.getElementById('surface');function render(data){out.textContent=JSON.stringify(data,null,2);if(data.status){states.innerHTML=Object.entries(data.status).map(([k,v])=>`<div class="state-row"><span>${k}</span><span class="status ${v}">${v}</span></div>`).join('')}if(data.decision_surface){surface.innerHTML=data.decision_surface.length?data.decision_surface.map(d=>`<div class="decision"><strong>${d.bundle_id}</strong><span class="small">${d.ready?'READY':'FUTURE'} · grants ${d.grants.join(', ')} · prereqs ${d.prereqs.join(', ')||'none'}</span></div>`).join(''):'<div class="small">No additional authority currently required.</div>'}}async function request(url,options){const r=await fetch(url,options);const data=await r.json();render(data);if(!r.ok)throw new Error(data.detail||'request failed');return data}async function post(url,body={}){try{return await request(url,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(body)})}catch(e){out.textContent+='\n\nFAIL-CLOSED: '+e.message}}function decision(id){return post('/api/decisions/'+id,{approved:true,rationale:'Controlled external principal approval'})}function correct(){return post('/api/corrections/vendor-risk',{reason:'Principal withdraws the previously granted vendor-risk authority'})}</script></body></html>"""


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return HTML
