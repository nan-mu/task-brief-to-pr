---
name: task-brief-to-pr
description: 按任务书在独立 Git worktree 实现和验收改动，再创建或更新 PR。
---

# Task brief to PR

Run this workflow when the user explicitly invokes the skill and asks you to implement a task brief. Finish with a PR ready for the user to review.

## 1. Read the brief and enter the worktree

1. Read the brief from pasted text, a Markdown file, or an archive containing `taskbook.md` at its root. Resolve provided paths to absolute paths. For ZIP and TAR archives, pass the archive path to [read-taskbook.py](scripts/read-taskbook.py) with Python 3. For other formats, use an available reader to read the single regular file at that same location. Open supporting materials as needed. Ask for a usable source when the entry is missing, unreadable, or ambiguous.
2. Resolve the repository, acceptance criteria, starting ref, and PR base. For an existing PR, verify its number, head repository, head branch, and base, then use its head. Honor a branch the user names and ask when branch ownership is unclear. For a new branch, use the requested name or choose an unused one. Start independent work from the latest remote default branch, or the local default if there is no remote. Start dependent work from the ref containing the dependency and use the PR base specified by the brief.
3. Reuse the task's worktree when it exists. In T3, call `t3_worktree_status` first. For a new branch in a session that can move, use `t3_worktree_handoff` with the branch, `baseRef`, and a `continuationPrompt` containing the original brief or a readable absolute path. Set `startFromOrigin: true` for a remote start or `false` when using local commits. End the turn with that call and resume in the new worktree. For a manual checkout, use `git worktree add -b <branch> <path> <base>` for a new branch or `git worktree add <path> <branch>` for an existing one. Run the remaining steps from the task worktree.

## 2. Commit the brief

Read [the commit format and commands](references/commit-message.md) before committing. Apply them to every commit in this round.

On resume, use the round's commits to identify completed steps. If the deletion commit exists, continue at step 4. If the intake commit exists and the brief is still present, reuse it and resume the unfinished work in step 3.

For a new round, check `taskbook.md` at the worktree root. If the path belongs to the project or another round, preserve it and ask the user to resolve the collision. Copy the original brief to that path, commit it alone, and record the commit SHA. Start implementation after this commit succeeds.

Commit each addition, clarification, and deletion of `taskbook.md` separately from implementation changes. Preserve unrelated staged changes.

## 3. Implement, clarify, and verify

1. Resolve routine implementation choices yourself. Ask the user about ambiguities, conflicts, or blockers that affect implementation or acceptance. For each reply, append the question and the user's answer under `澄清记录` in `taskbook.md`. Preserve the original brief and earlier answers. Commit each update before resuming implementation. Record any answers received before worktree setup the same way, immediately after the intake commit.
2. Run the acceptance tests or reproduction commands yourself in the worktree. Inspect the final diff and record the commands you ran and their results. When a plan review, diff review, or final review is needed, follow the [read-only review prompt](references/review-prompt.md) and resolve the findings yourself.
3. After implementation passes acceptance, commit the implementation and record the SHA containing the latest brief. Delete `taskbook.md` in its own commit.

## 4. Publish the PR

Recover the final brief with `git show <brief-sha>:taskbook.md`. Draft the PR body with the goal, actual changes, acceptance results, and relevant limitations. Save the draft outside the tracked files and reuse it on publication retries.

Verify that this round's diff matches its scope and that the PR diff contains no `taskbook.md`. Push the task branch, then follow [PR delivery](references/pr-delivery.md) to create or update the PR. Confirm the PR points to the pushed head and contains the saved body. Give the user the link, a change summary, and the verification you ran.

When the user supplies a revision brief for the PR, start a new round at step 1.
