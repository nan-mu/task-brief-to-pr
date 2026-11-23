# PR delivery

Use T3's `pull_request_*` tools when available. Otherwise use Magpie GitHub MCP's `create_pull_request`, `pull_request_read`, `add_issue_comment`, and `update_pull_request`. If the required operation or permission is unavailable, identify the specific blocker.

In T3, link the full PR URL with `link_pull_request` immediately after creating, taking over, or pushing to a PR. Reuse the link when the tool creates it automatically.

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
