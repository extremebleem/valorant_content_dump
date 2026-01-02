import requests
import pathlib
import json

BASE_URL = "https://eu.api.riotgames.com/val/content/v1/contents"

LOCALES = [
    "ar-AE",
    "de-DE",
    "en-GB",
    "en-US",
    "es-ES",
    "es-MX",
    "fr-FR",
    "id-ID",
    "it-IT",
    "ja-JP",
    "ko-KR",
    "pl-PL",
    "pt-BR",
    "ru-RU",
    "th-TH",
    "tr-TR",
    "vi-VN",
    "zh-CN",
    "zh-TW",
]

HEADERS = {
    "User-Agent":   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/143.0.0.0 Safari/537.36",
                    "Accept-Language": "q=0.9,en-US;q=0.8,en;q=0.7",
                    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Origin": "https://developer.riotgames.com",
                    "X-Riot-Token": "PLACE_YOUR_TOKEN_HERE", # <- TOKEN
}

OUTPUT_DIR = pathlib.Path(".")
OUTPUT_DIR.mkdir(exist_ok=True)

for locale in LOCALES:
    response = requests.get(
        BASE_URL,
        headers=HEADERS,
        params={"locale": locale},
        timeout=30,
    )

    filename = OUTPUT_DIR / f"content_{locale}.json"

    data = response.json()

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2,
            sort_keys=False,
        )

    print(f"{locale}: HTTP {response.status_code} -> pretty JSON saved")