#!/usr/bin/env node

/**
 * office-quotes CLI tool for Clawdbot
 * 
 * Usage: node office-quotes.js [--mode offline|api] [--theme dark|light] [--image]
 */

const API_BASE = "https://officeapi.akashrajpurohit.com";

// Parse arguments
const args = process.argv.slice(2);
let mode = "offline";
let theme = "dark";
let includeImage = false;

for (let i = 0; i < args.length; i++) {
  const arg = args[i];
  if (arg === "--mode" && args[i + 1]) {
    mode = args[++i];
  } else if (arg === "--theme" && args[i + 1]) {
    theme = args[++i];
  } else if (arg === "--image") {
    includeImage = true;
  }
}

async function getOfflineQuote() {
  // Use built-in quotes array for offline mode
  const quotes = [
    { character: "Michael Scott", content: "Would I rather be feared or loved? Easy. Both. I want people to be afraid of how much they love me." },
    { character: "Jim Halpert", content: "Bears. Beets. Battlestar Galactica." },
    { character: "Dwight Schrute", content: "Whenever I'm about to do something, I think, 'Would an idiot do that?' And if they would, I do not do that thing." },
    { character: "Michael Scott", content: "That's what she said!" },
    { character: "Michael Scott", content: "I am Beyoncé, always." },
    { character: "Dwight Schrute", content: "How would I describe myself? Three words: hardworking, alpha male, jackhammer, merciless, insatiable." },
    { character: "Pam Beesly", content: "I feel God in this Chili's tonight." },
    { character: "Andy Bernard", content: "I wish there was a way to know you're in the good old days, before you've actually left them." },
    { character: "Michael Scott", content: "I’m not superstitious, but I am a little stitious." },
    { character: "Michael Scott", content: "I love inside jokes. Love to be a part of one someday." },
    { character: "Michael Scott", content: "Fool me once, strike one. Fool me twice, strike three." },
    { character: "Michael Scott", content: "Sometimes I'll start a sentence and I don't even know where it's going. I just hope I find it along the way." },
    { character: "Michael Scott", content: "You miss 100 percent of the shots you don't take. Wayne Gretzky." },
    { character: "Michael Scott", content: "I… declare…. bankruptcy!" },
    { character: "Michael Scott", content: "It’s Britney, bitch." },
    { character: "Dwight Schrute", content: "'R' is among the most menacing of sounds. That's why they call it 'murder' and not 'mukduk.'" },
    { character: "Kevin Malone", content: "Why waste time say lot word when few word do trick?" },
    { character: "Angela Martin", content: "I'm not gaining anything from this seminar. I'm a professional woman. The head of accounting. I'm in the healthiest relationship of my life." },
    { character: "Kelly Kapoor", content: "I talk a lot, so I've learned to tune myself out." },
    { character: "Oscar Martinez", content: "Saddle Shoes With Denim? I Will Literally Call Protective Services." }
  ];
  
  const randomIndex = Math.floor(Math.random() * quotes.length);
  const quote = quotes[randomIndex];
  return `${quote.character}: ${quote.content}`;
}

async function getApiQuote() {
  const url = `${API_BASE}/quote/random?responseType=svg&mode=${theme}&width=400&height=200`;
  
  if (includeImage) {
    return url;
  }
  
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.text();
  } catch (error) {
    return `Error fetching quote: ${error.message}`;
  }
}

async function main() {
  let result;
  
  if (mode === "api") {
    result = await getApiQuote();
  } else {
    result = await getOfflineQuote();
  }
  
  // Output as JSON for tool use
  console.log(JSON.stringify({
    result,
    mode,
    theme: mode === "api" ? theme : null,
    includeImage
  }, null, 2));
}

main().catch(console.error);
