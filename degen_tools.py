import json
import webbrowser
import httpx
from solders.keypair import Keypair
from solders.pubkey import Pubkey

WALLET_FILE = "solana_wallet.json"
RPC_URL = "https://api.devnet.solana.com"
TOKEN_PROGRAM_ID = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"


def generate_wallet():
    kp = Keypair()
    pubkey = str(kp.pubkey())
    privkey = list(kp.to_bytes())
    with open(WALLET_FILE, "w") as f:
        json.dump({"public_key": pubkey, "secret_key": privkey}, f)
    return pubkey


def load_wallet():
    with open(WALLET_FILE) as f:
        return json.load(f)["public_key"]


def check_balance(pubkey_str):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [pubkey_str]
    }
    try:
        response = httpx.post(RPC_URL, json=payload, timeout=10.0)
        lamports = response.json()["result"]["value"]
        sol = lamports / 1e9
        return sol
    except Exception as e:
        print("❌ Failed to fetch SOL balance:", e)
        return 0


def get_token_price_usd(token_mint):
    try:
        url = f"https://api.dexscreener.com/latest/dex/pairs/solana/{token_mint}"
        response = httpx.get(url, timeout=5.0)
        data = response.json()
        return float(data["pair"]["priceUsd"])
    except Exception:
        return None


def summarise_portfolio_value(pubkey_str):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenAccountsByOwner",
        "params": [
            pubkey_str,
            {"programId": TOKEN_PROGRAM_ID},
            {"encoding": "jsonParsed"}
        ]
    }

    try:
        response = httpx.post(RPC_URL, json=payload, timeout=10.0)
        data = response.json()["result"]["value"]

        print("\n📊 Wallet Value Summary:\n")
        total_usd = 0

        for token in data:
            try:
                info = token["account"]["data"]["parsed"]["info"]
                mint = info["mint"]
                amount = info["tokenAmount"]["uiAmount"]

                if amount is None or amount == 0:
                    continue

                price = get_token_price_usd(mint)
                if price:
                    value = float(amount) * price
                    total_usd += value
                    print(f" - {mint[:4]}...: {amount:,.0f}   (${value:.2f})")
                else:
                    print(f" - {mint[:4]}...: {amount:,.0f}   (price N/A)")

            except Exception as e:
                print("⚠️ Token parse failed:", e)

        sol = check_balance(pubkey_str)
        sol_price = get_token_price_usd("So11111111111111111111111111111111111111112")
        if sol_price:
            sol_value = sol * sol_price
            total_usd += sol_value
            print(f"\n - SOL: {sol:.4f}   (${sol_value:.2f})")

        print(f"\n💰 Total: ${total_usd:.2f}\n")

    except Exception as e:
        print("❌ Portfolio summary failed:", e)


def open_jupiter_trade(token_mint):
    url = f"https://jupiter-terminal.dexscreener.com/?outputMint={token_mint}"
    print(f"🛒 Simulated trade link:\n{url}")
    webbrowser.open(url)
