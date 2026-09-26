// Shows the real AI runs saved in web/runs/, formatted by markdown.js.
//
// A run file starts with header lines (Date, Tool, Model, Example), then a
// blank line, then the AI's reply exactly as it came (personal details taken
// out). A run with several turns marks each one with a line of its own:
//   === AI ===            what the AI said
//   === YOU ===           what you typed back
//   === FILE <name> ===   a file the AI saved
// Nothing is sent anywhere: the page only reads this repo's own files and
// never talks to an AI. All page text is in each index.html.
"use strict";

const Runs = (() => {
  const MARK = /^=== (AI|YOU|FILE)(?: (.+?))? ===$/;
  // runs/ sits next to this script, however deep the page is.
  const RUNS = typeof document === "object" ? new URL("runs/", document.currentScript.src) : null;

  function parse(text) {
    text = text.replace(/\r\n/g, "\n");
    const split = text.indexOf("\n\n");
    const meta = {};
    for (const line of text.slice(0, split).split("\n")) {
      const m = line.match(/^(\w+):\s*(.*)$/);
      if (m) meta[m[1]] = m[2].trim();
    }
    const turns = [];
    let turn = { who: "AI", name: "", lines: [] };
    const keep = () => { if (turn.lines.join("").trim()) turns.push({ ...turn, text: turn.lines.join("\n").trim() }); };
    for (const line of text.slice(split + 2).split("\n")) {
      const m = line.trim().match(MARK);
      if (m) {
        keep();
        turn = { who: m[1], name: m[2] || "", lines: [] };
      } else {
        turn.lines.push(line);
      }
    }
    keep();
    return { meta, turns };
  }

  // "2026-09-27" → "27 September 2026"
  function niceDate(iso) {
    const d = new Date(`${iso}T12:00:00Z`);
    return isNaN(d) ? iso : d.toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric", timeZone: "UTC" });
  }

  // The first part of a long answer, the rest behind "Show all" (the cut
  // itself is in style.css). An answer only a little longer than the cut is
  // shown in full: hiding a few lines behind a button isn't worth the click.
  // Measured once the answer is on screen: a team tab that isn't picked yet
  // is hidden and has no height.
  function answerBox(text, labels) {
    const box = document.createElement("div");
    box.className = "answer";
    const md = document.createElement("div");
    md.className = "md clamped";
    md.append(...Markdown.tree(text).map(Markdown.toDom));
    box.append(md);
    const seen = new ResizeObserver(() => {
      if (!md.clientHeight) return;
      seen.disconnect();
      if (md.scrollHeight <= md.clientHeight * 1.5) { md.classList.remove("clamped"); return; }
      const more = document.createElement("button");
      more.type = "button";
      more.className = "more-btn";
      more.textContent = labels.show;
      more.setAttribute("aria-expanded", "false");
      more.addEventListener("click", () => {
        const open = md.classList.toggle("clamped") === false;
        more.textContent = open ? labels.less : labels.show;
        more.setAttribute("aria-expanded", String(open));
        if (!open) more.scrollIntoView({ block: "nearest" }); // don't leave the reader far below
      });
      box.append(more);
    });
    seen.observe(md);
    return box;
  }

  function show(el, run) {
    const labels = el.dataset;
    const { meta, turns } = run;
    el.querySelector(".run-meta").textContent =
      `${labels.recorded} ${niceDate(meta.Date)} · ${meta.Model} (${meta.Tool}). ${labels.vary}`;
    const list = el.querySelector(".turns");
    for (const t of turns) {
      const li = document.createElement("li");
      li.className = `turn turn-${t.who.toLowerCase()}`;
      const who = document.createElement("p");
      who.className = "turn-who";
      who.textContent = t.who === "YOU" ? labels.you : t.who === "FILE" ? `${labels.file} ` : labels.ai;
      if (t.who === "FILE") {
        const name = document.createElement("span");
        name.className = "file-name"; // keeps the file name's real spelling
        name.textContent = t.name;
        who.append(name);
      }
      li.append(who);
      if (t.who === "YOU") {
        const said = document.createElement("p");
        said.className = "you-said";
        said.textContent = t.text;
        li.append(said);
      } else {
        li.append(answerBox(t.text, labels));
      }
      list.append(li);
    }
    const stops = el.querySelector(".stops");
    const asked = turns.filter((t) => t.who === "YOU").length;
    if (stops) stops.textContent = asked === 0 && labels.stopsNone ? labels.stopsNone : asked === 1 ? labels.stopsOne : labels.stops.replace("{n}", asked);
  }

  async function loadAll() {
    for (const el of document.querySelectorAll(".run[data-run]")) {
      const status = el.querySelector(".run-status");
      try {
        const res = await fetch(new URL(`${el.dataset.run}.md`, RUNS));
        if (res.status === 404) { status.textContent = el.dataset.missing; continue; }
        if (!res.ok) throw new Error(`${el.dataset.run}: ${res.status}`);
        show(el, parse(await res.text()));
        status.textContent = "";
      } catch (err) {
        status.textContent = el.dataset.failed;
        console.error(err);
      }
    }
  }

  return { parse, loadAll };
})();

if (typeof module === "object") module.exports = Runs; // lets node run the self-check
else document.addEventListener("DOMContentLoaded", Runs.loadAll);
