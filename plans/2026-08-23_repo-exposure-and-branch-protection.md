# Repo exposure and branch protection

*Audited 2026-08-23, prompted by GitHub's "your main branch is not protected" banner.*

Two separate questions got tangled together by that banner: whether the repo is
exposed, and what an unprotected `main` actually costs us. The first is a
deliberate choice and is fine. The second is a real gap, and it is small to close.

## What the audit found

`jhave/narracode` is **public** (`private: false`, `visibility: public`) and
intentionally so — it serves GitHub Pages at https://jhave.github.io/narracode/.
Anyone can read, clone, and fork it. Forking is enabled.

Write access is not exposed. The collaborator list is one entry: `jhave`, admin.

No credentials are committed. `.gitignore` covers `.env`, `.claude/`,
`__pycache__/`, `node_modules/`. No tracked file carries a secret-shaped name
(`.env`, `*.pem`, `*.key`) and no tracked file contains a key-shaped string
(`sk-ant-`, `ghp_`, `github_pat_`, `AKIA…`, `AIza…`).

One caveat worth writing down: that scan covered the **current tree, not every
past commit**. History is public too, so anything ever committed and later
deleted is still retrievable by anyone. If a key ever did land in a commit, the
fix is to rotate it, not to delete the file.

## What "main is not protected" means

Not a leak. It means no branch protection rule or ruleset exists on `main` —
every branch in the repo currently reports `protected: false`.

With no rule, anyone holding write access can:

- push straight to `main` with no pull request and no review
- **force-push and rewrite history** on `main`
- **delete `main`** outright
- merge with failing or absent checks

"Anyone holding write access" is the phrase that matters here. It is not only
jhave at a keyboard — it is every token, GitHub App, and agent session acting
with those credentials. This repo has agent sessions pushing branches routinely,
which is exactly the population that produces an accidental force-push.

Two things sharpen the cost:

1. **Pages publishes from this repo.** A bad commit to `main` is live on the
   public site immediately. There is no staging step between the push and the
   reader.
2. **The corpus is the asset.** `versions/`, the diff pairs, the story history —
   the value of this repo is accumulated history, and history is precisely what a
   force-push destroys.

## Recommendation

Settings → Rules → Rulesets → New branch ruleset, target `main`, enable:

- **Restrict deletions**
- **Block force pushes**

Both are pure safety net at zero workflow cost: ordinary pushes to `main` still
work exactly as they do now. This is the whole recommendation.

**Require a pull request before merging** is deliberately *not* recommended. It
would mean no more direct pushes to `main`, which for a single-author repo buys
review discipline nobody is present to exercise. Worth adopting only if a second
regular contributor appears.

This cannot be committed — branch protection is repo configuration, not a file in
the tree, so it has to be set in the GitHub UI by hand.
