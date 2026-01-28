#!/usr/bin/env node
/**
 * Check current positions and calculate P&L
 */
import { Hyperliquid } from 'hyperliquid';
import { readFileSync, writeFileSync } from 'fs';

const sdk = new Hyperliquid({
  privateKey: process.env.HYPERLIQUID_PRIVATE_KEY,
  enableWs: false
});

const stateFile = '/home/ana/clawd/trading-state.json';

async function main() {
  console.log('=== HYPERLIQUID POSITION CHECK ===\n');
  
  const address = sdk.walletAddress || process.env.HYPERLIQUID_ADDRESS;
  if (!address) {
    console.error('Error: No wallet address available');
    process.exit(1);
  }
  
  console.log(`Checking address: ${address}\n`);
  
  // Get current state
  const state = await sdk.info.perpetuals.getClearinghouseState(address);
  
  // Get current prices
  const prices = await sdk.info.getAllMids();
  
  console.log('Account Status:');
  console.log(`  Equity: $${state.marginSummary.accountValue}`);
  console.log(`  Available: $${state.withdrawable}`);
  console.log(`  Margin Used: $${state.marginSummary.totalMarginUsed}`);
  
  if (state.assetPositions && state.assetPositions.length > 0) {
    console.log('\n=== OPEN POSITIONS ===');
    for (const pos of state.assetPositions) {
      const p = pos.position;
      const coin = p.coin;
      const currentPrice = parseFloat(prices[coin]);
      const entryPrice = parseFloat(p.entryPx);
      const size = parseFloat(p.szi);
      const pnl = parseFloat(p.unrealizedPnl);
      const pnlPct = (pnl / Math.abs(size * entryPrice)) * 100;
      
      console.log(`\n${coin}:`);
      console.log(`  Direction: ${size > 0 ? 'LONG' : 'SHORT'}`);
      console.log(`  Size: ${Math.abs(size)}`);
      console.log(`  Entry: $${entryPrice}`);
      console.log(`  Current: $${currentPrice}`);
      console.log(`  P&L: $${pnl.toFixed(2)} (${pnlPct > 0 ? '+' : ''}${pnlPct.toFixed(2)}%)`);
      
      // Check if profit target or stop loss hit
      if (pnlPct >= 2) {
        console.log(`  ⚠️  PROFIT TARGET HIT! Consider taking profit.`);
      } else if (pnlPct <= -1) {
        console.log(`  🛑 STOP LOSS HIT! Consider closing position.`);
      }
    }
  } else {
    console.log('\n✅ No open positions');
  }
  
  // Current prices
  console.log('\n=== CURRENT PRICES ===');
  console.log(`BTC-PERP: $${prices['BTC-PERP']}`);
  console.log(`ETH-PERP: $${prices['ETH-PERP']}`);
  console.log(`SOL-PERP: $${prices['SOL-PERP']}`);
  
  // Update state file
  try {
    const tradingState = JSON.parse(readFileSync(stateFile, 'utf8'));
    tradingState.last_check = new Date().toISOString();
    tradingState.current_positions = state.assetPositions || [];
    tradingState.parameters.account_size = parseFloat(state.marginSummary.accountValue);
    writeFileSync(stateFile, JSON.stringify(tradingState, null, 2));
    console.log('\n✅ Trading state updated');
  } catch (err) {
    console.log('\n⚠️  Could not update trading state:', err.message);
  }
}

main().catch(console.error);
