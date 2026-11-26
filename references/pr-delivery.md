# PR delivery

Use the local Magpie GitHub MCP for PR writes, including `create_pull_request`, `update_pull_request`, and `add_issue_comment`. Follow the [local Magpie routing](../SKILL.md#local-magpie-routing).

In T3, link the full PR URL with `link_pull_request` immediately after creating, taking over, or pushing to a PR. Reuse the link when the tool creates it automatically.

## Record validation evidence

Use the existing [taskbook audit record](experiment-results.md#extract-and-reuse), adding missing evidence on resume. Keep the detailed results there and cite them in the PR body.

- Record the current taskbook's source SHA (the intake SHA for a local brief), the clarification SHA if applicable, the reviewed code SHA or SHAs, and the actual independent model and scope. Cite the taskbook history and user decisions used to establish which original goals remain active.
- Map each specified verification requirement and each active goal to its conclusion, source locations, and evidence. Identify the checks run in this round, the applicable evidence reused, any independent validation blocker, and unresolved findings or disputes. For a fix, retain the original result and record the independent recheck at its new code SHA. Record changes between the reviewed snapshot and the delivered head that explain why the evidence still applies.
- State whether this round's goals are complete and whether the full PR's active original goals are complete as two separate conclusions. List open original goals and any explicitly withdrawn or replaced goals with the decision source. Only supported `PASS` results count as independent verification. `FAIL`, `UNVERIFIED`, and `BLOCKED` leave the affected conclusion open. Primary-agent checks are recorded under their own source. An open PR can be delivered for user review with its outstanding validation made explicit.

## Create a PR

Verify the repository, head, and base. Open a review-ready PR unless the brief requests a draft. If the creation result is uncertain, look up the head and base before retrying.

## Update an existing PR

1. Work on the original PR. Keep its base, title, and review status unless the brief asks to change them. Read the current body and conversation comments before publishing.
2. Look for `<!-- taskbook-revision:<intake-commit-sha> -->` in the comments. If this round has no archive comment, post one to the PR conversation. Outside the fold, put the marker and a short summary of the issues and their resolution. Inside `<details>` with `<summary>上一版 PR 说明</summary>`, place the previous PR body verbatim in a fenced code block. Use a fence longer than any run of backticks in the body. Label an empty body `上一版无正文`.
3. Confirm the archive comment exists before editing the body. Re-read the current body and compare it with the saved draft and archived text.
   - If it matches the saved draft, finish.
   - If it matches the archived text, replace it with the saved draft.
   - If it differs from both, preserve the concurrent edit and resolve how to incorporate it before updating.
4. If either write returns an uncertain result, re-read the comments and body before deciding whether to retry.
