#!/usr/bin/env node

const CRYPTO_PATTERNS = [
  /\bcrypto\b/i,
  /\bbitcoin\b/i,
  /\beth\b/i,
  /\bethereum\b/i,
  /\bweb3\b/i,
  /\bnft\b/i,
  /\btoken\b/i,
  /\bdefi\b/i,
  /\bsolana\b/i,
  /\bxrp\b/i,
  /\bdogecoin\b/i,
];

const TOPICS = {
  tech: {
    boost: [
      /\bcompiler(s)?\b/i,
      /\brust\b/i,
      /\bgo\b/i,
      /\bjavascript\b/i,
      /\btypescript\b/i,
      /\bbuild\b/i,
      /\bperformance\b/i,
      /\bprofil(e|ing)\b/i,
      /\bdistributed\b/i,
      /\bkernel\b/i,
      /\bnetwork\b/i,
      /\bsecurity\b/i,
      /\bdatabase\b/i,
      /\bpostgres\b/i,
      /\bsqlite\b/i,
      /\bllm(s)?\b/i,
      /\bai\b/i,
      /\bopen source\b/i,
    ],
  },
  health: {
    boost: [
      /\bhealth\b/i,
      /\bfitness\b/i,
      /\bsleep\b/i,
      /\bnutrition\b/i,
      /\bprotein\b/i,
      /\bcardio\b/i,
      /\blongevity\b/i,
      /\bmetabolism\b/i,
      /\bclinical\b/i,
      /\btrial\b/i,
      /\bstudy\b/i,
    ],
  },
  hacking: {
    boost: [
      /\bhack(ing)?\b/i,
      /\breverse engineering\b/i,
      /\bexploit\b/i,
      /\bvulnerabilit(y|ies)\b/i,
      /\bcve-\d{4}-\d+/i,
      /\bsecurity\b/i,
      /\bmalware\b/i,
      /\bphishing\b/i,
      /\bctf\b/i,
      /\bpwn\b/i,
    ],
  },
  lifehacks: {
    boost: [
      /\bhack\b/i,
      /\bhow to\b/i,
      /\bguide\b/i,
      /\btips\b/i,
      /\bworkflow\b/i,
      /\bhabit\b/i,
      /\bproductivity\b/i,
      /\bkeyboard\b/i,
      /\bshortcut\b/i,
      /\bchecklist\b/i,
    ],
  },
};

function parseArgs(argv) {
  const args = {
    count: 5,
    offset: 0,
    topic: "tech",
    format: "json",
  };

  for (let i = 0; i < argv.length; i++) {
    const token = argv[i];

    if (token === "--count") {
      const value = argv[++i];
      const parsed = Number.parseInt(value, 10);
      if (Number.isFinite(parsed) && parsed > 0 && parsed <= 30) args.count = parsed;
      continue;
    }

    if (token === "--offset") {
      const value = argv[++i];
      const parsed = Number.parseInt(value, 10);
      if (Number.isFinite(parsed) && parsed >= 0 && parsed <= 200) args.offset = parsed;
      continue;
    }

    if (token === "--topic") {
      const value = (argv[++i] ?? "").toLowerCase();
      if (value === "life" || value === "lifehacks") args.topic = "lifehacks";
      else if (value in TOPICS) args.topic = value;
      continue;
    }

    if (token === "--format") {
      const value = (argv[++i] ?? "").toLowerCase();
      if (value === "json" || value === "text") args.format = value;
      continue;
    }
  }

  return args;
}

function isCrypto(text) {
  return CRYPTO_PATTERNS.some((re) => re.test(text));
}

function topicBoostScore(title, topic) {
  const patterns = TOPICS[topic]?.boost ?? [];
  let score = 0;
  for (const re of patterns) {
    if (re.test(title)) score += 1;
  }
  return score;
}

function hnItemLink(hit) {
  return `https://news.ycombinator.com/item?id=${hit.objectID}`;
}

function ageTextFromUnixSeconds(createdAtSeconds, nowSeconds) {
  const deltaSeconds = Math.max(0, nowSeconds - createdAtSeconds);
  if (deltaSeconds < 60) return "just now";
  const minutes = Math.floor(deltaSeconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 48) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

async function fetchFrontPage() {
  const url = "https://hn.algolia.com/api/v1/search?tags=front_page";
  const res = await fetch(url, {
    headers: {
      "accept": "application/json",
      "user-agent": "clawdbot-hn-digest/1.0",
    },
  });
  if (!res.ok) throw new Error(`HN request failed: ${res.status} ${res.statusText}`);
  return res.json();
}

function rank(hits, topic) {
  // Simple heuristic: points and comments matter, plus a small topic boost.
  // Keep it deterministic and cheap; the LLM can do the final taste/selection.
  return hits
    .filter((hit) => hit && typeof hit.title === "string")
    .filter((hit) => !isCrypto(hit.title) && !isCrypto(hit.url ?? ""))
    .map((hit) => {
      const points = Number.isFinite(hit.points) ? hit.points : 0;
      const comments = Number.isFinite(hit.num_comments) ? hit.num_comments : 0;
      const createdAt = Number.isFinite(hit.created_at_i) ? hit.created_at_i : null;
      const nowSeconds = Math.floor(Date.now() / 1000);
      const age = createdAt ? ageTextFromUnixSeconds(createdAt, nowSeconds) : "";
      const boost = topicBoostScore(hit.title, topic);
      const score = points * 1.0 + comments * 0.6 + boost * 10;
      return {
        id: String(hit.objectID),
        title: hit.title,
        hnLink: hnItemLink(hit),
        age,
        comments,
        score,
      };
    })
    .sort((a, b) => b.score - a.score);
}

function print(items, format) {
  if (format === "text") {
    for (const item of items) {
      const meta = item.age ? `${item.age} · ${item.comments} comments` : `${item.comments} comments`;
      process.stdout.write(`${item.title}\n${meta}\n${item.hnLink}\n\n`);
    }
    return;
  }

  process.stdout.write(JSON.stringify({ items }, null, 2));
  process.stdout.write("\n");
}

async function main() {
  const { count, offset, topic, format } = parseArgs(process.argv.slice(2));

  const data = await fetchFrontPage();
  const hits = Array.isArray(data?.hits) ? data.hits : [];
  const ranked = rank(hits, topic).slice(offset, offset + count);

  print(ranked, format);
}

main().catch((err) => {
  process.stderr.write(String(err?.stack ?? err));
  process.stderr.write("\n");
  process.exitCode = 1;
});
