// Cookie-free visit counting with GoatCounter (https://www.goatcounter.com).
// Sends only the page's address (like /k_ai-agent-skills/web/skills/find/),
// and only from the live github.io site. We don't load GoatCounter's own
// script: the pages' CSP allows only this site's scripts.
"use strict";

const Count = (() => {
  const ENDPOINT = "https://khadir-syed.goatcounter.com/count";

  function url(path) {
    const q = new URLSearchParams({ p: path, rnd: Math.random().toString(36).slice(2) });
    return `${ENDPOINT}?${q}`;
  }

  const isLiveSite = (host) => host.endsWith(".github.io"); // local testing never counts

  function page() {
    if (!isLiveSite(location.hostname)) return false;
    try { return navigator.sendBeacon(url(location.pathname)); } catch { return false; }
  }

  return { url, isLiveSite, page };
})();

if (typeof module === "object") module.exports = Count; // lets node run the self-check
else Count.page();
