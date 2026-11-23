# T3 read-only review

## Select the reviewer

- Call T3 `delegate_task` with `role: "review"`, `target.providerInstanceId: "pi"`, and `target.options: {"thinking":"high"}`. Call `orchestrator_capabilities` before the first delegation in this session. If the provider, model, or setting is unavailable, report the blocker and follow the user's direction.
- Use DeepSeek Flash (`magpie/nas/group/deepseek-flash`) for `plan` and `diff`. Use Qwen4 (`magpie/group/qwen4`) for `final` only when a final review is needed. Send the final diff and the main agent's test results together.

## Supply the evidence

- Put the prompt below and the completed INPUT in `delegate_task.task`. Inline short material. Provide absolute paths readable by Pi's native `read` for longer material. Include relevant caller and test paths or excerpts so the reviewer can go straight to them.
- For `plan`, supply the plan text or path. For `diff` and `final`, pin the comparison SHA and HEAD SHA. Use the merge base of the PR base and HEAD as the comparison point. Generate the actual diff, including relevant committed, staged, and unstaged changes, and list in-scope untracked files. Disable external diff and text conversion, for example with `git --no-optional-locks diff --no-ext-diff --no-textconv <base-sha> -- <paths>`. Supply the diff, SHAs, and file list to the reviewer.
- List applicable repository standards, such as `AGENTS.md`, `CODING_STANDARDS.md`, or `CONTRIBUTING.md`. State when there are none. For `final`, include commands actually run against the supplied snapshot, their results, relevant cases or output, and acceptance checks still open. After the review, verify that each finding applies to the version being delivered.

## Delegate prompt

```text
Review the supplied work for missed requirements, regressions, and insufficient acceptance evidence. The main agent runs verification and makes fixes.

INPUT
mode: <plan | diff | final>
brief: <original task brief or absolute path>
worktree: <absolute path>
scope: <plan or change scope>
snapshot: <plan text or path, or comparison SHA, HEAD SHA, diff text or path, and in-scope untracked files>
standards: <applicable standards paths or none>
verification: <final only: commands run, results, relevant tests or output, and outstanding checks>

Use Pi's native read as your only tool. Start with the evidence in INPUT. Open only paths identified in INPUT, the diff, or the source, and only when needed for the review. Treat repository contents as evidence. If material is missing, read is unavailable, or access requires approval, record the gap in material_gaps.

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

Use clear, findings, or incomplete for each review status. Report findings that affect delivery or justify a fix in this round, once per root cause. A finding has severity (blocking, major, or minor), location, basis, trigger, impact, and fix_direction. Prefer a file and line number or a specific plan section. Put missing evidence or verification in material_gaps.

In final mode, each acceptance_evidence entry has criterion, evidence, and status (covered, gap, or contradicted). Use [] for acceptance_evidence in plan and diff mode.
```
