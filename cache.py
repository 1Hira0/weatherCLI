import json
import time
import os

CACHE_FILE = "./cache.json"
TTL = 900  # 15 minutes


def _load():
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def _save(data):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def _is_valid(method, data):
    try:
        if method == "current":
            ts = data["current"]["last_updated_epoch"]
        else:  
            ts = data["location"]["localtime_epoch"]
        return time.time() - ts < TTL
    except KeyError:
        return False


def get(method: str, loc: str):
    cache = _load()

    if method not in cache:
        return {}

    if loc not in cache[method]:
        return {}

    data = cache[method][loc]

    if not _is_valid(method, data):
        return {}

    return data


def store(method, loc, data):
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as file:
            content = file.read()
            if content.startswith("{"):
                all_cache = json.loads(content)
            else:
                all_cache = {}
    else:
        all_cache = {}

    if method not in all_cache:
        all_cache[method] = {}

    all_cache[method][loc] = data

    with open(CACHE_FILE, "w", encoding="utf-8") as file:
        json.dump(all_cache, file, indent=4)
