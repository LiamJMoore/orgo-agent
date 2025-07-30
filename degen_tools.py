# degen_tools.py
import requests
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
import json
import base58

def save_wallet_to_file(kp, filename="wallet.json"):
    wallet_data = {
        "public_key": str(kp.pubkey()),
        "secret_key": list(kp.secret())  # Store as list of ints for JSON compatibility
    }
    with open(filename, "w") as f:
        json.dump(wallet_data, f)
    print(f"💾 Wallet saved to {filename}")
# Create a new wallet
def generate_keypair():
    return Keypair()

# Get SOL balance
def check_balance(pubkey_str):
    client = Client("https://api.devnet.solana.com")
    try:
        response = client.get_balance(Pubkey.from_string(pubkey_str))
        if response.value is not None:
            return response.value / 1e9  # convert lamports to SOL
        else:
            return 0.0
    except Exception as e:
        print(f"❌ Balance check failed: {e}")
        return 0.0

# Scan token balances (mocked for now)
def scan_wallet_tokens(pubkey_str):
    try:
        return {}  # Replace with real token fetch later
    except Exception as e:
        print(f"❌ Token scan failed: {e}")
        return {}

# Get total USD portfolio value
def get_usd_portfolio_value(token_dict):
    try:
        return sum(token_dict.values())
    except:
        return 0.0
