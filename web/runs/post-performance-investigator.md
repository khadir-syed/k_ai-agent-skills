Date: 2026-09-26
Tool: Codex CLI 0.154.0
Model: gpt-5.6-sol
Example: skills/socialmedia/post-performance-investigator/examples/underperforming-launch-post.md

## Investigation report

**Status:** Partially explained  
**Confidence:** Moderate

### Symptom

- **Reported:** Reach was 400.
- **Reported:** Typical reach is approximately 3,000, based on the marketing lead’s average of the previous 10 posts.
- This represents an approximately **87% reach shortfall** against that reported baseline.

### Leading explanations

1. **The baseline is not an apples-to-apples comparison — strongly supported.**

   - **Observed:** Three of the previous 10 posts received paid promotion; this post did not.
   - **Observed:** The previous posts typically used short video or carousel formats, whereas this was a single static image.
   - **Inferred:** The 3,000 average combines posts with materially different distribution conditions. It may therefore overstate the reach expected from an unpromoted static post.
   - **Unknown:** The organic-only average and the typical reach of comparable static-image posts.

2. **The static format likely reduced organic distribution — supported, but not isolated.**

   - **Observed:** This post used one static image; the comparison posts generally used video or carousel formats.
   - **Inferred:** The format change is a plausible contributor because it is systematic and coincides with the reach decline.
   - **Unknown:** Whether initial engagement, shares, saves, or non-follower distribution were lower. Without those metrics, format cannot be established as the sole cause.

3. **Minimal caption and absent hashtags may have contributed — plausible but untested.**

   - **Observed:** The caption contained two lines and no hashtags.
   - **Observed:** Previous posts averaged four to six hashtags.
   - **Unknown:** Whether those hashtags historically produced meaningful discovery, and whether the caption supplied a strong hook or interaction prompt.
   - **Status:** Untested; the available evidence cannot separate this effect from format and promotion differences.

### Other hypotheses

| Hypothesis | Current status | Assessment |
|---|---|---|
| Tuesday at 9am was a weak publishing time | Untested | No account-level time-of-day comparison was supplied. |
| Instagram’s algorithm changed | Untested | No evidence of a broader decline across comparable posts or accounts was supplied. |
| Competing content suppressed attention | Untested | No information about external activity that morning is available. |
| The feature itself lacked audience appeal | Untested | Reach alone measures distribution, not whether people who saw the post cared about the feature. Engagement and click data would be needed. |
| Paid promotion alone explains the gap | Weakened | Only three of the 10 baseline posts were promoted, so promotion may inflate the average but cannot automatically explain the entire shortfall. |

### Most defensible diagnosis

The post’s apparent underperformance is best explained by a **confounded baseline combined with less distribution-friendly conditions**: it was an unpromoted static post being compared with a set dominated by videos/carousels and partially inflated by paid promotion.

The evidence does **not** establish whether static format, lack of promotion, hashtags, caption quality, or timing was the dominant causal factor. An algorithm change and competing content remain unsupported possibilities rather than demonstrated explanations.

### Validation limits

This is one post, so it cannot establish a trend. Reach also cannot distinguish limited platform distribution from weak audience response after exposure.

**Recommended next check — not yet performed:** Recalculate the baseline using only unpromoted posts, segmented by format, then compare follower versus non-follower reach and early engagement for this post against those genuinely comparable posts.