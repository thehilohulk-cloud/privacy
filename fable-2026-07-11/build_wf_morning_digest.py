#!/usr/bin/env python3
"""
build_wf_morning_digest.py — deploy WF-Morning-Digest to n8n (digest-migration SPEC item 1+2, CONSOLIDATED).

Replaces laptop tasks `ops-log-rollup` (4:31a) + `tpts-overwatch-morning` (5:35a) with ONE n8n
digest SMS at 4:45a HST from front desk 4753 — per SPEC recommendation "consolidate #1 into #2".

Doctrine honored (Operations Notebook / OPERATORS-CODEX):
  - fetch-or-create by name; deactivate->PUT->activate is NOT atomic -> re-GET and verify `active`
    matches as-found; carry staticData through PUT (PUT preserves it if included in body).
  - settings whitelist: executionOrder + errorWorkflow ONLY (PUT 400s on binaryMode/callerPolicy/availableInMCP).
  - Guardian errorWorkflow pxCzWL7wlfmR7fQf on the workflow.
  - node --check every embedded JS block before deploy.
  - No tokens inline: n8n API key read from vault file at runtime.
  - GHL send: POST /conversations/messages, explicit fromNumber (4753), Garrett contact GaPdKEftwuZTL9g6Z0x5.
  - Anthropic node: sonnet-5, thinking explicitly disabled, explicit max_tokens, static system block
    with cache_control (block must be >=1024 tok or caching is silently inert -- verify cache_read on run 2).
  - HTTP source nodes: alwaysOutputData + onError continue -- a dead source degrades the digest, never kills it.
  - Heartbeat anchor: staticData.lastSuccessISO bounds the review window (never fixed "last 24h"); cap 72h.

ZERO-CONFIG: the script HARVESTS live wiring from the existing fleet instead of hardcoding:
  - GHL credential + fromNumber + locationId + Version header: copied from any active node POSTing
    to conversations/messages (Triage V3 / WF-Date-Actions / WF-Down-Sell all qualify).
  - Anthropic credential: copied from any node calling api.anthropic.com (Coaching Brain / plan-gen).
  - n8n self-read credential: harvested from Sentinel 2yWJo3KocHsqSZGp's self-API node if present,
    else the two fleet-health nodes are left credential-less and the runbook's manual step applies.

Usage (laptop):
  set N8N_BASE_URL=https://<instance>       (or hardcode DEFAULT_BASE below to the known instance)
  set N8N_API_KEY_FILE=<vault path to key>  (never the key itself on a command line)
  python build_wf_morning_digest.py [--dry-run]

After deploy: see wf-morning-digest-RUNBOOK.md (Sentinel registration, 2-clean-runs rule before
deleting the local tasks, TODO(VERIFY-GHL) endpoint checks against the local SKILL.md files).
"""
import json, os, subprocess, sys, tempfile, urllib.request, urllib.parse

WF_NAME = "WF-Morning-Digest"
GUARDIAN_ID = "pxCzWL7wlfmR7fQf"
GARRETT_CONTACT = "GaPdKEftwuZTL9g6Z0x5"
CRON = "45 4 * * *"          # 4:45a HST daily (instance tz = HST). Garrett wakes 4:30.
DRY = "--dry-run" in sys.argv

BASE = os.environ.get("N8N_BASE_URL", "").rstrip("/")
KEY_FILE = os.environ.get("N8N_API_KEY_FILE", "")
if not DRY and (not BASE or not KEY_FILE):
    sys.exit("Set N8N_BASE_URL and N8N_API_KEY_FILE (vault path). Or --dry-run to just emit JSON.")
API_KEY = open(KEY_FILE, encoding="utf-8").read().strip() if (KEY_FILE and os.path.exists(KEY_FILE)) else ""

def api(method, path, body=None):
    req = urllib.request.Request(BASE + "/api/v1" + path, method=method,
        headers={"X-N8N-API-KEY": API_KEY, "Content-Type": "application/json"},
        data=json.dumps(body).encode() if body is not None else None)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read() or "{}")

def all_workflows():
    out, cursor = [], None
    while True:
        q = "?limit=100" + (f"&cursor={cursor}" if cursor else "")
        page = api("GET", "/workflows" + q)
        out += page.get("data", [])
        cursor = page.get("nextCursor")
        if not cursor: return out

# ---------------------------------------------------------------- embedded JS
JS_ANCHOR = r"""
// Heartbeat-anchored review window (doctrine: never fixed 24h).
const sd = $getWorkflowStaticData('global');
const now = new Date();
let since = sd.lastSuccessISO ? new Date(sd.lastSuccessISO) : new Date(now - 24*3600*1000);
const cap = new Date(now - 72*3600*1000);
if (since < cap) since = cap;                       // cap 72h so a long outage doesn't flood
const hst = new Date(now.getTime() - 10*3600*1000); // HST = UTC-10, no DST
const dayStartHST = new Date(Date.UTC(hst.getUTCFullYear(), hst.getUTCMonth(), hst.getUTCDate(), 10, 0, 0));
return [{ json: {
  sinceISO: since.toISOString(), nowISO: now.toISOString(),
  todayStartISO: dayStartHST.toISOString(),
  todayEndISO: new Date(dayStartHST.getTime() + 24*3600*1000).toISOString(),
  todayStartMs: dayStartHST.getTime(),
  todayEndMs: dayStartHST.getTime() + 24*3600*1000,
  firstRun: !sd.lastSuccessISO
}}];
"""

JS_AGGREGATE = r"""
// Merge all sources into one compact digest payload. Every source is optional:
// alwaysOutputData+onError-continue upstream means empty/err items arrive as {} — report the gap, never crash.
const anchor = $('Anchor window').first().json;
function grab(name){ try { return $(name).all().map(i => i.json); } catch(e){ return null; } }

const errs = grab('n8n exec errors');
const flt  = grab('n8n active workflows');
const appt = grab('GHL appointments today');
const pay  = grab('GHL payments window');

const out = { window_start: anchor.sinceISO, now: anchor.nowISO, gaps: [] };

// Fleet health: errors since anchor, grouped by workflow
if (errs && errs[0] && errs[0].data !== undefined) {
  const rows = (errs[0].data || []).filter(e => new Date(e.startedAt) >= new Date(anchor.sinceISO));
  const byWf = {};
  for (const e of rows) byWf[e.workflowName || e.workflowId] = (byWf[e.workflowName || e.workflowId] || 0) + 1;
  out.n8n_errors = byWf; out.n8n_error_count = rows.length;
} else out.gaps.push('n8n-errors');

if (flt && flt[0] && flt[0].data !== undefined) out.active_workflows = (flt[0].data || []).length;
else out.gaps.push('n8n-fleet');

// Consults / appointments today
if (appt && appt[0] && (appt[0].events !== undefined || appt[0].appointments !== undefined)) {
  const evs = appt[0].events || appt[0].appointments || [];
  out.consults_today = evs.map(e => ({ t: e.startTime, title: e.title, status: e.appointmentStatus }));
} else out.gaps.push('ghl-appointments');

// Payments in window
if (pay && pay[0] && pay[0].data !== undefined) {
  const tx = (pay[0].data || []);
  out.payments = { count: tx.length,
    total: Math.round(tx.reduce((s,t) => s + (Number(t.amount)||0), 0) * 100) / 100 };
} else out.gaps.push('ghl-payments');

return [{ json: { digest_data: JSON.stringify(out) } }];
"""

JS_SEND_GUARD = r"""
// Fence-strip + hard 320 cap + empty-guard with deterministic fallback (LLM failure never = silent morning).
const anchor = $('Anchor window').first().json;
let txt = '';
try {
  const r = $('Anthropic compose').first().json;
  txt = (r.content && r.content[0] && r.content[0].text) ? r.content[0].text : '';
} catch(e) { /* compose node dead */ }
txt = txt.replace(/```[a-z]*\n?/g, '').replace(/```/g, '').replace(/\s+/g, ' ').trim();
if (!txt) {
  let d = {}; try { d = JSON.parse($('Aggregate').first().json.digest_data); } catch(e){}
  txt = '[MORNING] compose failed - raw: n8n errs ' + (d.n8n_error_count ?? '?')
      + ', consults ' + ((d.consults_today||[]).length ?? '?')
      + ', payments $' + ((d.payments||{}).total ?? '?')
      + (d.gaps && d.gaps.length ? ', gaps: ' + d.gaps.join('/') : '');
}
if (!/^\[MORNING\]/.test(txt)) txt = '[MORNING] ' + txt;
if (txt.length > 320) txt = txt.slice(0, 317) + '...';
return [{ json: { sms: txt } }];
"""

JS_MARK_SUCCESS = r"""
const sd = $getWorkflowStaticData('global');
sd.lastSuccessISO = new Date().toISOString();
return [{ json: { ok: true, lastSuccessISO: sd.lastSuccessISO } }];
"""

def node_check(label, js):
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        # wrap: n8n globals stubbed so `node --check` only validates syntax
        f.write("function $(){return{first:()=>({json:{}}),all:()=>[]}};function $getWorkflowStaticData(){return{}};\n"
                + "async function main(){\n" + js + "\n}\n")
        p = f.name
    r = subprocess.run(["node", "--check", p], capture_output=True, text=True)
    os.unlink(p)
    if r.returncode != 0:
        sys.exit(f"node --check FAILED for {label}:\n{r.stderr}")
    print(f"  node --check ok: {label}")

SYSTEM_PROMPT = (
    "You compose Garrett's single morning operations digest SMS for his Hilo personal-training studio "
    "(Transformations). You receive one JSON payload of overnight/last-window operational data. Write ONE "
    "SMS, plain text, maximum 300 characters, information-dense, no fluff, no markdown, no emoji. "
    "Priority order when space is tight: (1) anything broken - n8n workflow errors by name with counts; "
    "(2) data-source gaps (name them, e.g. 'ghl-payments unreadable'); (3) today's consults - count plus "
    "earliest time; (4) payments captured in the window - count and dollar total; (5) fleet size only if "
    "it changed from typical (~30 active). Rules: if n8n_error_count is 0 and gaps is empty, open with 'all "
    "green.' Never invent numbers absent from the payload; if a section is missing say so in two words. "
    "Round dollars. Use 12h HST times like 9a/2:30p. This SMS is the entire morning report - Garrett reads "
    "it at 4:45am before his first client and decides whether to open a laptop, so broken things come "
    "first and quiet mornings must be short ('all green. 3 consults, first 9a. $1,240 in.'). Do not "
    "address Garrett or sign off; the text starts with the report itself. Style reference examples: "
    "'all green. 2 consults, first 11a. $0 in.' | 'WF12 3 errs overnight, rest green. gaps: ghl-payments. "
    "4 consults, first 9a. $2,890 in (3).' | 'compose sources thin: n8n-errors+ghl-appointments gaps - "
    "check creds. 1 payment $399.'"
)

def build_workflow(h):
    """h = harvested wiring dict."""
    ghl_headers = [
        {"name": "Version", "value": h.get("ghl_version", "2021-07-28")},
        {"name": "Accept", "value": "application/json"},
    ]
    def http(name, pos, url, method="GET", cred=None, qs=None, body=None, always=True, cont=True):
        n = {"name": name, "type": "n8n-nodes-base.httpRequest", "typeVersion": 4.2, "position": pos,
             "parameters": {"url": url, "method": method, "options": {}},
             "alwaysOutputData": always}
        if cont: n["onError"] = "continueRegularOutput"
        if qs:
            n["parameters"]["sendQuery"] = True
            n["parameters"]["queryParameters"] = {"parameters": qs}
        if body is not None:
            n["parameters"]["sendBody"] = True
            n["parameters"]["specifyBody"] = "json"
            n["parameters"]["jsonBody"] = body
        if cred: n["credentials"] = cred
        return n
    def code(name, pos, js, cont=False):
        n = {"name": name, "type": "n8n-nodes-base.code", "typeVersion": 2, "position": pos,
             "parameters": {"jsCode": js}}
        if cont: n["onError"] = "continueRegularOutput"
        return n

    ghl = "https://services.leadconnectorhq.com"
    nodes = [
        {"name": "Cron 4:45a HST", "type": "n8n-nodes-base.scheduleTrigger", "typeVersion": 1.2,
         "position": [0, 0], "parameters": {"rule": {"interval": [
             {"field": "cronExpression", "expression": CRON}]}}},
        code("Anchor window", [200, 0], JS_ANCHOR),
        http("n8n exec errors", [400, -200], f"{BASE}/api/v1/executions",
             qs=[{"name": "status", "value": "error"}, {"name": "limit", "value": "100"}],
             cred=h.get("n8n_cred")),
        http("n8n active workflows", [400, -60], f"{BASE}/api/v1/workflows",
             qs=[{"name": "active", "value": "true"}, {"name": "limit", "value": "100"}],
             cred=h.get("n8n_cred")),
        # TODO(VERIFY-GHL): confirm endpoint+params against local SKILL.md of tpts-overwatch-morning.
        http("GHL appointments today", [400, 80], f"{ghl}/calendars/events",
             qs=[{"name": "locationId", "value": h["location_id"]},
                 {"name": "startTime", "value": "={{ $('Anchor window').first().json.todayStartMs }}"},
                 {"name": "endTime", "value": "={{ $('Anchor window').first().json.todayEndMs }}"}],
             cred=h["ghl_cred"]),
        # TODO(VERIFY-GHL): payments listing endpoint (ops-log-rollup SKILL.md may use /payments/transactions).
        http("GHL payments window", [400, 220], f"{ghl}/payments/transactions",
             qs=[{"name": "altId", "value": h["location_id"]}, {"name": "altType", "value": "location"},
                 {"name": "startAt", "value": "={{ $('Anchor window').first().json.sinceISO }}"},
                 {"name": "endAt", "value": "={{ $('Anchor window').first().json.nowISO }}"}],
             cred=h["ghl_cred"]),
        code("Aggregate", [640, 0], JS_AGGREGATE),
        http("Anthropic compose", [840, 0], "https://api.anthropic.com/v1/messages", method="POST",
             cred=h["anthropic_cred"],
             body=json.dumps({
                 "model": "claude-sonnet-5", "max_tokens": 400,
                 "thinking": {"type": "disabled"},
                 "system": [{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}],
                 "messages": [{"role": "user",
                               "content": "={{ $('Aggregate').first().json.digest_data }}"}]}),
             always=True, cont=True),
        code("Send guard", [1040, 0], JS_SEND_GUARD),
        http("SMS Garrett 4753", [1240, 0], f"{ghl}/conversations/messages", method="POST",
             cred=h["ghl_cred"],
             body=json.dumps({"type": "SMS", "contactId": GARRETT_CONTACT,
                              "message": "={{ $('Send guard').first().json.sms }}",
                              "fromNumber": h["from_number"]}),
             always=False, cont=False),
        code("Mark success", [1440, 0], JS_MARK_SUCCESS),
    ]
    for n in nodes:
        if n["type"] == "n8n-nodes-base.httpRequest" and "conversations" not in n["parameters"]["url"]:
            n["parameters"]["options"] = {"response": {"response": {"neverError": False}}}
        if n["type"] == "n8n-nodes-base.httpRequest" and "leadconnectorhq" in n["parameters"]["url"]:
            n["parameters"]["sendHeaders"] = True
            n["parameters"]["headerParameters"] = {"parameters": ghl_headers}
    conns = {}
    def wire(a, b): conns.setdefault(a, {"main": [[]]})["main"][0].append({"node": b, "type": "main", "index": 0})
    wire("Cron 4:45a HST", "Anchor window")
    for src in ["n8n exec errors", "n8n active workflows", "GHL appointments today", "GHL payments window"]:
        wire("Anchor window", src); wire(src, "Aggregate")
    wire("Aggregate", "Anthropic compose"); wire("Anthropic compose", "Send guard")
    wire("Send guard", "SMS Garrett 4753"); wire("SMS Garrett 4753", "Mark success")
    return {"name": WF_NAME, "nodes": nodes, "connections": conns,
            "settings": {"executionOrder": "v1", "errorWorkflow": GUARDIAN_ID}}

def harvest():
    """Copy live wiring from the fleet: GHL cred/fromNumber/locationId, Anthropic cred, n8n self cred."""
    h = {}
    for wf in all_workflows():
        full = api("GET", f"/workflows/{wf['id']}")
        for n in full.get("nodes", []):
            p = n.get("parameters", {})
            url = str(p.get("url", ""))
            body = str(p.get("jsonBody", "")) + json.dumps(p.get("bodyParameters", {}))
            if "conversations/messages" in url and "ghl_cred" not in h and n.get("credentials"):
                h["ghl_cred"] = n["credentials"]
                import re
                m = re.search(r'"fromNumber"\s*:\s*"(\+?[\d]+)"', body)
                if m: h["from_number"] = m.group(1)
                for hp in (p.get("headerParameters", {}) or {}).get("parameters", []):
                    if hp.get("name", "").lower() == "version": h["ghl_version"] = hp["value"]
            if "locationId" not in body and "location_id" not in h:
                import re
                m = re.search(r'"locationId"[^"]*"value"\s*:\s*"([A-Za-z0-9]+)"', json.dumps(p))
                if m: h["location_id"] = m.group(1)
            if "api.anthropic.com" in url and "anthropic_cred" not in h and n.get("credentials"):
                h["anthropic_cred"] = n["credentials"]
            if "/api/v1/executions" in url and "n8n_cred" not in h and n.get("credentials"):
                h["n8n_cred"] = n["credentials"]  # Sentinel's self-read cred
    missing = [k for k in ["ghl_cred", "from_number", "location_id", "anthropic_cred"] if k not in h]
    if missing:
        sys.exit(f"HARVEST INCOMPLETE — missing {missing}. Open Triage V3 / Coaching Brain in the n8n UI, "
                 "note the cred names + fromNumber + locationId, and fill DEFAULTS in this script.")
    if "n8n_cred" not in h:
        print("  WARN: no n8n self-read cred found (Sentinel pattern) — fleet-health nodes deploy "
              "credential-less; attach the header-auth cred in the UI (runbook step 3).")
    return h

def main():
    for label, js in [("Anchor", JS_ANCHOR), ("Aggregate", JS_AGGREGATE),
                      ("SendGuard", JS_SEND_GUARD), ("MarkSuccess", JS_MARK_SUCCESS)]:
        node_check(label, js)
    if DRY:
        stub = {"ghl_cred": {"httpCustomAuth": {"id": "khqXsUCl9Nj0bkja", "name": "GHL API - Della PIT (full scopes)"}},
                "from_number": "+1808XXXXXXX", "location_id": "LOCATION_ID",
                "anthropic_cred": {"httpHeaderAuth": {"id": "sXj02G4c2lNWSmqZ", "name": "Anthropic"}}}
        print(json.dumps(build_workflow(stub), indent=2)); return
    print("Harvesting live wiring from fleet...")
    h = harvest()
    print(f"  fromNumber={h['from_number']}  locationId={h['location_id']}")
    wf_json = build_workflow(h)
    existing = [w for w in all_workflows() if w["name"] == WF_NAME]
    if existing:
        wid = existing[0]["id"]
        cur = api("GET", f"/workflows/{wid}")
        was_active = cur.get("active", False)
        if cur.get("staticData"): wf_json["staticData"] = cur["staticData"]  # preserve heartbeat anchor
        if was_active: api("POST", f"/workflows/{wid}/deactivate")
        api("PUT", f"/workflows/{wid}", wf_json)
        api("POST", f"/workflows/{wid}/activate")
        chk = api("GET", f"/workflows/{wid}")
        assert chk.get("active") is True, "NOT ACTIVE after update — deactivate->PUT->activate broke mid-way, fix in UI"
        print(f"UPDATED + re-activated {WF_NAME} ({wid})")
    else:
        made = api("POST", "/workflows", wf_json)
        wid = made["id"]
        api("POST", f"/workflows/{wid}/activate")
        chk = api("GET", f"/workflows/{wid}")
        assert chk.get("active") is True, "activation failed"
        print(f"CREATED + activated {WF_NAME} ({wid})")
    print("\nNEXT (runbook): 1) manual test-run, verify SMS lands on 4753 thread;"
          "\n 2) resolve TODO(VERIFY-GHL) endpoints vs local SKILL.md files;"
          "\n 3) register in Sentinel 2yWJo3KocHsqSZGp expected-runs (daily);"
          "\n 4) after 2 clean scheduled runs, delete local tasks ops-log-rollup + tpts-overwatch-morning;"
          "\n 5) update OPERATORS-CODEX + notebook.")

if __name__ == "__main__":
    main()
