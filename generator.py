import requests
import json
import pathlib
from collections import defaultdict

BASE_URL = "https://eu.api.riotgames.com/val/content/v1/contents"

LOCALES = [
    "ar-AE",
    "de-DE",
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
    "zh-TW"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/143.0.0.0 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": "", # YOUR TOKEN HERE
}

OUTPUT_DIR = pathlib.Path(".")
TIMEOUT = 30

def download_all():
    for locale in LOCALES:
        response = requests.get(
            BASE_URL,
            headers=HEADERS,
            params={"locale": locale},
            timeout=TIMEOUT,
        )

        data = response.json()

        filename = OUTPUT_DIR / f"content_{locale}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False,
                sort_keys=False,
            )

        print(f"[OK] {locale} -> {filename} (HTTP {response.status_code})")

def collect_paths(obj, prefix=""):
    paths = set()

    if isinstance(obj, dict):
        for k, v in obj.items():
            path = f"{prefix}.{k}" if prefix else k
            paths.add(path)
            paths |= collect_paths(v, path)

    elif isinstance(obj, list):
        path = f"{prefix}[]"
        paths.add(path)
        for v in obj:
            paths |= collect_paths(v, path)

    return paths


def analyze_schema():
    locale_paths = {}

    for locale in LOCALES:
        filename = OUTPUT_DIR / f"content_{locale}.json"
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        locale_paths[locale] = collect_paths(data)

    path_usage = defaultdict(set)
    for locale, paths in locale_paths.items():
        for p in paths:
            path_usage[p].add(locale)

    all_locales = set(LOCALES)

    unique_only = {}
    missing_some = {}

    for path, used_in in path_usage.items():
        if len(used_in) == 1:
            unique_only[path] = next(iter(used_in))

        if used_in != all_locales:
            missing_some[path] = {
                "present_in": sorted(used_in),
                "missing_in": sorted(all_locales - used_in),
            }

    result = {
        "unique_only": unique_only,
        "missing_in_some_locales": missing_some,
    }

    with open("unique.json", "w", encoding="utf-8") as f:
        json.dump(
            result,
            f,
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )

    print("[OK] unique.json written")

if __name__ == "__main__":
    download_all()
    analyze_schema()
