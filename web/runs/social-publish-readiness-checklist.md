Date: 2026-09-26
Tool: Codex CLI 0.154.0
Model: gpt-5.6-sol
Example: skills/socialmedia/social-publish-readiness-checklist/examples/launch-post-checklist.md

## Source

Checked the pasted caption for Twitter/X. `draft-caption.md` and the referenced image were not found in the workspace. No posting calendar was supplied.

| Check | Status | Evidence |
|---|---|---|
| Within the platform’s character limit | **Could not determine** | Caption is 110 characters, including the line break, but the applicable limit was not confirmed. |
| Hashtags are formatted and relevant | **Fail** | `# export` has invalid spacing. `#trending`, `#followus`, `#like`, and `#share` are not clearly related to the export feature. |
| Media meets platform specs | **Could not determine** | No image format, dimensions, file size, or inspectable image was supplied. |
| Alt text or captions present on media | **Fail** | The supplied `<img src="export-screenshot.png">` has no alt text. |
| Links are tracked and resolve to a real destination | **Could not determine** | `bit.ly/xyz` could not be resolved with the available check, and no campaign-tracking convention was supplied. |
| No scheduling conflict | **Could not determine** | No posting time, calendar, or blackout-window information was supplied. |

## Summary

The checklist found two failures: hashtag formatting/relevance and missing image alt text. Character-limit compliance, media compatibility, link resolution/tracking, and scheduling remain unresolved. This report is input to the post owner’s publishing decision.