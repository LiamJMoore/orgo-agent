import requests
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
import json


def save_wallet_to_file(kp, filename="wallet.json"):
    wallet_data = {
        "public_key": str(kp.pubkey()),
        "secret_key": list(kp.secret())  # List of ints for JSON
    }
    with open(filename, "w") as f:
        json.dump(wallet_data, f)
    print(f"💾 Wallet saved to {filename}")


def generate_keypair():
    return Keypair()


def check_balance(pubkey_str):
    client = Client("https://api.devnet.solana.com")
    try:
        response = client.get_balance(Pubkey.from_string(pubkey_str))
        return response.value / 1e9 if response.value else 0.0
    except Exception as e:
        print(f"❌ Balance check failed: {e}")
        return 0.0


def scan_wallet_tokens(pubkey_str):
    try:
        return {}  # Placeholder for real token scan
    except Exception as e:
        print(f"❌ Token scan failed: {e}")
        return {}


def get_usd_portfolio_value(token_dict):
    try:
        return sum(token_dict.values())
    except:
        return 0.0
