# AI Skills and Agents Samples

A **skill** is a text file that teaches an AI coding assistant how to do a
specific job — kind of like a recipe card, or step-by-step instructions you'd
give a new team member. Instead of typing out the same detailed instructions
every single time, you write them once, save them as a skill, and reuse them
whenever you need them. This repository is a collection of skills like that,
built to work the same way across three different AI tools: Codex, Claude
Code, and GitHub Copilot CLI.

[![Links: K THE TECHMAN](https://img.shields.io/badge/K_THE_TECHMAN-All_links-D97706?style=flat-square&labelColor=181512)](https://khadir-syed.github.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-D97706?style=flat-square&labelColor=181512)](LICENSE)

## Quick start

```bash
git clone https://github.com/khadir-syed/ai-agent-skills.git && cd ai-agent-skills
mkdir -p .claude
./install.sh root-cause-investigator
```

(The `mkdir` step matters — a fresh clone has no `.claude`, `.agents`, or
`.github` folder yet, and `install.sh` only copies into folders that
already exist. Using Codex or Copilot CLI instead? Make `.agents` or
`.github` instead of `.claude`.)

Then, in Codex, Claude Code, or Copilot CLI, try the first prompt from
[Try the samples](skills/README.md#try-the-samples) in the Skills doc. On
Claude Code specifically, this first try can be inconsistent — see
[Troubleshooting](#troubleshooting) if it asks you for real system access
instead of just running the investigation.

## Contents

- [About this collection](#about-this-collection)
- [Skills (Stage 1)](skills/README.md) — how a skill works, the full list of skills, example runs, and prompts you can try yourself
- [Agents (Stage 2)](agents/README.md) — six agents, some that check in with you at every step and some that check in less, example runs, and tests where we tried to trick them
- [Orchestrators (Stage 3)](orchestrators/README.md) — a "router" that figures out which agent should handle your request
- [Use a skill, agent, or orchestrator in an AI coding tool](#use-a-skill-in-an-ai-coding-tool)
- [Troubleshooting](#troubleshooting)
- [What these samples do not provide](#what-these-samples-do-not-provide)
- [Customise them](#customise-them)
- [Official documentation](#official-documentation)

## About this collection

This collection is being built up in three stages, one at a time:

1. Skills
2. Agents
3. Orchestrators — one thing deciding which agent to use

**Stage 1 (Skills)** covers four topic areas (we call them "domains"), and
each one has the same three kinds of skill: one that only looks and reports
back, one that's allowed to write something (but always asks first), and one
that runs through a checklist. Learn the pattern once, and every other skill
just feels like a variation on it. See [skills/README.md](skills/README.md)
for the full list.

| Domain | Status |
|---|---|
| Tech / Software | Done — 3 skills |
| Product | Done — 3 skills |
| Content | Done — 3 skills |
| Social Media | Done — 3 skills |

**Stage 2 (Agents)** takes one real job per domain and does it *twice* —
once where a human approves every single step ("controlled"), and once where
a human approves fewer steps ("autonomous") — so you can see exactly what
changes when a human isn't checking in as often. See
[agents/README.md](agents/README.md) for all six agents, how we tested
them, and what happened when we tried to trick one into skipping a step.

| Domain | Status |
|---|---|
| Tech / Software | Done — 2 agents (1 checks in every step, 1 checks in less) |
| Product | Done — 2 agents (1 checks in every step, 1 checks in less) |
| Content | Done — 2 agents (1 checks in every step, 1 checks in less) |

**Stage 3 (Orchestrators)** adds a "router" — something that reads your
request and figures out *which* Stage 2 agent should handle it, then hands
it off, in both a "checks in every step" and a "checks in less" version. See
[orchestrators/README.md](orchestrators/README.md) for how each one works,
example runs, and a real bug we found and fixed while testing.

| Orchestrator | Status |
|---|---|
| request-router-agent-controlled | Done — decides between the software, product, and content agents |
| request-router-agent-autonomous | Done — same three-way decision, with fewer check-ins; the software path runs to completion with no check-ins at all, and says so upfront |

More skills, agents, orchestrators, and topic areas are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) if you'd like to add one.

## Use a skill in an AI coding tool

Copy the whole skill folder — not just the one file inside it — into a
location your AI tool looks in. You can do this by hand, or use the
`install.sh` script below to do it for you. This works the same way whether
it's a Stage 1 skill, a Stage 2 agent, or a Stage 3 orchestrator — they're
all just text files, installed the same way. If you install an orchestrator,
also install the agent(s) it might hand off to (`bug-fix-agent`,
`feature-launch-readiness-agent-controlled` or `-autonomous`,
`content-publish-readiness-agent-controlled` or `-autonomous`), so it has
something to hand off *to*.

| Tool | Project location | Personal location | Example invocation |
|---|---|---|---|
| Codex | `.agents/skills/<skill-name>/` | `~/.agents/skills/<skill-name>/` | `$<skill-name> investigate why the customer list is empty` |
| Claude Code | `.claude/skills/<skill-name>/` | `~/.claude/skills/<skill-name>/` | `/<skill-name> investigate why the customer list is empty` |
| GitHub Copilot CLI | `.github/skills/<skill-name>/`, `.agents/skills/<skill-name>/`, or `.claude/skills/<skill-name>/` | `~/.copilot/skills/<skill-name>/` or `~/.agents/skills/<skill-name>/` | `/<skill-name> investigate why the customer list is empty` |

If your tool doesn't notice a skill you just added, close it and reopen it.
The exact way you invoke a skill can change as these tools update, so check
your tool's own docs if something here looks out of date.

### CLI apps vs. desktop apps

The table above is for the **CLI tools** you type commands into (Codex CLI,
Claude Code CLI or its editor plugin, Copilot CLI) and the Codex desktop
app. All of these read a skill straight from a project folder, so copying
the folder in is all you need to do.

The **Claude desktop app and Claude on the web are different.** They don't
look at your project folder at all. Instead, you upload skills as a ZIP file
through the settings menu:

1. **Settings → Capabilities** → turn on "Code execution and file creation."
   A skill won't run without this turned on.
2. **Customize → Skills** → **+** → **Create skill** → **Upload a skill**.
3. Pick a ZIP file of the skill folder, with `SKILL.md` right at the top of
   the ZIP — not buried inside another folder. This is the most common
   reason an upload fails.
4. Turn the skill **on** after uploading. Uploading it doesn't automatically
   turn it on.

This upload method works for any skill, agent, or orchestrator in this repo
that's just text — including both
[request-router-agent-controlled](orchestrators/request-router-agent-controlled/)
and
[request-router-agent-autonomous](orchestrators/request-router-agent-autonomous/).
If you upload a router, also upload and turn on the agent(s) it might route
to, so it has something to hand off to, same as with the CLI.

It does **not** work for
[test-fix-loop-agent](agents/software/test-fix-loop-agent/), because that
one is an actual computer program (Python), not a text instruction file, and
Claude Desktop and Claude web can't run programs. That one only works from a
terminal — see its own
[README](agents/software/test-fix-loop-agent/README.md).

### Using the install script

`install.sh` is just a helper — it's not a skill itself, it simply copies a
skill folder for you so you don't have to do it by hand. It copies into
whichever folders your tools already use on your computer. It doesn't do
anything else: no internet access, no deleting files, nothing sneaky.

```bash
./install.sh root-cause-investigator
```

It looks for `<skill-name>` inside `skills/<domain>/`, `agents/<domain>/`,
and `orchestrators/` — so this exact same command also installs
`request-router-agent-controlled` or `request-router-agent-autonomous`.

By default it only copies into your current project's folders
(`.agents/skills/`, `.claude/skills/`, `.github/skills/`) — whichever of
those already exist. Add `--global` to also copy into your personal home
folder, so the skill is available in every project:

```bash
./install.sh --global changelog-entry-drafter
```

## Troubleshooting

Real problems we actually ran into while building and testing this repo —
not guesses about what might go wrong.

**A skill doesn't show up when I try to use it.**
Your tool only checks for new skills when it starts up, not while it's
running. Close it and reopen it after copying a new skill in. Also double
check you copied the *whole* folder (`SKILL.md` plus its `examples/` and
`references/` folders), not just the one `SKILL.md` file by itself.

**A skill doesn't trigger unless I type its name exactly.**
That means the tool couldn't tell your plain-language request matched the
skill — it's not a broken skill. Try typing the skill's name directly first
(like `/skill-name`) to check it's installed at all, then make the skill's
short description mention the situations it should catch.

**On Claude Code, the very first sample prompt can be genuinely
inconsistent — even the `/skill-name` form.** We tested this for real on a
fresh install: the `root-cause-investigator` sample prompt (both as plain
language and as `/root-cause-investigator ...`) sometimes ran the actual
investigation as documented, and sometimes asked for real system access
instead — across several tries, on identical wording, with no pattern tied
to which phrasing was used. Codex was consistent in our testing. If this
happens to you: try again in a fresh session (it may simply work the next
time), and check whether a personal `~/.claude/CLAUDE.md` is competing with
the skill — see "A skill on Claude Code ignores its own rules..." further
down this list. This repo now ships a project-level [`CLAUDE.md`](CLAUDE.md)
and [`AGENTS.md`](AGENTS.md) that fixes this for both tools — see that entry
for what it does and why it's still not a 100% guarantee.

**`install.sh` printed "Nothing copied."**
It only copies into folders that already exist in your current project
(`.agents/`, `.claude/`, `.github/`) — it won't create them for you. Make
one yourself first (like `mkdir .claude`), or use `--global` to install into
your personal home folder instead.

**Claude Desktop can't see a skill that works fine in Claude Code.**
That's expected — they work differently. Claude Code reads straight from
your project's `.claude/skills/` folder. Claude Desktop needs the skill
uploaded as a ZIP file through Settings, with code execution turned on (see
[CLI apps vs. desktop apps](#cli-apps-vs-desktop-apps) above).

**A skill that's supposed to ask before writing a file didn't ask the second
time.**
Check whether an earlier message accidentally gave it standing permission
(something like "yes, and don't ask again"). If you never said that, this is
a bug in that skill's wording — it should ask every single time, not
remember one "yes" as permission forever.

**A skill ignores its own rules, or a Codex answer comes wrapped in
unrelated headers.**
This can happen if you have your own personal instructions file —
`~/.claude/CLAUDE.md` for Claude Code, or `~/.codex/AGENTS.md` for Codex (a
global file you wrote yourself, separate from this repo). If those personal
instructions give the AI a different job — for example, telling it to
always give advice and ask discussion questions before doing anything —
they can win out over a skill's own instructions, especially on a request
that sounds like it needs a judgment call. We saw this happen for real: on
Claude Code, a router skill was asked a genuinely tricky question, and
instead of following its own "state the mix-up, ask which one" rule, it
answered as a general advisor instead, because that's what a personal
`CLAUDE.md` file told it to prioritize. Codex has the same kind of
competing file at `~/.codex/AGENTS.md`; in our testing it never changed
Codex's actual answer or skipped an approval step, but it did sometimes
wrap a correct answer in unrequested "Critique / Alternatives / Pros & Cons"
headers from that personal file.

This repo ships a project-level [`CLAUDE.md`](CLAUDE.md) and
[`AGENTS.md`](AGENTS.md) at the repo root specifically to fix this: when you
explicitly invoke one of this repo's skills, agents, or orchestrators, these
files tell the tool to follow that skill's own instructions as written
instead of layering your personal file's persona or format on top. In our
testing this fixed the formatting bleed-through on Codex completely, and
made the Claude Code behavior noticeably more consistent (it's still not a
100% guarantee — if a skill still seems to "forget" its own rules, check
your personal instructions file for something that could be pulling it in a
different direction, before assuming the skill itself is broken).

**GitHub shows a different name than what I typed for my commit.**
If your commit's email matches a verified email on a GitHub account
(including the private `@users.noreply.github.com` kind), GitHub shows that
account's name and picture instead of the plain text name you typed. This is
just how GitHub displays things — it's not a bug, and it's not a sign your
push failed.

## What these samples do not provide

- They don't guarantee an AI tool will pick the right skill on its own.
- They don't give access to files, terminals, logs, databases, or outside
  services by themselves.
- They don't override your tool's own permission settings or your own
  instructions.
- Following the right format doesn't automatically make a diagnosis, draft,
  or check *correct* — you still need to read the output.
- These are learning examples, not a real production system for handling
  incidents, releases, or security.

## Customise them

Copy a sample and change one thing at a time:

1. Rewrite the short description so it matches the kinds of problems you
   actually want it to catch.
2. Add places specific to your own project that it should look at — for
   example, "check the browser, then the API, then the database."
3. Add whatever sources of evidence you actually have available.
4. Change the report format without removing the parts that separate facts
   from guesses.
5. Test it with a real, known problem — and also test it with something it
   should *not* react to.

Remember: saying a skill is "read-only" describes what it's *supposed* to
do. It's your AI tool's own permission settings that actually stop it from
doing more than that.

## Official documentation

- [OpenAI: Build skills for ChatGPT and Codex](https://learn.chatgpt.com/docs/build-skills)
- [Anthropic: Extend Claude with skills](https://code.claude.com/docs/en/slash-commands)
- [GitHub: Add agent skills for GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)
