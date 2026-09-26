Date: 2026-09-26
Tool: Codex CLI 0.154.0
Model: gpt-5.6-sol
Example: skills/product/feature-launch-readiness-checklist/examples/export-feature-launch.md

## Feature

- **Feature described:** CSV export of the currently filtered Reports view for Analyst-role users and above
- **Source:** User’s description, including PRD details

## Checklist

| # | Check | Status | Evidence |
|---|---|---|---|
| 1 | Rollback plan exists | **Pass** | The feature can be disabled using its feature flag. This is a viable rapid rollback mechanism, although no broader rollback procedure is documented. |
| 2 | Rollout control configured | **Fail** | The flag is enabled for 100% of eligible users, with no staged rollout planned. |
| 3 | Success metric defined | **Fail** | The PRD identifies reducing export-related support tickets from a baseline of approximately 15 per month, but provides neither a target nor a dashboard or measurement mechanism. |
| 4 | Docs or help content updated | **Fail** | This is a user-visible feature, but no documentation or help-center article has been prepared. |
| 5 | Support/customer-facing team briefed | **Fail** | The support team has received no advance notice or briefing. |
| 6 | No known blocking issues open | **Fail** | Exports fail silently above 10,000 rows. The defect remains unresolved and has not been explicitly accepted as a known limitation. |

## Overall readiness

**Blockers found.** Five checks fail. The most significant unresolved issue is the silent failure above 10,000 rows; the absence of staged rollout, measurable success criteria, documentation, and support preparation creates additional launch risk.

This is readiness input, not a go/no-go decision.

## Not performed

This checklist does not assess security, privacy, CSV injection risk, authorization enforcement, accessibility, browser compatibility, performance testing, data correctness, or legal/compliance requirements.