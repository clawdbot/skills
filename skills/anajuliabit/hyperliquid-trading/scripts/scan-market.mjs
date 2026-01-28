#!/usr/bin/env node
import { Hyperliquid } from 'hyperliquid';

const sdk = new Hyperliquid({ enableWs: false });

console.log('Fetching current prices...\n');

const prices = await sdk.info.getAllMids();

// Major assets
const majors = ['BTC-PERP', 'ETH-PERP', 'SOL-PERP', 'AVAX-PERP', 'DOGE-PERP', 'ARB-PERP'];

console.log('=== MAJOR ASSETS ===');
for (const coin of majors) {
  if (prices[coin]) {
    console.log(`${coin.padEnd(12)} $${prices[coin]}`);
  }
}

// Find top movers (we'll need historical data for this, so just show available assets for now)
console.log('\n=== AVAILABLE PERPS (first 20) ===');
const perps = Object.keys(prices)
  .filter(k => k.endsWith('-PERP'))
  .slice(0, 20);

for (const coin of perps) {
  console.log(`${coin.padEnd(12)} $${prices[coin]}`);
}

console.log(`\nTotal perpetuals available: ${Object.keys(prices).filter(k => k.endsWith('-PERP')).length}`);
