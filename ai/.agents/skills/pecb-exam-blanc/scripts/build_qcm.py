#!/usr/bin/env python3
"""build_qcm.py — Génère un QCM interactif HTML autonome depuis un JSON d'examen.
Usage : python3 build_qcm.py exam.json -o exam.html
Stdlib uniquement (json, html, argparse, pathlib). HTML offline, aucune dépendance.
Schéma JSON : voir ~/.agents/skills/pecb-exam-blanc/SKILL.md §5-bis.
"""
import argparse, json, sys
from pathlib import Path

POIDS_OFFICIELS = {"D1": 18.75, "D2": 15.0, "D3": 22.5, "D4": 17.5,
                   "D5": 12.5, "D6": 7.5, "D7": 6.25}

def validate(data):
    assert "titre" in data and "questions" in data, "JSON: clés titre/questions manquantes"
    for i, q in enumerate(data["questions"], 1):
        for k in ("id", "domaine", "niveau", "enonce", "options", "bonne"):
            assert k in q, f"Q{i}: clé '{k}' manquante"
        assert set(q["options"].keys()) == {"A", "B", "C"}, f"Q{i}: il faut exactement 3 options A/B/C"
        assert q["bonne"] in "ABC", f"Q{i}: bonne réponse invalide"

TEMPLATE = r"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITRE__</title>
<style>
:root{--bg:#0f1420;--card:#1a2233;--card2:#222c42;--txt:#e8edf5;--mut:#9aa8bd;--acc:#4f9cf9;
--ok:#3fb96f;--ko:#e05656;--warn:#e8a13c;--bord:#2e3a52}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--txt);font:16px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;padding:16px;max-width:880px;margin:auto}
h1{font-size:1.35rem;margin-bottom:4px}h2{font-size:1.1rem;margin:14px 0 8px}
.card{background:var(--card);border:1px solid var(--bord);border-radius:12px;padding:18px;margin-bottom:14px}
.muted{color:var(--mut)}.small{font-size:.85rem}
.chip{display:inline-block;background:var(--card2);border:1px solid var(--bord);border-radius:99px;padding:2px 10px;font-size:.78rem;margin-right:6px;color:var(--mut)}
.chip.d{color:var(--acc);border-color:var(--acc)}
.btn{background:var(--acc);color:#fff;border:0;border-radius:9px;padding:10px 20px;font-size:1rem;cursor:pointer;font-weight:600}
.btn.sec{background:var(--card2);color:var(--txt);border:1px solid var(--bord)}
.btn:disabled{opacity:.4;cursor:default}
.opt{display:block;width:100%;text-align:left;background:var(--card2);color:var(--txt);border:2px solid var(--bord);border-radius:10px;padding:13px 15px;margin:9px 0;cursor:pointer;font-size:.98rem;line-height:1.45}
.opt:hover:not(:disabled){border-color:var(--acc)}
.opt.sel{border-color:var(--acc)}
.opt.ok{border-color:var(--ok);background:rgba(63,185,111,.12)}
.opt.ko{border-color:var(--ko);background:rgba(224,86,86,.10)}
.opt:disabled{cursor:default}
.opt b{color:var(--acc);margin-right:8px}
.topbar{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:12px}
#timer{font-variant-numeric:tabular-nums;font-size:1.15rem;font-weight:700}
#timer.low{color:var(--ko)}
.fb{border-top:1px solid var(--bord);margin-top:14px;padding-top:12px}
.fb .ok{color:var(--ok);font-weight:700}.fb .ko{color:var(--ko);font-weight:700}
.chem{background:var(--card2);border-left:3px solid var(--warn);border-radius:0 8px 8px 0;padding:10px 14px;margin:10px 0;font-size:.92rem}
.chem ol{margin:6px 0 0 20px}
.src{font-size:.85rem;color:var(--mut);margin-top:8px}
table{border-collapse:collapse;width:100%;font-size:.92rem}
th,td{border:1px solid var(--bord);padding:7px 10px;text-align:left}
th{background:var(--card2)}
.bar{height:8px;background:var(--card2);border-radius:99px;overflow:hidden;margin-top:4px}
.bar>i{display:block;height:100%;background:var(--acc)}
.score{font-size:2.6rem;font-weight:800}
.pill{display:inline-block;border-radius:99px;padding:3px 12px;font-weight:700;font-size:.9rem}
.pill.p{background:rgba(63,185,111,.15);color:var(--ok)}.pill.f{background:rgba(224,86,86,.15);color:var(--ko)}
.qnav{display:flex;gap:8px;justify-content:space-between;margin-top:14px}
label.rad{display:block;padding:9px 12px;border:1px solid var(--bord);border-radius:9px;margin:7px 0;cursor:pointer}
label.rad:has(input:checked){border-color:var(--acc);background:rgba(79,156,249,.08)}
.rev{border:1px solid var(--bord);border-radius:10px;margin:8px 0;padding:0;overflow:hidden}
.rev summary{cursor:pointer;padding:11px 14px;background:var(--card2);list-style:none}
.rev summary::marker,.rev summary::-webkit-details-marker{display:none}
.rev[open] summary{border-bottom:1px solid var(--bord)}
.dim{opacity:.65}
</style></head><body>
<div id="app"></div>
<script id="exam-data" type="application/json">__EXAM_DATA__</script>
<script>
"use strict";
const EXAM = JSON.parse(document.getElementById('exam-data').textContent);
const POIDS = __POIDS__;
const LS_KEY = 'pecb-qcm::' + EXAM.titre;
const esc = s => { const d = document.createElement('div'); d.textContent = s == null ? '' : String(s); return d.innerHTML; };
let S = null;

function state(blocIdx, mode, order){ return {blocIdx, mode, order, cur:0, answers:{}, locked:{}, startTs:Date.now(), done:false}; }
function qById(id){ return EXAM.questions.find(q => q.id === id); }

function resume(){
  try { const raw = localStorage.getItem(LS_KEY); if(!raw) return null;
    const st = JSON.parse(raw); if(!st || !st.order || !st.answers) return null; return st;
  } catch(e){ return null; }
}
function persist(){ try { localStorage.setItem(LS_KEY, JSON.stringify(S)); } catch(e){} }
function clearPersist(){ try { localStorage.removeItem(LS_KEY); } catch(e){} }

function home(){
  S = null;
  const prev = resume();
  let prevHtml = '';
  if(prev){ prevHtml = `<div class="card"><b>Session précédente trouvée</b> <span class="muted small">(${prev.answers ? Object.keys(prev.answers).length : 0}/${prev.order.length} répondu${prev.mode==='exam'?', mode examen':''})</span><br><button class="btn sec" style="margin-top:8px" onclick="restore()">Reprendre</button></div>`; }
  const blocs = (EXAM.blocs && EXAM.blocs.length ? EXAM.blocs : [{nom:'Toutes les questions', ids:[1, EXAM.questions[EXAM.questions.length-1].id], duree_minutes:null}])
    .map((b,i)=>{
      const n = b.ids[1]-b.ids[0]+1;
      return `<label class="rad"><input type="radio" name="bloc" value="${i}" ${i===0?'checked':''}> <b>${esc(b.nom)}</b> <span class="muted small">— Q${b.ids[0]}–Q${b.ids[1]} (${n} Q${b.duree_minutes?`, ${b.duree_minutes} min`:''})</span></label>`;
    }).join('');
  app.innerHTML = `
  <h1>${esc(EXAM.titre)}</h1>
  <p class="muted small" style="margin-bottom:12px">${esc(EXAM.origine||'')} · Seuil de réussite : ${EXAM.seuil_reussite_pct}% · Format PECB : 3 options, 1 bonne réponse</p>
  ${prevHtml}
  <div class="card">
    <h2>1 · Choisis ton bloc</h2>${blocs}
    <h2>2 · Choisis ton mode</h2>
    <label class="rad"><input type="radio" name="mode" value="train" checked> <b>Entraînement</b> <span class="muted small">— correction immédiate après chaque réponse (avec chemin &lt;30 s)</span></label>
    <label class="rad"><input type="radio" name="mode" value="exam"> <b>Examen</b> <span class="muted small">— timer, navigation, correction au rendu final</span></label>
    <div style="margin-top:14px"><button class="btn" onclick="start()">Commencer →</button></div>
  </div>
  <p class="muted small">⚠ Entraînement ≠ blanc diagnostique : le blanc #1 officiel (Q1-Q40, 90 min, sans assistance) se passe sur papier ou en mode EXAMEN.</p>`;
}

function restore(){ S = resume(); if(!S){ home(); return; } bindTimer(); render(); }

function start(){
  const blocIdx = parseInt(document.querySelector('input[name=bloc]:checked').value, 10);
  const mode = document.querySelector('input[name=mode]:checked').value;
  const b = EXAM.blocs[blocIdx];
  const ids = []; for(let i=b.ids[0]; i<=b.ids[1]; i++) ids.push(i);
  S = state(blocIdx, mode, ids);
  bindTimer(); persist(); render();
}

function bindTimer(){
  if(S.timer) clearInterval(S.timer);
  const b = EXAM.blocs[S.blocIdx] || {};
  const total = (b.duree_minutes || 0) * 60;
  if(!total){ S.remaining = null; return; }
  S.remaining = total - Math.floor((Date.now() - S.startTs)/1000);
  S.timer = setInterval(tick, 1000);
  function tick(){
    if(S.done){ clearInterval(S.timer); return; }
    S.remaining--;
    const t = document.getElementById('timer'); if(!t) return;
    t.textContent = fmt(S.remaining); t.className = S.remaining < 300 ? 'low' : '';
    if(S.remaining <= 0){ clearInterval(S.timer); if(S.mode==='exam'){ finish(); } }
  }
}
function fmt(s){ if(s==null) return ''; s=Math.max(0,s); return Math.floor(s/60)+':'+String(s%60).padStart(2,'0'); }

function render(){
  const q = qById(S.order[S.cur]);
  const answered = Object.keys(S.answers).length;
  const last = S.cur === S.order.length-1;
  let opts = 'ABC'.split('').map(L=>{
    let cls='opt', dis='';
    if(S.mode==='train' && S.locked[q.id]){
      dis='disabled';
      if(L===q.bonne) cls+=' ok';
      else if(S.answers[q.id]===L) cls+=' ko';
      else cls+=' dim';
    } else if(S.answers[q.id]===L) cls+=' sel';
    return `<button class="${cls}" ${dis} onclick="pick('${L}')"><b>${L}.</b> ${esc(q.options[L])}</button>`;
  }).join('');
  let fb = '';
  if(S.mode==='train' && S.locked[q.id]){
    const good = S.answers[q.id]===q.bonne;
    const fausses = q.fausses ? Object.entries(q.fausses).map(([L,t])=>`<li><b>${L}</b> — ${esc(t)}</li>`).join('') : '';
    const chem = (q.chemin_30s&&q.chemin_30s.length) ? `<div class="chem"><b>⏱ Retrouver en &lt;30 s</b><ol>${q.chemin_30s.map(s=>`<li>${esc(s)}</li>`).join('')}</ol></div>` : '';
    fb = `<div class="fb"><span class="${good?'ok':'ko'}">${good?'✔ Correct':'✘ Incorrect — la bonne réponse était '+q.bonne}</span>
      <p style="margin-top:8px">${esc(q.pourquoi||'')}</p>
      ${fausses?`<p class="muted small" style="margin-top:8px"><b>Pourquoi les autres sont fausses :</b></p><ul class="small" style="margin:4px 0 0 20px">${fausses}</ul>`:''}
      ${chem}<div class="src">📚 Source : ${esc(q.source||'—')}</div></div>`;
  }
  app.innerHTML = `
  <div class="topbar">
    <div><span class="chip d">${esc(q.domaine)}</span><span class="chip">${esc(q.niveau)}</span></div>
    <div class="muted">Q${S.cur+1} / ${S.order.length} · ${answered} répondue${answered>1?'s':''}</div>
    ${S.remaining!=null?`<div id="timer" class="${S.remaining<300?'low':''}">${fmt(S.remaining)}</div>`:''}
  </div>
  <div class="card">
    <p style="white-space:pre-wrap">${esc(q.enonce)}</p>
    <div style="margin-top:10px">${opts}</div>
    ${fb}
    <div class="qnav">
      <button class="btn sec" ${S.cur===0?'disabled':''} onclick="nav(-1)">← Précédent</button>
      ${S.mode==='exam'&&last
        ? `<button class="btn" onclick="finish()">Terminer et corriger ✓</button>`
        : `<button class="btn" ${last?'disabled':''} onclick="nav(1)">Suivant →</button>`}
    </div>
    ${S.mode==='exam'&&!last?`<p class="muted small" style="margin-top:10px;text-align:center"><a href="#" onclick="finish();return false" class="muted">Terminer maintenant</a></p>`:''}
  </div>`;
  persist();
}

function pick(L){
  const q = qById(S.order[S.cur]);
  if(S.mode==='train' && S.locked[q.id]) return;
  S.answers[q.id] = L;
  if(S.mode==='train'){ S.locked[q.id] = true; }
  persist(); render();
}
function nav(d){ S.cur = Math.min(S.order.length-1, Math.max(0, S.cur+d)); render(); }

function finish(){
  S.done = true; if(S.timer) clearInterval(S.timer); persist();
  const ids = S.order;
  const correct = ids.filter(id => S.answers[id]===qById(id).bonne);
  const pct = ids.length ? Math.round(100*correct.length/ids.length) : 0;
  const pass = pct >= EXAM.seuil_reussite_pct;
  const doms = {};
  ids.forEach(id=>{ const q=qById(id); (doms[q.domaine]=doms[q.domaine]||[]).push(id); });
  const domRows = Object.keys(POIDS).filter(d=>doms[d]).map(d=>{
    const list = doms[d], c = list.filter(id=>S.answers[id]===qById(id).bonne).length;
    const p = Math.round(100*c/list.length);
    return `<tr><td><b>${d}</b></td><td>${c}/${list.length}</td><td>${p}%${p>=EXAM.seuil_reussite_pct?'':' <span class="ko">⚠</span>'}</td><td class="muted small">poids officiel ${POIDS[d]}%</td></tr>`;
  }).join('');
  const nivs = {};
  ids.forEach(id=>{ const q=qById(id); (nivs[q.niveau]=nivs[q.niveau]||[]).push(id); });
  const nivRows = Object.keys(nivs).map(n=>{
    const list=nivs[n], c=list.filter(id=>S.answers[id]===qById(id).bonne).length;
    return `<tr><td>${esc(n)}</td><td>${c}/${list.length}</td><td>${Math.round(100*c/list.length)}%</td></tr>`;
  }).join('');
  const skipped = ids.filter(id=>!S.answers[id]).length;
  const wrong = ids.filter(id=>S.answers[id] && S.answers[id]!==qById(id).bonne);
  const revList = ids.map(id=>{
    const q=qById(id); const a=S.answers[id]; const good=a===q.bonne;
    const badge = !a ? '<span class="chip">non répondue</span>' : (good?'<span class="pill p">✔</span>':'<span class="pill f">✘</span>');
    const fausses = q.fausses ? Object.entries(q.fausses).map(([L,t])=>`<li><b>${L}</b> — ${esc(t)}</li>`).join('') : '';
    const chem = (q.chemin_30s&&q.chemin_30s.length) ? `<div class="chem"><b>⏱ Retrouver en &lt;30 s</b><ol>${q.chemin_30s.map(s=>`<li>${esc(s)}</li>`).join('')}</ol></div>` : '';
    return `<details class="rev"><summary>${badge} <b>Q${id}</b> <span class="chip d">${esc(q.domaine)}</span><span class="chip">${esc(q.niveau)}</span> ${a?`<span class="muted small">ta réponse : ${a}${good?'':' · bonne : '+q.bonne}</span>`:'<span class="muted small">bonne : '+q.bonne+'</span>'}</summary>
      <div style="padding:12px 14px"><p style="white-space:pre-wrap">${esc(q.enonce)}</p>
      <p style="margin-top:8px">A. ${esc(q.options.A)}<br>B. ${esc(q.options.B)}<br>C. ${esc(q.options.C)}</p>
      <p style="margin-top:10px" class="${good?'ok':'ko'}">${good?'✔ Correct':'✘ Bonne réponse : <b>'+q.bonne+'</b> — '+esc(q.options[q.bonne])}</p>
      <p style="margin-top:8px">${esc(q.pourquoi||'')}</p>
      ${fausses?`<ul class="small" style="margin:6px 0 0 20px">${fausses}</ul>`:''}${chem}
      <div class="src">📚 Source : ${esc(q.source||'—')}</div></div></details>`;
  }).join('');
  app.innerHTML = `
  <h1>Résultat</h1>
  <div class="card" style="text-align:center">
    <div class="score">${pct}%</div>
    <p><span class="pill ${pass?'p':'f'}">${pass?'✔ Seuil atteint (≥ '+EXAM.seuil_reussite_pct+'%)':'✘ Sous le seuil ('+EXAM.seuil_reussite_pct+'%)'}</span></p>
    <p class="muted" style="margin-top:6px">${correct.length}/${ids.length} correctes${skipped?` · ${skipped} non répondue${skipped>1?'s':''}`:''}${S.remaining!=null?` · temps restant : ${fmt(S.remaining)}`:''}</p>
    <div class="qnav" style="justify-content:center;gap:10px;margin-top:16px">
      ${wrong.length?`<button class="btn sec" onclick="retryWrong()">Revoir les ${wrong.length} ratées</button>`:''}
      <button class="btn sec" onclick="clearPersist();home()">Nouvelle session</button>
    </div>
  </div>
  <div class="card"><h2>Par domaine</h2><table><tr><th>Domaine</th><th>Score</th><th>%</th><th></th></tr>${domRows}</table></div>
  <div class="card"><h2>Par niveau</h2><table><tr><th>Niveau</th><th>Score</th><th>%</th></tr>${nivRows}</table></div>
  <h2>Correction détaillée</h2>${revList}`;
  S._wrong = wrong;
  persist();
}
function retryWrong(){
  const wrong = S._wrong || [];
  if(!wrong.length) return;
  const mode = S.mode;
  S = state(S.blocIdx, mode, wrong); S._wrong = null;
  bindTimer(); persist(); render();
}
const app = document.getElementById('app');
home();
</script></body></html>"""

def build(json_path, out_path):
    data = json.loads(Path(json_path).read_text(encoding="utf-8"))
    validate(data)
    payload = json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")
    html = (TEMPLATE
            .replace("__TITRE__", data["titre"])
            .replace("__POIDS__", json.dumps(POIDS_OFFICIELS))
            .replace("__EXAM_DATA__", payload))
    Path(out_path).write_text(html, encoding="utf-8")
    print(f"OK : {out_path} ({len(data['questions'])} questions, {len(html)//1024} Ko)")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("json"); ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()
    build(a.json, a.out)
