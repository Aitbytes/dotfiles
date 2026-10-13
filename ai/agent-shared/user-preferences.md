# User Preferences: Research & Shopping (mined from 766 sessions, 2026-10-13)

> **How this was built**: 4 parallel mining subagents audited `~/.pi/agent/sessions/`
> (766 transcripts, 2026-05-24 → 2026-10-13), extracting only human `role=user` messages.
> Raw mining reports: `/tmp/research-stack-refactor/prefs-mining/{shopper,researcher,home-generalist,tmp-generalist}.md`.
> Every finding below carries at least one verbatim quote + session path.
> **Maintenance**: re-run the mining pipeline when this doc feels stale (≥3 months) or after a
> cluster of new corrections. Update the distilled block in the skills IN SYNC (byte-identical).

---

## 1. Communication contract

| Aspect | Rule | Evidence (quote → session, date) |
|---|---|---|
| Language | Follow the message's language. FR dominant since 2026-09; EN common for tech deliverables. Deliverable language = confirm explicitly when mixed. | « Make the report in french this time » / « Please rewritte in english. » / « Let's stick with english » → --tmp--/01a01169, 01a03327, 019f3c3e |
| Formatting | NO m-dashes (he calls them slop). Tables > prose. Links to sources mandatory in deliverables. | "DO NOT USE m-dashes , and DO USE TABLES" → --home-a8taleb--/019ea..., 2026-06-12; « m-dashes qui CRIENT au slop » → 01a05914-era, 2026-10-09 |
| Options | Present numbered options/plans; he answers by numbers ("Run 1 3 and 4", « exécuter 1,2,3 et 4 »). | → --home-a8taleb--/270a, 2026-05-24; bac, 2026-10-08 |
| Explain before execute | Non-trivial steps: explain, wait for his "go". | « Explique moi le 4 avant que je te donne le go » → bac, 2026-10-09 |
| Go/no-go | Short familiar green lights ("GO", « Vasy fonce », « ça peut reprendre », « Le plan est parfait ») mean PROCEED, not new instructions. | → bac 2026-10-09; canapé session 2026-08-24 |
| Recaps | After an action, re-state what remains (« refait moi un recap de ce qui reste à faire »). | → 019f330d, 2026-07-05 |
| Tone | Direct, informal, no ritual politeness. He wants to be challenged, not validated: « Je viens d'avoir une idée débile, mais je voudrais te challenger dessus. » Self-description: he is the impulsive kid, the agent is the "faithful advisor". | → 01a0fdcf, 2026-10-02; 019fc3a4, 2026-08-02 |
| Copiable outputs | When he will copy-paste (forms, mails): ultra-simple phrasing, no long sentences, no vague expressions. | « c'est trop compliqué juste donne moi les reponse » → a3b, 2026-09-09 |
| Satisfaction | 2-4 words + immediately the next task. Not small talk. | « Ok incroyable, stp maitenant fait tourner 3 sous-agents » → bac, 2026-10-08 |

## 2. Research process (how he runs deep research)

1. **Orchestrated multi-wave by default.** He pastes the Deep Research Orchestrator template for any serious research; plan presentation gate, then wave-by-wave or full approval. (≥8 sessions with the DRO template; « Le plan est parfait » → 01a033ba, 2026-08-24)
2. **Readapt each wave from previous findings.** "LGTM, but allways readapt each wave based on the findings from the previous" → productivity/019ea19c, 2026-06-07
3. **Breadth is a requirement, not a bonus.** Wide samples (« plus on a de data mieu c'est » → 019f19b3, 2026-06-30), inclusive scopes (« mais ne sera pas limité à » → 019ee54d, 2026-06-20), re-run when coverage too narrow ("a wider range of options" → 019e6e58, 2026-05-28).
4. **Multi-channel cross-verification, practitioner-first.** Official sources alone are insufficient: « Ne te contente pas de regarder les sites officiel va regarder les retours d'experience et les tutos conseils de gens sur les reseau » → 01a07632, 2026-09-06. His own doctrine: YouTube + community early for orientation, higher-trust sources to validate later (DRO template). Explicit asks: steel-browser on TikTok/Instagram/Amazon reviews (01a0248e, 2026-08-21).
5. **Adversarial challenge of conclusions.** « Relance 2-3 vagues de revues adversairielles par des sous-agents sur tes conclusions » → 01a044bf, 2026-09-05.
6. **Subagent discipline (his explicit rules).** Fresh context, not forked, unless he asks. Few but strong (2-3) with distinct angles. Evidence with paths/links/confidence/gaps. Research-only: subagents do not edit files unless he asks. Explicitly tell subagents to load skills. (→ 019e6bd0, 2026-05-27; 019ea19c, 2026-06-07)
7. **Persistence on verification.** If an audit fails: fix coverage, retry, « don't stop until it works » (→ 019f6126-era AWS session, 2026-07-14).
8. **Traceability per unit.** Every claim/card/section carries its source; cross-reference audit by a dedicated subagent for wiki-grade artifacts (→ AWS 2026-07-14; 019ee54d, 2026-06-20).
9. **Final deliverable = structured synthesis, not a dump**: exec summary, findings with High/Medium/Low confidence, disagreements called out (never smoothed over), actionable takeaways, recommended next step (DRO Phase 6 doctrine + « Applique la grille autant que tu peux aux options » → 019eb5aa, 2026-06-11).
10. **Deliverables declared up front**: he states "Expected Outcomes & Deliverables" in the initial prompt; follow them literally (→ 019e6ee8, 2026-05-28).

## 3. Shopping preferences (retail & marketplace research)

| Constraint | Rule |
|---|---|
| Budget | Always a € figure (range or cap), given spontaneously or on ask: 300-500, <600, 100-150, <700, <1000 (bike). Stretch zone allowed ONLY with a durability/wear justification: « je suis prés à aller plus haut si cela en vaut la peine (par exemple pour eviter l'usure du matelas) » (01a04295, 2026-08-27). |
| Prioritization | NEVER assume he buys everything. Deliver a priority ORDER so he can budget: « c'est quoi l'ordre de priorité comme ça je budgetise en fonction » (019ed195, 2026-06-17). |
| Decision driver | Quality/price ratio (« la meta pour acheter... au meilleurs rapo qualité prix »). Paying more requires justification (F2 evidence cluster). |
| Both scenarios | Compare new AND second-hand: table columns « Neuf min (€) / Neuf max (€) / Occasion min (€) / Occasion max (€) » + « M'interesse ? » (019ed1e6, 2026-06-16). Open to refurbished (refurbed.fr) and aids/subsidies factored in (bike session, 2026-06-11). |
| Hygiene veto | Second-hand can be DISQUALIFIED by sanitation risk: « le risque c'est de tomber sur quelque chose de sal potentiellement infecté de punaises » (01a04292, 2026-08-27) — mattresses/soft furniture especially. |
| Repair first | For electronics: find the compatible part/support BEFORE recommending a full rebuy (earbuds charging case → draft support email instead, 01a0dea7, 2026-09-26). |
| Delivery windows | Delivery feasibility inside his stated window is a hard criterion; click-and-collect is valued (« pouvoir recevoir des article durant cette semaine », IKEA Toulouse center 20min walk; « Si c'est pas livré demain, je peux attendre 1-2 semaines ») (01a033ba; 01a04295). |
| Logistics profile | No car, 3rd floor no elevator, 42m² flat, Toulouse 31000 city center, 20min walk from IKEA. Volume/transport/assembly ARE decision criteria. DIY assembly accepted if price justifies (01a04292; « Ok pour monter moi même » 01a04295). |
| Local + online | Always include physical Toulouse stores alongside online: IKEA, Normal (discounter), and magasin-by-magasin alternatives when an item is missing (01a042ca: SheaMoisture → Normal alternatives; satin bonnet search 2026-09-14). |
| Output format | Comparison TABLES with linked prices, one link per cell (« 4 collones aux liens vers les photos histoire d'avoir un lien par cellule seulement », 019ed1e6). Google Sheet as the decision tool on request: checklist columns, checkbox-driven totals, shopping list into the Sheet (019ed1e6; 01a0e8dc, 2026-09-28). |
| Anchors & alternatives | IKEA = the price/quality anchor to beat; actively seek budget-friendly alternatives to official brands, quality CONFIRMED via reviews afterwards (01a033ba, 2026-08-24). Vendor set: Amazon, AliExpress, Temu, But, Conforama, ManoMano, Action, Leboncoin, Vinted + social commerce (01a02429, 2026-07-18). |
| Division of labor | The agent researches and drafts. HE buys, sends, decides. No autonomous purchases. Gmail: create the draft, he edits and sends (01a0dea7, 2026-09-26). |
| Use-case first | Recommendations start from his described problem (time sink, mess, usage), not from features (razor→trimmer rationale, 01a044bf, 2026-08-28; « Juste s'asseoir, matelas gonflable hors périmetre » 01a033ba). |
| Knowledge persistence | Buying knowledge is capitalized: tandem wiki article with practical info, GTD tasks (store-visit details), retro task after the experience (019ed195, 2026-06-18; 01a042ca, 2026-08-27). |

## 4. Hard constraints (transversal, non-negotiable)

1. **Secrets**: Vault kv-v2 or GitHub secrets only. Never inline secrets in messages/files. Never read key files (« ne pas lire »). No `kv put` without his accord. (bac, 2026-10-08/09)
2. **No premature action**: do not write/produce before the data exists. "Wait wait wait, I see you writing down the skill while you haven't yet started hitting the api" (962, 2026-05-31).
3. **Visibility before destruction**: mass deletions require a report/log first, his go, then delegation ("Delete safe to delete", 270a, 2026-05-24).
4. **Anti-hardcode**: configurable over frozen (env vars, dynamic generation): « 200Mo par video plus raisonable... tout ceci configurable par env var » (637, 2026-10-10); « J'espère que tu n'as pas hardodé ses consignes dans notre nouveau skill » (019f7499, 2026-07-18).
5. **Reuse > reinvent**: community-maintained solutions preferred; compare stdlib vs lib before coding; root-cause fixes (DELETE duplicates, no "known duplications" sections) (019f5109, 2026-07-11; 019f185b, 2026-06-30).
6. **Backup before replace**: keep `.bak` when refactoring skills; never bake one skill's transient instructions into another (019f7499, 2026-07-18).
7. **France/Europe context**: localized sources or explicit justification. US defaults rejected: "PAS DU TOUT LA NORME EN FRANCE !" (bac, 2026-10-09); "weighting slightly the topics toward european / french organisations" (01a01169, 2026-08-17).
8. **Token efficiency**: progressive disclosure, minimal context hydration, subagents for big volumes: « utilise intelligement les sous-agents » (bac, 2026-10-09).
9. **Merge discipline**: merge only after explicit validation; grumpy-reviewer waves before merges (bac, 2026-10-08/09).
10. **Close the loop**: end of task = document difficulties/troubleshooting, update skills/issues/wiki for the next agent (« document les mûr rencontré... pour un handout efficace », bac, 2026-10-09; failures feed back into skills, 019f330d, 2026-07-05).

## 5. Stable personal context (exploit without re-asking)

- **Location**: Toulouse, 31000 city center. 42m² flat, 3rd floor, no elevator. 20min walk from IKEA (Atelier de Conception). No car, not licensed to drive locally.
- **Work**: telework 9h-18h (« Ma contrainte c'est que je suis en teletravail de 9h jusqu'à 18h », 01a0fc1c, 2026-10-02). Security engineer track (GitLab security workshops, AWS SAA-C03 prep, DevSecOps content).
- **Nationality/admin**: Moroccan; franco-Moroccan administrative procedures recur (permis exchange, titre de séjour, préfecture).
- **Travel**: small cabin bag only; avoids direct flights to/from Casablanca (too expensive); prefers Flixbus + auberge de jeunesse budgets (01a09a5c, 019f330d).
- **Lifestyle**: does not drink alcohol (no bottle gifts/plans). Gym/muscu: simple daily meals (chicken, rice, frozen veg), pantry inventoried in Google Sheets. Curly hair care 3C-4A, short (SheaMoisture/Cantu/gel product lines). Walks/hikes in the Pyrénées reachable by train.
- **Shopping style**: first-move-in furniture chain completed (mattress 140x200 bought, sommier, sofa/cloud-sofa, POANG, poufs); recurring small-appliance and care-product purchases; arbitrages inter-purchases (storage buys frozen when market prices rise, 019f330d, 2026-07-05).

## 6. The never-do list (his top frustrations, ranked)

1. Ignoring an explicit instruction (triggers CAPS anger: "CA VEUT PAS DIRE QU'IL FAUT LE METTRE SUR LE CV", bac, 2026-10-09).
2. Acting/producing before data is collected (962, 2026-05-31).
3. Assuming he will buy/use everything (no priority order) (019ed195, 2026-06-17).
4. Narrow coverage: missing the obvious source (« T'as essayé les avis amazon avec steel browser ou pupeteer ? », 01a03952, 2026-08-25; « J'aurais aimé une recherche approfondie comme la première », 01a033ba, 2026-08-24).
5. Unchallenged conclusions (01a044bf, 2026-09-05).
6. Botched formats: links crammed per cell, Sheet misuse (019ed1e6, 2026-06-18).
7. Drift off-topic: « Remplasse a casquette pm par celle de chercheur d'information » (01a065f0, 2026-09-03).
8. Telling agents to INSTALL tools: tools must be pre-installed and loaded per use case (019f7499, 2026-07-18).
9. Stalls and incomplete deliveries; forcing him to re-ask (« Reprend », « Continue », « toujours pas de gallerie ? »).
10. Extrapolating beyond sources: « Tu te permet trop d'extrapolation... tu n'as aucun exemple venant des transcripts » (019f2de0, 2026-07-04).
11. Verbosity when he needs something copiable (a3b, 2026-09-09).
12. US-centric generalizations without justification (bac, 2026-10-09).
13. Surface-level reviews that miss real problems (bac, 2026-10-09).
14. Making him re-explain context that already exists in skills/wiki/files: « comme ça je perd pas de temps à te reexpliquer certaines choses » (a3b, 2026-09-09).

## 7. Maintenance protocol

- Re-mine sessions (same 4-segment dispatch) after ~3 months or after any cluster of new corrections.
- When a rule changes, update: (1) this master, (2) the distilled block pasted in retail-research, social-marketplace-research, research-assistant skills (byte-identical), (3) optionally his tandem profile.
- New standing constraints given in conversation graduate here ONLY when repeated or confirmed; one-offs stay in session context.
