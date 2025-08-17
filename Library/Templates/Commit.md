# GPT-based Git Commit Message Generation 

### Prompt to generate commit messages using `git diff ` output or user-provided descriptions. Recommended for use after reviewing the rules of Semantic Versioning (SemVer) and Conventional Commits to maximize clarity and productivity.

```markdown
https://semver.org/
https://www.conventionalcommits.org/en/v1.0.0/
https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13

Read the above content carefully and properly. Generate commit messages strictly following the **Semantic Versioning (SemVer)** and **Conventional Commits** guidelines. I will provide the details of the commit, and you have to suggest a suitable commit title and additionally a commit body if necessary. If it is possible to fully summarize the commit only using the title, avoid adding a commit message. The wording of the commit must be clear, concise and properly formatted. Lastly, if I provide incorrect or unnecessary data with respect to the commit, you must point it out. If there are significant changes, mark them out. If a version bump is expected, inform me. Follow the rules to the fullest.

**Commit Types:** `feat`, `fix`, `chore`, `refactor`, `perf`, `test`, `docs`, `style`, `ci`, `build`, `revert`, etc.
**Optional Scope:** Only included if necessary.

**Commit Message Structure:**

- If a **title alone is sufficient**, do not generate a commit body.
- If **more context is needed**, add a body explaining the change.
- Separate the body into points. Do not use emojis anywhere.
- **Breaking changes** should be marked with `BREAKING CHANGE:`
```
