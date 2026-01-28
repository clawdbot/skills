#!/usr/bin/env node
/**
 * Get chart data from CoinGecko API (free, no auth)
 */
import fetch from 'node-fetch';

async function getChartData(coinId, days = 1) {
  // Don't specify interval - let CoinGecko auto-select (free tier limitation)
  const url = `https://api.coingecko.com/api/v3/coins/${coinId}/market_chart?vs_currency=usd&days=${days}`;
  
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${await response.text()}`);
  }
  
  const data = await response.json();
  return data;
}

async function analyzeCoin(coinId, coinName) {
  console.log(`\n=== ${coinName} Analysis ===\n`);
  
  try {
    const data = await getChartData(coinId, 1); // Last 24 hours
    
    const prices = data.prices.slice(-10); // Last 10 data points
    const volumes = data.total_volumes.slice(-10);
    
    // Recent price action
    console.log('Recent Price Action (last 10 hours):');
    console.log('Time                 Price        Volume');
    console.log('─'.repeat(60));
    
    for (let i = 0; i < prices.length; i++) {
      const time = new Date(prices[i][0]).toLocaleTimeString();
      const price = prices[i][1].toFixed(2);
      const volume = (volumes[i][1] / 1000000).toFixed(2) + 'M';
      console.log(`${time.padEnd(20)} $${price.padStart(10)}   $${volume.padStart(8)}`);
    }
    
    // Calculate metrics
    const currentPrice = prices[prices.length - 1][1];
    const prevPrice = prices[prices.length - 2][1];
    const price6hAgo = prices[Math.max(0, prices.length - 7)][1];
    
    const change1h = ((currentPrice - prevPrice) / prevPrice) * 100;
    const change6h = ((currentPrice - price6hAgo) / price6hAgo) * 100;
    
    // Volume analysis
    const currentVolume = volumes[volumes.length - 1][1];
    const avgVolume = volumes.slice(0, -1).reduce((sum, v) => sum + v[1], 0) / (volumes.length - 1);
    const volumeRatio = currentVolume / avgVolume;
    
    console.log('\n📊 Metrics:');
    console.log(`  Current Price: $${currentPrice.toFixed(2)}`);
    console.log(`  Change (1h): ${change1h > 0 ? '+' : ''}${change1h.toFixed(2)}%`);
    console.log(`  Change (6h): ${change6h > 0 ? '+' : ''}${change6h.toFixed(2)}%`);
    console.log(`  Current Volume: $${(currentVolume / 1000000).toFixed(2)}M`);
    console.log(`  Avg Volume (9h): $${(avgVolume / 1000000).toFixed(2)}M`);
    console.log(`  Volume Ratio: ${volumeRatio.toFixed(2)}x ${volumeRatio > 1.5 ? '🔥 HIGH' : volumeRatio < 0.7 ? '❄️  LOW' : '📊 NORMAL'}`);
    
    // Momentum signal
    console.log('\n🎯 Momentum Signal:');
    const strongUp = change1h > 0.5 && volumeRatio > 1.3;
    const weakUp = change1h > 0 && change1h < 0.5;
    const strongDown = change1h < -0.5 && volumeRatio > 1.3;
    
    if (strongUp) {
      console.log('  ✅ STRONG BULLISH - Price surging with high volume');
      console.log('  → Consider LONG entry');
    } else if (weakUp) {
      console.log('  ⚠️  WEAK BULLISH - Price up but momentum unclear');
      console.log('  → Wait for confirmation');
    } else if (strongDown) {
      console.log('  🔴 STRONG BEARISH - Price dropping with high volume');
      console.log('  → Consider SHORT entry');
    } else {
      console.log('  ⏸️  NEUTRAL - No clear momentum');
      console.log('  → Wait for clearer signal');
    }
    
    // Trend
    console.log('\n📈 Trend (6h):');
    if (change6h > 1) {
      console.log(`  🚀 Uptrend (+${change6h.toFixed(2)}%)`);
    } else if (change6h < -1) {
      console.log(`  📉 Downtrend (${change6h.toFixed(2)}%)`);
    } else {
      console.log(`  ➡️  Sideways (${change6h.toFixed(2)}%)`);
    }
    
    return {
      coin: coinName,
      currentPrice,
      change1h,
      change6h,
      volumeRatio,
      signal: strongUp ? 'strong_bull' : weakUp ? 'weak_bull' : strongDown ? 'strong_bear' : 'neutral'
    };
    
  } catch (err) {
    console.error(`Error: ${err.message}`);
    return null;
  }
}

// Main
console.log('🔍 Fetching market data from CoinGecko...\n');

const btc = await analyzeCoin('bitcoin', 'BTC');
const eth = await analyzeCoin('ethereum', 'ETH');

console.log('\n' + '='.repeat(80));
console.log('\n📋 TRADING RECOMMENDATION:\n');

if (btc && eth) {
  if (btc.signal === 'strong_bull' || eth.signal === 'strong_bull') {
    const coin = btc.signal === 'strong_bull' ? 'BTC' : 'ETH';
    console.log(`✅ TRADE SIGNAL: Enter ${coin} LONG`);
    console.log(`   Strong momentum confirmed with volume`);
  } else if (btc.signal === 'strong_bear' || eth.signal === 'strong_bear') {
    const coin = btc.signal === 'strong_bear' ? 'BTC' : 'ETH';
    console.log(`✅ TRADE SIGNAL: Enter ${coin} SHORT`);
    console.log(`   Strong selling pressure with volume`);
  } else {
    console.log(`⏸️  NO TRADE: Wait for clearer momentum signal`);
    console.log(`   Current momentum is too weak to justify entry`);
  }
}

console.log('\n' + '='.repeat(80));
