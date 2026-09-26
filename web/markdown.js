// A tiny Markdown formatter for the recorded AI runs. AI tools write their
// answers with formatting symbols (## heading, **bold**, | tables |); this
// turns them into headings, bold text, lists and tables.
// (Copied from k_ai-basics web/07/markdown.js, plus code blocks, `code`,
// > quotes and ```markdown file drafts, which agent runs use.)
//
// Safe by design: it never turns text into HTML. It builds a small tree of
// allowed tags, and every piece of text goes into the page as plain text.
// ponytail: only the Markdown the saved runs use (headings, bold, italic,
// code, quotes, lists, dividers, tables, <br>); anything else shows as plain text.
"use strict";

const Markdown = (() => {
  const INLINE = /(`[^`]+`|\*\*[^*]+?\*\*|\*[^*\s][^*]*?\*|<br\s*\/?>)/i;

  function inline(text) {
    const out = [];
    for (const part of text.split(INLINE)) {
      if (!part) continue;
      if (/^`.+`$/.test(part)) out.push({ tag: "code", children: [part.slice(1, -1)] });
      else if (/^<br/i.test(part)) out.push({ tag: "br", children: [] });
      else if (/^\*\*.+\*\*$/.test(part)) out.push({ tag: "strong", children: [part.slice(2, -2)] });
      else if (/^\*.+\*$/.test(part)) out.push({ tag: "em", children: [part.slice(1, -1)] });
      else out.push(part.replace(/\*\*/g, "")); // an unclosed ** (an answer cut off mid-word)
    }
    return out;
  }

  const cells = (row) => row.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((c) => c.trim());
  const isRule = (row) => /^\|[\s:|-]+\|$/.test(row.trim());

  function table(rows) {
    const body = rows.filter((r) => !isRule(r));
    const hasHead = rows.length > 1 && isRule(rows[1]);
    const makeRow = (row, cellTag) => ({
      tag: "tr", children: cells(row).map((c) => ({ tag: cellTag, children: inline(c) })),
    });
    const parts = [];
    if (hasHead) parts.push({ tag: "thead", children: [makeRow(body.shift(), "th")] });
    parts.push({ tag: "tbody", children: body.map((r) => makeRow(r, "td")) });
    // The wrapper scrolls sideways on a phone, so wide tables never break the page.
    return { tag: "div", cls: "md-table", children: [{ tag: "table", children: parts }] };
  }

  // Turn Markdown text into a tree: { tag, cls?, start?, children: [text or tree] }.
  function tree(text) {
    const out = [];
    const lines = text.split("\n");
    let para = null; // the paragraph being filled
    let list = null; // the list being filled
    let item = null; // its last item (nested lists and follow-on lines go here)
    let sub = null; // the nested list inside that item
    const endBlock = () => { para = list = item = sub = null; };

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const t = line.trim();
      const indent = line.length - line.trimStart().length;
      let m;
      if (!t) {
        para = null; // a blank line ends a paragraph, but a list can carry on
      } else if (t.startsWith("```")) {
        endBlock();
        const lang = t.slice(3).trim().toLowerCase();
        const code = [];
        while (++i < lines.length && !lines[i].trim().startsWith("```")) code.push(lines[i]);
        // A ```markdown block is a file the AI wants to save: show it formatted,
        // like a page. Any other code block stays exactly as written.
        if (lang === "markdown" || lang === "md") out.push({ tag: "div", cls: "md-doc", children: tree(code.join("\n")) });
        else out.push({ tag: "pre", children: [code.join("\n")] });
      } else if (t.startsWith(">")) {
        endBlock();
        const quote = [];
        while (i < lines.length && lines[i].trim().startsWith(">")) quote.push(lines[i++].trim().replace(/^>\s?/, ""));
        i--;
        out.push({ tag: "blockquote", children: tree(quote.join("\n")) });
      } else if ((m = t.match(/^(#{1,6})\s+(.*)$/))) {
        endBlock();
        out.push({ tag: m[1].length <= 2 ? "h3" : "h4", children: inline(m[2]) });
      } else if (/^(-{3,}|\*{3,}|_{3,})$/.test(t)) {
        endBlock();
        out.push({ tag: "hr", children: [] });
      } else if (t.startsWith("|")) {
        endBlock();
        const rows = [];
        while (i < lines.length && lines[i].trim().startsWith("|")) rows.push(lines[i++]);
        i--;
        out.push(table(rows));
      } else if ((m = t.match(/^([-*+]|(\d+)\.)\s+(.*)$/))) {
        para = null;
        const tag = m[2] ? "ol" : "ul";
        const li = { tag: "li", children: inline(m[3]) };
        if (indent > 0 && item) {
          if (!sub || sub.tag !== tag) {
            sub = { tag, children: [] };
            item.children.push(sub);
          }
          sub.children.push(li);
        } else {
          if (!list || list.tag !== tag) {
            list = { tag, children: [] };
            if (m[2] && m[2] !== "1") list.start = Number(m[2]);
            out.push(list);
          }
          list.children.push(li);
          item = li;
          sub = null;
        }
      } else if (indent > 0 && item) {
        item.children.push({ tag: "br", children: [] }, ...inline(t));
      } else {
        list = item = sub = null;
        if (para) para.children.push({ tag: "br", children: [] });
        else out.push((para = { tag: "p", children: [] }));
        para.children.push(...inline(t));
      }
    }
    return out;
  }

  // Build real page elements from the tree. Text only ever becomes text nodes.
  function toDom(node) {
    if (typeof node === "string") return document.createTextNode(node);
    const el = document.createElement(node.tag);
    if (node.cls) el.className = node.cls;
    if (node.start) el.start = node.start;
    for (const child of node.children) el.append(toDom(child));
    return el;
  }

  // The words in a tree, for the self-check in web/test_web.py.
  const BLOCKS = new Set(["p", "h3", "h4", "li", "tr", "th", "td", "br", "hr", "div", "ul", "ol", "pre", "blockquote"]);
  function textOf(node) {
    if (typeof node === "string") return node;
    const inner = node.children.map(textOf).join("");
    return BLOCKS.has(node.tag) ? `\n${inner}\n` : inner;
  }

  return { tree, toDom, textOf };
})();

if (typeof module === "object") module.exports = Markdown; // lets node run the self-check
