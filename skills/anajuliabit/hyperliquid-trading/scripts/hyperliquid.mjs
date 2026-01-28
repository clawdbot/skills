#!/usr/bin/env node
/**
 * Hyperliquid CLI - Trading and portfolio management
 * Using official Hyperliquid SDK
 */

import { Hyperliquid } from 'hyperliquid';

// Helper to ensure coin name has -PERP suffix
function normalizeCoin(coin) {
  if (!coin) return coin;
  const upper = coin.toUpperCase();
  if (upper.endsWith('-PERP') || upper.endsWith('-SPOT')) return upper;
  return upper + '-PERP'; // Default to perpetuals
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === 'help') {
    console.log(`
Hyperliquid CLI - Trading and Portfolio Management

ENVIRONMENT VARIABLES:
  HYPERLIQUID_PRIVATE_KEY  Private key for trading (optional for read-only)
  HYPERLIQUID_ADDRESS      Address to query (defaults to private key address)
  HYPERLIQUID_TESTNET      Set to '1' for testnet

READ OPERATIONS (no private key needed):
  balance [address]              Show account balance and equity
  positions [address]            Show open positions with P&L
  orders [address]               Show open orders
  fills [address]                Show recent trade history
  price <coin>                   Get current price for a coin (auto-adds -PERP)
  meta                           List all available coins

TRADING OPERATIONS (requires HYPERLIQUID_PRIVATE_KEY):
  market-buy <coin> <size>       Market buy (with slippage protection)
  market-sell <coin> <size>      Market sell (with slippage protection)
  limit-buy <coin> <size> <price>   Place limit buy order
  limit-sell <coin> <size> <price>  Place limit sell order
  cancel-all [coin]              Cancel all orders (optionally for one coin)

EXAMPLES:
  export HYPERLIQUID_ADDRESS=0x1234...
  hyperliquid balance
  hyperliquid price BTC

  export HYPERLIQUID_PRIVATE_KEY=0xabc...
  hyperliquid market-buy SOL 0.1
  hyperliquid cancel-all
    `);
    process.exit(0);
  }

  const privateKey = process.env.HYPERLIQUID_PRIVATE_KEY;
  const address = process.env.HYPERLIQUID_ADDRESS;
  const isTestnet = process.env.HYPERLIQUID_TESTNET === '1';

  // Initialize SDK
  const sdk = new Hyperliquid({
    privateKey: privateKey || undefined,
    testnet: isTestnet,
    enableWs: false, // Disable WebSocket for CLI usage
  });

  try {
    switch (command) {
      case 'balance': {
        const addr = args[1] || address || sdk.walletAddress;
        if (!addr) throw new Error('Address required (set HYPERLIQUID_ADDRESS or HYPERLIQUID_PRIVATE_KEY)');
        
        const state = await sdk.info.perpetuals.getClearinghouseState(addr);
        console.log(JSON.stringify(state, null, 2));
        break;
      }

      case 'positions': {
        const addr = args[1] || address || sdk.walletAddress;
        if (!addr) throw new Error('Address required');
        
        const state = await sdk.info.perpetuals.getClearinghouseState(addr);
        console.log(JSON.stringify(state.assetPositions || [], null, 2));
        break;
      }

      case 'orders': {
        const addr = args[1] || address || sdk.walletAddress;
        if (!addr) throw new Error('Address required');
        
        const state = await sdk.info.perpetuals.getClearinghouseState(addr);
        // Open orders are in state data
        console.log(JSON.stringify(state.assetPositions || [], null, 2));
        break;
      }

      case 'fills': {
        const addr = args[1] || address || sdk.walletAddress;
        if (!addr) throw new Error('Address required');
        
        const updates = await sdk.info.perpetuals.getUserNonFundingLedgerUpdates(addr);
        console.log(JSON.stringify(updates, null, 2));
        break;
      }

      case 'price': {
        const coin = normalizeCoin(args[1]);
        if (!coin) throw new Error('Coin required');
        
        const prices = await sdk.info.getAllMids();
        if (!prices[coin]) throw new Error(`Unknown coin: ${coin}`);
        console.log(prices[coin]);
        break;
      }

      case 'meta': {
        const meta = await sdk.info.perpetuals.getMeta();
        console.log(JSON.stringify(meta.universe, null, 2));
        break;
      }

      case 'market-buy':
      case 'market-sell': {
        if (!privateKey) throw new Error('Private key required for trading');
        
        const coin = normalizeCoin(args[1]);
        const size = args[2];
        
        if (!coin || !size) {
          throw new Error(`Usage: hyperliquid ${command} <coin> <size>`);
        }

        const isBuy = command === 'market-buy';
        
        // Get current price for slippage calculation
        const prices = await sdk.info.getAllMids();
        const currentPrice = parseFloat(prices[coin]);
        if (!currentPrice) throw new Error(`Unknown coin: ${coin}`);
        
        // 5% slippage protection
        const slippagePrice = isBuy 
          ? currentPrice * 1.05 
          : currentPrice * 0.95;

        const result = await sdk.exchange.placeOrder({
          coin,
          is_buy: isBuy,
          sz: parseFloat(size),
          limit_px: slippagePrice,
          order_type: { limit: { tif: 'Ioc' } }, // Immediate or cancel
          reduce_only: false,
        });
        
        console.log(JSON.stringify(result, null, 2));
        break;
      }

      case 'limit-buy':
      case 'limit-sell': {
        if (!privateKey) throw new Error('Private key required for trading');
        
        const coin = normalizeCoin(args[1]);
        const size = args[2];
        const price = args[3];
        
        if (!coin || !size || !price) {
          throw new Error(`Usage: hyperliquid ${command} <coin> <size> <price>`);
        }

        const isBuy = command === 'limit-buy';

        const result = await sdk.exchange.placeOrder({
          coin,
          is_buy: isBuy,
          sz: parseFloat(size),
          limit_px: parseFloat(price),
          order_type: { limit: { tif: 'Gtc' } }, // Good til cancelled
          reduce_only: false,
        });
        
        console.log(JSON.stringify(result, null, 2));
        break;
      }

      case 'cancel-all': {
        if (!privateKey) throw new Error('Private key required for trading');
        
        const coin = args[1] ? normalizeCoin(args[1]) : undefined;
        const result = await sdk.custom.cancelAllOrders(coin);
        console.log(JSON.stringify(result, null, 2));
        break;
      }

      default:
        console.error(`Unknown command: ${command}`);
        console.log('Run "hyperliquid help" for usage');
        process.exit(1);
    }
  } catch (error) {
    console.error('Error:', error.message);
    if (error.response) {
      console.error('Response:', JSON.stringify(error.response, null, 2));
    }
    process.exit(1);
  }
}

main();
