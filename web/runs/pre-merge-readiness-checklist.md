Date: 2026-09-26
Tool: Codex CLI 0.154.0
Model: gpt-5.6-sol
Example: skills/software/pre-merge-readiness-checklist/examples/missing-tests-example.md

## Change scope

- **Range evaluated:** Current branch against `main`
- **Source:** User-specified branch diff; local `main` ref was unavailable, so evidence relies on the supplied diff observations.

| # | Check | Status | Evidence |
|---|---|---|---|
| 1 | Tests present or updated | **Fail** | Both changed files are source files, but no matching `src/**/__tests__/*.test.js` files changed. |
| 2 | Docs touched for user-facing change | **Could not determine** | `README.md` documents the Export menu and was not touched, but the patch contents were unavailable to establish whether behavior changed. |
| 3 | No obvious leftover debug code | **Pass** | Supplied diff scan found no `console.log`, `debugger`, or `pdb` statements. |
| 4 | Commit messages follow a recognisable convention | **Fail** | History uses Conventional Commits; `wip`, `more changes`, and `fix stuff` do not follow it. |
| 5 | No secrets or credentials in the diff | **Pass** | Supplied diff scan found no secret-like patterns. |
| 6 | No sensitive files newly tracked | **Pass** | No new `.env`, `.pem`, or `credentials.json` files were added. |

## Overall readiness

**Not ready.** Tests are missing for both changed source files, and the commit messages violate the repository convention. Documentation readiness remains unresolved until the actual patch is reviewed for user-facing behavior.

## Not performed

Test execution, implementation review, linting, type-checking, performance testing, accessibility review, and independent inspection of the unavailable `main...HEAD` diff.