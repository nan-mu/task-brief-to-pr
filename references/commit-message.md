# 提交模板与 Git hook

## 提交格式

```text
📝 docs(taskbook): Record the clarification

Record the agreed behavior and the acceptance condition for empty input.

中文总结：记录空输入的处理约定。

Co-authored-by: Sam Example <sam@example.com>
```

主题使用一个 emoji、`type(scope)` 和英文标题。类型用小写，可采用项目惯用的类型和范围。英文正文说明改了什么以及原因。正文最后一段是一行以 `中文总结：` 开头的简短中文总结。联署可省略，提供时每人一行并使用实际姓名和用于归属提交的邮箱。联署和其他 Git trailer 放在总结之后的独立段落。

任务书的新增、澄清和删除可分别用 `📝 docs(taskbook): Record the task brief`、`📝 docs(taskbook): Record the clarification`、`🧹 chore(taskbook): Remove the completed task brief`。

## Commit from the task worktree

For each commit, write the complete message to a temporary file. Set `skill_dir` and `message` to absolute paths. Run the checker from the task worktree and commit only if it passes.

```sh
python3 "$skill_dir/hooks/commit-msg" "$message" &&
  git commit --cleanup=strip -F "$message"
```

To commit the brief alone, stage additions and updates with `git add -- taskbook.md` or stage deletion with `git rm -- taskbook.md`. Use `git commit --cleanup=strip -F "$message" --only -- taskbook.md` in place of the commit command above. Keep existing repository hooks enabled. The brief and clarifications remain in pushed history. If you find sensitive content, confirm it can be recorded in the target repository before committing it.

## 在自己的仓库启用

`commit-msg` 接收 Git 提供的消息文件路径。脚本校验其内容并用非零退出码阻止失败的提交。它检查结构、常见 emoji 及文字特征，英文语义和中文总结是否准确仍需人工判断。可用 Python 3 直接运行同一脚本测试消息。 [Git hooks 手册](https://git-scm.com/docs/githooks#_commit_msg)

如果希望每次从编辑器写提交都预填格式，在目标仓库执行。先将 `skill_dir` 设为技能根目录的绝对路径。

```sh
git config --local commit.template "$skill_dir/assets/commit-message.txt"
```

如果希望仓库自动校验每次本地提交，在使用默认 hooks 目录且没有现成 `commit-msg` 的仓库执行。这个目录由该仓库的各 worktree 共用。已有 `core.hooksPath` 或同名 hook 时，把检查脚本接进现有 hook，并传递 Git 原样提供的 `"$1"`。

```sh
if ! git config --get core.hooksPath >/dev/null &&
   git_dir=$(git rev-parse --path-format=absolute --git-common-dir); then
  hook_dir=$git_dir/hooks
  if [ ! -e "$hook_dir/commit-msg" ] && [ ! -L "$hook_dir/commit-msg" ]; then
    mkdir -p "$hook_dir" &&
      install -m 755 "$skill_dir/hooks/commit-msg" "$hook_dir/commit-msg"
  fi
fi
```

`commit.template` 为编辑器预填文本。脚本或代理用 `-m` 或 `-F` 时直接传入完整消息，已安装的 hook 同样会校验。 [Git 提交手册](https://git-scm.com/docs/git-commit#Documentation/git-commit.txt--tltfilegt)
