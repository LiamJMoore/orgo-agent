import requests
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

DEXSCREENER_API = "https://api.dexscreener.com/token-profiles/latest/v1"
HEADERS = {"User-Agent": "OrgoAlphaHunterBot/2.0"}


def analyze_token(name, description, tweet=""):
    prompt = f"""
Token Name: {name}
Description: {description}
Recent Tweet: {tweet}

Classify this token as one of the following categories:
- Meme
- Legit
- Rug

Also provide a 1-line summary and assign a risk level:
- 🟢 Low Risk
- 🟡 Medium Risk
- 🔴 High Risk

Return format:
1. Category: <one word>
2. Risk Level: <emoji>
3. 1-line summary: <summary>
"""
    try:
        res = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ GPT Error: {e}"


def run_alpha_hunter():
    print("🧠 Running GPT-Powered Alpha Hunter on Top Solana Tokens...\n")
    best_token = None

    try:
        res = requests.get(DEXSCREENER_API, headers=HEADERS, timeout=10)
        if res.status_code != 200:
            raise Exception(f"DEX API Error: {res.status_code}")

        data = res.json()
        tokens = [t for t in data if t.get("chainId") == "solana"][:5]
        print(f"✅ Found {len(tokens)} Solana tokens\n")

        results = []

        for token in tokens:
            name = token.get("header", "Unknown")
            description = token.get("description", "")
            address = token.get("tokenAddress", "")
            pair_address = token.get("pairAddress", "")
            url = f"https://dexscreener.com/solana/{pair_address}"

            print(f"🔍 {url} — {address}")
            summary = analyze_token(name, description)
            print(summary)
            print(f"🔗 {url}\n")

            if "🟢" in summary and "Legit" in summary:
                results.append({
                    "symbol": name,
                    "description": description,
                    "url": url,
                    "address": address
                })

        if results:
            best_token = sorted(results, key=lambda x: x["symbol"])[0]

        return best_token

    except Exception as e:
        print(f"❌ Failed to fetch tokens: {e}")
        return None
