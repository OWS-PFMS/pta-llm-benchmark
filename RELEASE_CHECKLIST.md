# Release checklist — gates before flipping this repository public

This repo is assembled *as if* everything can be released, so that going
public is a one-switch action once each gate below is cleared. Track
decisions inline.

## 1. Human-subjects / consent gates (blocking)

- [ ] **Jeff confirms** what the original Walters et al. (2022) consent and
      IRB terms permit for public archiving of:
  - [ ] `transcripts/` — the raw interview transcripts (identifying details,
        if any, and consent scope for verbatim publication).
  - [ ] `coded_statements/` — carries verbatim transcript **excerpts** in
        every record; releasable only under the same terms as transcripts.
  - [ ] `benchmark/` — N&J's aggregated edgelist (co-authors' own coding;
        expected unproblematic, confirm).
- [ ] If transcripts/excerpts cannot be public: delete those directories
      from this repo (and purge git history — see §4), switch the manuscript
      Data Availability statement to "available on reasonable request," and
      keep everything else.

## 2. Content gates

- [ ] Author list / paper title in `README.md` match the submitted manuscript.
- [ ] `[URL]` placeholders in the manuscript blurbs point at this repo.
- [ ] Figures/tables here match the submitted versions (regenerate after any
      manuscript revision).
- [ ] Repo name is what the team wants cited (renaming after submission
      breaks the printed URL).

## 3. Administrative gates

- [ ] Transfer to (or fork under) the org/account the team wants on record,
      if not `cfb3`.
- [ ] License check: MIT for code confirmed by all three authors; add a data
      license statement (e.g., CC BY 4.0) for the releasable data files.
- [ ] Mint an archival DOI (Zenodo–GitHub integration) at acceptance and add
      it to `README.md` + the manuscript.

## 4. If sensitive content must be removed before release

Deleting files in a later commit does **not** remove them from git history.
Either rebuild the repo fresh from a cleaned manifest (safest — rerun
`assemble_release_repo.py` from the working repo with the sensitive entries
removed, into a new repo), or use `git filter-repo` and force-push before
the repo is ever made public.
