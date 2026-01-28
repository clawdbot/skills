#!/bin/bash
# PRISM API Helper Script
# Usage: ./prism.sh <command> [args]

PRISM_URL="${PRISM_URL:-https://strykr-prism.up.railway.app}"

case "$1" in
  # Resolution
  resolve)
    curl -s "$PRISM_URL/resolve/$2" | jq .
    ;;
  resolve-nl)
    curl -s -X POST "$PRISM_URL/agent/resolve" \
      -H "Content-Type: application/json" \
      -d "{\"query\": \"$2\"}" | jq .
    ;;
  venues)
    curl -s "$PRISM_URL/resolve/venues/$2" | jq .
    ;;
    
  # Prices
  price)
    curl -s "$PRISM_URL/crypto/price/$2" | jq .
    ;;
  stock)
    curl -s "$PRISM_URL/stocks/$2/quote" | jq .
    ;;
    
  # Market
  overview)
    curl -s "$PRISM_URL/market/overview" | jq .
    ;;
  fear-greed)
    curl -s "$PRISM_URL/market/fear-greed" | jq .
    ;;
  trending)
    curl -s "$PRISM_URL/crypto/trending" | jq .
    ;;
  pumps)
    curl -s "$PRISM_URL/crypto/trending/solana/bonding" | jq .
    ;;
  gainers)
    curl -s "$PRISM_URL/stocks/gainers" | jq .
    ;;
  losers)
    curl -s "$PRISM_URL/stocks/losers" | jq .
    ;;
    
  # Analysis
  analyze)
    curl -s "$PRISM_URL/analyze/$2" | jq .
    ;;
  copycat)
    curl -s "$PRISM_URL/analyze/copycat/$2" | jq .
    ;;
  holders)
    curl -s "$PRISM_URL/analytics/holders/$2" | jq .
    ;;
    
  # DeFi
  funding)
    curl -s "$PRISM_URL/dex/$2/funding/all" | jq .
    ;;
  oi)
    curl -s "$PRISM_URL/dex/$2/oi/all" | jq .
    ;;
    
  # Wallet
  wallet)
    curl -s "$PRISM_URL/wallets/$2/balances" | jq .
    ;;
    
  # Health
  health)
    curl -s "$PRISM_URL/health" | jq .
    ;;
  status)
    curl -s "$PRISM_URL/crypto/sources/status" | jq .
    ;;
    
  *)
    echo "PRISM API Helper"
    echo ""
    echo "Usage: prism.sh <command> [args]"
    echo ""
    echo "Commands:"
    echo "  resolve <symbol>    - Resolve asset to canonical form"
    echo "  resolve-nl <query>  - Natural language resolution"
    echo "  venues <symbol>     - Get trading venues"
    echo "  price <symbol>      - Get crypto price"
    echo "  stock <symbol>      - Get stock quote"
    echo "  overview            - Market overview"
    echo "  fear-greed          - Fear & Greed Index"
    echo "  trending            - Trending crypto"
    echo "  pumps               - Pump.fun bonding tokens"
    echo "  gainers             - Stock gainers"
    echo "  losers              - Stock losers"
    echo "  analyze <symbol>    - Token analysis"
    echo "  copycat <symbol>    - Scam/copycat check"
    echo "  holders <contract>  - Holder analytics"
    echo "  funding <symbol>    - Cross-venue funding"
    echo "  oi <symbol>         - Cross-venue OI"
    echo "  wallet <address>    - Wallet balances"
    echo "  health              - API health"
    echo "  status              - Data source status"
    ;;
esac
