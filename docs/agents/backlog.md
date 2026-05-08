# Backlog: GitHub Issues

Issues and PRDs for this repo live as GitHub Issues, managed via the `gh` CLI.

## Conventions

- Triage state is tracked with GitHub labels (see `triage-labels.md` for the label strings)
- PRDs are created as issues with the `prd` label and a descriptive title
- Implementation issues reference their parent PRD issue number in the body
- Use `gh issue list`, `gh issue view`, `gh issue create`, and `gh issue edit` for all backlog operations

## When a skill says "publish to the backlog"

Create a GitHub issue:

```bash
gh issue create --title "<title>" --body "<body>" --label "needs-triage"
```

## When a skill says "fetch the relevant ticket"

```bash
gh issue view <number>
```

The user will normally pass the issue number directly.

## When a skill says "apply a triage label"

```bash
gh issue edit <number> --add-label "<label>" --remove-label "<old-label>"
```

## Note

Requires a GitHub remote to be configured. If `gh issue` commands fail, check that the repo has a remote with `git remote -v` and create one at github.com if needed.
