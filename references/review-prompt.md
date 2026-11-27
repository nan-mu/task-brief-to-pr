# T3 read-only review and independent validation

## Default review authorization

The user's explicit invocation of this repository's skill activates their standing authorization for the two Codex Magpie model routes below. It covers the complete review evidence for the selected task, including the private worktree, task brief and supporting files, plan, full diff, source and tests, repository standards, and experiment and verification results. Use this authorization across review stages without asking for it again. Apply any narrower scope the user gives for the run.

Identify the target repository or PR and review stage in the delegation so the approval reviewer can match the action to the invoked skill.

## Select the reviewer

Before the first delegation in the thread, call `orchestrator_capabilities` and verify the requested route. Call T3 `delegate_task` with `role: "review"`, `isolation: "shared"`, `target.providerInstanceId: "codex_magpie"`, and `target.options: {"reasoningEffort":"high"}`. Set `target.model` for the current stage.

| Stage | Reviewer | `target.model` |
| --- | --- | --- |
| `plan`, `diff` | DeepSeek Flash | `nas/group/deepseek-flash` |
| `final`, when needed | Qwen4-Max | `nas/qoder-cn/qmodel_latest` |

If the provider, model, or setting is unavailable, report the blocker and follow the user's direction.

Use `plan` to assess a proposal and `diff` to validate the implementation and its test evidence. Carry applicable diff results into delivery and use `final` when further independent validation is needed before delivery.

## Reconcile goals and requirements

1. Read the full brief, including any `独立模型验证要求` section and cited attachments. Resolve Gitea links at the fixed taskbook SHA. For a pasted or local brief, use its intake commit and retain the immutable original text and referenced materials. If the brief supplies no independent validation questions, derive them from the goals and acceptance criteria and list them under `additional_questions`.
2. For revisions, read [the same PR's taskbook history](gitea-intake.md#recover-the-prs-taskbook-history) and applicable user decisions. Track each goal with its source and whether it belongs to this round. Keep the author-specified questions, counterexamples, and expected evidence for every active goal. Record which goals have applicable evidence, which are still open or blocked, and which the user explicitly withdrew or replaced. Cite the decision and any replacement goal. Omission from a later brief leaves an earlier goal and its requirements in force.
3. Check that prior evidence still covers the same behavior and conditions on the current implementation. Cite it and identify the affected portion when a change invalidates it. If the brief, recorded decisions, or implementation conflict over what should be delivered, present the exact requirements, decision, and implementation location to the user. Keep the affected conclusion unresolved until the user decides. Treat an ordinary implementation defect under a clear active requirement as a finding.

## Supply the evidence

- Put the prompt below and the completed INPUT in `delegate_task.task`. Inline the full taskbook and evidence when they fit. Otherwise provide the absolute worktree root and index the full files at absolute paths for the reviewer to read. Include the original text of every applicable author question, counterexample and expected evidence, including referenced attachments, inline or through readable files. Identify each by source SHA, path, and section or item. Label additional questions separately. For evidence containing credentials, supply a masked excerpt in place of the file or path. Record any resulting gap.
- For `plan`, supply the plan text or path. For implementation validation in `diff` or `final`, pin the comparison SHA and the committed code snapshot. Use the merge base of the PR base and the code snapshot as the comparison point. Generate the complete in-scope diff from those commits with `git --no-optional-locks diff --no-ext-diff --no-textconv <base-sha> <code-sha> -- <paths>`. Verify that the source and tests the model reads match the pinned versions. Supply the relevant baseline source when a question depends on previous behavior. For a cross-repository contract, include the actual producer and consumer entry points, artifacts and corresponding repository SHAs. Record a gap when a required version or artifact cannot be supplied.
- Include the active goals and user decisions, the original source text that supports them, relevant historical validation records, repo standards, and the primary agent's actual checks and outputs. Show which version, conditions, and behavior each check covers, and identify open checks.

## Handle unavailable validation

- If Codex Auto-review rejects `delegate_task`, report the denial reason and follow the platform's approval response. For any tool, model, or evidence access blocker, record `BLOCKED` for the affected requirements and continue unaffected work.
- If a started review pauses for approval of a tool outside its scope, cancel it with `task_cancel`. Gather the missing evidence in the main thread. When independent validation is still needed, start a fresh `delegate_task` with the same provider and model and include that evidence inline when it fits.

## Resolve findings

1. Check every result against the cited snapshot, source, original requirement, and evidence. Missing answers or unsupported conclusions remain `UNVERIFIED`, or `BLOCKED` when a concrete dependency prevented the check. Record primary-agent checks separately from independent results.
2. Fix substantiated findings within the authorized task scope. Start a fresh `delegate_task` for the affected requirements at the new committed snapshot. Include the original requirements, the earlier finding and its evidence, and the changes or new evidence. Reuse unaffected results after checking applicability.
3. For disputed findings, retain both the primary agent's and reviewer's evidence and record the unresolved issue. Bring scope or requirement conflicts and out-of-scope fixes to the user. Keep the author requirements and acceptance criteria in the record.

## Delegate prompt

```text
Independently review the supplied plan or implementation according to the mode in INPUT. Your role is read-only. The main agent runs verification and tests and makes fixes. Start with the inline evidence and return the result directly when it suffices.

INPUT
mode: <plan | diff | final>
brief: <full current taskbook or absolute path, with taskbook source SHA>
scope: <repository or PR and plan or change scope>
worktree: <absolute checkout roots for evidence reads, or none>
active_goals: <current and earlier goals, source revisions, user decisions, and recorded withdrawals or replacements>
author_requirements: <verbatim questions, counterexamples and expected evidence with referenced attachments or readable paths, or none>
additional_questions: <derived or supplemental questions labeled with their source, or none>
snapshot: <plan text or path, or code SHA, comparison SHA, diff and any other repository SHAs>
files: <absolute paths and relevant ranges for briefs, decisions, source, tests and artifacts, or none>
standards: <applicable standards excerpts or paths, none, or unavailable>
verification: <actual commands and results, historical evidence with its scope, and open checks>

When more evidence is needed, use tools only to read indexed files and directly relevant source under the supplied checkout roots. Follow references from the diff, imports, and indexed files. Read evidence by absolute path and use supplied masked excerpts for sensitive evidence. If evidence is inaccessible, return the supported results and name the specific file, symbol, or evidence in material_gaps.

In plan mode, assess how the proposal addresses the active goals and repository standards. Return an empty validation list.

In diff and final modes, trace each active goal and specified question from the normal user-facing entry point to the observed or source-supported behavior. Evaluate goals outside this round against their original requirements. For a cross-component or cross-repository contract, trace the real producer's output into the real consumer's normal entry point at the pinned versions. Identify any unverified link in that chain.

For implementation counterexamples, inspect the actual tests, their inputs and assertions, and any observed outputs. Explain whether the wrong implementation would satisfy those assertions. Cite the expected evidence from the brief, the source branch taken, and the relevant test or output. Passing tests support only the behavior their assertions cover.

Assess Spec and Standards independently.

Spec
- Check each acceptance criterion against the proposed or actual entry point for the selected mode. Find missing, partial, incorrect, or out-of-scope behavior.
- Trace callers and interfaces that affect failure paths, existing data, and compatibility.
- Cite the brief clause, location, trigger, and effect for each finding.

Standards
- Start with explicit repository rules. Cite the rule and change location for each violation.
- Use Fowler's smells as heuristics. Focus on concrete maintenance or testing costs, and report each issue once per root cause.

For implementation validation, give each active goal and each assigned question or counterexample its own result, identified by its original label or source location. Cite the requirement source, reviewed implementation SHA or SHAs, source locations and supporting evidence. Distinguish observations, code-based conclusions and remaining gaps. Use PASS when evidence supports the requirement, FAIL when implementation or required verification violates it, UNVERIFIED when the evidence is insufficient, and BLOCKED when a missing tool, input, or environment prevents the check.

Return one JSON object:
{
  "spec": {"status": "clear", "findings": []},
  "standards": {"status": "clear", "findings": []},
  "validation": [
    {
      "requirement": "<goal or question and its source>",
      "status": "PASS|FAIL|UNVERIFIED|BLOCKED",
      "commits": ["<reviewed code SHA>"],
      "evidence": ["<source location, result or specific gap>"]
    }
  ],
  "material_gaps": []
}

Use clear, findings, or incomplete for each review axis. Findings have severity (blocking, major, or minor), location, basis, trigger, impact, and fix_direction. Report findings that affect delivery or justify a fix in this round. Include entries for assigned implementation questions even when evidence is missing.
```
