"""Self-check for the web pages: every request shown on a page must be exactly
the one in the repo's example file, every recorded run must be labelled and
format cleanly, and the pages must stay safe. Runs instantly, no network.
Run from the repo root with: python3 web/test_web.py
"""
import glob
import html
import json
import os
import re
import shutil
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPO_URL = "https://github.com/khadir-syed/k_ai-agent-skills/tree/main/"
JOBS = ["find", "draft", "check"]  # the skill pages, under skills/
TEAMS = ["product", "content", "social", "software"]
AGENT_PAGES = ["together", "content", "software"]  # one page per agent pair, under agents/
RUN_PAGES = ([f"skills/{job}/index.html" for job in JOBS] + [f"agents/{a}/index.html" for a in AGENT_PAGES]
             + ["orchestrators/index.html"])
PAGES = ["index.html", "skills/index.html", "agents/index.html"] + RUN_PAGES
# Old addresses from before the pages moved; each is now a tiny redirect.
MOVED = {"find": "skills/find", "draft": "skills/draft", "check": "skills/check", "together": "agents/together"}
GOATCOUNTER = "https://khadir-syed.goatcounter.com"
problems = []


def check(ok, message):
    if not ok:
        problems.append(message)


def read(path):
    return open(os.path.join(HERE, path), encoding="utf-8").read()


def plain(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment))


def squash(text):
    return " ".join(text.split())


# ---- Safety: the same rules on every page ------------------------------------
for name in PAGES + ["../index.html"] + [f"{old}/index.html" for old in MOVED]:
    page = read(name)
    csp = re.search(r'http-equiv="Content-Security-Policy"\s+content="([^"]+)"', page)
    check(csp and "default-src 'none'" in csp.group(1), f"{name}: strict Content-Security-Policy missing")
    if csp and "script-src" in csp.group(1):
        check("script-src 'self';" in csp.group(1), f"{name}: scripts may only come from this site")
    check(not re.search(r"<script(?![^>]*\bsrc=)[^>]*>", page), f"{name}: inline <script> found")
    check(not re.search(r'<script[^>]*src="(https?:)?//', page), f"{name}: script from another site")
    check(" style=" not in page, f"{name}: inline style= found (the CSP blocks it)")
    check(not re.search(r"\son[a-z]+=", page), f"{name}: inline event handler found")
    # Data may only go to this site and GoatCounter's visit counter.
    connect = re.search(r"connect-src ([^;]+);", csp.group(1)) if csp else None
    check(not connect or set(connect.group(1).split()) <= {"'self'", GOATCOUNTER},
          f"{name}: connect-src allows somewhere other than this site and GoatCounter")
    if name in PAGES:
        check(re.search(r'<script src="(\.\./)*count\.js" defer></script>', page) and connect
              and GOATCOUNTER in connect.group(1), f"{name}: visit count (count.js) missing")
    # Every link to this site's own files must lead somewhere real.
    folder = os.path.dirname(os.path.join(HERE, name))
    for target in re.findall(r'<[a-z][^>]*?\s(?:href|src)="([^"#:]+)"', page):
        path = os.path.normpath(os.path.join(folder, html.unescape(target)))
        if os.path.isdir(path):
            path = os.path.join(path, "index.html")
        check(os.path.isfile(path), f"{name}: broken link {target}")
    # Links to the repo on GitHub must point at folders that exist.
    for target in re.findall(r'href="' + re.escape(REPO_URL) + r'([^"#]+)"', page):
        check(os.path.isdir(os.path.join(ROOT, target)), f"{name}: GitHub link to missing folder {target}")

# ---- "In short": every page opens with a part a 7-year-old can read alone ----
for name in PAGES:
    easy = re.findall(r'<section class="card easy"[^>]*>(.*?)</section>', read(name), re.S)
    check(len(easy) == 1 and read(name).index("card easy") < read(name).index('<section class="card"'),
          f"{name}: needs one 'In short' part, before the rest of the page")
    lines = re.findall(r"<p>(.*?)</p>", easy[0]) if easy else []
    for sentence in (s for line in lines for s in re.split(r"(?<=[.?!])\s+", plain(line))):
        check(len(sentence.split()) <= 10, f"{name}: 'In short' sentence too long for a young reader: {sentence!r}")

# ---- Home -> Skills and Agents; Skills -> one card per job page ---------------
home = read("index.html")
check(all(f'href="{p}/"' in home for p in ["skills", "agents", "orchestrators"]),
      "home must link to the Skills, Agents and Orchestrators pages")
cards = re.findall(r'<a class="job-card j-(\w+)" href="(\w+)/">', read("skills/index.html"))
check(cards == [(job, job) for job in JOBS], f"skills page cards {cards} don't match the job pages {JOBS}")
for job in JOBS:
    check(f'<body class="j-{job}">' in read(f"skills/{job}/index.html"), f"{job}: page colour class missing")
agent_cards = re.findall(r'<a class="job-card j-together" href="(\w+)/">', read("agents/index.html"))
check(agent_cards == AGENT_PAGES, f"agents page cards {agent_cards} don't match the agent pages {AGENT_PAGES}")
for old, new in MOVED.items():
    check(f'url=../{new}/"' in read(f"{old}/index.html"), f"{old}/: should redirect to {new}/")

# ---- Skill pages: a tab per team, each with one request and one real run ------
shown_runs = []
for job in JOBS:
    page = read(f"skills/{job}/index.html")
    panels = re.split(r'<div class="team-panel p-(\w+)">', page)[1:]
    check([t for t in panels[0::2]] == TEAMS, f"{job}: team tabs should be {TEAMS}")
    for team, panel in zip(panels[0::2], panels[1::2]):
        check(len(re.findall(r"data-example=", panel)) == 1 and len(re.findall(r"data-run=", panel)) == 1,
              f"{job}/{team}: needs exactly one request and one run")
        check(f'class="l-{team}"' in page and f'class="t-{team}"' in page, f"{job}/{team}: tab button missing")
    shown_runs += re.findall(r'data-run="([^"]+)"', page)
skill_folders = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "skills", "*", "*")) if os.path.isdir(p))
check(sorted(shown_runs) == skill_folders, f"every skill should be on a page once:\n  pages: {sorted(shown_runs)}\n  repo:  {skill_folders}")


# ---- What we gave the AI == the repo's example files --------------------------
def example_parts(path):
    text = open(os.path.join(ROOT, path), encoding="utf-8").read()
    if "## User prompt" not in text:
        return None, None  # test-fix-loop-agent is a program: started by a command, not asked
    prompt = re.search(r"## User prompt\s+((?:>.*\n?)+)", text).group(1)
    prompt = squash(re.sub(r"^>\s?", "", prompt, flags=re.M))
    block = re.search(r"```text\n(.*?)\n```", text, re.S)
    # root-cause-investigator has an "Evidence packet" section instead of a text block
    block = block or re.search(r"## Evidence packet\n\n(.*?)\n\n## ", text, re.S)
    return prompt, block.group(1) if block else None


examples = {}  # run name -> example file, for the run header check below
commands = {}  # run name -> the command shown, for a program run
for name in RUN_PAGES:
    job = os.path.dirname(name)
    page = read(name)
    blocks = re.findall(r'data-example="([^"]+)">(.*?)</(?:section|div)>', page, re.S)
    check(blocks, f"{job}: no request shown")
    for path, block in blocks:
        prompt, evidence = example_parts(path)
        if prompt is None:
            command = re.findall(r'<p class="prompt command">(.*?)</p>', block, re.S)
            check(len(command) == 1, f"{job}: {path} needs the one command that started it")
            commands[os.path.basename(os.path.dirname(os.path.dirname(path)))] = plain(command[0]) if command else None
            continue
        shown = [squash(plain(p)) for p in re.findall(r'<p class="prompt">(.*?)</p>', block, re.S)]
        check(shown == [prompt], f"{job}: request differs from {path}\n  page: {shown}\n  file: {prompt}")
        for pre in re.findall(r'<pre class="evidence">(.*?)</pre>', block, re.S):
            check(plain(pre) == evidence, f"{job}: background differs from {path}")
    # A second run of the same skill is named <skill>--<example file name>, and owns that example.
    page_runs = re.findall(r'data-run="([^"]+)"', page)
    owned = {f"/{r.replace('--', '/examples/')}.md" for r in page_runs if "--" in r}
    for run in page_runs:
        skill, _, example = run.partition("--")
        matching = [p for p, _ in blocks if f"/{skill}/" in p
                    and (p.endswith(f"/{example}.md") if example else not any(p.endswith(o) for o in owned))]
        check(len(matching) == 1, f"{job}: run {run} has no matching example file")
        examples[run] = matching[0] if matching else None

# ---- The recorded runs ---------------------------------------------------------
missing = [run for run in examples if not os.path.isfile(os.path.join(HERE, "runs", f"{run}.md"))]
check(not missing, "recorded runs not added yet: " + ", ".join(f"web/runs/{r}.md" for r in missing))

# ponytail: needs node to run the JavaScript; skipped (with a note) without it.
RUN_CHECK = r"""
const fs = require("fs");
global.Markdown = require("./web/markdown.js");
const Runs = require("./web/run.js");
const out = {};
for (const name of JSON.parse(process.argv[1])) {
  const { meta, turns } = Runs.parse(fs.readFileSync(`web/runs/${name}.md`, "utf8"));
  out[name] = { meta, turns: turns.map((t) => {
    if (t.who === "YOU") return { who: t.who, text: t.text };
    const tree = Markdown.tree(t.text);
    const shown = tree.map(Markdown.textOf).join("");
    // The same, with `code` blanked: a code snippet may quote "# export" on purpose.
    const noCode = (n) => typeof n === "string" ? n : n.tag === "code" ? { ...n, children: ["·"] } : { ...n, children: n.children.map(noCode) };
    const prose = tree.map(noCode).map(Markdown.textOf).join("");
    return { who: t.who, text: t.text, shown, prose };
  }) };
}
console.log(JSON.stringify(out));
"""
MD_CHECK = r"""
const M = require("./web/markdown.js");
const t = M.tree("> quoted **bold**\n\n```\n| x |\n**raw**\n```\nsee `PRD.md`\n```markdown\n## Goals\n```");
const s = JSON.stringify(t);
if (!s.includes('"blockquote"') || !s.includes('"pre","children":["| x |\\n**raw**"]') || !s.includes('"code","children":["PRD.md"]')
    || !s.includes('"cls":"md-doc","children":[{"tag":"h3","children":["Goals"]}]')) {
  console.error(s); process.exit(1);
}
"""
# count.js sends only the page's address (and a cache-buster), only from the live site.
COUNT_CHECK = r"""
const C = require("./web/count.js");
const u = new URL(C.url("/k_ai-agent-skills/web/"));
const ok = u.origin === "https://khadir-syed.goatcounter.com" && u.pathname === "/count"
  && [...u.searchParams.keys()].sort().join() === "p,rnd" && u.searchParams.get("p") === "/k_ai-agent-skills/web/"
  && C.isLiveSite("khadir-syed.github.io")
  && !["localhost", "127.0.0.1", "github.io.evil.example"].some(C.isLiveSite);
if (!ok) { console.error(u.href); process.exit(1); }
"""
words = lambda text: re.findall(r"[\w']+", text)
present = [run for run in examples if run not in missing]
if shutil.which("node"):
    r = subprocess.run(["node", "-e", MD_CHECK], cwd=ROOT, capture_output=True, text=True)
    check(r.returncode == 0, f"markdown.js self-check failed: {r.stderr}")
    r = subprocess.run(["node", "-e", COUNT_CHECK], cwd=ROOT, capture_output=True, text=True)
    check(r.returncode == 0, f"count.js self-check failed: {r.stderr}")
    if present:
        r = subprocess.run(["node", "-e", RUN_CHECK, json.dumps(present)], cwd=ROOT, capture_output=True, text=True)
        check(r.returncode == 0, f"reading the runs failed: {r.stderr}")
        runs = json.loads(r.stdout) if r.returncode == 0 else {}
        for name, run in runs.items():
            meta, turns = run["meta"], run["turns"]
            check(re.fullmatch(r"\d{4}-\d\d-\d\d", meta.get("Date", "")), f"{name}: Date must look like 2026-09-27")
            check(meta.get("Tool") and meta.get("Model"), f"{name}: Tool and Model lines are needed")
            check(meta.get("Example") == examples[name], f"{name}: Example should be {examples[name]}")
            check(any(t["who"] == "AI" for t in turns), f"{name}: no AI answer in the run")
            if name in commands:
                check(turns and f"$ {commands[name]}" in turns[0]["text"],
                      f"{name}: the command on the page isn't the one the run shows")
            for t in turns:
                if t["who"] == "YOU":
                    continue
                # Formatting may drop symbols (and "1." list numbers, which the page
                # numbers itself), never words; and no raw symbols may show.
                source = re.sub(r"(?m)^\s*\d+\.\s", " ", t["text"])
                check(words(t["shown"]) == words(re.sub(r"```\w*|<br\s*/?>|[`*#|>]", " ", source)),
                      f"{name}: formatting changed the words of a turn")
                shown_lines = [line.strip() for line in t["prose"].split("\n")]
                # (a "#" table heading is fine; "# Title" is an unformatted heading)
                check(not any(re.match(r"#{1,6}\s|\||```", line) for line in shown_lines),
                      f"{name}: raw Markdown symbols left on screen")
        # Each agent page's picture gives a number of stops: the real runs must agree.
        pictured = {"feature-launch-readiness-agent-controlled": 3, "feature-launch-readiness-agent-autonomous": 1,
                    "content-publish-readiness-agent-controlled": 3, "content-publish-readiness-agent-autonomous": 1,
                    "bug-fix-agent": 2, "test-fix-loop-agent": 0,
                    "request-router-agent-controlled": 1, "request-router-agent-autonomous": 0}
        for name, want in pictured.items():
            if name in runs:
                got = sum(t["who"] == "YOU" for t in runs[name]["turns"])
                check(got == want, f"{name} stopped {got} times; its page's picture says {want}")
        # An orchestrator may only hand work to a real agent from its own list,
        # and the autonomous one must warn before its no-asking Software path runs.
        agents = {os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "agents", "*", "*"))}
        warning = "From here, this will run to completion with no further approval requests"
        for name in [n for n in runs if n.startswith("request-router-")]:
            skill, _, example = name.partition("--")
            said = "\n".join(t["text"] for t in runs[name]["turns"] if t["who"] == "AI")
            allowed = set(re.findall(r"^## .*?([a-z-]+-agent\S*)|`([a-z-]+-agent[a-z-]*)`",
                                     open(os.path.join(ROOT, "orchestrators", skill, "references", "target-agents.md"),
                                          encoding="utf-8").read(), re.M))
            allowed = {a for pair in allowed for a in pair if a} & agents
            named = set(re.findall(r"\b[a-z]+(?:-[a-z]+)*-agent(?:-controlled|-autonomous)?\b", said)) - {skill}
            # An unclear request must not be handed to anyone: it may only mention options.
            check((named or example) and named <= allowed,
                  f"{name}: hands work to {sorted(named)}; its list allows {sorted(allowed)}")
            if example == "ambiguous-request":
                # It must say it can't tell, end on its question, and never start the no-asking path.
                turns = runs[name]["turns"]
                check("Unclear" in said and turns and turns[-1]["who"] == "AI" and "?" in turns[-1]["text"],
                      f"{name}: must call the request Unclear and end by asking which one you meant")
                check(all(t["who"] == "AI" for t in turns) and warning not in said,
                      f"{name}: must stop at its question, with nothing run or handed over")
        said = "\n".join(t["text"] for t in runs.get("request-router-agent-autonomous", {"turns": []})["turns"])
        check(not said or (warning in said and said.index(warning) < said.find("completed")),
              "request-router-agent-autonomous: its warning must come before the result")
else:
    print("(node not installed: skipped the run-formatting checks)")

if problems:
    print(f"{len(problems)} problem(s):")
    for p in problems:
        print(" -", p)
    raise SystemExit(1)
print(f"All web checks passed ({len(PAGES)} pages, {len(present)} recorded runs).")
