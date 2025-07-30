import requests

url = "https://api.dexscreener.com/latest/dex/pairs/solana"
headers = {"User-Agent": "OrgoAlphaHunterBot/1.0"}

res = requests.get(url, headers=headers)

print("Status Code:", res.status_code)
print("Content-Type:", res.headers.get("Content-Type"))
print("Response snippet:", res.text[:500])