---
name: task-brief-to-pr
description: 按粘贴、文件或 Gitea 上的任务书在独立 Git worktree 实现和验收改动，再创建或更新 PR。
---

# Task brief to PR

Run this workflow when the user explicitly invokes the skill and asks you to implement a task brief. The invocation `task-brief-to-pr <gitea-owner>/<repo>:<ref>` is an implementation request with a [Gitea source](references/gitea-intake.md). Finish with a PR ready for the user to review.

An explicit invocation authorizes the workflow for the selected task, including [Magpie access to the full review evidence](references/review-prompt.md#default-review-authorization) and PR delivery. Apply any limits the user gives for that run.

## Local Magpie routing

On this machine, route Magpie calls exclusively through Codex's local `magpie` provider (`mcp__magpie__…`). Perform every Gitea read and write through its Gitea MCP tools (`mcp__magpie__gitea__…`). If a required local tool is unavailable, report the missing capability.

The local GitHub MCP uses a GitHub App installation token. Use the GitHub owner and repository from the Git remote or current PR metadata and call the needed operation directly. Skip `get_me` for this token.

For Matt Pocock's skills, the issue tracker is GitHub Issues in the implementation repository. Use the local Magpie GitHub MCP for issue operations when the task calls for them.

## 1. Read the brief and enter the worktree

When resuming an existing round, check for a [pending experiment report](references/experiment-results.md#stop-and-report) in the task worktree before resuming delivery. Then check for the commits in step 2 before retrieving the brief again.

1. Read the brief from the source the user supplies, including pasted text or a Markdown file. Resolve local paths to absolute paths and open supporting materials as needed. For ZIP and TAR archives, use Python 3 with [read-taskbook.py](scripts/read-taskbook.py) to read the root `taskbook.md`. For other archives, use an available reader to read the single regular file at that location. For an explicit Gitea source, or an existing PR with no supplied brief, follow [Gitea intake](references/gitea-intake.md). Ask for a usable source when the entry is missing, unreadable, or ambiguous.
2. Resolve the implementation repository, acceptance criteria, starting ref, and PR base from the brief and current project. Use an existing PR when the brief or task context identifies it independently of the Gitea source. Verify its number, head repository, head branch, and base, then use its head. For a revision, recover [the taskbook history for that PR](references/gitea-intake.md#recover-the-prs-taskbook-history). Otherwise use the new PR workflow. Honor an implementation branch the user names and ask when branch ownership is unclear. For a new branch, use the requested name or choose an unused one. Start independent work from the latest remote default branch, or the local default if there is no remote. Start dependent work from the ref containing the dependency and use the PR base specified by the brief.
3. Reuse the task's worktree when it exists. In T3, call `t3_worktree_status` first. For a new branch in a session that can move, use `t3_worktree_handoff` with the branch, `baseRef`, and a `continuationPrompt` containing the original brief or a readable absolute path. For a Gitea download, pass the absolute directory path and the paths and SHAs of any historical evidence already collected. Set `startFromOrigin: true` for a remote start or `false` when using local commits. End the turn with that call and resume in the new worktree. For a manual checkout, use `git worktree add -b <branch> <path> <base>` for a new branch or `git worktree add <path> <branch>` for an existing one. Run the remaining steps from the task worktree.

## 2. Commit the brief

Read [the commit format and commands](references/commit-message.md) before committing. Apply them to every commit in this round.

On resume, use the round's commits to identify completed steps. If the deletion commit exists, continue at step 4. If the intake commit exists and the brief is still present, reuse it and resume the unfinished work in step 3.

For a new round, check the destinations for existing files and symlinked parent directories. Preserve existing work and resolve any collision before copying. Copy the original brief to the worktree root as `taskbook.md`. For Gitea intake, also copy the downloaded supporting files at their relative paths and add a `Taskbook-Source: <owner>/<repo> <branch-or-ref> <pinned-commit-sha>` trailer to the intake commit. Use the source branch when known. Commit only the imported paths and record the intake commit SHA. Start implementation after this commit succeeds.

Commit each intake, clarification, and cleanup separately from implementation changes. Preserve unrelated staged changes.

## 3. Implement, clarify, and verify

Before implementing, [extract and match existing experiment results](references/experiment-results.md) if the brief includes test records or the worktree has audit results relevant to the task. If a downstream failure gives concrete reason to doubt a reused result, immediately follow [Stop and report](references/experiment-results.md#stop-and-report) and end the round after reporting.

Before implementing, also [load or initialize the project glossary on its dedicated Gitea branch](references/gitea-glossary.md). Read any terminology source named in the brief. Use the project's established terms and the user's wording for undocumented concepts.

1. Before coding, [reconcile the active goals and collect the author's verification requirements](references/review-prompt.md#reconcile-goals-and-requirements). Resolve routine implementation choices yourself. Present unresolved conflicts between taskbook revisions, user decisions, and the actual implementation when they require a decision about scope or behavior. Explain the evidence and effect on delivery. Append the question and answer under `澄清记录` in `taskbook.md`, preserving the original brief and earlier answers. Commit each update before resuming the affected work. Record any answers received before worktree setup immediately after the intake commit.
2. Personally verify the open acceptance criteria using the agreed entry points and required repository checks. Reuse applicable evidence. Add a lasting test only for a specific regression the existing checks would miss. Inspect the diff and record the evidence, commands, and results. Commit the implementation to pin the snapshot for [independent validation](references/review-prompt.md#supply-the-evidence) within the existing review workflow. Address and recheck findings before recording acceptance.
3. Commit the [validation and delivery evidence](references/pr-delivery.md#record-validation-evidence). Record the SHA containing the latest brief. Remove the imported paths in a separate commit and retain the audit results. Use the intake commit to recover the path list on resume. Compare the reviewed snapshot with the delivery head and revalidate affected requirements if code or other evidence inputs changed.

## 4. Publish the PR

Recover the final brief with `git show <brief-sha>:taskbook.md`. Draft the PR body with the goal, actual changes, and [separate conclusions for this round and the original PR goals](references/pr-delivery.md#record-validation-evidence). Cite any reused evidence and identify the checks actually run this round. Save the draft outside the tracked files and reuse it on publication retries.

Verify that this round's diff matches its scope and that the PR diff is free of the imported paths. Before writing to the PR, collect the validation results or record the blocker and account for every finding. Push the task branch, then follow [PR delivery](references/pr-delivery.md) to create or update the PR for user review. Confirm the PR points to the pushed head and contains the saved body. Give the user the link, a change summary, and the verification status. Leave the PR open for the user.

When the user supplies a revision brief for the PR, start a new round at step 1.
