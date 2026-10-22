"""Ronda — zero-dependency HTTP API + PWA host.

Run with:  python ronda/server.py
"""
from __future__ import annotations

import json
import mimetypes
import os
import queue
import re
import sys
import threading
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import core  # noqa: E402
from core import (  # noqa: E402
    AVATARS, CATEGORIES, CATEGORY_MAP, CITIES, DAILY_COINS, FMT, INTERESTS, LIKE_COST, ZONES,
    WELCOME_COINS, add_message, add_notification, city_coords, claim_daily, coin_balance,
    create_match, create_session, distance_km, ensure_plan_thread, fmt, grant_welcome, hash_password,
    initials, load_json, mark_read, now, now_str, other_user, parse_dt, public_user,
    seed_demo, spend_coins, unread_count, user_by_token, verify_password,
)
from db import DB_PATH, connect, init_db  # noqa: E402

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FROZEN = bool(getattr(sys, "frozen", False))
RESOURCE_DIR = getattr(sys, "_MEIPASS", BASE_DIR)
STATIC_DIR = os.path.join(RESOURCE_DIR, "static")
HOST = os.environ.get("RONDA_HOST", "0.0.0.0")
PORT = int(os.environ.get("RONDA_PORT", "8788"))

mimetypes.add_type("font/woff2", ".woff2")
mimetypes.add_type("application/manifest+json", ".webmanifest")


# --------------------------------------------------------------------- events
class EventHub:
    """Server-sent events, one channel per user."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._clients: dict[int, set[queue.Queue]] = {}

    def subscribe(self, user_id: int) -> queue.Queue:
        q: queue.Queue = queue.Queue(maxsize=64)
        with self._lock:
            self._clients.setdefault(user_id, set()).add(q)
        return q

    def unsubscribe(self, user_id: int, q: queue.Queue) -> None:
        with self._lock:
            clients = self._clients.get(user_id, set())
            clients.discard(q)
            if not clients:
                self._clients.pop(user_id, None)

    def publish(self, user_ids) -> None:
        with self._lock:
            targets = []
            for user_id in set(user_ids):
                targets.extend(self._clients.get(int(user_id), ()))
        for q in targets:
            try:
                q.put_nowait({"at": now_str()})
            except queue.Full:
                pass

    def publish_all(self) -> None:
        with self._lock:
            targets = [q for clients in self._clients.values() for q in clients]
        for q in targets:
            try:
                q.put_nowait({"at": now_str()})
            except queue.Full:
                pass


HUB = EventHub()


class ApiError(Exception):
    def __init__(self, message: str, status: int = 400) -> None:
        super().__init__(message)
        self.message = message
        self.status = status


# ------------------------------------------------------------------ helpers
def require(data: dict, key: str, label: str | None = None):
    value = data.get(key)
    if isinstance(value, str):
        value = value.strip()
    if value in (None, "", []):
        raise ApiError(f"Falta «{label or key}»")
    return value


def as_int(value, default=None):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def user_index(conn):
    return {row["id"]: row for row in conn.execute("SELECT * FROM users").fetchall()}


def wallet_payload(conn, user_row) -> dict:
    transactions = [
        {
            "id": row["id"],
            "delta": row["delta"],
            "kind": row["kind"],
            "note": row["note"],
            "balance_after": row["balance_after"],
            "created_at": row["created_at"],
        }
        for row in conn.execute(
            "SELECT * FROM coin_ledger WHERE user_id = ? ORDER BY id DESC LIMIT 30",
            (user_row["id"],),
        ).fetchall()
    ]
    today = now().strftime(core.DATE_FMT)
    return {
        "coins": user_row["coins"],
        "daily_available": user_row["last_daily"] != today,
        "daily_amount": DAILY_COINS,
        "like_cost": LIKE_COST,
        "welcome_amount": WELCOME_COINS,
        "transactions": transactions,
    }


def plan_thread_map(conn):
    return {
        row["plan_id"]: row["id"]
        for row in conn.execute("SELECT id, plan_id FROM threads WHERE kind = 'plan'").fetchall()
    }


def plan_members(conn, plan_id):
    rows = conn.execute(
        """SELECT pm.user_id, pm.role, pm.status, pm.joined_at, u.*
           FROM plan_members pm JOIN users u ON u.id = pm.user_id
           WHERE pm.plan_id = ?
           ORDER BY CASE pm.role WHEN 'host' THEN 0 ELSE 1 END, pm.id""",
        (plan_id,),
    ).fetchall()
    return rows


def public_venue(row, me=None):
    data = {
        "id": row["id"],
        "name": row["name"],
        "city": row["city"],
        "area": row["area"],
        "category": row["category"],
        "emoji": row["emoji"],
        "lat": row["lat"],
        "lon": row["lon"],
        "blurb": row["blurb"],
    }
    if me is not None:
        data["distance_km"] = distance_km(me, row)
    return data


def serialize_plan(conn, row, me, users, threads=None):
    members_rows = plan_members(conn, row["id"])
    joined = [r for r in members_rows if r["status"] == "joined"]
    pending = [r for r in members_rows if r["status"] == "pending"]
    host = users.get(row["host_id"])
    my_status = None
    for r in members_rows:
        if r["user_id"] == me["id"] and r["status"] in ("joined", "pending"):
            my_status = "host" if r["role"] == "host" else r["status"]
            break
    my_interests = set(load_json(me["interests"]))
    shared = set()
    for r in joined:
        shared.update(my_interests.intersection(load_json(r["interests"])))
    capacity = row["spots"] + 1
    start = parse_dt(row["start_at"])
    data = {
        "id": row["id"],
        "title": row["title"],
        "category": row["category"],
        "category_label": CATEGORY_MAP.get(row["category"], CATEGORY_MAP["planes"])["label"],
        "emoji": row["emoji"],
        "description": row["description"],
        "start_at": row["start_at"],
        "city": row["city"] if "city" in row.keys() else "Madrid",
        "zone": row["zone"],
        "venue": row["venue"],
        "venue_id": row["venue_id"] if "venue_id" in row.keys() else None,
        "spots": row["spots"],
        "capacity": capacity,
        "spots_left": max(0, capacity - len(joined)),
        "approval": bool(row["approval"]),
        "vibe": load_json(row["vibe"]),
        "status": row["status"],
        "created_at": row["created_at"],
        "host": public_user(host, me),
        "members": [public_user(r, me) for r in joined],
        "member_count": len(joined),
        "my_status": my_status,
        "pending": [public_user(r, me) for r in pending] if row["host_id"] == me["id"] else [],
        "pending_count": len(pending) if row["host_id"] == me["id"] else 0,
        "thread_id": (threads or {}).get(row["id"]),
        "compatibility": len(shared),
        "shared_interests": sorted(shared),
        "distance_km": distance_km(me, row),
        "past": bool(start and start < now()),
    }
    return data


def serialize_thread(conn, thread_row, me, users, plans):
    thread_id = thread_row["id"]
    plan = plans.get(thread_row["plan_id"]) if thread_row["plan_id"] else None
    other = other_user(conn, thread_id, me["id"])
    last = conn.execute(
        """SELECT m.*, u.name AS author_name FROM messages m
           LEFT JOIN users u ON u.id = m.user_id
           WHERE m.thread_id = ? ORDER BY m.id DESC LIMIT 1""",
        (thread_id,),
    ).fetchone()
    member_count = conn.execute(
        "SELECT COUNT(*) AS n FROM thread_members WHERE thread_id = ?", (thread_id,)
    ).fetchone()["n"]
    last_message = None
    if last:
        last_message = {
            "id": last["id"],
            "body": last["body"],
            "kind": last["kind"],
            "created_at": last["created_at"],
            "user_id": last["user_id"],
            "author": last["author_name"] or "Ronda",
        }
    title = plan["title"] if plan else (other["name"] if other else "Chat")
    return {
        "id": thread_id,
        "kind": thread_row["kind"],
        "title": title,
        "plan": {
            "id": plan["id"], "title": plan["title"], "emoji": plan["emoji"],
            "start_at": plan["start_at"], "zone": plan["zone"],
            "city": plan["city"] if "city" in plan.keys() else "Madrid",
            "status": plan["status"],
        } if plan else None,
        "other": public_user(other, me) if other else None,
        "member_count": member_count,
        "last_message": last_message,
        "last_at": thread_row["last_at"],
        "unread": unread_count(conn, me["id"], thread_id),
        "created_at": thread_row["created_at"],
    }


def build_state(conn, me_row) -> dict:
    me = public_user(me_row)
    users = user_index(conn)
    threads = plan_thread_map(conn)
    all_plans = {row["id"]: row for row in conn.execute("SELECT * FROM plans").fetchall()}

    threshold = fmt(now() - timedelta(hours=3))
    plan_rows = conn.execute(
        """SELECT * FROM plans WHERE status IN ('open', 'full') AND start_at >= ?
           ORDER BY start_at ASC LIMIT 120""",
        (threshold,),
    ).fetchall()
    plans = [serialize_plan(conn, row, me_row, users, threads) for row in plan_rows]
    plan_by_id = {p["id"]: p for p in plans}
    my_plans = [p for p in plans if p["my_status"] in ("host", "joined", "pending")]

    swiped = {
        row["to_user"]: row["action"]
        for row in conn.execute("SELECT to_user, action FROM swipes WHERE from_user = ?", (me_row["id"],)).fetchall()
    }
    open_plans_by_host: dict[int, list] = {}
    for p in plans:
        if p["status"] == "open" and p["start_at"] >= now_str():
            open_plans_by_host.setdefault(p["host"]["id"], []).append(p)

    deck = []
    for row in users.values():
        if row["id"] == me_row["id"] or row["id"] in swiped:
            continue
        dist = distance_km(me_row, row)
        if dist > me_row["max_distance"]:
            continue
        if not (me_row["age_min"] <= row["age"] <= me_row["age_max"]):
            continue
        person = public_user(row, me_row)
        hosted = open_plans_by_host.get(row["id"], [])
        deck.append({
            "user": person,
            "plans_count": len(hosted),
            "plan": hosted[0] if hosted else None,
            "shared_interests": person["shared_interests"],
            "distance_km": dist,
        })
    deck.sort(key=lambda item: (-len(item["shared_interests"]), item["distance_km"], -item["plans_count"]))

    thread_rows = conn.execute(
        """SELECT t.* FROM threads t JOIN thread_members tm ON tm.thread_id = t.id
           WHERE tm.user_id = ? ORDER BY t.last_at DESC LIMIT 80""",
        (me_row["id"],),
    ).fetchall()
    thread_list = [serialize_thread(conn, row, me_row, users, all_plans) for row in thread_rows]

    notif_rows = conn.execute(
        "SELECT * FROM notifications WHERE user_id = ? ORDER BY id DESC LIMIT 30",
        (me_row["id"],),
    ).fetchall()
    notifications = [dict(row) for row in notif_rows]
    unread_notifications = sum(1 for n in notifications if not n["read"])

    match_threads = [t for t in thread_list if t["kind"] == "match"]
    joined_plans = [p for p in my_plans if p["my_status"] in ("host", "joined")]
    pending_requests = sum(p["pending_count"] for p in my_plans if p["my_status"] == "host")
    stats = {
        "plans": len(joined_plans),
        "matches": len(match_threads),
        "connections": len({t["other"]["id"] for t in thread_list if t["other"]}),
        "pending": pending_requests,
    }
    wallet = wallet_payload(conn, me_row)
    venue_rows = conn.execute("SELECT * FROM venues ORDER BY id").fetchall()
    venues = [public_venue(row, me_row) for row in venue_rows]
    venues.sort(key=lambda item: item["distance_km"])
    me_payload = dict(me)
    me_payload.update({
        "max_distance": me_row["max_distance"],
        "age_min": me_row["age_min"],
        "age_max": me_row["age_max"],
        "lat": me_row["lat"],
        "lon": me_row["lon"],
        "location_exact": me_row["location_exact"],
        "stats": stats,
        "username": me_row["username"],
        "coins": me_row["coins"],
    })

    return {
        "me": me_payload,
        "plans": plans,
        "my_plans": my_plans,
        "deck": deck,
        "threads": thread_list,
        "matches": match_threads,
        "notifications": notifications,
        "unread_notifications": unread_notifications,
        "unread_messages": sum(t["unread"] for t in thread_list),
        "stats": stats,
        "wallet": wallet,
        "venues": venues,
        "catalog": {
            "cities": [CITIES[name] for name in sorted(CITIES)],
            "venues": [public_venue(row) for row in venue_rows],
            "zones": list(ZONES.keys()),
            "categories": CATEGORIES,
            "interests": INTERESTS,
            "avatars": AVATARS,
        },
        "server_time": now_str(),
    }


# ------------------------------------------------------------------- auth
def api_register(data, me=None):
    username = str(require(data, "username", "usuario")).lower().strip()
    if not re.fullmatch(r"[a-z0-9_.]{3,20}", username):
        raise ApiError("El usuario debe tener 3-20 caracteres: letras, números, punto o guion bajo")
    name = str(require(data, "name", "nombre"))[:40]
    password = str(require(data, "password", "contraseña"))
    if len(password) < 8:
        raise ApiError("La contraseña necesita al menos 8 caracteres")
    age = as_int(data.get("age"), 24)
    if not 18 <= age <= 99:
        raise ApiError("La edad debe estar entre 18 y 99")
    city = str(data.get("city") or "Madrid")
    if city not in CITIES:
        raise ApiError("Esa ciudad no está disponible")
    area = str(data.get("zone") or data.get("area") or "")[:60]
    lat, lon = city_coords(city)
    interests = clean_interests(data.get("interests"))
    bio = str(data.get("bio") or "")[:200]
    looking_for = str(data.get("looking_for") or "")[:120]
    status_note = str(data.get("status_note") or "")[:80]
    avatar = str(data.get("avatar") or "🦋")[:8]
    variant = as_int(data.get("variant"), 0) % 8
    with connect() as conn:
        exists = conn.execute("SELECT 1 FROM users WHERE username = ?", (username,)).fetchone()
        if exists:
            raise ApiError("Ese usuario ya existe")
        digest, salt = hash_password(password)
        stamp = now_str()
        cur = conn.execute(
            """INSERT INTO users(name, username, pass_hash, pass_salt, age, zone, city, lat, lon,
               bio, avatar, variant, interests, looking_for, status_note, created_at, last_seen)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (name, username, digest, salt, age, area, city, lat, lon,
             bio, avatar, variant, json.dumps(interests, ensure_ascii=False),
             looking_for, status_note, stamp, stamp),
        )
        user_id = cur.lastrowid
        grant_welcome(conn, user_id)
        token = create_session(conn, user_id)
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        HUB.publish_all()
        return {
            "token": token,
            "user": public_user(row),
            "coins": row["coins"],
            "welcome_granted": True,
            "wallet": wallet_payload(conn, row),
        }


def api_login(data, me=None):
    username = str(require(data, "username", "usuario")).lower().strip()
    password = str(require(data, "password", "contraseña"))
    with connect() as conn:
        row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if not row or not verify_password(password, row["pass_hash"], row["pass_salt"]):
            raise ApiError("Usuario o contraseña incorrectos", 401)
        conn.execute("UPDATE users SET last_seen = ? WHERE id = ?", (now_str(), row["id"]))
        welcome = grant_welcome(conn, row["id"])
        token = create_session(conn, row["id"])
        row = conn.execute("SELECT * FROM users WHERE id = ?", (row["id"],)).fetchone()
        return {
            "token": token,
            "user": public_user(row),
            "coins": row["coins"],
            "welcome_granted": welcome is not None,
            "wallet": wallet_payload(conn, row),
        }


def api_demo_accounts(data=None, me=None):
    wanted = ["lucia", "hugo", "vera", "nico"]
    with connect() as conn:
        rows = conn.execute(
            f"SELECT * FROM users WHERE username IN ({','.join('?' * len(wanted))})", wanted
        ).fetchall()
        by_name = {row["username"]: row for row in rows}
        return {
            "accounts": [
                {
                    "username": username,
                    "name": by_name[username]["name"],
                    "age": by_name[username]["age"],
                    "city": by_name[username]["city"],
                    "zone": by_name[username]["zone"],
                    "avatar": by_name[username]["avatar"],
                    "variant": by_name[username]["variant"] % 8,
                    "initials": initials(by_name[username]["name"]),
                }
                for username in wanted if username in by_name
            ]
        }


def api_catalog(data=None, me=None):
    with connect() as conn:
        venues = [public_venue(row) for row in conn.execute("SELECT * FROM venues ORDER BY city, name").fetchall()]
    return {
        "cities": [CITIES[name] for name in sorted(CITIES)],
        "venues": venues,
        "zones": list(ZONES.keys()),
        "categories": CATEGORIES,
        "interests": INTERESTS,
        "avatars": AVATARS,
    }


def api_logout(data, me):
    token = str(data.get("token") or "")
    with connect() as conn:
        conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
    return {"ok": True}


# ------------------------------------------------------------------- state
def api_state(data=None, me=None):
    with connect() as conn:
        conn.execute("UPDATE users SET last_seen = ? WHERE id = ?", (now_str(), me["id"]))
        grant_welcome(conn, me["id"])
        row = conn.execute("SELECT * FROM users WHERE id = ?", (me["id"],)).fetchone()
        return build_state(conn, row)


def api_wallet(data=None, me=None):
    with connect() as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (me["id"],)).fetchone()
        return wallet_payload(conn, row)


def api_daily(data, me):
    with connect() as conn:
        balance = claim_daily(conn, me["id"])
        if balance is None:
            raise ApiError("Ya has reclamado tus monedas de hoy. Vuelve mañana.", 400)
        row = conn.execute("SELECT * FROM users WHERE id = ?", (me["id"],)).fetchone()
        HUB.publish([me["id"]])
        return {
            "claimed": True,
            "amount": DAILY_COINS,
            "coins": balance,
            "wallet": wallet_payload(conn, row),
        }


# ------------------------------------------------------------------- plans
def clean_interests(value):
    if value is None:
        return []
    if not isinstance(value, list):
        raise ApiError("Los intereses deben ser una lista")
    cleaned = []
    for item in value:
        text = str(item).strip()[:24]
        if text and text not in cleaned:
            cleaned.append(text)
    if len(cleaned) > 8:
        raise ApiError("Elige como máximo 8 intereses")
    return cleaned


def api_plan_create(data, me):
    title = str(require(data, "title", "título"))[:70]
    category = str(data.get("category") or "planes")
    if category not in CATEGORY_MAP:
        raise ApiError("Categoría no válida")
    start_date = str(require(data, "date", "fecha"))
    start_time = str(require(data, "time", "hora"))
    start_at = parse_dt(f"{start_date}T{start_time}")
    if not start_at:
        raise ApiError("Fecha u hora no válida")
    if start_at < now() - timedelta(minutes=10):
        raise ApiError("Ese plan ya ha empezado. Elige otra fecha")
    city = str(data.get("city") or me["city"] or "Madrid")
    if city not in CITIES:
        raise ApiError("Esa ciudad no está disponible")
    area = str(data.get("zone") or data.get("area") or "")[:60]
    venue_name = str(data.get("venue") or "")[:80]
    venue_id = as_int(data.get("venue_id"))
    spots = as_int(data.get("spots"), 2)
    if not 1 <= spots <= 12:
        raise ApiError("Busca entre 1 y 12 personas")
    vibe = clean_interests(data.get("vibe") or [])
    stamp = now_str()
    with connect() as conn:
        venue_row = None
        if venue_id:
            venue_row = conn.execute("SELECT * FROM venues WHERE id = ?", (venue_id,)).fetchone()
        if not venue_row and venue_name:
            venue_row = conn.execute(
                "SELECT * FROM venues WHERE name = ? AND city = ?", (venue_name, city)
            ).fetchone()
        if venue_row:
            city = venue_row["city"]
            area = venue_row["area"] or area
            venue_name = venue_row["name"]
            venue_id = venue_row["id"]
            lat, lon = venue_row["lat"], venue_row["lon"]
        else:
            venue_id = None
            lat, lon = city_coords(city)
        meta = CATEGORY_MAP[category]
        cur = conn.execute(
            """INSERT INTO plans(host_id, title, category, emoji, description, start_at, zone, city,
               lat, lon, venue, venue_id, spots, approval, vibe, status, created_at, updated_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,'open',?,?)""",
            (me["id"], title, category, meta["emoji"], str(data.get("description") or "")[:400],
             fmt(start_at), area, city, lat, lon, venue_name, venue_id, spots,
             1 if data.get("approval") else 0, json.dumps(vibe, ensure_ascii=False), stamp, stamp),
        )
        plan_id = cur.lastrowid
        conn.execute(
            """INSERT INTO plan_members(plan_id, user_id, role, status, joined_at)
               VALUES (?,?,'host','joined',?)""",
            (plan_id, me["id"], stamp),
        )
        row = conn.execute("SELECT * FROM plans WHERE id = ?", (plan_id,)).fetchone()
        plan = serialize_plan(conn, row, me, user_index(conn), plan_thread_map(conn))
        HUB.publish([me["id"]])
        return {"plan": plan}


def api_plan_join(data, me, plan_id):
    with connect() as conn:
        plan = conn.execute("SELECT * FROM plans WHERE id = ?", (plan_id,)).fetchone()
        if not plan:
            raise ApiError("Ese plan ya no existe", 404)
        if plan["host_id"] == me["id"]:
            raise ApiError("Este plan es tuyo")
        if plan["status"] != "open":
            raise ApiError("El plan ya está completo o cancelado")
        existing = conn.execute(
            "SELECT * FROM plan_members WHERE plan_id = ? AND user_id = ?", (plan_id, me["id"])
        ).fetchone()
        if existing and existing["status"] == "joined":
            raise ApiError("Ya estás dentro de este plan")
        if existing and existing["status"] == "pending":
            raise ApiError("Tu solicitud ya está enviada")
        stamp = now_str()
        if existing:
            conn.execute(
                "UPDATE plan_members SET status = ?, joined_at = ? WHERE id = ?",
                ("pending" if plan["approval"] else "joined", stamp, existing["id"]),
            )
        else:
            conn.execute(
                """INSERT INTO plan_members(plan_id, user_id, role, status, joined_at)
                   VALUES (?,?,'member',?,?)""",
                (plan_id, me["id"], "pending" if plan["approval"] else "joined", stamp),
            )
        if plan["approval"]:
            host = conn.execute("SELECT * FROM users WHERE id = ?", (plan["host_id"],)).fetchone()
            add_notification(
                conn, plan["host_id"], "request",
                f"{me['name']} quiere apuntarse a «{plan['title']}»",
                plan_id=plan_id,
            )
            HUB.publish([plan["host_id"]])
            return {"pending": True}
        joined_count = conn.execute(
            "SELECT COUNT(*) AS n FROM plan_members WHERE plan_id = ? AND status = 'joined'", (plan_id,)
        ).fetchone()["n"]
        if joined_count >= plan["spots"] + 1:
            conn.execute("UPDATE plans SET status = 'full', updated_at = ? WHERE id = ?", (stamp, plan_id))
        thread_id = ensure_plan_thread(conn, plan_id)
        if thread_id:
            add_message(conn, thread_id, None, f"{me['name']} se ha apuntado al plan 👋", "system")
        members = [r["user_id"] for r in conn.execute(
            "SELECT user_id FROM plan_members WHERE plan_id = ? AND status = 'joined'", (plan_id,)
        ).fetchall()]
        add_notification(conn, plan["host_id"], "join", f"{me['name']} se ha apuntado a «{plan['title']}»", plan_id=plan_id)
        HUB.publish(members + [plan["host_id"]])
        return {"joined": True, "thread_id": thread_id, "full": joined_count >= plan["spots"] + 1}


def api_plan_leave(data, me, plan_id):
    with connect() as conn:
        plan = conn.execute("SELECT * FROM plans WHERE id = ?", (plan_id,)).fetchone()
        if not plan:
            raise ApiError("Ese plan ya no existe", 404)
        if plan["host_id"] == me["id"]:
            raise ApiError("Si eres el anfitrión, cancela el plan")
        member = conn.execute(
            "SELECT * FROM plan_members WHERE plan_id = ? AND user_id = ?", (plan_id, me["id"])
        ).fetchone()
        if not member or member["status"] == "declined":
            raise ApiError("No estabas apuntado a este plan")
        conn.execute("DELETE FROM plan_members WHERE id = ?", (member["id"],))
        if plan["status"] == "full":
            conn.execute("UPDATE plans SET status = 'open', updated_at = ? WHERE id = ?", (now_str(), plan_id))
        thread_id = ensure_plan_thread(conn, plan_id)
        if thread_id:
            add_message(conn, thread_id, None, f"{me['name']} ha salido del plan", "system")
        HUB.publish([plan["host_id"]])
        return {"left": True}


def api_plan_resolve(data, me, plan_id, user_id):
    action = str(data.get("action") or "")
    if action not in ("accept", "reject"):
        raise ApiError("Acción no válida")
    with connect() as conn:
        plan = conn.execute("SELECT * FROM plans WHERE id = ?", (plan_id,)).fetchone()
        if not plan:
            raise ApiError("Ese plan ya no existe", 404)
        if plan["host_id"] != me["id"]:
            raise ApiError("Solo el anfitrión puede decidir", 403)
        member = conn.execute(
            "SELECT * FROM plan_members WHERE plan_id = ? AND user_id = ? AND status = 'pending'",
            (plan_id, user_id),
        ).fetchone()
        if not member:
            raise ApiError("Esa solicitud ya no está pendiente")
        target = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        stamp = now_str()
        if action == "reject":
            conn.execute("UPDATE plan_members SET status = 'declined' WHERE id = ?", (member["id"],))
            add_notification(conn, user_id, "reject",
                             f"{me['name']} no ha podido aceptarte en «{plan['title']}»", plan_id=plan_id)
            HUB.publish([user_id, me["id"]])
            return {"ok": True}
        conn.execute("UPDATE plan_members SET status = 'joined', joined_at = ? WHERE id = ?", (stamp, member["id"]))
        joined_count = conn.execute(
            "SELECT COUNT(*) AS n FROM plan_members WHERE plan_id = ? AND status = 'joined'", (plan_id,)
        ).fetchone()["n"]
        if joined_count >= plan["spots"] + 1:
            conn.execute("UPDATE plans SET status = 'full', updated_at = ? WHERE id = ?", (stamp, plan_id))
        thread_id = ensure_plan_thread(conn, plan_id)
        if thread_id:
            add_message(conn, thread_id, None, f"{target['name']} se ha unido al plan. ¡Bienvenido! 👋", "system")
        add_notification(conn, user_id, "accept",
                         f"¡Estás dentro de «{plan['title']}»! Ya puedes hablar con el grupo", plan_id=plan_id, thread_id=thread_id)
        HUB.publish([user_id, me["id"]])
        return {"ok": True, "thread_id": thread_id}


def api_plan_cancel(data, me, plan_id):
    with connect() as conn:
        plan = conn.execute("SELECT * FROM plans WHERE id = ?", (plan_id,)).fetchone()
        if not plan:
            raise ApiError("Ese plan ya no existe", 404)
        if plan["host_id"] != me["id"]:
            raise ApiError("Solo el anfitrión puede cancelar el plan", 403)
        conn.execute("UPDATE plans SET status = 'cancelled', updated_at = ? WHERE id = ?", (now_str(), plan_id))
        members = [r["user_id"] for r in conn.execute(
            "SELECT user_id FROM plan_members WHERE plan_id = ? AND status = 'joined'", (plan_id,)
        ).fetchall()]
        thread = conn.execute("SELECT id FROM threads WHERE plan_id = ? AND kind = 'plan'", (plan_id,)).fetchone()
        if thread:
            add_message(conn, thread["id"], None, "El anfitrión ha cancelado el plan 😔", "system")
        for uid in members:
            if uid != me["id"]:
                add_notification(conn, uid, "cancel", f"«{plan['title']}» se ha cancelado", plan_id=plan_id)
        HUB.publish(members)
        return {"ok": True}


# ------------------------------------------------------------------- swipes
def api_swipe(data, me):
    target_id = as_int(data.get("user_id"))
    action = str(data.get("action") or "like")
    if action not in ("like", "pass", "super"):
        raise ApiError("Acción no válida")
    if not target_id or target_id == me["id"]:
        raise ApiError("Perfil no válido")
    with connect() as conn:
        target = conn.execute("SELECT * FROM users WHERE id = ?", (target_id,)).fetchone()
        if not target:
            raise ApiError("Ese perfil ya no existe", 404)
        previous = conn.execute(
            "SELECT action FROM swipes WHERE from_user = ? AND to_user = ?", (me["id"], target_id)
        ).fetchone()
        already_liked = bool(previous and previous["action"] in ("like", "super"))
        if action in ("like", "super") and not already_liked:
            balance = spend_coins(
                conn, me["id"], LIKE_COST,
                "superlike" if action == "super" else "like",
                f"{'Superlike' if action == 'super' else 'Like'} a {target['name']}",
            )
            if balance is None:
                current = coin_balance(conn, me["id"])
                raise ApiError(
                    f"Te faltan monedas: tienes {current} y cada like cuesta {LIKE_COST}. "
                    "Reclama tus monedas diarias o vuelve mañana.",
                    402,
                )
        else:
            balance = coin_balance(conn, me["id"])
        conn.execute(
            """INSERT INTO swipes(from_user, to_user, action, created_at) VALUES (?,?,?,?)
               ON CONFLICT(from_user, to_user) DO UPDATE SET action = excluded.action, created_at = excluded.created_at""",
            (me["id"], target_id, action, now_str()),
        )
        match = None
        if action in ("like", "super"):
            back = conn.execute(
                "SELECT action FROM swipes WHERE from_user = ? AND to_user = ? AND action IN ('like','super')",
                (target_id, me["id"]),
            ).fetchone()
            if back:
                pair = tuple(sorted((me["id"], target_id)))
                previously = conn.execute(
                    "SELECT thread_id FROM matches WHERE user_a = ? AND user_b = ?", pair
                ).fetchone()
                thread_id = create_match(conn, me["id"], target_id)
                if not previously:
                    add_notification(conn, target_id, "match", f"¡Nuevo match con {me['name']}! Ya podéis hablar", thread_id=thread_id)
                    add_notification(conn, me["id"], "match", f"¡Nuevo match con {target['name']}! Ya podéis hablar", thread_id=thread_id)
                    HUB.publish([me["id"], target_id])
                thread = conn.execute("SELECT * FROM threads WHERE id = ?", (thread_id,)).fetchone()
                plans = {row["id"]: row for row in conn.execute("SELECT * FROM plans").fetchall()}
                users = user_index(conn)
                match = {
                    "thread_id": thread_id,
                    "user": public_user(target, me),
                    "thread": serialize_thread(conn, thread, me, users, plans),
                    "is_new": not previously,
                }
        HUB.publish([me["id"]])
        return {"match": match, "coins": balance, "cost": 0 if already_liked or action == "pass" else LIKE_COST}

def api_swipe_reset(data, me):
    with connect() as conn:
        matches = conn.execute(
            "SELECT user_a, user_b FROM matches WHERE user_a = ? OR user_b = ?", (me["id"], me["id"])
        ).fetchall()
        keep = set()
        for row in matches:
            keep.add(row["user_a"])
            keep.add(row["user_b"])
        keep.discard(me["id"])
        if keep:
            placeholders = ",".join("?" * len(keep))
            conn.execute(
                f"DELETE FROM swipes WHERE from_user = ? AND to_user NOT IN ({placeholders})",
                [me["id"], *keep],
            )
        else:
            conn.execute("DELETE FROM swipes WHERE from_user = ?", (me["id"],))
        HUB.publish([me["id"]])
        return {"ok": True}


# ------------------------------------------------------------------- chats
def api_thread(data, me, thread_id):
    with connect() as conn:
        thread = conn.execute("SELECT * FROM threads WHERE id = ?", (thread_id,)).fetchone()
        if not thread:
            raise ApiError("Ese chat no existe", 404)
        member = conn.execute(
            "SELECT 1 FROM thread_members WHERE thread_id = ? AND user_id = ?", (thread_id, me["id"])
        ).fetchone()
        if not member:
            raise ApiError("No tienes acceso a este chat", 403)
        rows = conn.execute(
            """SELECT m.*, u.name AS author_name, u.avatar, u.variant
               FROM messages m LEFT JOIN users u ON u.id = m.user_id
               WHERE m.thread_id = ? ORDER BY m.id ASC LIMIT 300""",
            (thread_id,),
        ).fetchall()
        messages = [{
            "id": r["id"],
            "body": r["body"],
            "kind": r["kind"],
            "created_at": r["created_at"],
            "user_id": r["user_id"],
            "author": r["author_name"] or "Ronda",
            "avatar": r["avatar"] or "✨",
            "variant": (r["variant"] or 0) % 8,
        } for r in rows]
        mark_read(conn, me["id"], thread_id)
        plans = {row["id"]: row for row in conn.execute("SELECT * FROM plans").fetchall()}
        users = user_index(conn)
        data = serialize_thread(conn, thread, me, users, plans)
        data["unread"] = 0
        data["messages"] = messages
        if thread["plan_id"] and thread["plan_id"] in plans:
            plan_row = conn.execute("SELECT * FROM plans WHERE id = ?", (thread["plan_id"],)).fetchone()
            data["plan_full"] = serialize_plan(conn, plan_row, me, users, plan_thread_map(conn))
        else:
            data["plan_full"] = None
        return data


def api_send_message(data, me, thread_id):
    body = str(require(data, "body", "mensaje")).strip()
    if len(body) > 1000:
        raise ApiError("El mensaje es demasiado largo")
    with connect() as conn:
        thread = conn.execute("SELECT * FROM threads WHERE id = ?", (thread_id,)).fetchone()
        if not thread:
            raise ApiError("Ese chat no existe", 404)
        members = [r["user_id"] for r in conn.execute(
            "SELECT user_id FROM thread_members WHERE thread_id = ?", (thread_id,)
        ).fetchall()]
        if me["id"] not in members:
            raise ApiError("No tienes acceso a este chat", 403)
        message_id = add_message(conn, thread_id, me["id"], body)
        mark_read(conn, me["id"], thread_id)
        preview = body if len(body) <= 55 else body[:52] + "…"
        for uid in members:
            if uid != me["id"]:
                add_notification(conn, uid, "message", f"{me['name']}: «{preview}»", thread_id=thread_id)
        HUB.publish(members)
        return {"id": message_id, "at": now_str()}


def api_thread_read(data, me, thread_id):
    with connect() as conn:
        member = conn.execute(
            "SELECT 1 FROM thread_members WHERE thread_id = ? AND user_id = ?", (thread_id, me["id"])
        ).fetchone()
        if not member:
            raise ApiError("No tienes acceso a este chat", 403)
        mark_read(conn, me["id"], thread_id)
        return {"ok": True}


# ------------------------------------------------------------------- export
def api_me_export(data=None, me=None):
    """Download everything that belongs to the signed-in user (no passwords)."""
    with connect() as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (me["id"],)).fetchone()
        users = user_index(conn)
        threads_map = plan_thread_map(conn)
        all_plans = {item["id"]: item for item in conn.execute("SELECT * FROM plans").fetchall()}

        plan_rows = conn.execute(
            """SELECT DISTINCT p.* FROM plans p
               LEFT JOIN plan_members pm ON pm.plan_id = p.id AND pm.user_id = ?
               WHERE p.host_id = ? OR pm.user_id IS NOT NULL
               ORDER BY p.start_at DESC""",
            (me["id"], me["id"]),
        ).fetchall()
        plans = [serialize_plan(conn, plan, me, users, threads_map) for plan in plan_rows]

        thread_rows = conn.execute(
            """SELECT t.* FROM threads t JOIN thread_members tm ON tm.thread_id = t.id
               WHERE tm.user_id = ? ORDER BY t.last_at DESC""",
            (me["id"],),
        ).fetchall()
        threads = []
        for thread in thread_rows:
            summary = serialize_thread(conn, thread, me, users, all_plans)
            messages = []
            for message in conn.execute(
                """SELECT m.*, u.name AS author_name, u.avatar
                   FROM messages m LEFT JOIN users u ON u.id = m.user_id
                   WHERE m.thread_id = ? ORDER BY m.id""",
                (thread["id"],),
            ).fetchall():
                messages.append({
                    "id": message["id"],
                    "author": message["author_name"] or "Ronda",
                    "body": message["body"],
                    "kind": message["kind"],
                    "created_at": message["created_at"],
                })
            summary["messages"] = messages
            threads.append(summary)

        notifications = [dict(item) for item in conn.execute(
            "SELECT * FROM notifications WHERE user_id = ? ORDER BY id DESC", (me["id"],)
        ).fetchall()]
        wallet = wallet_payload(conn, row)
        swipes = [dict(item) for item in conn.execute(
            "SELECT to_user, action, created_at FROM swipes WHERE from_user = ? ORDER BY id", (me["id"],)
        ).fetchall()]

        profile = public_user(row)
        profile.update({
            "created_at": row["created_at"],
            "last_seen": row["last_seen"],
            "preferences": {
                "max_distance": row["max_distance"],
                "age_min": row["age_min"],
                "age_max": row["age_max"],
            },
            "location": {
                "city": row["city"],
                "zone": row["zone"],
                "exact": bool(row["location_exact"]),
                "lat": row["lat"],
                "lon": row["lon"],
            },
            "coins": row["coins"],
        })
        return {
            "app": "Ronda",
            "version": "1.0",
            "exported_at": now_str(),
            "user": profile,
            "plans": plans,
            "threads": threads,
            "swipes": swipes,
            "wallet": wallet,
            "notifications": notifications,
        }


# ------------------------------------------------------------------- profile
def api_profile(data, me):
    fields = {}
    exact_value = data.get("location_exact")
    if "name" in data:
        name = str(data.get("name") or "").strip()[:40]
        if not name:
            raise ApiError("El nombre no puede estar vacío")
        fields["name"] = name
    if "age" in data:
        age = as_int(data.get("age"), me["age"])
        if not 18 <= age <= 99:
            raise ApiError("La edad debe estar entre 18 y 99")
        fields["age"] = age
    if "city" in data:
        city = str(data.get("city") or "")
        if city not in CITIES:
            raise ApiError("Esa ciudad no está disponible")
        fields["city"] = city
        if city != (me["city"] or "Madrid"):
            lat, lon = city_coords(city)
            fields["lat"] = lat
            fields["lon"] = lon
            fields["location_exact"] = 0
            if "zone" not in data and "area" not in data:
                fields["zone"] = ""
    if "zone" in data or "area" in data:
        fields["zone"] = str(data.get("zone") or data.get("area") or "")[:60]
    if "lat" in data and "lon" in data:
        try:
            lat = float(data.get("lat"))
            lon = float(data.get("lon"))
        except (TypeError, ValueError):
            raise ApiError("Coordenadas no válidas")
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            raise ApiError("Coordenadas no válidas")
        fields["lat"] = lat
        fields["lon"] = lon
        fields["location_exact"] = 0 if exact_value is False else 1
    elif exact_value is False:
        city = str(fields.get("city") or me["city"] or "Madrid")
        lat, lon = city_coords(city)
        fields["lat"] = lat
        fields["lon"] = lon
        fields["location_exact"] = 0
    elif exact_value is True and not me["location_exact"]:
        raise ApiError("Falta la ubicación exacta")
    if "bio" in data:
        fields["bio"] = str(data.get("bio") or "")[:200]
    if "avatar" in data:
        fields["avatar"] = str(data.get("avatar") or "🦋")[:8]
    if "variant" in data:
        fields["variant"] = as_int(data.get("variant"), 0) % 8
    if "interests" in data:
        fields["interests"] = json.dumps(clean_interests(data.get("interests")), ensure_ascii=False)
    if "looking_for" in data:
        fields["looking_for"] = str(data.get("looking_for") or "")[:120]
    if "status_note" in data:
        fields["status_note"] = str(data.get("status_note") or "")[:80]
    if "max_distance" in data:
        value = as_int(data.get("max_distance"), 20)
        fields["max_distance"] = max(1, min(40, value))
    if "age_min" in data:
        fields["age_min"] = max(18, min(60, as_int(data.get("age_min"), 18)))
    if "age_max" in data:
        fields["age_max"] = max(18, min(80, as_int(data.get("age_max"), 45)))
    if "age_min" in fields and "age_max" in fields and fields["age_min"] > fields["age_max"]:
        fields["age_min"], fields["age_max"] = fields["age_max"], fields["age_min"]
    if not fields:
        raise ApiError("No hay cambios que guardar")
    assignments = ", ".join(f"{key} = ?" for key in fields)
    with connect() as conn:
        conn.execute(f"UPDATE users SET {assignments} WHERE id = ?", [*fields.values(), me["id"]])
        row = conn.execute("SELECT * FROM users WHERE id = ?", (me["id"],)).fetchone()
        HUB.publish([me["id"]])
        return {"user": public_user(row)}


# ------------------------------------------------------------------- notifs
def api_notifications_read(data, me):
    with connect() as conn:
        conn.execute("UPDATE notifications SET read = 1 WHERE user_id = ?", (me["id"],))
        HUB.publish([me["id"]])
        return {"ok": True}


# ------------------------------------------------------------------- routes
ROUTES = [
    ("POST", r"/api/auth/register", api_register),
    ("POST", r"/api/auth/login", api_login),
    ("POST", r"/api/auth/logout", api_logout),
    ("GET", r"/api/demo-accounts", api_demo_accounts),
    ("GET", r"/api/catalog", api_catalog),
    ("GET", r"/api/state", api_state),
    ("GET", r"/api/wallet", api_wallet),
    ("POST", r"/api/economy/daily", api_daily),
    ("POST", r"/api/plans", api_plan_create),
    ("POST", r"/api/plans/(\d+)/join", api_plan_join),
    ("POST", r"/api/plans/(\d+)/leave", api_plan_leave),
    ("POST", r"/api/plans/(\d+)/cancel", api_plan_cancel),
    ("POST", r"/api/plans/(\d+)/members/(\d+)/resolve", api_plan_resolve),
    ("POST", r"/api/swipes", api_swipe),
    ("POST", r"/api/swipes/reset", api_swipe_reset),
    ("GET", r"/api/threads/(\d+)", api_thread),
    ("POST", r"/api/threads/(\d+)/messages", api_send_message),
    ("POST", r"/api/threads/(\d+)/read", api_thread_read),
    ("PATCH", r"/api/profile", api_profile),
    ("GET", r"/api/me/export", api_me_export),
    ("POST", r"/api/notifications/read", api_notifications_read),
]

PUBLIC_ROUTES = {api_register, api_login, api_demo_accounts, api_catalog}


# ------------------------------------------------------------------- server
class Handler(BaseHTTPRequestHandler):
    server_version = "Ronda/1.0"
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt_str, *args):
        if os.environ.get("RONDA_LOG", "0" if FROZEN else "1") == "1":
            sys.stderr.write("%s - %s\n" % (self.address_string(), fmt_str % args))

    def _send(self, status: int, payload: bytes, ctype: str, extra: dict | None = None):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("X-Content-Type-Options", "nosniff")
        for key, value in (extra or {}).items():
            self.send_header(key, value)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(payload)

    def _json(self, status: int, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self._send(status, body, "application/json; charset=utf-8", {"Cache-Control": "no-store"})

    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length") or 0)
        if not length:
            return {}
        raw = self.rfile.read(length)
        try:
            data = json.loads(raw.decode("utf-8") or "{}")
            return data if isinstance(data, dict) else {}
        except (ValueError, UnicodeDecodeError):
            raise ApiError("Cuerpo JSON no válido")

    def _token(self):
        header = self.headers.get("Authorization") or ""
        if header.lower().startswith("bearer "):
            return header[7:].strip()
        return parse_qs(urlparse(self.path).query).get("token", [None])[0]

    def _me(self, conn):
        me = user_by_token(conn, self._token())
        if not me:
            raise ApiError("Sesión caducada, vuelve a entrar", 401)
        return me

    def do_OPTIONS(self):
        self._send(204, b"", "text/plain", {
            "Access-Control-Allow-Methods": "GET,POST,PATCH,PUT,DELETE,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
        })

    def do_GET(self):
        self.dispatch("GET")

    def do_POST(self):
        self.dispatch("POST")

    def do_PATCH(self):
        self.dispatch("PATCH")

    def do_PUT(self):
        self.dispatch("PUT")

    def do_DELETE(self):
        self.dispatch("DELETE")

    def do_HEAD(self):
        self.dispatch("GET")

    def dispatch(self, method: str):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        if path == "/api/health":
            return self._json(200, {"ok": True, "time": now_str()})

        if path == "/api/events":
            return self.stream_events()

        if path.startswith("/api/"):
            try:
                body = self._read_body() if method in ("POST", "PATCH", "PUT", "DELETE") else {}
                for route_method, pattern, fn in ROUTES:
                    if route_method != method:
                        continue
                    match = re.fullmatch(pattern, path)
                    if not match:
                        continue
                    args = [int(g) for g in match.groups()]
                    if fn in PUBLIC_ROUTES:
                        return self._json(200, fn(body))
                    with connect() as conn:
                        me = self._me(conn)
                    if fn is api_logout:
                        return self._json(200, fn(body, me))
                    with connect() as conn:
                        me = self._me(conn)
                        result = fn(body, me, *args) if args else fn(body, me)
                    return self._json(200, result or {"ok": True})
                raise ApiError("Ruta no encontrada", 404)
            except ApiError as exc:
                return self._json(exc.status, {"error": exc.message})
            except Exception as exc:
                import traceback
                traceback.print_exc()
                return self._json(500, {"error": f"Error interno: {exc}"})

        return self.serve_static(path)

    # -- SSE
    def stream_events(self):
        token = self._token()
        with connect() as conn:
            me = user_by_token(conn, token)
        if not me:
            return self._json(401, {"error": "Sesión caducada"})
        user_id = me["id"]
        q = HUB.subscribe(user_id)
        try:
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
            self.send_header("Cache-Control", "no-cache, no-transform")
            self.send_header("Connection", "keep-alive")
            self.send_header("X-Accel-Buffering", "no")
            self.end_headers()
            self.wfile.write(b"retry: 3000\n\n")
            self.wfile.flush()
            while True:
                try:
                    event = q.get(timeout=20)
                    data = json.dumps(event).encode()
                    self.wfile.write(b"event: update\ndata: " + data + b"\n\n")
                except queue.Empty:
                    self.wfile.write(b": ping\n\n")
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass
        finally:
            HUB.unsubscribe(user_id, q)

    # -- static files
    def serve_static(self, path: str):
        if path in ("/", ""):
            path = "/index.html"
        safe = os.path.normpath(os.path.join(STATIC_DIR, path.lstrip("/\\")))
        if not safe.startswith(STATIC_DIR) or not os.path.isfile(safe):
            return self._json(404, {"error": "No encontrado"})
        ctype = mimetypes.guess_type(safe)[0] or "application/octet-stream"
        if ctype.startswith("text/") or ctype in ("application/javascript", "application/manifest+json"):
            ctype += "; charset=utf-8"
        with open(safe, "rb") as fh:
            payload = fh.read()
        self._send(200, payload, ctype, {"Cache-Control": "no-cache", "Service-Worker-Allowed": "/"})


class RondaServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = False

    def handle_error(self, request, client_address):
        exc = sys.exc_info()[1]
        if isinstance(exc, (ConnectionResetError, ConnectionAbortedError, BrokenPipeError, TimeoutError)):
            return
        super().handle_error(request, client_address)


def bind_server():
    """Bind the preferred port, falling back to the next free ones."""
    last_error = None
    for candidate in range(PORT, PORT + 20):
        try:
            return RondaServer((HOST, candidate), Handler), candidate
        except OSError as exc:
            last_error = exc
    raise SystemExit(f"No se pudo abrir ningún puerto entre {PORT} y {PORT + 19}: {last_error}")


def local_ip() -> str:
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        return ip
    except OSError:
        return "127.0.0.1"


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    init_db()
    seed_demo()
    server, port = bind_server()

    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW("Ronda · Que nunca falte gente")  # type: ignore[attr-defined]
    except Exception:
        pass

    share_ip = local_ip()
    print("")
    print("  ╭──────────────────────────────────────────────╮")
    print("  │  Ronda · Que nunca falte gente               │")
    print("  ╰──────────────────────────────────────────────╯")
    print(f"  Este equipo:  http://localhost:{port}")
    if HOST in ("0.0.0.0", "::"):
        print(f"  Comparte:     http://{share_ip}:{port}")
    print(f"  Datos:        {DB_PATH}")
    print("")
    print("  Demo:         lucia / demo1234")
    print("  Deja esta ventana abierta para que los demás entren.")
    print("  Misma wifi · pulsa Ctrl+C para parar.")
    print("")

    if FROZEN and os.environ.get("RONDA_OPEN", "1") != "0":
        def open_browser():
            try:
                import webbrowser
                webbrowser.open(f"http://localhost:{port}")
            except Exception:
                pass
        threading.Timer(1.3, open_browser).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Ronda detenido")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
