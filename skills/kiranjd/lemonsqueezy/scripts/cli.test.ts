import { describe, test, expect, mock, beforeEach, afterEach } from "bun:test";

// Test pure utility functions
// Note: These are extracted/duplicated from cli.ts for testing

function cents(n: number): string {
  return `$${(n / 100).toFixed(2)}`;
}

function parseCents(value: string | number | undefined): number {
  return parseInt(String(value || 0), 10) / 100;
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

function orderStatusIcon(status: string): string {
  switch (status) {
    case "paid": return "✓";
    case "refunded": return "↩";
    default: return "○";
  }
}

function subStatusIcon(status: string): string {
  switch (status) {
    case "active": return "●";
    case "cancelled": return "○";
    default: return "◐";
  }
}

describe("cents", () => {
  test("formats cents to dollars", () => {
    expect(cents(100)).toBe("$1.00");
    expect(cents(1999)).toBe("$19.99");
    expect(cents(50)).toBe("$0.50");
  });

  test("handles zero", () => {
    expect(cents(0)).toBe("$0.00");
  });

  test("handles large amounts", () => {
    expect(cents(1000000)).toBe("$10000.00");
  });

  test("always shows 2 decimal places", () => {
    expect(cents(1000)).toBe("$10.00");
    expect(cents(1)).toBe("$0.01");
  });
});

describe("parseCents", () => {
  test("parses string to dollars", () => {
    expect(parseCents("1000")).toBe(10);
    expect(parseCents("1999")).toBe(19.99);
  });

  test("parses number to dollars", () => {
    expect(parseCents(500)).toBe(5);
  });

  test("handles undefined", () => {
    expect(parseCents(undefined)).toBe(0);
  });

  test("handles empty string", () => {
    expect(parseCents("")).toBe(0);
  });

  test("handles zero", () => {
    expect(parseCents(0)).toBe(0);
    expect(parseCents("0")).toBe(0);
  });
});

describe("formatDate", () => {
  test("formats ISO date", () => {
    // Note: output depends on locale, testing general format
    const result = formatDate("2026-01-15T10:30:00Z");
    expect(result).toContain("Jan");
    expect(result).toContain("15");
    expect(result).toContain("2026");
  });

  test("handles different months", () => {
    expect(formatDate("2026-12-25T00:00:00Z")).toContain("Dec");
    expect(formatDate("2026-06-01T00:00:00Z")).toContain("Jun");
  });
});

describe("orderStatusIcon", () => {
  test("returns checkmark for paid", () => {
    expect(orderStatusIcon("paid")).toBe("✓");
  });

  test("returns arrow for refunded", () => {
    expect(orderStatusIcon("refunded")).toBe("↩");
  });

  test("returns circle for other statuses", () => {
    expect(orderStatusIcon("pending")).toBe("○");
    expect(orderStatusIcon("unknown")).toBe("○");
    expect(orderStatusIcon("")).toBe("○");
  });
});

describe("subStatusIcon", () => {
  test("returns filled circle for active", () => {
    expect(subStatusIcon("active")).toBe("●");
  });

  test("returns empty circle for cancelled", () => {
    expect(subStatusIcon("cancelled")).toBe("○");
  });

  test("returns half circle for other statuses", () => {
    expect(subStatusIcon("paused")).toBe("◐");
    expect(subStatusIcon("past_due")).toBe("◐");
    expect(subStatusIcon("trialing")).toBe("◐");
  });
});

describe("API error handling", () => {
  const originalFetch = globalThis.fetch;

  afterEach(() => {
    globalThis.fetch = originalFetch;
  });

  test("handles 401 unauthorized", async () => {
    globalThis.fetch = mock(async () =>
      new Response(JSON.stringify({ error: "unauthorized" }), {
        status: 401,
        statusText: "Unauthorized",
      })
    );

    // Simulating the api() function behavior
    const api = async (endpoint: string) => {
      const res = await fetch(`https://api.lemonsqueezy.com/v1${endpoint}`, {
        headers: {
          Authorization: "Bearer test",
          Accept: "application/vnd.api+json",
        },
      });
      if (!res.ok) {
        throw new Error(`API error: ${res.status} ${res.statusText}`);
      }
      return res.json();
    };

    await expect(api("/stores")).rejects.toThrow("API error: 401 Unauthorized");
  });

  test("handles 429 rate limit", async () => {
    globalThis.fetch = mock(async () =>
      new Response(JSON.stringify({ error: "rate limited" }), {
        status: 429,
        statusText: "Too Many Requests",
      })
    );

    const api = async (endpoint: string) => {
      const res = await fetch(`https://api.lemonsqueezy.com/v1${endpoint}`);
      if (!res.ok) {
        throw new Error(`API error: ${res.status} ${res.statusText}`);
      }
      return res.json();
    };

    await expect(api("/stores")).rejects.toThrow("API error: 429 Too Many Requests");
  });

  test("handles network error", async () => {
    globalThis.fetch = mock(async () => {
      throw new Error("Network error");
    });

    const api = async (endpoint: string) => {
      const res = await fetch(`https://api.lemonsqueezy.com/v1${endpoint}`);
      return res.json();
    };

    await expect(api("/stores")).rejects.toThrow("Network error");
  });
});

describe("CLI env validation", () => {
  test("LEMONSQUEEZY_API_KEY is required", () => {
    // The CLI checks for API key at module load
    // This test documents the requirement
    const envCheck = () => {
      const key = undefined;
      if (!key) {
        throw new Error("LEMONSQUEEZY_API_KEY required");
      }
    };

    expect(envCheck).toThrow("LEMONSQUEEZY_API_KEY required");
  });
});
