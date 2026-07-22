# Repository Data and Privacy Policy

## Purpose

This repository contains software, synthetic fixtures, and non-sensitive project documentation only. Source application materials, private medical inputs, and identifying information must remain local and untracked.

## Mandatory rules

- The entire `wiki/` directory is local source material and must never be committed.
- Real clinical records, de-identified clinical records, licensed textbooks, guidelines, evaluation exports, and runtime case packages must not be committed.
- Tracked examples must be synthetic and must not be adapted by copying identifiable source text.
- Personal names, contact details, identity numbers, signatures, and other identifying attributes from local source documents must not appear in tracked files.
- Secrets and API keys must only be stored in ignored local configuration.
- Office and PDF artifacts are ignored by default because they are difficult to inspect reliably before commit.

## Enforcement

The repository uses `.githooks/pre-commit`, which invokes `scripts/check-sensitive-content.ps1`. The check:

1. rejects every staged path under `wiki/`;
2. scans staged text against an ignored, workstation-local sensitive-term denylist;
3. rejects common email, mobile-number, and identity-number patterns.

The local denylist is stored at `.local/sensitive_terms.txt`. It must contain the relevant names and identifying terms from local source materials, one term per line. The denylist itself is ignored and must never be committed.

This automated check is a guardrail, not a substitute for human review. Before every push, inspect `git diff --cached` and confirm that staged samples are fully synthetic.

## Future clones

After cloning, each developer must create `.local/sensitive_terms.txt` from approved local source material before the first commit. The hook fails closed when the denylist is missing or empty.

