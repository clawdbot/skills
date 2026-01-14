#!/usr/bin/env node

function readStdin() {
  return new Promise((resolve, reject) => {
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => (data += chunk));
    process.stdin.on("end", () => resolve(data));
    process.stdin.on("error", reject);
  });
}

function pickEasterEggs(items) {
  const eggs = [];

  // Always: banana sticker (Nano Banana) + subtle lion cameo.
  eggs.push("a tiny banana sticker hidden on the laptop");
  eggs.push("a small friendly lion figurine on a shelf");

  const titles = items.map((i) => String(i.title || "")).join(" \n ");

  if (/performance|gap|\bfast\b|\bbenchmark\b/i.test(titles)) {
    eggs.push("a comically oversized speedometer with the needle pegged, surrounded by hundreds of tiny sparkles (hinting at a huge speedup)"
    );
  }

  if (/github|object|id\b|identifier/i.test(titles)) {
    eggs.push(
      "a blueprint page filled with paired geometric tokens (two different shapes per item), suggesting 'two IDs' without using any logos or text"
    );
  }

  if (/management|team|anti-pattern/i.test(titles)) {
    eggs.push(
      "a whiteboard with simple stick-figure team diagrams and a few playful 'anti-pattern' doodles (no words)"
    );
  }

  // Keep it to ~3-4 eggs.
  return eggs.slice(0, 4);
}

function main() {
  const args = process.argv.slice(2);
  const topicIndex = args.indexOf("--topic");
  const topic = topicIndex !== -1 ? (args[topicIndex + 1] || "tech") : "tech";

  readStdin()
    .then((raw) => {
      const parsed = JSON.parse(raw);
      const items = Array.isArray(parsed?.items) ? parsed.items : [];
      const eggs = pickEasterEggs(items);

      const postObjects = items.slice(0, 5).map((item) => {
        const title = String(item.title || "");
        // Convert title to a visual object hint, but keep it general.
        if (/performance|gap|\bfix\b/i.test(title)) return "a performance graph and a pile of neatly cut paper strips (hinting at a small fix)";
        if (/github|object|id\b/i.test(title)) return "abstract geometric ID tokens and a tidy diagram";
        if (/management|team|anti-pattern/i.test(title)) return "a simple team flow diagram on a whiteboard";
        return "a curious gadget or schematic related to modern tech";
      });

      const prompt = [
        "Cartoony editorial illustration, bright clean colors, playful but thoughtful mood.",
        "Scene: a cozy developer workshop desk with warm lighting, inviting and delightful.",
        "Main vibe: practical engineering deep dives, systems/tooling internals, and curious tinkering.",
        `Theme focus: Hacker News front page (${topic}).`,
        "Include visual references inspired by these post themes (no text, no logos):",
        ...postObjects.map((o) => `- ${o}`),
        "Add 3-4 subtle Easter eggs to reward close inspection (no text):",
        ...eggs.map((e) => `- ${e}`),
        "Constraints: no text, no brand logos, no crypto imagery, not dark/menacing.",
        "Style: 2D cartoon, crisp linework, soft shading, high detail.",
      ].join("\n");

      process.stdout.write(prompt);
      process.stdout.write("\n");
    })
    .catch((err) => {
      process.stderr.write(String(err?.stack ?? err));
      process.stderr.write("\n");
      process.exitCode = 1;
    });
}

main();
