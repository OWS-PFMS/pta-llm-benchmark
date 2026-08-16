# PTA Coding Rules — v0

Rules used by Claude as the PTA coder for the WASH KII corpus. Derived from Kim & Andersen (2012) and the application in Walters et al. (2022) and Valcourt et al. (2024). This is the prompt artifact for stage 2 of the pipeline (raw transcript → coded causal statements).

## Inputs

- A single transcript file (e.g. `WASH KII Transcripts (txt files)/WASH KII (001).txt`).
- Transcript structure: numbered question prompts (`1.`, `2.`, `3.`, sometimes followed by `Interviewer:` follow-ups) with prose answers in between. UTF-8 BOM at the start of the file is stripped before reading.

## Output

JSONL, one causal statement per line. Schema:

```json
{
  "transcript_id": "WASH KII (001)",
  "stmt_id": 1,
  "cause": "<short factor name, verbatim where possible>",
  "effect": "<short factor name, verbatim where possible>",
  "polarity": "+" | "-",
  "label": "challenge" | "solution",
  "question": "Q1" | "Q2" | "Q3" | "Q1-followup" | "Q2-followup" | ...,
  "excerpt": "<the exact source quote, ≤300 chars, ellipses allowed>"
}
```

## Coding rules

1. **One argument per record.** A statement asserts ONE cause → effect pair. If a sentence chains three factors (A → B → C), emit two records: A → B and B → C.
2. **Factor names stay close to verbatim.** Use the speaker's terminology for cause and effect. Light cleanup is OK (drop articles, pluralize consistently, fix obvious typos). Do **not** pre-aggregate into cross-case categories — that happens in stage 4.
3. **Each factor is a single noun phrase.** Not a clause. "Lack of personnel" → factor name is `professional personnel` or `staffing`, not `there is a lack of personnel`. Polarity carries the directionality, not the factor name.
4. **Polarity convention.**
   - `+` = increase in cause → increase in effect (or decrease → decrease).
   - `−` = increase in cause → decrease in effect (or decrease → increase).
   - When a speaker says "low X causes high Y", the underlying relationship is X (−) → Y. Code the underlying relationship, not the surface phrasing.
5. **Challenge vs solution label.**
   - Default to the question type the answer is responding to: Q1-style ("what are the problems") → `challenge`; Q2/Q3-style ("what solutions / what's most important") → `solution`.
   - Override per-statement when the speaker explicitly switches register inside an answer (e.g., describing a new problem mid-solution-answer). When in doubt, follow the speaker's framing, not the question's.
6. **Dedupe within a transcript.** A given (cause, effect, label) triple is coded **once per transcript** even if the speaker mentions it multiple times. The same (cause, effect) pair can appear under both `challenge` and `solution` labels — those are separate maps in Walters 2022.
7. **Implicit factors are allowed but flagged.** When a stock or factor is implicit (e.g. "inventory" in Kim & Andersen's FOMC example), code it but keep the factor name simple. If the link is too speculative to defend from the excerpt, skip it.
8. **Every record carries an excerpt.** Without the source quote, traceability — Kim & Andersen's core contribution — is lost. The excerpt must support the coded link on its own; do not rely on context the reader does not have.
9. **Question-block tagging.** Track which numbered question or follow-up the answer is responding to (`Q1`, `Q2`, `Q3`, `Q1-followup`, etc.). This is what determines the default `label` in rule 5 and is needed downstream for per-question diagnostics.
10. **No factor merging across speakers/transcripts.** Stage 3 handles per-corpus dedupe; stage 4 handles affinity grouping. Stage 2 must preserve the speaker's voice.

## Common pitfalls to avoid

- **Don't code descriptive state as a causal claim.** "There are old pipelines" alone is not a causal statement; "old pipelines cause service breakdowns" is.
- **Don't bundle multiple effects into one record.** "Awareness leads to better hygiene and lower disease" → two records.
- **Don't normalize factor names too aggressively.** Two different speakers' phrasings (`mobilization programs` vs `community education`) should both survive into stage 2 — affinity grouping in stage 4 handles this.
- **Don't drop factors just because they look minor.** Stage 5 weights connections by reference count; rare factors falling out is fine, but it should fall out from aggregation, not from the coder pre-filtering.

## Versioning

Bump the `v0` in the title when rules change. Coded outputs reference the rule version they were produced under in a top-of-file comment so re-codings can be diffed.
