#!/usr/bin/env python3
"""Build a public Steam playtime snapshot for Hugo without exposing the API key."""

import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlencode, urlparse
from urllib.request import Request, urlopen


API_ROOT = "https://api.steampowered.com"
OUTPUT = Path(__file__).resolve().parents[1] / "data" / "steam.json"
GAME_LIMIT = 8
RECENT_LIMIT = 4
EXCLUDED_APP_IDS = {431960}  # Wallpaper Engine is software, not a game.


def request_steam(interface, method, params, api_key):
    url = f"{API_ROOT}/{interface}/{method}/v1/?{urlencode(params)}"
    request = Request(
        url,
        headers={"x-webapi-key": api_key, "Accept": "application/json"},
    )
    with urlopen(request, timeout=20) as response:
        return json.load(response)


def resolve_steam_id(profile, api_key):
    profile = profile.strip()
    if re.fullmatch(r"\d{17}", profile):
        return profile

    if profile.startswith("steamcommunity.com/"):
        profile = "https://" + profile
    parsed = urlparse(profile)
    if parsed.scheme not in ("http", "https") or parsed.netloc.lower() not in (
        "steamcommunity.com",
        "www.steamcommunity.com",
    ):
        raise ValueError("STEAM_ID must be a SteamID64 or a steamcommunity.com profile URL")

    parts = [unquote(part) for part in parsed.path.strip("/").split("/")]
    if len(parts) != 2:
        raise ValueError("STEAM_ID must point to a Steam profile")
    kind, value = parts
    if kind == "profiles" and re.fullmatch(r"\d{17}", value):
        return value
    if kind != "id" or not value:
        raise ValueError("STEAM_ID must point to a Steam profile")

    result = request_steam("ISteamUser", "ResolveVanityURL", {"vanityurl": value}, api_key)
    response = result.get("response", {})
    if response.get("success") != 1 or not re.fullmatch(r"\d{17}", str(response.get("steamid", ""))):
        raise ValueError("Could not resolve the Steam profile URL")
    return str(response["steamid"])


def playtime_label(minutes):
    if minutes < 60:
        return f"{minutes} 分钟"
    return f"{minutes / 60:,.1f} 小时"


def normalize_game(item):
    try:
        appid = int(item["appid"])
        minutes = int(item.get("playtime_forever", 0))
    except (KeyError, TypeError, ValueError):
        return None
    if appid <= 0 or appid in EXCLUDED_APP_IDS or minutes <= 0:
        return None
    icon_hash = str(item.get("img_icon_url", ""))
    icon_url = ""
    if re.fullmatch(r"[0-9a-fA-F]{40}", icon_hash):
        icon_url = f"https://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{icon_hash}.jpg"
    return {
        "appid": appid,
        "name": str(item.get("name") or f"Steam App {appid}"),
        "playtime_minutes": minutes,
        "playtime_label": playtime_label(minutes),
        "store_url": f"https://store.steampowered.com/app/{appid}/",
        "icon_url": icon_url,
    }


def build_snapshot(steam_id, owned_response, recent_response=None):
    now = datetime.now(timezone.utc)
    china_time = now.astimezone(timezone(timedelta(hours=8)))
    count = owned_response.get("game_count")
    raw_games = owned_response.get("games", [])
    if not isinstance(count, int) or not isinstance(raw_games, list):
        status = "unavailable"
        raw_games = []
    else:
        status = "ok" if count > 0 else "empty"

    all_games = {}
    for item in raw_games:
        game = normalize_game(item)
        if game:
            all_games[game["appid"]] = game

    recent_raw = recent_response.get("games", []) if isinstance(recent_response, dict) else None
    recent_available = isinstance(recent_raw, list)
    recent_games = []
    recent_ids = set()
    if recent_available and status == "ok":
        for item in recent_raw:
            try:
                appid = int(item["appid"])
            except (KeyError, TypeError, ValueError):
                continue
            if appid in EXCLUDED_APP_IDS or appid in recent_ids:
                continue
            game = all_games.get(appid) or normalize_game(item)
            if not game:
                continue
            all_games.setdefault(appid, game)
            recent_ids.add(appid)
            try:
                recent_minutes = max(0, int(item.get("playtime_2weeks", 0) or 0))
            except (TypeError, ValueError):
                recent_minutes = 0
            recent_game = dict(all_games[appid])
            recent_game["recent_playtime_minutes"] = recent_minutes
            recent_game["recent_playtime_label"] = playtime_label(recent_minutes) if recent_minutes else ""
            recent_games.append(recent_game)

    recent_games.sort(key=lambda game: (-game["recent_playtime_minutes"], -game["playtime_minutes"], game["appid"]))
    history_games = sorted(
        (game for appid, game in all_games.items() if appid not in recent_ids),
        key=lambda game: (-game["playtime_minutes"], game["appid"]),
    )
    total_minutes = sum(game["playtime_minutes"] for game in all_games.values())
    if not all_games:
        status = "empty" if status == "ok" else status
    return {
        "status": status,
        "steam_id": steam_id,
        "profile_url": f"https://steamcommunity.com/profiles/{steam_id}/",
        "played_game_count": len(all_games),
        "total_playtime_label": playtime_label(total_minutes),
        "recent_available": recent_available,
        "recent_game_count": len(recent_games),
        "recent_games": recent_games[:RECENT_LIMIT],
        "history_game_count": len(history_games),
        "history_games": history_games[:GAME_LIMIT],
        "updated_at_iso": now.isoformat(timespec="seconds"),
        "updated_at_display": china_time.strftime("%Y-%m-%d %H:%M"),
    }


def main():
    api_key = os.environ.get("STEAM_API_KEY", "").strip()
    profile = os.environ.get("STEAM_ID", "").strip()
    if not api_key:
        print("STEAM_API_KEY is not configured; skipping Steam snapshot.")
        return 0
    if not profile:
        print("STEAM_ID must be configured when STEAM_API_KEY is set.", file=sys.stderr)
        return 1

    try:
        steam_id = resolve_steam_id(profile, api_key)
        result = request_steam(
            "IPlayerService",
            "GetOwnedGames",
            {"steamid": steam_id, "include_appinfo": 1, "include_played_free_games": 1},
            api_key,
        )
        response = result.get("response") if isinstance(result, dict) else None
        if not isinstance(response, dict):
            raise ValueError("Steam returned an unexpected response")
        recent_response = None
        try:
            recent_result = request_steam(
                "IPlayerService", "GetRecentlyPlayedGames", {"steamid": steam_id, "count": 0}, api_key
            )
            recent_response = recent_result.get("response") if isinstance(recent_result, dict) else None
        except (HTTPError, URLError, ValueError, TypeError, json.JSONDecodeError):
            print("Recent Steam activity is unavailable; showing historical games only.", file=sys.stderr)
        snapshot = build_snapshot(steam_id, response, recent_response)
    except HTTPError as error:
        print(f"Steam API returned HTTP {error.code}.", file=sys.stderr)
        return 1
    except URLError:
        print("Could not connect to the Steam API.", file=sys.stderr)
        return 1
    except (ValueError, TypeError, json.JSONDecodeError) as error:
        print(f"Steam data is unavailable: {error}", file=sys.stderr)
        return 1

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Steam snapshot generated: {snapshot['played_game_count']} played games, "
        f"{snapshot['recent_game_count']} recently played."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
