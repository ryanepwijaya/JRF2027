// Tombol "Sinkronkan" → cek PIN → jalankan routine Claude (tarik Strava & Coros → update data/actuals.json → push → Vercel deploy ulang).
// Env (Vercel): SYNC_PIN, ROUTINE_ID (trig_…), ROUTINE_TOKEN (sk-ant-oat01-…, dibuat di claude.ai/code/routines → API trigger).
const crypto = require("crypto");

const MAX_FAILS = 5;            // salah PIN berturut-turut sebelum dikunci
const LOCK_MS = 15 * 60 * 1000; // lama kunci
const COOLDOWN_MS = 3 * 60 * 1000; // jeda antar-sinkron sukses

const fails = new Map(); // ip -> {n, until}
let lastFire = 0;

const ipOf = req => String(req.headers["x-forwarded-for"] || req.socket?.remoteAddress || "?").split(",")[0].trim();
const same = (a, b) => {
  const x = crypto.createHash("sha256").update(String(a)).digest();
  const y = crypto.createHash("sha256").update(String(b)).digest();
  return crypto.timingSafeEqual(x, y);
};
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function readBody(req) {
  if (req.body && typeof req.body === "object") return req.body;
  if (typeof req.body === "string") { try { return JSON.parse(req.body); } catch { return {}; } }
  let raw = "";
  for await (const c of req) { raw += c; if (raw.length > 2000) break; }
  try { return JSON.parse(raw || "{}"); } catch { return {}; }
}

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") { res.setHeader("Allow", "POST"); return res.status(405).json({ error: "method" }); }

  const { SYNC_PIN, ROUTINE_ID, ROUTINE_TOKEN } = process.env;
  if (!SYNC_PIN) return res.status(503).json({ error: "setup", what: "SYNC_PIN" });

  const ip = ipOf(req), now = Date.now();
  const f = fails.get(ip);
  if (f && f.until > now) return res.status(429).json({ error: "locked", retry: Math.ceil((f.until - now) / 1000) });

  const { pin } = await readBody(req);
  if (!/^\d{6}$/.test(String(pin || "")) || !same(pin, SYNC_PIN)) {
    await sleep(700);
    const n = (f && f.until <= now && f.n >= MAX_FAILS ? 0 : (f?.n || 0)) + 1;
    const rec = { n, until: n >= MAX_FAILS ? now + LOCK_MS : 0 };
    fails.set(ip, rec);
    if (rec.until) return res.status(429).json({ error: "locked", retry: LOCK_MS / 1000 });
    return res.status(401).json({ error: "pin", left: MAX_FAILS - n });
  }
  fails.delete(ip);

  if (!ROUTINE_ID || !ROUTINE_TOKEN) return res.status(503).json({ error: "setup", what: !ROUTINE_ID ? "ROUTINE_ID" : "ROUTINE_TOKEN" });
  if (now - lastFire < COOLDOWN_MS) return res.status(409).json({ error: "busy", retry: Math.ceil((COOLDOWN_MS - (now - lastFire)) / 1000) });

  try {
    const r = await fetch(`https://api.anthropic.com/v1/claude_code/routines/${encodeURIComponent(ROUTINE_ID)}/fire`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${ROUTINE_TOKEN}`,
        "anthropic-version": "2026-10-21",
        "anthropic-beta": "experimental-cc-routine-2026-04-01",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text: `Dipicu dari tombol Sinkronkan di web pada ${new Date().toISOString()}.` })
    });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) {
      const retry = r.headers.get("retry-after");
      return res.status(502).json({ error: "routine", status: r.status, type: j?.error?.type || null, retry: retry ? +retry : null });
    }
    lastFire = now;
    return res.status(200).json({ ok: true, session_url: j.claude_code_session_url || null });
  } catch (e) {
    return res.status(502).json({ error: "network" });
  }
};
