from degen_tools import (
    generate_keypair,
    check_balance,
    scan_wallet_tokens,
    get_usd_portfolio_value,
    save_wallet_to_file
)
from alpha_hunter import run_alpha_hunter
import time


def run_degen_mode():
    print("🔥 ORGO DEGEN MODE v1 🔥\n")

    print("🧠 Scanning top Solana tokens with Alpha Hunter...\n")
    best_token = run_alpha_hunter()
    print("🔍 Alpha hunt complete. Proceeding with wallet ops...\n")

    print("🔐 Generating new wallet...")
    kp = generate_keypair()
    pubkey = str(kp.pubkey())
    print(f"🪪 Public Key: {pubkey}\n")

    save_wallet_to_file(kp)

    print("💰 Checking SOL balance...")
    sol_balance = check_balance(pubkey)
    print(f"💰 Balance: {sol_balance:.4f} SOL\n")

    print("📦 Scanning wallet tokens...")
    tokens = scan_wallet_tokens(pubkey)

    print("📊 Calculating USD value of holdings...\n")
    total = get_usd_portfolio_value(tokens)
    print("\n📊 Wallet Value Summary:\n")
    for symbol, value in tokens.items():
        print(f"• {symbol}: ${value:.2f}")
    print(f"\n💰 Total: ${total:.2f}\n")

    if best_token:
        print(f"🛒 Simulating trade on Jupiter for {best_token['symbol']}...")
        print("🛒 Simulated trade link:")
        print(f"https://jupiter-terminal.dexscreener.com/?outputMint={best_token['address']}\n")
    else:
        print("🛒 Simulating BONK trade on Jupiter...")
        print("🛒 Simulated trade link:")
        print("https://jupiter-terminal.dexscreener.com/?outputMint=DezXyvT6XiYkxjzF8rr4LwFxLyh9fjGCDNx8g9PAVyrR\n")

    print(f"✅ Orgo is wallet-aware and USD-literate. Time to degen.")


if __name__ == "__main__":
    run_degen_mode()
