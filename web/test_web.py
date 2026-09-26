"""Self-check for the web pages: every request shown on a page must be exactly
the one in the repo's example file, every recorded run must be labelled and
format cleanly, and the pages must stay safe. Runs instantly, no network.
Run from the repo root with: python3 web/test_web.py
"""
import html
import json
import os
import re
import shutil
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPO_URL = "https://github.com/khadir-syed/k_ai-agent-skills/tree/main/"
JOBS = ["find", "draft", "check", "together"]
PAGES = ["index.html"] + [f"{job}/index.html" for job in JOBS]
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
for name in PAGES + ["../index.html"]:
    page = read(name)
    csp = re.search(r'http-equiv="Content-Security-Policy"\s+content="([^"]+)"', page)
    check(csp and "default-src 'none'" in csp.group(1), f"{name}: strict Content-Security-Policy missing")
    if csp and "script-src" in csp.group(1):
        check("script-src 'self';" in csp.group(1), f"{name}: scripts may only come from this site")
    check(not re.search(r"<script(?![^>]*\bsrc=)[^>]*>", page), f"{name}: inline <script> found")
    check(not re.search(r'<script[^>]*src="(https?:)?//', page), f"{name}: script from another site")
    check(" style=" not in page, f"{name}: inline style= found (the CSP blocks it)")
    check(not re.search(r"\son[a-z]+=", page), f"{name}: inline event handler found")
    # Every link to this site's own files must lead somewhere real.
    folder = os.path.dirname(os.path.join(HERE, name))
    for target in re.findall(r'(?:href|src)="([^"#:]+)"', page):
        path = os.path.normpath(os.path.join(folder, html.unescape(target)))
        if os.path.isdir(path):
            path = os.path.join(path, "index.html")
        check(os.path.isfile(path), f"{name}: broken link {target}")
    # Links to the repo on GitHub must point at folders that exist.
    for target in re.findall(r'href="' + re.escape(REPO_URL) + r'([^"#]+)"', page):
        check(os.path.isdir(os.path.join(ROOT, target)), f"{name}: GitHub link to missing folder {target}")

# ---- Home: one card per job page, in story order ------------------------------
cards = re.findall(r'<a class="job-card j-(\w+)" href="(\w+)/">', read("index.html"))
check(cards == [(job, job) for job in JOBS], f"home cards {cards} don't match the job pages {JOBS}")
for job in JOBS:
    check(f'<body class="j-{job}">' in read(f"{job}/index.html"), f"{job}: page colour class missing")


# ---- What we gave the AI == the repo's example files --------------------------
def example_parts(path):
    text = open(os.path.join(ROOT, path), encoding="utf-8").read()
    prompt = re.search(r"## User prompt\s+((?:>.*\n?)+)", text).group(1)
    prompt = squash(re.sub(r"^>\s?", "", prompt, flags=re.M))
    block = re.search(r"```text\n(.*?)\n```", text, re.S)
    return prompt, block.group(1) if block else None


examples = {}  # run name -> example file, for the run header check below
for job in JOBS:
    page = read(f"{job}/index.html")
    blocks = re.findall(r'data-example="([^"]+)">(.*?)</(?:section|div)>', page, re.S)
    check(blocks, f"{job}: no request shown")
    for path, block in blocks:
        prompt, evidence = example_parts(path)
        shown = [squash(plain(p)) for p in re.findall(r'<p class="prompt">(.*?)</p>', block, re.S)]
        check(shown == [prompt], f"{job}: request differs from {path}\n  page: {shown}\n  file: {prompt}")
        for pre in re.findall(r'<pre class="evidence">(.*?)</pre>', block, re.S):
            check(plain(pre) == evidence, f"{job}: background differs from {path}")
    for run in re.findall(r'data-run="([^"]+)"', page):
        matching = [p for p, _ in blocks if f"/{run}/" in p]
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
    const shown = Markdown.tree(t.text).map(Markdown.textOf).join("");
    return { who: t.who, text: t.text, shown };
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
words = lambda text: re.findall(r"[\w']+", text)
present = [run for run in examples if run not in missing]
if shutil.which("node"):
    r = subprocess.run(["node", "-e", MD_CHECK], cwd=ROOT, capture_output=True, text=True)
    check(r.returncode == 0, f"markdown.js self-check failed: {r.stderr}")
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
            for t in turns:
                if t["who"] == "YOU":
                    continue
                # Formatting may drop symbols (and "1." list numbers, which the page
                # numbers itself), never words; and no raw symbols may show.
                source = re.sub(r"(?m)^\s*\d+\.\s", " ", t["text"])
                check(words(t["shown"]) == words(re.sub(r"```\w*|<br\s*/?>|[`*#|>]", " ", source)),
                      f"{name}: formatting changed the words of a turn")
                shown_lines = [line.strip() for line in t["shown"].split("\n")]
                # (a "#" table heading is fine; "# Title" is an unformatted heading)
                check(not any(re.match(r"#{1,6}\s|\||```", line) for line in shown_lines),
                      f"{name}: raw Markdown symbols left on screen")
        # The picture on the agents page says 3 stops vs 1 stop: the real runs must agree.
        stops = {name: sum(t["who"] == "YOU" for t in run["turns"]) for name, run in runs.items()}
        if "feature-launch-readiness-agent-controlled" in stops:
            check(stops["feature-launch-readiness-agent-controlled"] >= 3,
                  f"controlled run stopped {stops['feature-launch-readiness-agent-controlled']} times; the page says 3")
        if "feature-launch-readiness-agent-autonomous" in stops:
            check(stops["feature-launch-readiness-agent-autonomous"] == 1,
                  f"autonomous run stopped {stops['feature-launch-readiness-agent-autonomous']} times; the page says 1")
else:
    print("(node not installed: skipped the run-formatting checks)")

if problems:
    print(f"{len(problems)} problem(s):")
    for p in problems:
        print(" -", p)
    raise SystemExit(1)
print(f"All web checks passed ({len(PAGES)} pages, {len(present)} recorded runs).")
