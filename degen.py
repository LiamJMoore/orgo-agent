from degen_tools import *

def run_degen_mode():
    print("\n🔥 ORGO DEGEN MODE v2 — With USD Portfolio 🔥\n")

    webbrowser.open("https://solflare.com/download")

    print("🔐 Generating new wallet...")
    pubkey = generate_wallet()
    print(f"🪪 Public Key: {pubkey}")

    print("\n📊 Calculating USD value of holdings...")
    summarise_portfolio_value(pubkey)

    print("\n🛒 Simulating BONK trade on Jupiter...")
    open_jupiter_trade("DezXyvT6XiYkxjzF8rr4LwFxLyh9fjGCDNx8g9PAVyrR")

    print("\n✅ Orgo is wallet-aware and USD-literate. Time to degen.\n")

if __name__ == "__main__":
    run_degen_mode()
