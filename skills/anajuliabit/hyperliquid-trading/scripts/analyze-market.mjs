#!/usr/bin/env node
/**
 * Get historical candles and volume for technical analysis
 */
import { Hyperliquid } from 'hyperliquid';

const sdk = new Hyperliquid({ enableWs: false });

async function analyzeCoin(coin, interval = '15m', lookback = 20) {
  console.log(`\n=== ${coin} Analysis (${interval} candles) ===\n`);
  
  // Get candle data
  const candles = await sdk.info.getCandleSnapshot({
    coin,
    interval,
    startTime: Date.now() - (lookback * getIntervalMs(interval)),
    endTime: Date.now()
  });
  
  if (!candles || candles.length === 0) {
    console.log('No candle data available');
    return null;
  }
  
  // Recent candles
  const recentCandles = candles.slice(-5);
  console.log('Recent Candles:');
  console.log('Time                 Open      High      Low       Close     Volume');
  console.log('─'.repeat(80));
  
  for (const c of recentCandles) {
    const time = new Date(c.t).toLocaleTimeString();
    console.log(
      `${time.padEnd(20)} ${c.o.padEnd(9)} ${c.h.padEnd(9)} ${c.l.padEnd(9)} ${c.c.padEnd(9)} ${c.v}`
    );
  }
  
  // Calculate metrics
  const latest = candles[candles.length - 1];
  const previous = candles[candles.length - 2];
  const current = parseFloat(latest.c);
  const prev = parseFloat(previous.c);
  const change = ((current - prev) / prev) * 100;
  
  // Volume analysis
  const avgVolume = candles.slice(-10).reduce((sum, c) => sum + parseFloat(c.v), 0) / 10;
  const currentVolume = parseFloat(latest.v);
  const volumeRatio = currentVolume / avgVolume;
  
  console.log('\n📊 Metrics:');
  console.log(`  Current Price: $${current}`);
  console.log(`  Change (${interval}): ${change > 0 ? '+' : ''}${change.toFixed(2)}%`);
  console.log(`  Current Volume: ${currentVolume.toFixed(2)}`);
  console.log(`  Avg Volume (10 bars): ${avgVolume.toFixed(2)}`);
  console.log(`  Volume Ratio: ${volumeRatio.toFixed(2)}x ${volumeRatio > 1.5 ? '🔥 HIGH' : volumeRatio < 0.7 ? '❄️  LOW' : '📊 NORMAL'}`);
  
  // Momentum detection
  const priceUp = change > 0;
  const volumeUp = volumeRatio > 1.2;
  
  console.log('\n🎯 Momentum Signal:');
  if (priceUp && volumeUp) {
    console.log('  ✅ BULLISH - Price up with high volume (strong momentum)');
  } else if (priceUp && !volumeUp) {
    console.log('  ⚠️  WEAK BULLISH - Price up but low volume (weak momentum)');
  } else if (!priceUp && volumeUp) {
    console.log('  🔴 BEARISH - Price down with high volume (strong selling)');
  } else {
    console.log('  ⏸️  NEUTRAL - No clear momentum');
  }
  
  // Simple support/resistance
  const highs = candles.slice(-20).map(c => parseFloat(c.h));
  const lows = candles.slice(-20).map(c => parseFloat(c.l));
  const resistance = Math.max(...highs);
  const support = Math.min(...lows);
  
  console.log('\n📈 Levels:');
  console.log(`  Resistance: $${resistance} (${((resistance - current) / current * 100).toFixed(2)}% away)`);
  console.log(`  Support: $${support} (${((current - support) / current * 100).toFixed(2)}% away)`);
  
  return {
    coin,
    current,
    change,
    volumeRatio,
    signal: priceUp && volumeUp ? 'bullish' : !priceUp && volumeUp ? 'bearish' : 'neutral',
    resistance,
    support
  };
}

function getIntervalMs(interval) {
  const units = {
    'm': 60000,
    'h': 3600000,
    'd': 86400000
  };
  const match = interval.match(/^(\d+)([mhd])$/);
  if (!match) return 60000;
  return parseInt(match[1]) * units[match[2]];
}

// Main
const coins = process.argv.slice(2);
if (coins.length === 0) {
  coins.push('BTC-PERP', 'ETH-PERP');
}

for (const coin of coins) {
  try {
    await analyzeCoin(coin);
  } catch (err) {
    console.error(`Error analyzing ${coin}:`, err.message);
  }
}

console.log('\n' + '='.repeat(80));
