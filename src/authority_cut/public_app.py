"""Human-first public judge service for Authority Cut.

The live endpoint executes the real Strands Agent loop using a deterministic custom
Model provider. It is intentionally credential-free and does not claim that this
public request uses a foundation model or AgentCore Runtime.
"""
from __future__ import annotations

from dataclasses import asdict

from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse

from .evaluate import run_evaluation
from .live_proof import run_live_strands_proof
from .strands_app import STRANDS_TOOL_NAMES

app = FastAPI(title="Authority Cut — Bank Vendor Onboarding", version="2.0.0")


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
        "bank_ecp_bridge": "DEVELOPMENT_ONLY",
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
        "evidence_update_channel": "EXTERNAL_NON_MODEL",
    }


@app.post("/api/strands-proof")
def strands_proof() -> dict[str, object]:
    return run_live_strands_proof()


@app.get("/favicon.ico", include_in_schema=False)
@app.get("/favicon.png", include_in_schema=False)
def favicon() -> Response:
    return Response(status_code=204)


HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Authority Cut — Bank vendor onboarding</title>
<style>
:root{--bg:#f5f7fb;--panel:#fff;--ink:#101828;--muted:#667085;--line:#e4e7ec;--deep:#182230;--blue:#175cd3;--blue-soft:#eff8ff;--green:#067647;--green-soft:#ecfdf3;--amber:#b54708;--amber-soft:#fffaeb;--red:#b42318;--red-soft:#fef3f2}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}.wrap{max-width:1140px;margin:auto;padding:34px 22px 72px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:20px;box-shadow:0 12px 36px rgba(16,24,40,.06)}.hero{padding:34px}.eyebrow{font-size:12px;font-weight:850;letter-spacing:.12em;text-transform:uppercase;color:var(--blue)}h1{font-size:clamp(38px,6vw,68px);line-height:.98;letter-spacing:-.055em;max-width:900px;margin:10px 0 18px}.lede{font-size:18px;line-height:1.65;max-width:900px;color:#344054}.cta{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-top:24px}button{border:0;border-radius:12px;background:var(--deep);color:white;padding:13px 17px;font-weight:800;cursor:pointer;font-size:14px}button:disabled{opacity:.6;cursor:wait}.micro{font-size:12px;color:var(--muted)}.flow{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:16px}.step{padding:20px}.num{width:30px;height:30px;border-radius:50%;display:grid;place-items:center;font-weight:900;background:var(--blue-soft);color:var(--blue);margin-bottom:12px}.step h2{font-size:18px;margin:0 0 7px}.step p{margin:0;color:var(--muted)}.result{margin-top:16px;padding:26px}.result-head{display:flex;justify-content:space-between;gap:16px;align-items:flex-start}.result h2,.technical h2{font-size:24px;letter-spacing:-.025em;margin:0}.result-sub{color:var(--muted);margin:7px 0 0}.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:18px}.card{border:1px solid var(--line);border-radius:15px;padding:16px;background:#fff}.card .label{font-size:12px;text-transform:uppercase;letter-spacing:.08em;font-weight:800;color:var(--muted)}.card .value{font-size:23px;font-weight:900;letter-spacing:-.03em;margin-top:6px}.ok{background:var(--green-soft);border-color:#abefc6}.ok .value{color:var(--green)}.warn{background:var(--amber-soft);border-color:#fedf89}.warn .value{color:var(--amber)}.stop{background:var(--red-soft);border-color:#fecdca}.stop .value{color:var(--red)}.timeline{display:grid;gap:10px;margin-top:18px}.event{display:grid;grid-template-columns:128px 1fr;gap:14px;padding:13px 0;border-top:1px solid var(--line)}.event:first-child{border-top:0}.time{font-size:12px;font-weight:850;color:var(--blue);text-transform:uppercase;letter-spacing:.06em}.event strong{display:block}.event span{color:var(--muted);font-size:13px}.hidden{display:none}.technical{margin-top:16px;padding:26px}.tech-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:16px}.tech{border:1px solid var(--line);border-radius:14px;padding:16px}.tech strong{display:block;margin-bottom:5px}.truth{margin-top:16px;padding:14px 16px;border-left:4px solid var(--blue);background:var(--blue-soft);border-radius:0 12px 12px 0;color:#344054}.raw{margin-top:14px}details{border:1px solid var(--line);border-radius:14px;padding:14px 16px}summary{font-weight:800;cursor:pointer}pre{white-space:pre-wrap;background:#101828;color:#d0d5dd;border-radius:12px;padding:16px;max-height:560px;overflow:auto;font:12px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace}.footer{padding-top:18px;color:var(--muted);font-size:12px}@media(max-width:860px){.flow,.cards,.tech-grid{grid-template-columns:1fr 1fr}.event{grid-template-columns:1fr;gap:3px}}@media(max-width:580px){.flow,.cards,.tech-grid{grid-template-columns:1fr}.wrap{padding:18px 12px 48px}.hero,.result,.technical{padding:20px}h1{font-size:40px}}
</style>
</head>
<body>
<main class="wrap">
<section class="panel hero">
<div class="eyebrow">Bank vendor onboarding · EvidenceBound</div>
<h1>Onboard a vendor without giving the AI the final say.</h1>
<p class="lede">The AI handles routine vendor work. A person approves decisions that carry real compliance or financial risk. If the evidence changes later, affected work is undone and payment stays blocked.</p>
<div class="cta"><button id="run" onclick="runProof()">Run the end-to-end banking scenario</button><span class="micro">Real Strands SDK Agent/tool loop. Human authority stays outside the model toolset.</span></div>
</section>

<section class="flow">
<article class="panel step"><div class="num">1</div><h2>AI does the routine work</h2><p>Vendor packet, tax and bank checks, draft setup and follow-up happen before the human is interrupted.</p></article>
<article class="panel step"><div class="num">2</div><h2>A human decides what carries risk</h2><p>When vendor activation and payment setup become consequential, the bank employee provides the required authority.</p></article>
<article class="panel step"><div class="num">3</div><h2>Evidence changes</h2><p>The regulatory evidence gate moves from PASS to HOLD. Stale authority stops working: affected setup is undone, unrelated safe work remains, and first payment cannot proceed.</p></article>
</section>

<section id="result" class="panel result hidden">
<div class="result-head"><div><div class="eyebrow">What changed</div><h2>The correction changes execution, not just the audit log.</h2><p class="result-sub">The system re-evaluates what the prior human approval can still authorize.</p></div></div>
<div class="cards">
<div class="card warn"><div class="label">Evidence after correction</div><div id="evidence" class="value">HOLD</div></div>
<div class="card stop"><div class="label">Affected setup</div><div id="rollback" class="value">6 undone</div></div>
<div class="card ok"><div class="label">Unrelated safe work</div><div id="preserved" class="value">5 preserved</div></div>
<div class="card stop"><div class="label">First payment</div><div class="value">BLOCKED</div></div>
</div>
<div id="timeline" class="timeline"></div>
</section>

<section class="panel technical">
<div class="eyebrow">Technical evidence</div>
<h2>Simple banking behavior, backed by explicit control boundaries.</h2>
<div class="tech-grid">
<div class="tech"><strong>Strands is load-bearing</strong><span>The public judge path executes a real Strands Agent/tool loop with three model-callable operational tools.</span></div>
<div class="tech"><strong>The model cannot approve itself</strong><span>Approve/revoke authority mutation tools are absent from the Strands tool schema. Human authority is external.</span></div>
<div class="tech"><strong>BANK-ECP changes authority</strong><span>A sanitized DORA vendor-responsibility bridge moves PASS → HOLD and invalidates the stale vendor-risk approval.</span></div>
</div>
<div class="truth"><strong>Truth boundary.</strong> This public page uses a deterministic custom Strands Model provider so anyone can reproduce the judge path without credentials. It proves live Strands orchestration and authority separation. This request does not claim a foundation-model or AgentCore invocation. The BANK-ECP bridge shown here is DEVELOPMENT_ONLY and is not formal benchmark-performance evidence.</div>
<div class="raw"><details><summary>Show execution diagnostics</summary><pre id="out">Run the banking scenario to populate the execution ledger.</pre></details></div>
</section>
<div class="footer">Authority Cut · AWS Agents for Humans · Professional Agents</div>
</main>
<script>
function phaseCopy(p){const phase=p.phase||'';if(phase==='routine-work-and-evidence-check')return['AI working','Routine vendor checks finish and the BANK-ECP evidence gate is PASS.'];if(phase==='human-approved-vendor-risk')return['Human decision','The vendor-risk reviewer approves the risky step; protected vendor setup proceeds.'];if(phase==='protected-setup-complete')return['Protected work','Vendor activation, ERP/purchasing and payment-profile preparation proceed; first funds still waits for separate authority.'];if(phase==='evidence-changed')return['Evidence changed','The evidence gate becomes HOLD. Affected reversible work is undone, safe routine work stays, and first payment remains blocked.'];return[phase,''];}
async function runProof(){const b=document.getElementById('run'),r=document.getElementById('result'),o=document.getElementById('out'),t=document.getElementById('timeline');b.disabled=true;b.textContent='Running banking scenario…';try{const res=await fetch('/api/strands-proof',{method:'POST'});const d=await res.json();if(!res.ok)throw new Error(JSON.stringify(d));document.getElementById('evidence').textContent=(d.bank_ecp_evidence_after_correction||{}).verdict||'HOLD';document.getElementById('rollback').textContent=d.protected_reversible_effects_rolled_back+' undone';document.getElementById('preserved').textContent=d.safe_actions_preserved+' preserved';t.innerHTML=(d.phases||[]).map(p=>{const c=phaseCopy(p);return `<div class="event"><div class="time">${c[0]}</div><div><strong>${c[1]}</strong><span>${p.phase==='evidence-changed'?' Payment execution state: '+d.irreversible_transmit_after_correction+'.':''}</span></div></div>`}).join('');o.textContent=JSON.stringify(d,null,2);r.classList.remove('hidden');r.scrollIntoView({behavior:'smooth',block:'start'});b.textContent='Run scenario again';}catch(e){o.textContent='FAIL-CLOSED: '+e;b.textContent='Retry scenario';document.getElementById('result').classList.remove('hidden');}finally{b.disabled=false}}
</script>
</body>
</html>'''


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return HTML
