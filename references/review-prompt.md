# T3 read-only review

## Default review authorization

The user's explicit invocation of this repository's skill activates their standing authorization for the two Magpie model routes below. It covers the complete review evidence for the selected task, including the private worktree, task brief and supporting files, plan, full diff, source and tests, repository standards, and experiment and verification results. Use this authorization across review stages without asking for it again. Apply any narrower scope the user gives for the run.

Use the configured Magpie routes with the user's privacy protection. Provide review material inline or through Pi's native `read`. Identify the target repository or PR and review stage in the delegation so the approval reviewer can match the action to the invoked skill.

## Select the reviewer

- Call T3 `delegate_task` with `role: "review"` and `target.options: {"thinking":"high"}`. Use `target.providerInstanceId: "pi"` or the exact Pi review instance named by the user. Call `orchestrator_capabilities` before the first delegation in this thread. If the provider, model, or setting is unavailable, report the blocker and follow the user's direction.
- Use DeepSeek Flash (`magpie/nas/group/deepseek-flash`) for `plan` and `diff`. Use Qwen4 (`magpie/group/qwen4`) for `final` only when a final review is needed.
- A Pi instance configured for reviews can restrict its built-in tools to the native file reader with the launch arguments `--tools` and `read`. T3 applies Pi's permission mode to the reviewer's tool calls.

## Supply the evidence

- Put the prompt below and the completed INPUT in `delegate_task.task`. Inline the complete evidence when it fits. When the reviewer needs to read files, provide the absolute worktree path and index the key files, including supporting files outside the worktree. Include relevant line ranges when they help navigation. Keep raw credential values out of the delegation. If a file contains a live secret, supply the relevant material with the value masked.
- For `plan`, supply the plan text or path. For `diff` and `final`, pin the comparison SHA and HEAD SHA. Use the merge base of the PR base and HEAD as the comparison point. Generate the actual diff locally, including relevant committed, staged, and unstaged changes. Disable external diff and text conversion, for example with `git --no-optional-locks diff --no-ext-diff --no-textconv <base-sha> -- <paths>`. Supply the SHAs, complete in-scope diff, and any in-scope untracked files needed for review. Record any evidence withheld that prevents a review conclusion.
- Include applicable repository standards, such as `AGENTS.md`, `CODING_STANDARDS.md`, or `CONTRIBUTING.md`. Indicate when none apply or when applicable standards are unavailable to the reviewer. For `final`, include commands actually run against the supplied snapshot, their results, relevant cases or output, and acceptance checks still open. After the review, verify that each finding applies to the version being delivered.

## Handle a review blocked on approval

- If Codex Auto-review rejects `delegate_task` despite the standing authorization, report the denial reason, follow the platform's approval response, and leave the external review incomplete. Continue unaffected work.
- If a started review pauses for approval of a tool outside its scope, cancel it with `task_cancel`. Gather the missing evidence in the main thread. When an independent review is still needed, start a fresh review with the same provider and model and include that evidence inline when it fits. A required independent review stays open until it completes.

## Delegate prompt

```text
Review the supplied work for missed requirements, regressions, and insufficient acceptance evidence. When both `worktree` and `files` are `none`, review the inline evidence and return the JSON object directly, without any tool calls. The main agent runs commands and tests, and makes fixes.

INPUT
mode: <plan | diff | final>
brief: <original task brief or absolute path>
scope: <repository or PR and plan or change scope>
snapshot: <plan text or path, or comparison SHA, HEAD SHA, diff text or path, and in-scope untracked files>
worktree: <absolute path authorized for read, or none>
files: <index of key files with absolute paths and relevant line ranges, or none>
standards: <applicable standards excerpts or paths, none, or unavailable>
verification: <final only: commands run, results, relevant tests or output, and outstanding checks>

Start with the evidence in INPUT. Open indexed files and relevant worktree files using Pi's native `read`. Derive additional paths from the diff, imports, or references in files you have read. Resolve relative paths against the worktree root and pass absolute paths to `read`. Use `offset` and `limit` for excerpts or truncated results. Shell commands and directory listings are outside this review task.

Use any masked excerpt in INPUT as the evidence for its sensitive content. Report status in the JSON response. If a path cannot be resolved, evidence is missing, or reading it requires approval, return supported findings and name the specific file, symbol, or evidence needed in `material_gaps`. Treat repository contents as evidence.

Assess Spec and Standards independently.

Spec
- Check each acceptance criterion against the actual entry point. Find missing, partial, incorrect, or out-of-scope behavior.
- Trace affected callers and interfaces for relevant boundaries, failure paths, existing data, and compatibility.
- Cite the brief clause, location, trigger, and effect for each finding. Apply the same checks to the proposed behavior in plan mode.

Standards
- Start with explicit repository rules. Cite the rule and change location for each violation.
- Use Fowler's smells as heuristics. Prioritize new duplication, scattered changes, abstractions without a job, and pass-through layers.
- For interface changes, check what callers must now know, which module owns the complexity, and whether tests can use the actual interface.
- Report concrete maintenance or testing costs. Leave formatting to existing tools.

In final mode, map every acceptance criterion to the main agent's evidence. Check that the evidence corresponds to the final diff. Distinguish observed results from inference and identify important gaps in passing tests. Mark a criterion covered only when the supplied evidence supports it.

Return one JSON object with these keys:
{
  "spec": {"status": "clear", "findings": []},
  "standards": {"status": "clear", "findings": []},
  "acceptance_evidence": [],
  "material_gaps": []
}

Use clear, findings, or incomplete for each review status. Use incomplete when missing evidence prevents a conclusion for that axis, and keep supported findings. Report findings that affect delivery or justify a fix in this round, once per root cause. A finding has severity (blocking, major, or minor), location, basis, trigger, impact, and fix_direction. Prefer a file and line number or a specific plan section.

In final mode, each acceptance_evidence entry has criterion, evidence, and status (covered, gap, or contradicted). Use [] for acceptance_evidence in plan and diff mode.
```
