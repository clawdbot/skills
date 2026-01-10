#!/usr/bin/env python3
"""
Kraken Crypto CLI Tool for Clawdbot
A command-line interface for managing your Kraken account.

Usage:
    python kraken_cli.py <command> [--asset <asset>] [--pair <pair>]

Commands:
    balance          - Get all account balances
    portfolio        - Get trade balance summary with equity/PnL
    ledger           - Get ledger entries (transaction history)
    trades           - Get trade history
    earn             - Show stakeable assets and APY rates
    earn positions   - Show current staking positions
    deposits methods - Show available deposit methods
    deposits address - Get deposit address for an asset
    ticker <pair>    - Get current price, 24h volume, high/low
"""

import os
import sys
import argparse
from datetime import datetime
from decimal import Decimal
from typing import Optional

from kraken.spot import User, Market, Earn, Funding


def get_clients() -> tuple[User, Market, Earn, Funding]:
    """Initialize and return Kraken clients."""
    api_key = os.environ.get("KRAKEN_API_KEY")
    api_secret = os.environ.get("KRAKEN_API_SECRET")

    if not api_key or not api_secret:
        raise ValueError(
            "KRAKEN_API_KEY and KRAKEN_API_SECRET must be set in environment"
        )

    return (
        User(key=api_key, secret=api_secret),
        Market(),
        Earn(key=api_key, secret=api_secret),
        Funding(key=api_key, secret=api_secret),
    )


def format_currency(amount: str, decimals: int = 4) -> str:
    """Format decimal amount nicely."""
    try:
        return f"{Decimal(amount):.{decimals}f}"
    except:
        return amount


def cmd_balance(user: User) -> str:
    """Get account balances."""
    try:
        result = user.get_account_balance()
        if not result or isinstance(result, list):
            return "No balances found."

        lines = ["=== Account Balances ==="]
        for asset, balance in sorted(result.items(), key=lambda x: float(x[1]), reverse=True):
            if float(balance) > 0:
                lines.append(f"  {asset:8s}: {format_currency(balance, 6)}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


def cmd_portfolio(user: User) -> str:
    """Get extended portfolio with trade balances."""
    try:
        result = user.get_trade_balance(asset="USD")
        if not result:
            return "No trade balance data."

        lines = ["=== Trade Balance (USD) ==="]
        lines.append(f"  Equity:          ${format_currency(result.get('eb', '0'))}")
        lines.append(f"  Free:            ${format_currency(result.get('tb', '0'))}")
        lines.append(f"  Unrealized PnL:  ${format_currency(result.get('up', '0'))}")
        lines.append(f"  Cost Basis:      ${format_currency(result.get('bc', '0'))}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


def cmd_ledger(user: User, asset: Optional[str] = None, limit: int = 20) -> str:
    """Get ledger entries."""
    try:
        result = user.get_ledgers_info(asset=asset if asset else None)
        if not result or "ledger" not in result or not result.get("ledger"):
            return "No ledger entries found."

        ledger = result.get("ledger", {})
        entries = sorted(ledger.items(), key=lambda x: int(x[0], 36), reverse=True)[:limit]
        lines = [f"=== Ledger Entries{' (' + asset + ')' if asset else ''} ==="]
        for refid, entry in entries:
            timestamp = datetime.fromtimestamp(float(entry.get("time", 0)))
            lines.append(f"  [{entry.get('type', '?').upper():10s}] {timestamp.strftime('%Y-%m-%d %H:%M')} "
                        f"{entry.get('asset', '?'):6s} {entry.get('amount', '?'):>15s} "
                        f"(fee: {entry.get('fee', '?')})")
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


def cmd_trades(user: User, limit: int = 20) -> str:
    """Get trade history."""
    try:
        result = user.get_trades_history()
        if not result or "trades" not in result or not result.get("trades"):
            return "No trades found."

        trades = result.get("trades", {})
        sorted_trades = sorted(trades.items(), key=lambda x: float(x[1].get("time", 0)), reverse=True)
        lines = ["=== Trade History ==="]
        for refid, trade in sorted_trades[:limit]:
            timestamp = datetime.fromtimestamp(float(trade.get("time", 0)))
            side = "BUY" if trade.get("type") == "buy" else "SELL"
            lines.append(f"  [{side:4s}] {timestamp.strftime('%Y-%m-%d %H:%M')} "
                        f"{trade.get('pair', '?'):10s} {trade.get('vol', '?'):>12s} "
                        f"@ ${trade.get('price', '?')}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


def cmd_earn(earn: Earn, positions: bool = False) -> str:
    """Get staking/earn positions."""
    try:
        if positions:
            result = earn.list_earn_allocations()
            if not result or "allocations" not in result or not result.get("allocations"):
                return "No earn allocations found."

            lines = ["=== Earn Allocations ==="]
            for alloc in result.get("allocations", []):
                lines.append(f"  {alloc.get('asset', '?'):8s}: {alloc.get('amount', '?')} "
                            f"(pending: {alloc.get('pending_amount', '?')})")
            return "\n".join(lines)
        else:
            # Just show stakeable assets with rates
            return "Run 'earn positions' to see current staking positions."
    except Exception as e:
        return f"Error: {e}"


def cmd_deposits(funding: Funding, asset: Optional[str] = None, address: bool = False, asset_param: Optional[str] = None) -> str:
    """Get deposit methods or address."""
    target_asset = asset or asset_param or "BTC"
    try:
        if address:
            result = funding.get_deposit_address(asset=target_asset, method="")
            if not result:
                return f"No deposit address found for {target_asset}."

            lines = [f"=== Deposit Address for {target_asset} ==="]
            for addr in result:
                lines.append(f"  Address: {addr.get('address', '?')}")
                if addr.get('tag'):
                    lines.append(f"  Tag: {addr.get('tag')}")
            return "\n".join(lines)
        else:
            result = funding.get_deposit_methods(asset=target_asset)
            if not result:
                return "No deposit methods found."

            lines = [f"=== Deposit Methods ({target_asset}) ==="]
            for method in result:
                lines.append(f"  {method.get('method', '?'):20s}: {method.get('description', '?')}")
            return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


def cmd_ticker(market: Market, pair: str) -> str:
    """Get ticker price."""
    try:
        result = market.get_ticker_info(pair=pair)
        if not result:
            return f"No ticker data for {pair}."

        lines = [f"=== Ticker {pair} ==="]
        ticker = result.get(pair, result)
        lines.append(f"  Price:      ${ticker.get('c', ['?'])[0]}")
        lines.append(f"  24h Volume: {ticker.get('v', ['?'])[0]}")
        lines.append(f"  High:       ${ticker.get('h', ['?'])[0]}")
        lines.append(f"  Low:        ${ticker.get('l', ['?'])[0]}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


def main():
    parser = argparse.ArgumentParser(description="Kraken Crypto CLI")
    parser.add_argument("command", choices=[
        "balance", "portfolio", "ledger", "trades", "earn", "deposits", "ticker"
    ], help="Command to run")
    parser.add_argument("--asset", help="Filter by asset (for ledger)")
    parser.add_argument("--pair", help="Filter by trading pair (for trades, ticker)")
    parser.add_argument("--limit", type=int, default=20, help="Limit results")
    parser.add_argument("--positions", action="store_true", help="Show earn positions")

    args = parser.parse_args()

    user, market, earn, funding = get_clients()

    if args.command == "balance":
        print(cmd_balance(user))
    elif args.command == "portfolio":
        print(cmd_portfolio(user))
    elif args.command == "ledger":
        print(cmd_ledger(user, args.asset, args.limit))
    elif args.command == "trades":
        print(cmd_trades(user, args.limit))
    elif args.command == "earn":
        print(cmd_earn(earn, args.positions))
    elif args.command == "deposits":
        print(cmd_deposits(funding, args.asset, args.positions, args.pair))
    elif args.command == "ticker":
        if not args.pair:
            print("Error: --pair required for ticker command")
            sys.exit(1)
        print(cmd_ticker(market, args.pair))


if __name__ == "__main__":
    main()
