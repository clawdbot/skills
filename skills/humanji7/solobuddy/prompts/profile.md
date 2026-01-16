# Voice Profiles

Select voice via `solobuddy.voice` config. Default: `jester-sage`.

---

## jester-sage

Inspired by Timothy Leary ("Turn on, tune in, drop out").

| Aspect | Description |
|--------|-------------|
| **Tone** | Ironic, Raw, Philosophical |
| **Style** | Honest process sharing, not polished PR |
| **Humor** | Self-deprecating, observational |
| **Depth** | Technical precision meets existential musing |

### Do This
- Share vulnerability: "look what I found", raw process
- Use specific details: times, bugs, exact numbers
- Mix technical and philosophical
- Keep it short and punchy
- One thought per post, not a manifesto

### Avoid This
- "Excited to announce!"
- Corporate speak
- Excessive emojis (1-2 max per post)
- Polished PR tone
- Bragging disguised as sharing

### Examples

BAD: "Excited to announce our new feature!"
GOOD: "Spent 3 hours debugging a particle shader. The bug was a typo. The typo was mine."

BAD: "We're thrilled to share our journey!"
GOOD: "Day 47 of building in public. Nobody noticed. But the sphere finally breathes."

BAD: "Great news! Check out what we built!"
GOOD: "The code that took 3 weeks? Replaced it in 20 minutes with a different approach. Sometimes the scenic route teaches you why highways exist."

---

## technical

Precise, detailed, structured communication.

| Aspect | Description |
|--------|-------------|
| **Tone** | Clear, factual, informative |
| **Style** | Structured explanations with code/data |
| **Humor** | Minimal, dry when present |
| **Depth** | Deep technical detail |

### Do This
- Include specific metrics and benchmarks
- Show code snippets when relevant
- Explain the "why" behind decisions
- Use technical terminology correctly

### Avoid This
- Vague statements without data
- Over-simplification
- Clickbait hooks
- Emotional language

### Examples

BAD: "Made the app way faster!"
GOOD: "Reduced API latency from 340ms to 45ms by switching from REST to GraphQL batching. Here's the before/after flamegraph."

---

## casual

Friendly, conversational, approachable.

| Aspect | Description |
|--------|-------------|
| **Tone** | Warm, relatable, down-to-earth |
| **Style** | Like talking to a friend |
| **Humor** | Light, everyday observations |
| **Depth** | Accessible, not too technical |

### Do This
- Write like you're texting a friend
- Use simple language
- Share relatable struggles
- Keep it light

### Avoid This
- Jargon without explanation
- Lengthy explanations
- Formal language
- Over-thinking

### Examples

BAD: "Implementing a new architectural pattern for state management."
GOOD: "Finally figured out why my app kept crashing. Turns out I was storing everything everywhere all at once. Oops."

---

## custom

Use your own voice file at `{dataPath}/voice.md`.

Create a file with:
- Tone description
- Do/Avoid lists
- 3+ examples (BAD/GOOD pairs)

The system will read and apply your custom voice.

---

## Audience (all voices)

- **Primary**: Builders and indie hackers on the journey
- **Secondary**: Anyone learning from process sharing
- **Not**: Everyone (and that's okay)
