/* Ronda — single-page app (vanilla ES modules, no build step) */

/* ------------------------------------------------------------- constants */
const FALLBACK_CATALOG = {
  cities: [
    { name: "Madrid", province: "Madrid", lat: 40.4168, lon: -3.7038 },
    { name: "Barcelona", province: "Barcelona", lat: 41.3874, lon: 2.1686 },
    { name: "Valencia", province: "Valencia", lat: 39.4699, lon: -0.3763 },
    { name: "Sevilla", province: "Sevilla", lat: 37.3891, lon: -5.9845 },
    { name: "Zaragoza", province: "Zaragoza", lat: 41.6488, lon: -0.8891 },
    { name: "Málaga", province: "Málaga", lat: 36.7213, lon: -4.4214 },
    { name: "Murcia", province: "Murcia", lat: 37.9922, lon: -1.1307 },
    { name: "Palma", province: "Illes Balears", lat: 39.5696, lon: 2.6502 },
    { name: "Las Palmas de Gran Canaria", province: "Las Palmas", lat: 28.1235, lon: -15.4363 },
    { name: "Bilbao", province: "Bizkaia", lat: 43.2630, lon: -2.9350 },
    { name: "Alicante", province: "Alicante", lat: 38.3452, lon: -0.4815 },
    { name: "Córdoba", province: "Córdoba", lat: 37.8882, lon: -4.7794 },
    { name: "Valladolid", province: "Valladolid", lat: 41.6523, lon: -4.7245 },
    { name: "Vigo", province: "Pontevedra", lat: 42.2406, lon: -8.7207 },
    { name: "Gijón", province: "Asturias", lat: 43.5322, lon: -5.6611 },
    { name: "A Coruña", province: "A Coruña", lat: 43.3623, lon: -8.4115 },
    { name: "Vitoria-Gasteiz", province: "Álava", lat: 42.8467, lon: -2.6716 },
    { name: "Granada", province: "Granada", lat: 37.1773, lon: -3.5986 },
    { name: "Pamplona", province: "Navarra", lat: 42.8125, lon: -1.6458 },
    { name: "San Sebastián", province: "Gipuzkoa", lat: 43.3183, lon: -1.9812 },
    { name: "Santander", province: "Cantabria", lat: 43.4623, lon: -3.8100 },
    { name: "Salamanca", province: "Salamanca", lat: 40.9701, lon: -5.6635 },
    { name: "Toledo", province: "Toledo", lat: 39.8628, lon: -4.0273 },
    { name: "Cádiz", province: "Cádiz", lat: 36.5271, lon: -6.2886 },
    { name: "Ibiza", province: "Illes Balears", lat: 38.9067, lon: 1.4206 },
  ],
  venues: [],
  interests: ["Conciertos", "Música indie", "Terrazas", "Fotografía", "Brunch", "Cine", "Baile", "Gastronomía", "Viajes", "Bici", "Café", "Senderismo", "Running", "Arte", "Museos", "Cañas", "Tapas", "Fútbol", "Fiesta", "Cócteles", "Yoga", "Cerámica", "Pádel", "Gaming", "Rock", "Series", "Vinilos", "Moda", "Lectura", "Jazz", "Karaoke", "Ramen", "Skate", "Festivales", "Electrónica", "Teatro", "Playa", "Piscina", "Mercadillos", "Idiomas"],
  avatars: ["🦋", "🎸", "🍒", "🚲", "🌸", "🍻", "🪩", "🏓", "🏃", "🎨", "🍷", "🛹", "🎧", "🍜"],
  categories: [
    { key: "cañas", label: "Cañas", emoji: "🍻" },
    { key: "concierto", label: "Concierto", emoji: "🎸" },
    { key: "comida", label: "Comida", emoji: "🍜" },
    { key: "cine", label: "Cine", emoji: "🎬" },
    { key: "deporte", label: "Deporte", emoji: "⚡" },
    { key: "baile", label: "Baile", emoji: "💃" },
    { key: "cultura", label: "Cultura", emoji: "🎨" },
    { key: "aire", label: "Aire libre", emoji: "🌿" },
    { key: "planes", label: "Otros", emoji: "✨" },
  ],
};

const CAT_COLORS = {
  cañas: "#ffc24b", concierto: "#ff6fa5", comida: "#ff8a5b", cine: "#9b7bff",
  deporte: "#43e0d0", baile: "#ff4d6d", cultura: "#6db4ff", aire: "#c6ff4a",
  planes: "#ffc24b",
};

const THEMES = [
  { key: "noche", label: "Noche", bg: "#0d0913", dot: "#ff4d6d", dot2: "#c6ff4a" },
  { key: "neon", label: "Neón", bg: "#05080a", dot: "#c6ff4a", dot2: "#43e0d0" },
  { key: "sunset", label: "Sunset", bg: "#1b0c14", dot: "#ff7a45", dot2: "#ffd166" },
  { key: "claro", label: "Claro", bg: "#f6f0e7", dot: "#ff4d6d", dot2: "#b9e93f" },
];

const DAYS = ["dom", "lun", "mar", "mié", "jue", "vie", "sáb"];
const MONTHS = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"];
const QUICK_MATCH = ["¿Quedamos este finde?", "¿A qué hora te va bien?", "Te paso el sitio 📍"];
const QUICK_PLAN = ["Confirmo, allí estaré", "¿Dónde quedamos?", "¡Nos vemos! 🙌"];
const WELCOME_COINS = 100;
const DAILY_COINS = 10;
const LIKE_COST = 10;

const ICONS = {
  pin: '<path d="M12 21s7-6.1 7-11a7 7 0 1 0-14 0c0 4.9 7 11 7 11Z"/><circle cx="12" cy="10" r="2.6"/>',
  clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7.5V12l3 2"/>',
  calendar: '<rect x="3.5" y="5" width="17" height="15.5" rx="3"/><path d="M8 3v4M16 3v4M3.5 10h17"/>',
  users: '<circle cx="9" cy="8.5" r="3.2"/><path d="M3.4 19c.5-3 2.7-4.7 5.6-4.7s5.1 1.7 5.6 4.7"/><path d="M15.5 5.7a3 3 0 0 1 0 5.7M17.5 14.8c2 .3 3.2 1.8 3.5 4.2"/>',
  check: '<path d="m5 12.5 4.2 4L19 6.8"/>',
  close: '<path d="M6 6l12 12M18 6 6 18"/>',
  heart: '<path d="M12 20s-7.2-4.5-7.2-9.6A4.2 4.2 0 0 1 12 7.5a4.2 4.2 0 0 1 7.2 2.9C19.2 15.5 12 20 12 20Z"/>',
  star: '<path d="M12 3.6l2.5 5 5.5.8-4 3.9.9 5.5-4.9-2.6-4.9 2.6.9-5.5-4-3.9 5.5-.8Z"/>',
  send: '<path d="M4 11.5 20 4l-7.5 16-2-6.5Z"/><path d="m10.5 13.5 4.2-4.2"/>',
  back: '<path d="M15 5l-7 7 7 7"/>',
  filter: '<path d="M4 7h16M7 12h10M10 17h4"/>',
  settings: '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.9l.1.1-2.8 2.8-.1-.1a1.7 1.7 0 0 0-1.9-.3 1.7 1.7 0 0 0-1 1.5V21h-4v-.1a1.7 1.7 0 0 0-1-1.5 1.7 1.7 0 0 0-1.9.3l-.1.1L4.2 17l.1-.1a1.7 1.7 0 0 0 .3-1.9A1.7 1.7 0 0 0 3 14H3v-4h.1a1.7 1.7 0 0 0 1.5-1 1.7 1.7 0 0 0-.3-1.9L4.2 7 7 4.2l.1.1a1.7 1.7 0 0 0 1.9.3 1.7 1.7 0 0 0 1-1.5V3h4v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.9-.3l.1-.1L19.8 7l-.1.1a1.7 1.7 0 0 0-.3 1.9 1.7 1.7 0 0 0 1.5 1H21v4h-.1a1.7 1.7 0 0 0-1.5 1Z"/>',
  edit: '<path d="M4 20h4.2L20 8.2 15.8 4 4 15.8Z"/><path d="m14.2 5.6 4.2 4.2"/>',
  logout: '<path d="M9 4H5.5A1.5 1.5 0 0 0 4 5.5v13A1.5 1.5 0 0 0 5.5 20H9"/><path d="M14 8l4 4-4 4M9 12h9"/>',
  sparkles: '<path d="M12 3l1.7 4.3L18 9l-4.3 1.7L12 15l-1.7-4.3L6 9l4.3-1.7Z"/><path d="M18.5 15.5l.8 2 2 .8-2 .8-.8 2-.8-2-2-.8 2-.8Z"/>',
  refresh: '<path d="M20 11a8 8 0 1 0-2.3 5.7"/><path d="M20 5v6h-6"/>',
  shield: '<path d="M12 3.5 5 6v5.5c0 4.2 2.8 7.4 7 9 4.2-1.6 7-4.8 7-9V6Z"/><path d="m9 12 2 2 4-4"/>',
  bell: '<path d="M18 8a6 6 0 1 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9"/><path d="M10.2 21a2 2 0 0 0 3.6 0"/>',
  chevron: '<path d="m9 6 6 6-6 6"/>',
  plus: '<path d="M12 5v14M5 12h14"/>',
  minus: '<path d="M5 12h14"/>',
  map: '<path d="M9 4 3.5 6v14L9 18l6 2 5.5-2V4L15 6Z"/><path d="M9 4v14M15 6v14"/>',
  message: '<path d="M20 11.4a7.7 7.7 0 0 1-8.2 7.6 9 9 0 0 1-2.6-.4L4.5 20l1.2-3.7A7.3 7.3 0 0 1 4 11.4a7.7 7.7 0 0 1 8-7.4 7.7 7.7 0 0 1 8 7.4Z"/>',
  flame: '<path d="M12 21c4 0 6.5-2.5 6.5-6 0-2.7-1.6-4.7-3.2-6.2-.7-.7-1.2-1.5-1.3-2.6-2 1-3 2.6-3.2 4.4-1.2-.9-1.9-2-2-3.4C7 9.4 5.5 12 5.5 15c0 3.5 2.5 6 6.5 6Z"/>',
  link: '<path d="M10 14a4 4 0 0 0 5.7 0l2.8-2.8a4 4 0 0 0-5.7-5.7l-1.3 1.3"/><path d="M14 10a4 4 0 0 0-5.7 0l-2.8 2.8a4 4 0 0 0 5.7 5.7l1.3-1.3"/>',
  eye: '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12Z"/><circle cx="12" cy="12" r="3"/>',
  lock: '<rect x="4.5" y="10" width="15" height="10.5" rx="3"/><path d="M8 10V7.5a4 4 0 0 1 8 0V10"/>',
  dotgrid: '<circle cx="6" cy="6" r="1.3" fill="currentColor" stroke="none"/><circle cx="12" cy="6" r="1.3" fill="currentColor" stroke="none"/><circle cx="18" cy="6" r="1.3" fill="currentColor" stroke="none"/><circle cx="6" cy="12" r="1.3" fill="currentColor" stroke="none"/><circle cx="12" cy="12" r="1.3" fill="currentColor" stroke="none"/><circle cx="18" cy="12" r="1.3" fill="currentColor" stroke="none"/>',
  coin: '<circle cx="12" cy="12" r="8.6"/><path d="m12 7.6 1.3 2.6 2.9.4-2.1 2 .5 2.9-2.6-1.4-2.6 1.4.5-2.9-2.1-2 2.9-.4Z"/>',
  locate: '<circle cx="12" cy="12" r="6.5"/><circle cx="12" cy="12" r="2.2"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/>',
  search: '<circle cx="10.8" cy="10.8" r="6.3"/><path d="m16 16 4.5 4.5"/>',
  store: '<path d="M4 10v9h16v-9"/><path d="M3 6h18l-1 4H4Z"/><path d="M8.5 10c0 1.2 1 2 2 2s2-.8 2-2c0 1.2 1 2 2 2s2-.8 2-2c0 1.2 1 2 2 2"/>',
  download: '<path d="M12 4v11"/><path d="m7.5 10.5 4.5 4.5 4.5-4.5"/><path d="M5 20h14"/>',
};

const heartFill = '<svg viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M12 20.4S4.2 15.6 4.2 10.3A4.8 4.8 0 0 1 12 6.6a4.8 4.8 0 0 1 7.8 3.7c0 5.3-7.8 10.1-7.8 10.1Z"/></svg>';

const S = {
  token: localStorage.getItem("ronda.token") || null,
  data: null,
  deck: [],
  tab: "plans",
  chat: null,
  busy: false,
  authTab: "login",
  theme: localStorage.getItem("ronda.theme") || "noche",
  filters: { cat: "all", when: "near" },
  catalog: FALLBACK_CATALOG,
  reg: { interests: [], avatar: "🦋", variant: 0, avatarTouched: false },
  edit: null,
  source: null,
  sseTimer: null,
  suppressChat: false,
  pendingConfirm: null,
  planVenueId: null,
};

/* ------------------------------------------------------------- tiny utils */
const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function esc(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function ico(name, cls = "ico") {
  return `<svg class="${cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONS[name] || ICONS.sparkles}</svg>`;
}

function avatarHTML(user, size = "", online = false) {
  if (!user) return "";
  const inner = `<span class="avatar ${size}" data-v="${(user.variant || 0) % 8}"><span>${esc(user.avatar || "✨")}</span></span>`;
  return online
    ? `<span class="avatar-wrap">${inner}${user.online ? '<span class="online"></span>' : ""}</span>`
    : inner;
}

function parseDate(iso) {
  if (!iso) return null;
  const date = new Date(String(iso).replace(" ", "T"));
  return Number.isNaN(date.getTime()) ? null : date;
}

function sameDay(a, b) {
  return a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();
}

function dayLabel(iso) {
  const date = parseDate(iso);
  if (!date) return "Próximamente";
  const today = new Date();
  const tomorrow = new Date(today);
  tomorrow.setDate(today.getDate() + 1);
  if (sameDay(date, today)) return "Hoy";
  if (sameDay(date, tomorrow)) return "Mañana";
  return `${DAYS[date.getDay()]} ${date.getDate()}`;
}

function timeLabel(iso) {
  const date = parseDate(iso);
  return date ? `${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}` : "";
}

function fullWhen(iso) {
  const date = parseDate(iso);
  if (!date) return "Fecha por confirmar";
  return `${DAYS[date.getDay()]} ${date.getDate()} ${MONTHS[date.getMonth()]} · ${timeLabel(iso)}`;
}

function longDate(date) {
  return `${DAYS[date.getDay()]} ${date.getDate()} de ${MONTHS[date.getMonth()]}`;
}

function planWhen(iso) {
  return `${dayLabel(iso).toUpperCase()} · ${timeLabel(iso)}`;
}

function ago(iso) {
  const date = parseDate(iso);
  if (!date) return "";
  const diff = Math.max(0, Date.now() - date.getTime());
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "ahora";
  if (mins < 60) return `hace ${mins} min`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `hace ${hours} h`;
  const days = Math.floor(hours / 24);
  if (days === 1) return "ayer";
  if (days < 7) return `hace ${days} d`;
  const d = parseDate(iso);
  return `${d.getDate()} ${MONTHS[d.getMonth()]}`;
}

function shortTime(iso) {
  const date = parseDate(iso);
  if (!date) return "";
  const diff = Math.max(0, Date.now() - date.getTime());
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "ahora";
  if (mins < 60) return `${mins} min`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours} h`;
  if (sameDay(date, new Date(Date.now() - 86400000))) return "ayer";
  return `${date.getDate()} ${MONTHS[date.getMonth()]}`;
}

function km(value) {
  return `${String(value ?? 0).replace(".", ",")} km`;
}

function haversineKm(lat1, lon1, lat2, lon2) {
  const rad = Math.PI / 180;
  const dLat = (lat2 - lat1) * rad;
  const dLon = (lon2 - lon1) * rad;
  const h = Math.sin(dLat / 2) ** 2 + Math.cos(lat1 * rad) * Math.cos(lat2 * rad) * Math.sin(dLon / 2) ** 2;
  return Math.round(2 * 6371 * Math.asin(Math.sqrt(h)) * 10) / 10;
}

function foldText(value) {
  return String(value ?? "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();
}

function cityByName(name) {
  return (S.catalog.cities || []).find((city) => city.name === name) || null;
}

function cityOptions(selected, includeAny = false) {
  const cities = S.catalog.cities || [];
  return `${includeAny ? '<option value="">Toda España</option>' : ""}${cities.map((city) => (
    `<option value="${esc(city.name)}" ${city.name === selected ? "selected" : ""}>${esc(city.name)}${city.province && city.province !== city.name ? ` · ${esc(city.province)}` : ""}</option>`
  )).join("")}`;
}

function myCoords() {
  const me = S.data?.me;
  if (me?.lat != null && me?.lon != null) return [Number(me.lat), Number(me.lon)];
  const city = cityByName(me?.city) || cityByName("Madrid");
  return city ? [city.lat, city.lon] : [40.4168, -3.7038];
}

function cityDistance(city) {
  const [lat, lon] = myCoords();
  return haversineKm(lat, lon, city.lat, city.lon);
}

function venueById(id) {
  const venueId = Number(id);
  return (S.data?.venues || []).find((venue) => venue.id === venueId) ||
    (S.catalog.venues || []).find((venue) => venue.id === venueId) || null;
}

function nearbyVenues(limit = 10, city = null) {
  const me = S.data?.me;
  if (!me) return [];
  const radius = Number(me.max_distance || 20);
  return (S.data?.venues || [])
    .filter((venue) => venue.distance_km <= radius && (!city || venue.city === city))
    .slice(0, limit);
}

function num(value) {
  return new Intl.NumberFormat("es-ES").format(Number(value) || 0);
}

function catOf(key) {
  const all = S.catalog?.categories || FALLBACK_CATALOG.categories;
  return all.find((c) => c.key === key) || FALLBACK_CATALOG.categories.at(-1);
}

function isHost(p) { return p.my_status === "host"; }
function isJoined(p) { return p.my_status === "joined" || p.my_status === "host"; }

function firstName(name) { return String(name || "").split(" ")[0]; }

/* ------------------------------------------------------------- api */
async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json" };
  if (S.token) headers.Authorization = `Bearer ${S.token}`;
  let response;
  try {
    response = await fetch(`/api${path}`, {
      method: options.method || "GET",
      headers,
      body: options.body ? JSON.stringify(options.body) : undefined,
    });
  } catch (error) {
    throw new Error("No hay conexión con el servidor");
  }
  let payload = {};
  try { payload = await response.json(); } catch { /* empty body */ }
  if (!response.ok) {
    if (response.status === 401 && S.token) {
      hardLogout("Sesión caducada. Vuelve a entrar.");
    }
    const error = new Error(payload.error || "Algo salió mal");
    error.status = response.status;
    throw error;
  }
  return payload;
}

/* ------------------------------------------------------------- ui helpers */
function toast(message, type = "ok") {
  const root = $("#toasts");
  if (!root) return;
  const item = document.createElement("div");
  item.className = `toast ${type}`;
  item.innerHTML = `${type === "error" ? ico("close") : ico("sparkles")}<span>${esc(message)}</span>`;
  root.append(item);
  setTimeout(() => {
    item.classList.add("out");
    setTimeout(() => item.remove(), 240);
  }, 3200);
}

function setTheme(key) {
  const theme = THEMES.find((t) => t.key === key) ? key : "noche";
  S.theme = theme;
  document.documentElement.dataset.theme = theme;
  localStorage.setItem("ronda.theme", theme);
  const meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.setAttribute("content", THEMES.find((t) => t.key === theme)?.bg || "#0a0810");
  $$(".swatch").forEach((el) => el.classList.toggle("active", el.dataset.themeChoice === theme));
}

function openLayer(element) {
  $("#layers").append(element);
  document.body.classList.add("modal-open");
}

function closeLayer(element) {
  if (!element) return;
  element.remove();
  if (element.classList.contains("sheet-layer")) S.pendingConfirm = null;
  if (!$(".chat-layer, .sheet-layer, .match-layer, .notif-layer")) {
    document.body.classList.remove("modal-open");
  }
}

function closeAllLayers() {
  $("#layers").innerHTML = "";
  S.pendingConfirm = null;
  document.body.classList.remove("modal-open");
  S.chat = null;
}

function closeTopLayer() {
  const layers = $$("#layers > *");
  if (layers.length) closeLayer(layers.at(-1));
  if (!layers.length || layers.length === 1) S.chat = S.chat && layers.at(-1)?.classList.contains("chat-layer") ? null : S.chat;
}

function openSheet({ title, content, foot = "", className = "" }) {
  const layer = document.createElement("div");
  layer.className = "sheet-layer";
  layer.innerHTML = `
    <div class="sheet ${className}" role="dialog" aria-modal="true" aria-label="${esc(title)}">
      <div class="sheet-grab"></div>
      <div class="sheet-head">
        <h2>${esc(title)}</h2>
        <button class="sheet-close" type="button" data-action="close-layer" aria-label="Cerrar">${ico("close")}</button>
      </div>
      ${content}
      ${foot ? `<div class="sheet-foot">${foot}</div>` : ""}
    </div>`;
  layer.addEventListener("click", (event) => {
    if (event.target === layer) closeLayer(layer);
  });
  openLayer(layer);
  return layer;
}

function confirmSheet({ title, message, confirmLabel = "Confirmar", danger = false, onConfirm = null }) {
  S.pendingConfirm = onConfirm;
  return openSheet({
    title,
    content: `<div class="sheet-body"><p style="color:var(--muted);font-size:13px;line-height:1.55">${esc(message)}</p></div>`,
    foot: `<button class="btn btn-soft" type="button" data-action="close-layer">Cancelar</button>
           <button class="btn ${danger ? "btn-danger" : "btn-primary"}" type="button" data-action="confirm-pending">${esc(confirmLabel)}</button>`,
  });
}

async function runPendingConfirm(button) {
  const callback = S.pendingConfirm;
  if (!callback) return;
  const original = button.innerHTML;
  button.disabled = true;
  button.textContent = "Un momento…";
  try {
    await callback();
  } catch (error) {
    toast(error.message || "No se pudo completar la acción", "error");
    button.disabled = false;
    button.innerHTML = original;
  }
}

/* ------------------------------------------------------------- auth */
function showAuth() {
  $("#auth-screen").classList.remove("hidden");
  $("#app-shell").classList.add("hidden");
  renderAuthCatalog();
}

function showApp() {
  $("#auth-screen").classList.add("hidden");
  $("#app-shell").classList.remove("hidden");
  renderNav();
  updateChrome();
}

function setAuthTab(tab) {
  S.authTab = tab;
  $$(".auth-tab").forEach((el) => el.classList.toggle("active", el.dataset.authTab === tab));
  $("#login-form").classList.toggle("hidden", tab !== "login");
  $("#register-form").classList.toggle("hidden", tab !== "register");
}

async function renderAuthCatalog() {
  const demoRoot = $("#demo-accounts");
  if (demoRoot && !demoRoot.dataset.ready) {
    demoRoot.innerHTML = `<div class="demo-card skeleton" style="height:56px;border:0"></div><div class="demo-card skeleton" style="height:56px;border:0"></div>`;
  }
  const citySelect = $("#reg-city");
  if (citySelect && !citySelect.options.length) {
    citySelect.innerHTML = cityOptions("Madrid");
    citySelect.value = "Madrid";
  }
  const interestRoot = $("#reg-interests");
  if (interestRoot && !interestRoot.dataset.ready) {
    interestRoot.innerHTML = S.catalog.interests.slice(0, 24).map((interest) => (
      `<button class="chip chip-toggle" type="button" data-action="reg-interest" data-value="${esc(interest)}">${esc(interest)}</button>`
    )).join("");
    interestRoot.dataset.ready = "1";
  }
  const avatarRoot = $("#reg-avatars");
  if (avatarRoot && !avatarRoot.dataset.ready) {
    avatarRoot.innerHTML = S.catalog.avatars.map((emoji, index) => (
      `<button class="avatar-pick ${index === 0 ? "active" : ""}" type="button" data-action="reg-avatar" data-value="${esc(emoji)}" data-index="${index}">${esc(emoji)}</button>`
    )).join("");
    avatarRoot.dataset.ready = "1";
  }
  if (demoRoot) {
    try {
      const data = await api("/demo-accounts");
      demoRoot.innerHTML = data.accounts.map((account) => `
        <button class="demo-card" type="button" data-action="demo-login" data-username="${esc(account.username)}">
          <span class="avatar" data-v="${account.variant}"><span>${esc(account.avatar)}</span></span>
          <span><strong>${esc(account.name)}</strong><span>${account.age} · ${esc(account.city || account.zone)}</span></span>
          <span class="enter">↗</span>
        </button>`).join("");
      demoRoot.dataset.ready = "1";
    } catch {
      demoRoot.innerHTML = "";
    }
  }
}

function toggleRegChip(button) {
  const value = button.dataset.value;
  if (!value) return;
  if (S.reg.interests.includes(value)) {
    S.reg.interests = S.reg.interests.filter((item) => item !== value);
  } else {
    if (S.reg.interests.length >= 6) return toast("Elige como máximo 6 intereses");
    S.reg.interests.push(value);
  }
  button.classList.toggle("active", S.reg.interests.includes(value));
  button.setAttribute("aria-pressed", S.reg.interests.includes(value) ? "true" : "false");
}

function pickRegAvatar(button) {
  S.reg.avatar = button.dataset.value || "🦋";
  S.reg.variant = Number(button.dataset.index || 0) % 8;
  $$("#reg-avatars .avatar-pick").forEach((el) => el.classList.toggle("active", el === button));
}

async function doLogin(username, password) {
  const data = await api("/auth/login", { method: "POST", body: { username, password } });
  await afterAuth(data.token, data.user, data);
}

async function afterAuth(token, user, meta = {}) {
  S.token = token;
  localStorage.setItem("ronda.token", token);
  S.data = null;
  S.chat = null;
  showApp();
  try {
    await loadState();
    connectEvents();
    toast(`¡Hola, ${firstName(user.name)}!`);
    if (meta.welcome_granted) {
      setTimeout(() => toast(`+${WELCOME_COINS} monedas de bienvenida 🪙`), 700);
    }
  } catch (error) {
    toast(error.message, "error");
  }
}

async function submitLogin(form) {
  const button = form.querySelector("button[type=submit]");
  const body = new FormData(form);
  setBusy(button, true, "Entrando…");
  try {
    await doLogin(String(body.get("username") || "").trim(), String(body.get("password") || ""));
  } catch (error) {
    toast(error.message, "error");
  } finally {
    setBusy(button, false);
  }
}

async function submitRegister(form) {
  const button = form.querySelector("button[type=submit]");
  const body = new FormData(form);
  const payload = {
    name: body.get("name"),
    age: Number(body.get("age")),
    username: String(body.get("username") || "").toLowerCase().trim(),
    city: body.get("city"),
    password: body.get("password"),
    bio: body.get("bio"),
    interests: S.reg.interests,
    avatar: S.reg.avatar,
    variant: S.reg.variant,
    looking_for: "Conocer gente para planes espontáneos",
    status_note: "Nuevo por aquí, busco plan ✨",
  };
  if (!/^[a-z0-9_.]{3,20}$/.test(payload.username)) {
    return toast("El usuario debe tener 3-20 letras, números, punto o _", "error");
  }
  if (String(body.get("password") || "").length < 8) {
    return toast("La contraseña necesita 8 caracteres", "error");
  }
  setBusy(button, true, "Creando…");
  try {
    const data = await api("/auth/register", { method: "POST", body: payload });
    await afterAuth(data.token, data.user, data);
  } catch (error) {
    toast(error.message, "error");
  } finally {
    setBusy(button, false);
  }
}

function setBusy(button, busy, busyLabel = "Guardando…") {
  if (!button) return;
  if (busy) {
    button.dataset.label = button.innerHTML;
    button.disabled = true;
    button.textContent = busyLabel;
  } else {
    button.disabled = false;
    if (button.dataset.label) button.innerHTML = button.dataset.label;
  }
}

async function hardLogout(message) {
  S.token = null;
  S.data = null;
  S.deck = [];
  S.source?.close();
  S.source = null;
  localStorage.removeItem("ronda.token");
  closeAllLayers();
  showAuth();
  if (message) toast(message, "error");
}

async function logout() {
  try { await api("/auth/logout", { method: "POST", body: { token: S.token } }); } catch { /* ignore */ }
  await hardLogout();
}

/* ------------------------------------------------------------- state */
async function loadState(options = {}) {
  const data = await api("/state");
  S.data = data;
  if (!S.busy) S.deck = data.deck;
  updateChrome();
  if (S.chat && !options.skipChat && !S.suppressChat) refreshChat();
  if (!S.busy && !$(".sheet-layer, .chat-layer, .match-layer, .notif-layer")) {
    renderView({ preserveScroll: options.preserveScroll !== false });
  }
}

function connectEvents() {
  S.source?.close();
  if (!S.token) return;
  const source = new EventSource(`/api/events?token=${encodeURIComponent(S.token)}`);
  S.source = source;
  source.addEventListener("update", () => {
    clearTimeout(S.sseTimer);
    S.sseTimer = setTimeout(() => loadState({ preserveScroll: true }).catch(() => {}), 420);
  });
}

function updateChrome() {
  if (!S.data) return;
  const zone = $("#topbar-zone");
  if (zone) zone.textContent = S.data.me.city || "Madrid";
  const zoneChip = $("#zone-chip");
  if (zoneChip) zoneChip.title = `${S.data.me.city || "Madrid"}${S.data.me.zone ? ` · ${S.data.me.zone}` : ""}${S.data.me.location_exact ? " · GPS exacto" : ""} · Cambiar ubicación`;
  const bellDot = $("#bell-dot");
  if (bellDot) bellDot.classList.toggle("hidden", S.data.unread_notifications === 0);
  const chatBadge = $("#tab-chat-badge");
  if (chatBadge) {
    chatBadge.textContent = S.data.unread_messages > 99 ? "99+" : String(S.data.unread_messages);
    chatBadge.classList.toggle("hidden", S.data.unread_messages === 0);
  }
  const wallet = S.data.wallet || { coins: S.data.me.coins || 0, daily_available: false };
  const coinBalance = $("#coin-balance");
  if (coinBalance) coinBalance.textContent = num(wallet.coins);
  const coinDaily = $("#coin-daily");
  if (coinDaily) coinDaily.classList.toggle("hidden", !wallet.daily_available);
  const coinChip = $("#coin-chip");
  if (coinChip) {
    coinChip.classList.toggle("has-reward", !!wallet.daily_available);
    coinChip.title = wallet.daily_available
      ? `Tienes ${num(wallet.coins)} monedas · Recompensa diaria disponible`
      : `${num(wallet.coins)} monedas`;
  }
  document.title = S.data.unread_messages
    ? `(${S.data.unread_messages}) Ronda · Que nunca falte gente`
    : "Ronda · Que nunca falte gente";
  renderNav();
}

function renderNav() {
  $$(".tab[data-tab]").forEach((tab) => tab.classList.toggle("active", tab.dataset.tab === S.tab));
}

function setTab(tab) {
  if (!["plans", "discover", "chats", "profile"].includes(tab)) return;
  S.tab = tab;
  S.composerDraft = "";
  renderView();
  window.scrollTo({ top: 0, behavior: "instant" });
}

function renderView(options = {}) {
  if (!S.data) return;
  const scrollY = window.scrollY;
  renderNav();
  updateChrome();
  if (S.tab === "plans") renderPlans();
  else if (S.tab === "discover") renderDiscover();
  else if (S.tab === "chats") renderChats();
  else renderProfile();
  if (options.preserveScroll) window.scrollTo({ top: scrollY, behavior: "instant" });
}

/* ------------------------------------------------------------- plans view */
function filteredPlans() {
  const today = new Date();
  const radius = Number(S.data.me.max_distance || 20);
  const plans = S.data.plans.filter((plan) => {
    if (S.filters.cat !== "all" && plan.category !== S.filters.cat) return false;
    if (S.filters.when === "today" && !sameDay(parseDate(plan.start_at) || today, today)) return false;
    if (S.filters.when === "weekend") {
      const day = (parseDate(plan.start_at) || today).getDay();
      if (![0, 5, 6].includes(day)) return false;
    }
    if (S.filters.when === "near" && plan.distance_km > radius) return false;
    return true;
  });
  return plans.sort((a, b) => (a.start_at > b.start_at ? 1 : -1));
}

function heroHTML() {
  const radius = Number(S.data.me.max_distance || 20);
  const nearby = S.data.plans.filter((plan) => plan.distance_km <= radius);
  const online = S.deck.filter((item) => item.user.online).length +
    S.data.matches.filter((thread) => thread.other?.online).length;
  const people = [...S.deck.map((item) => item.user), ...S.data.matches.map((m) => m.other)]
    .filter(Boolean)
    .filter((user, index, all) => all.findIndex((u) => u.id === user.id) === index)
    .slice(0, 3);
  const today = longDate(new Date());
  return `
    <section class="hero">
      <span class="hero-pill"><span class="live"></span>${nearby.length} planes cerca</span>
      <div class="hero-copy">
        <span class="eyebrow">${esc(today)} · ${esc(S.data.me.city)}</span>
        <h1>Tu próxima <em>ronda</em> empieza aquí.</h1>
        <p>Hay ${nearby.length} planes en tu radio de ${km(radius)} y ${online} personas conectadas. Elige uno y deja de escribir «a ver si sale algo».</p>
      </div>
      <div class="hero-orbit" aria-hidden="true">
        <div class="orbit-ring"></div>
        ${people.map((user, index) => `<span class="orbit-avatar" style="--i:${index}">${avatarHTML(user)}</span>`).join("")}
        <span class="orbit-core">${ico("sparkles", "")}</span>
      </div>
    </section>
    <div class="stat-strip">
      <div class="stat"><b>${nearby.length}</b><span>planes cerca</span></div>
      <div class="stat"><b class="accent-num">${online}</b><span>en línea</span></div>
      <div class="stat"><b>${S.data.stats.matches}</b><span>tus matches</span></div>
    </div>`;
}

function miniPlanHTML(plan) {
  const color = CAT_COLORS[plan.category] || "var(--accent)";
  const statePill = isHost(plan)
    ? `<span class="pill-state host">Tu plan</span>`
    : plan.my_status === "pending"
      ? `<span class="pill-state pending">Pendiente</span>`
      : `<span class="pill-state joined">Apuntado</span>`;
  return `
    <button class="mini-plan" type="button" data-action="plan-detail" data-id="${plan.id}" style="--cat-color:${color}">
      <div class="mini-top">
        <span class="mini-emoji">${plan.emoji}</span>
        ${statePill}
      </div>
      <h4>${esc(plan.title)}</h4>
      <span class="mini-meta">${ico("calendar")}${esc(dayLabel(plan.start_at))} · ${timeLabel(plan.start_at)}</span>
      ${plan.city !== S.data.me.city ? `<span class="mini-meta">${ico("pin")}${esc(plan.city)}${plan.zone ? ` · ${esc(plan.zone)}` : ""}</span>` : ""}
      <div class="mini-foot">
        <span class="mini-people">
          ${plan.members.slice(0, 3).map((member) => avatarHTML(member, "avatar-sm")).join("")}
          <span class="more">${plan.pending_count ? `${plan.pending_count} solicitud${plan.pending_count > 1 ? "es" : ""}` : `${plan.member_count}/${plan.capacity}`}</span>
        </span>
        ${plan.pending_count ? `<span class="pill-state pending">${plan.pending_count} ⏳</span>` : ""}
      </div>
    </button>`;
}

function venueCardHTML(venue) {
  const place = venue.city === S.data?.me?.city
    ? (venue.area || venue.city)
    : `${venue.city}${venue.area ? ` · ${venue.area}` : ""}`;
  return `
    <button class="venue-card" type="button" data-action="plan-from-venue" data-id="${venue.id}" aria-label="Crear plan en ${esc(venue.name)}">
      <span class="venue-emoji">${venue.emoji || "📍"}</span>
      <span class="venue-main">
        <strong>${esc(venue.name)}</strong>
        <span>${esc(place)} · ${km(venue.distance_km)}</span>
      </span>
      <span class="venue-plus">+</span>
    </button>`;
}

function venuesSectionHTML() {
  const venues = nearbyVenues(8);
  if (!venues.length) return "";
  return `
    <section class="section">
      <div class="section-head">
        <h2 class="section-title">Locales cerca <span class="count">${venues.length}</span></h2>
        <button class="link-btn" type="button" data-action="venues">Ver todos ${ico("chevron")}</button>
      </div>
      <div class="venue-strip">${venues.map(venueCardHTML).join("")}</div>
      <p class="venue-hint">${ico("sparkles")} Toca un sitio para montar un plan ahí mismo.</p>
    </section>`;
}

function planCardHTML(plan) {
  const color = CAT_COLORS[plan.category] || "var(--accent)";
  const hasChat = !!plan.thread_id && (plan.my_status === "joined" || plan.my_status === "host");
  let action;
  if (hasChat) {
    action = `<button class="plan-chat-pill" type="button" data-action="open-chat" data-id="${plan.thread_id}" aria-label="Abrir chat del plan">
      ${ico(plan.my_status === "host" ? "star" : "check")} ${plan.my_status === "host" ? "Tu plan" : "Apuntado"} <span class="chat-divider"></span> ${ico("message")} Chat
    </button>`;
  } else if (isHost(plan)) action = `<span class="plan-joined">${ico("star")} Tu plan</span>`;
  else if (plan.my_status === "joined") action = `<span class="plan-joined">${ico("check")} Apuntado</span>`;
  else if (plan.my_status === "pending") action = `<span class="pill-state pending">Pendiente</span>`;
  else if (plan.status === "full" || plan.spots_left <= 0) action = `<span class="spots-pill full">Completo</span>`;
  else action = `<button class="btn btn-sm ${plan.spots_left === 1 ? "btn-lime" : "btn-soft"}" type="button" data-action="join-plan" data-id="${plan.id}">${plan.approval ? "Solicitar" : "Me apunto"}</button>`;
  const spotText = plan.status === "full" || plan.spots_left <= 0 ? "Completo" : plan.approval ? "Con aprobación" : `Faltan ${plan.spots_left}`;
  const spotClass = plan.status === "full" ? "full" : plan.spots_left === 1 ? "hot" : "";
  return `
    <article class="plan-card" data-action="plan-detail" data-id="${plan.id}" style="--cat-color:${color}">
      <span class="plan-thumb">${plan.emoji}</span>
      <div class="plan-main">
        <div class="plan-topline">
          <span class="plan-time">${esc(planWhen(plan.start_at))}</span>
          <span class="spots-pill ${spotClass}">${spotText}</span>
        </div>
        <h3 class="plan-title">${esc(plan.title)}</h3>
        <div class="plan-meta">
          <span class="meta-item">${ico("pin")}${esc(plan.city)}${plan.zone ? ` · ${esc(plan.zone)}` : ""}</span>
          <span class="meta-item">${ico("map")}${km(plan.distance_km)}</span>
          ${plan.compatibility ? `<span class="meta-item">${ico("sparkles")}${plan.compatibility} en común</span>` : ""}
        </div>
        <p class="plan-desc">${esc(plan.description)}</p>
        <div class="plan-foot">
          <span class="plan-people">
            <span class="avatar-stack">${plan.members.slice(0, 3).map((member) => avatarHTML(member, "avatar-sm")).join("")}</span>
            <span class="plan-host">${isHost(plan) ? "Tú organizas" : `Va ${esc(firstName(plan.host.name))}`}</span>
          </span>
          ${action}
        </div>
      </div>
    </article>`;
}

function renderPlans() {
  const myPlans = S.data.my_plans;
  const plans = filteredPlans();
  const categories = S.catalog.categories;
  const view = $("#view");
  view.innerHTML = `
    ${heroHTML()}

    <section class="section">
      <div class="section-head">
        <h2 class="section-title">Tus planes <span class="count">${myPlans.length}</span></h2>
        <button class="link-btn" type="button" data-tab="chats">Ver chats ${ico("chevron")}</button>
      </div>
      ${myPlans.length
        ? `<div class="my-plans-row">${myPlans.map(miniPlanHTML).join("")}</div>`
        : `<div class="card" style="display:flex;align-items:center;gap:12px">
             <span class="mini-emoji">${ico("sparkles")}</span>
             <div style="flex:1;min-width:0"><strong style="font-size:13px">Todavía no tienes planes</strong><div class="muted" style="font-size:11px;margin-top:2px">Crea uno o apúntate a cualquiera de abajo.</div></div>
             <button class="btn btn-sm btn-lime" type="button" data-action="create-plan">Crear</button>
           </div>`}
    </section>

    <section class="section">
      <div class="section-head">
        <h2 class="section-title">Planes abiertos <span class="count">${plans.length}</span></h2>
        <div style="display:flex;align-items:center;gap:12px">
          <button class="link-btn" type="button" data-action="venues">${ico("store")} Locales</button>
          <button class="link-btn" type="button" data-action="filters">${ico("filter")} Ajustar</button>
        </div>
      </div>

      <div class="filter-row" aria-label="Filtrar por categoría">
        <button class="chip ${S.filters.cat === "all" ? "active" : ""}" type="button" data-filter-cat="all">✨ Todos</button>
        ${categories.map((cat) => `<button class="chip ${S.filters.cat === cat.key ? "active" : ""}" type="button" data-filter-cat="${cat.key}"><span>${cat.emoji}</span>${esc(cat.label)}</button>`).join("")}
      </div>
      <div class="filter-tools">
        <div class="segmented">
          ${[["all", "Todos"], ["today", "Hoy"], ["weekend", "Finde"], ["near", "Cerca"]].map(([key, label]) => (
            `<button class="seg-btn ${S.filters.when === key ? "active" : ""}" type="button" data-filter-when="${key}">${label}</button>`
          )).join("")}
        </div>
        <span class="eyebrow">${plans.length} resultados</span>
      </div>

      <div class="plan-list" style="margin-top:12px">
        ${plans.length ? plans.map(planCardHTML).join("") : `
          <div class="empty-state">
            <div class="empty-art">🫥</div>
            <h3>Nada por aquí… todavía</h3>
            <p>No hay planes con esos filtros en ${esc(S.data.me.city)}. Cambia de ciudad, amplía el radio o crea tú el plan que te apetece.</p>
            <div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap">
              <button class="btn btn-soft btn-sm" type="button" data-action="location">${ico("locate")} Cambiar ciudad</button>
              <button class="btn btn-primary btn-sm" type="button" data-action="create-plan">Crear un plan</button>
            </div>
          </div>`}
      </div>
    </section>

    ${venuesSectionHTML()}`;

  renderNav();
}

/* ------------------------------------------------------------- discover */
function deckCardHTML(item, index) {
  const user = item.user;
  const interests = user.interests.slice(0, 4);
  const tags = interests.map((interest) => (
    `<span class="tag ${item.shared_interests.includes(interest) ? "shared" : ""}">${item.shared_interests.includes(interest) ? '<span class="mini-dot"></span>' : ""}${esc(interest)}</span>`
  )).join("");
  return `
    <article class="deck-card" data-depth="${index}" data-uid="${user.id}" data-v="${(user.variant || 0) % 8}" style="z-index:${10 - index}">
      <div class="deck-hero">
        <span class="deck-flag">${user.online ? '<span class="live"></span>Activo ahora' : `${ico("clock")} Hace un rato`}</span>
        <span class="deck-index">${String(index + 1).padStart(2, "0")} / ${S.deck.length}</span>
        ${avatarHTML(user)}
      </div>
      <div class="deck-body">
        <div class="deck-name">${esc(user.name)}, ${user.age}<span class="verified">${ico("check", "")}</span></div>
        <div class="deck-loc">${ico("pin")} ${esc(user.city)}${user.zone ? ` · ${esc(user.zone)}` : ""} · ${km(item.distance_km)}</div>
        ${user.status_note ? `<span class="deck-status">${esc(user.status_note)}</span>` : ""}
        <p class="deck-bio">${esc(user.bio)}</p>
        ${tags ? `<div class="deck-tags">${tags}</div>` : ""}
        ${item.plan ? `<div class="deck-plan"><span class="emoji">${item.plan.emoji}</span><span><b>${esc(item.plan.title)}</b> · ${esc(dayLabel(item.plan.start_at))} · faltan ${item.plan.spots_left}</span></div>` : ""}
      </div>
      <div class="stamp like">ME APUNTO</div>
      <div class="stamp nope">PASO</div>
    </article>`;
}

function deckHTML() {
  if (!S.deck.length) {
    return `
      <div class="deck-empty">
        <div class="empty-art">👀</div>
        <h3>Has visto a todo el mundo</h3>
        <p>En ${esc(S.data.me.city)} no queda nadie nuevo en tu radio. Cambia de ciudad, amplía la distancia o crea un plan para que vengan a ti.</p>
        <div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center">
          <button class="btn btn-soft btn-sm" type="button" data-action="location">${ico("locate")} Cambiar ciudad</button>
          <button class="btn btn-soft btn-sm" type="button" data-action="filters">${ico("filter")} Ampliar radio</button>
          <button class="btn btn-soft btn-sm" type="button" data-action="reset-deck">${ico("refresh")} Volver a ver</button>
          <button class="btn btn-primary btn-sm" type="button" data-action="create-plan">Crear plan</button>
        </div>
      </div>`;
  }
  return `<div class="deck" id="deck">${S.deck.slice(0, 3).map((item, index) => deckCardHTML(item, index)).join("")}</div>`;
}

function renderDiscover() {
  const matches = S.data.matches;
  const filters = `${km(S.data.me.max_distance)} · ${S.data.me.age_min}-${S.data.me.age_max} años`;
  const wallet = S.data.wallet || { coins: S.data.me.coins || 0, daily_available: false, daily_amount: DAILY_COINS, like_cost: LIKE_COST };
  const coins = wallet.coins ?? 0;
  const likeCost = wallet.like_cost ?? LIKE_COST;
  const canAfford = coins >= likeCost;
  $("#view").innerHTML = `
    <div class="discover-head">
      <div>
        <span class="eyebrow">Modo descubrir</span>
        <h1 class="screen-heading" style="margin-top:8px">Gente con <em>planes.</em></h1>
        <p class="screen-sub">${S.deck.length} cerca en ${esc(S.data.me.city)} · ${esc(filters)}${matches.length ? ` · ${matches.length} matches` : ""}</p>
      </div>
      <div style="display:flex;gap:6px;flex:none">
        <button class="icon-btn" type="button" data-action="location" aria-label="Cambiar ciudad">${ico("locate")}</button>
        <button class="icon-btn" type="button" data-action="filters" aria-label="Ajustar filtros">${ico("filter")}</button>
      </div>
    </div>

    <section class="section" style="margin-top:2px">
      <div id="deck-wrap">${deckHTML()}</div>
      ${S.deck.length ? `
        <div class="deck-actions">
          <button class="round-btn pass" type="button" data-action="swipe" data-dir="pass" aria-label="Pasar">${ico("close")}</button>
          <button class="round-btn super" type="button" data-action="swipe" data-dir="super" aria-label="Superlike">${ico("star")}<span class="cost-tag">${likeCost}</span></button>
          <button class="round-btn like" type="button" data-action="swipe" data-dir="like" aria-label="Me interesa">${heartFill}<span class="cost-tag">${likeCost}</span></button>
        </div>
        <p class="deck-hint">${canAfford
          ? `Cada like cuesta <b>${likeCost}</b> monedas · Tienes <b>${num(coins)}</b>`
          : `Te faltan monedas · Tienes <b>${num(coins)}</b>`}${wallet.daily_available ? ` · <button class="inline-link" type="button" data-action="wallet">Reclama +${wallet.daily_amount ?? DAILY_COINS}</button>` : ""}</p>` : ""}
    </section>`;
}

function refreshDeck() {
  const wrap = $("#deck-wrap");
  if (!wrap) return;
  wrap.innerHTML = deckHTML();
  attachSwipe();
}

function attachSwipe() {
  const card = $("#deck [data-depth='0']");
  if (!card) return;
  let startX = 0;
  let startY = 0;
  let dx = 0;
  let dy = 0;
  let dragging = false;
  let pointerId = null;
  const likeStamp = card.querySelector(".stamp.like");
  const nopeStamp = card.querySelector(".stamp.nope");

  const reset = () => {
    card.style.transition = "transform .32s cubic-bezier(.2,.9,.25,1), opacity .25s ease";
    card.style.transform = "";
    card.style.opacity = "";
    if (likeStamp) likeStamp.style.opacity = "0";
    if (nopeStamp) nopeStamp.style.opacity = "0";
  };

  card.addEventListener("pointerdown", (event) => {
    if (S.busy || event.target.closest("button")) return;
    dragging = true;
    pointerId = event.pointerId;
    startX = event.clientX;
    startY = event.clientY;
    dx = 0;
    dy = 0;
    card.style.transition = "none";
    try { card.setPointerCapture(pointerId); } catch { /* ignore */ }
  });

  card.addEventListener("pointermove", (event) => {
    if (!dragging) return;
    dx = event.clientX - startX;
    dy = event.clientY - startY;
    if (Math.abs(dx) < 4 && Math.abs(dy) < 4) return;
    const rotate = Math.max(-16, Math.min(16, dx / 14));
    card.style.transform = `translate(${dx}px, ${dy * 0.35}px) rotate(${rotate}deg)`;
    if (likeStamp) likeStamp.style.opacity = String(Math.min(1, Math.max(0, dx / 90)));
    if (nopeStamp) nopeStamp.style.opacity = String(Math.min(1, Math.max(0, -dx / 90)));
  });

  const finish = (event) => {
    if (!dragging) return;
    dragging = false;
    try { card.releasePointerCapture(pointerId); } catch { /* ignore */ }
    if (Math.abs(dx) > 92) {
      applySwipe(dx > 0 ? "like" : "pass");
    } else if (dy < -110 && Math.abs(dx) < 70) {
      applySwipe("super");
    } else {
      reset();
    }
  };
  card.addEventListener("pointerup", finish);
  card.addEventListener("pointercancel", () => { dragging = false; reset(); });
  card.addEventListener("lostpointercapture", () => { if (dragging) { dragging = false; reset(); } });
}

async function applySwipe(direction) {
  if (S.busy || !S.deck.length) return;
  const wallet = S.data.wallet || { coins: S.data.me.coins || 0, daily_available: false, daily_amount: DAILY_COINS, like_cost: LIKE_COST };
  if (!S.data.wallet) S.data.wallet = wallet;
  const likeCost = wallet.like_cost ?? LIKE_COST;
  if (direction !== "pass" && wallet.coins < likeCost) {
    toast(`Te faltan monedas: cada like cuesta ${likeCost}`, "error");
    showWallet();
    return;
  }
  S.busy = true;
  const item = S.deck[0];
  const card = $("#deck [data-depth='0']");
  if (card) {
    const x = direction === "pass" ? -520 : 520;
    card.style.transition = "transform .34s cubic-bezier(.3,.7,.3,1), opacity .3s ease";
    card.style.transform = `translate(${x}px, -40px) rotate(${direction === "pass" ? -22 : 22}deg)`;
    card.style.opacity = "0";
  }
  await wait(270);
  S.deck = S.deck.slice(1);
  refreshDeck();
  try {
    const result = await api("/swipes", { method: "POST", body: { user_id: item.user.id, action: direction } });
    if (typeof result.coins === "number") {
      S.data.wallet.coins = result.coins;
      S.data.me.coins = result.coins;
      updateChrome();
    }
    if (result.match?.is_new) {
      showMatch(result.match);
    } else if (result.match) {
      toast("Ya hicisteis match. El chat os espera 💬");
    } else if (direction === "super") {
      toast("Superlike enviado ⭐");
    }
  } catch (error) {
    if (error.status === 402) {
      S.deck = [item, ...S.deck.filter((entry) => entry.user.id !== item.user.id)];
      refreshDeck();
      showWallet();
    }
    toast(error.message, "error");
  }
  S.busy = false;
  try { await loadState({ preserveScroll: true }); } catch { /* ignore */ }
}

/* ------------------------------------------------------------- match modal */
function showMatch(match) {
  closeAllLayers();
  const me = S.data.me;
  const other = match.user;
  const shared = (other.shared_interests || []).slice(0, 3);
  const layer = document.createElement("div");
  layer.className = "match-layer";
  const colors = ["#ff4d6d", "#c6ff4a", "#43e0d0", "#9b7bff", "#ffc24b"];
  const confetti = Array.from({ length: 22 }, (_, i) => {
    const left = (i * 37 + 8) % 100;
    const dur = 2 + ((i * 13) % 18) / 10;
    const delay = ((i * 7) % 20) / 10;
    const color = colors[i % colors.length];
    return `<i style="left:${left}%;--dur:${dur}s;--delay:${delay}s;background:${color}"></i>`;
  }).join("");
  layer.innerHTML = `
    <div class="match-card">
      <div class="confetti">${confetti}</div>
      <span class="match-kicker">Match · ${esc(other.city || other.zone)}</span>
      <h2 class="match-title">¡Match!</h2>
      <p class="match-sub">A ti y a ${esc(firstName(other.name))} os va la misma vibe${shared.length ? `: ${esc(shared.join(", ").toLowerCase())}` : ""}. Ya tenéis un chat privado.</p>
      <div class="match-avatars">
        ${avatarHTML(me)}
        <span class="match-heart">${ico("heart", "")}</span>
        ${avatarHTML(other)}
      </div>
      <div class="match-actions">
        <button class="btn btn-primary btn-lg" type="button" data-action="match-chat" data-thread="${match.thread_id}">Mandar mensaje</button>
        <button class="btn btn-soft" type="button" data-action="close-layer">Seguir explorando</button>
      </div>
    </div>`;
  layer.addEventListener("click", (event) => { if (event.target === layer) closeLayer(layer); });
  openLayer(layer);
}

/* ------------------------------------------------------------- chats */
function threadRowHTML(thread) {
  const isPlan = thread.kind === "plan";
  const last = thread.last_message;
  const who = thread.other;
  const title = isPlan ? (thread.plan?.title || thread.title) : (who?.name || "Match");
  const avatar = isPlan
    ? `<span class="thread-avatar"><span class="avatar" data-v="${(who?.variant || 0) % 8}" style="background:linear-gradient(135deg,color-mix(in srgb,var(--accent) 32%,transparent),var(--surface-3))"><span>${thread.plan?.emoji || "📍"}</span></span><span class="plan-mark">👥</span></span>`
    : `<span class="thread-avatar">${avatarHTML(who, "", true)}</span>`;
  const preview = last
    ? `<span class="plan-tag">${isPlan ? "PLAN" : "DM"}</span>${last.kind === "system" ? esc(last.body) : `${last.user_id === S.data.me.id ? "Tú: " : ""}${esc(last.body)}`}`
    : `<span class="muted">${isPlan ? "Chat del plan" : "Di hola 👋"}</span>`;
  return `
    <button class="thread ${thread.unread ? "unread" : ""}" type="button" data-action="open-chat" data-id="${thread.id}">
      ${avatar}
      <span class="thread-main">
        <span class="thread-title-row">
          <span class="thread-title">${esc(title)} ${isPlan ? `<span class="muted" style="font-weight:400;font-size:10px">· ${thread.member_count}</span>` : ""}</span>
          <span class="thread-time">${shortTime(thread.last_at)}</span>
        </span>
        <span class="thread-preview">${preview}</span>
      </span>
      ${thread.unread ? `<span class="unread-badge">${thread.unread > 9 ? "9+" : thread.unread}</span>` : ""}
    </button>`;
}

function renderChats() {
  const threads = S.data.threads;
  const matches = S.data.matches;
  $("#view").innerHTML = `
    <div class="screen-head">
      <div>
        <span class="eyebrow">La previa empieza aquí</span>
        <h1 class="screen-heading" style="margin-top:8px">Tus <em>chats.</em></h1>
        <p class="screen-sub">${threads.length} conversaciones · ${S.data.unread_messages} sin leer. Los planes también tienen chat de grupo.</p>
      </div>
    </div>

    ${matches.length ? `
      <section class="section" style="margin-top:10px">
        <div class="section-head"><h2 class="section-title">Matches <span class="count">${matches.length}</span></h2></div>
        <div class="match-strip">
          ${matches.map((thread) => `
            <button class="match-bubble" type="button" data-action="open-chat" data-id="${thread.id}">
              ${avatarHTML(thread.other, "", true)}
              <span>${esc(firstName(thread.other?.name))}</span>
            </button>`).join("")}
        </div>
      </section>` : ""}

    <section class="section">
      <div class="section-head"><h2 class="section-title">Conversaciones <span class="count">${threads.length}</span></h2></div>
      ${threads.length ? `<div class="thread-list">${threads.map(threadRowHTML).join("")}</div>` : `
        <div class="empty-state">
          <div class="empty-art">💬</div>
          <h3>Aún no hay conversaciones</h3>
          <p>Haz match en Gente o apúntate a un plan para abrir un chat con el grupo.</p>
          <button class="btn btn-primary btn-sm" type="button" data-tab="discover">Descubrir gente</button>
        </div>`}
    </section>`;
}

const messageDayLabel = (date) => {
  const today = new Date();
  if (sameDay(date, today)) return "Hoy";
  const yesterday = new Date(today);
  yesterday.setDate(today.getDate() - 1);
  if (sameDay(date, yesterday)) return "Ayer";
  return `${DAYS[date.getDay()]} ${date.getDate()} ${MONTHS[date.getMonth()]}`;
};

function messagesHTML(thread) {
  let html = "";
  if (thread.plan_full) {
    html += `<button class="pinned-plan" type="button" data-action="chat-plan" data-id="${thread.plan_full.id}">
      <span class="emoji">${thread.plan_full.emoji}</span>
      <div><strong>${esc(thread.plan_full.title)}</strong><span>${esc(fullWhen(thread.plan_full.start_at))} · ${esc(thread.plan_full.city)}${thread.plan_full.zone ? ` · ${esc(thread.plan_full.zone)}` : ""}</span></div>
      <span class="arrow">›</span>
    </button>`;
  } else {
    html += `<button class="pinned-plan" type="button" data-action="create-plan">
      <span class="emoji">⚡</span>
      <div><strong>Poned fecha al plan</strong><span>Elegid qué hacer y cread un plan abierto</span></div>
      <span class="arrow">›</span>
    </button>`;
  }

  let lastDay = "";
  let lastAuthor = null;
  if (!thread.messages.length) {
    html += `<div class="chat-empty">Todavía no hay mensajes. Rompe el hielo con un plan concreto 👇</div>`;
  }
  for (const message of thread.messages) {
    const date = parseDate(message.created_at);
    if (date) {
      const label = messageDayLabel(date);
      if (label !== lastDay) {
        html += `<div class="day-sep">${esc(label)}</div>`;
        lastDay = label;
        lastAuthor = null;
      }
    }
    if (message.kind === "system") {
      html += `<div class="msg system">${esc(message.body)}</div>`;
      lastAuthor = null;
      continue;
    }
    const mine = message.user_id === S.data.me.id;
    const showAuthor = thread.kind === "plan" && !mine && message.user_id !== lastAuthor;
    html += `<div class="msg ${mine ? "me" : "other"}">
      ${showAuthor ? `<span class="msg-author">${esc(message.author)}</span>` : ""}
      <div class="msg-bubble">${esc(message.body)}</div>
      <span class="msg-time">${timeLabel(message.created_at)}</span>
    </div>`;
    lastAuthor = message.user_id;
  }
  return html;
}

function chatPanelHTML(thread) {
  const isPlan = thread.kind === "plan";
  const who = thread.other;
  const title = isPlan ? (thread.plan_full?.title || thread.title) : (who?.name || "Match");
  const subtitle = isPlan
    ? `${thread.member_count} personas · ${thread.plan_full ? `${fullWhen(thread.plan_full.start_at)} · ${thread.plan_full.city}` : "plan abierto"}`
    : `${esc(who?.city || "")}${who?.zone ? ` · ${esc(who.zone)}` : ""}${who?.online ? " · en línea" : ""}`;
  return `
    <div class="chat-panel">
      <header class="chat-head">
        <button class="chat-back" type="button" data-action="close-chat" aria-label="Volver">${ico("back")}</button>
        <div class="chat-user">
          ${isPlan
            ? `<span class="avatar" data-v="${(who?.variant || 0) % 8}" style="background:linear-gradient(135deg,color-mix(in srgb,var(--accent) 35%,transparent),var(--surface-3))"><span>${thread.plan_full?.emoji || "📍"}</span></span>`
            : avatarHTML(who, "", true)}
          <div style="min-width:0">
            <h3>${esc(title)}</h3>
            <p>${isPlan ? `<span class="live"></span>${esc(subtitle)}` : `${esc(subtitle)}`}</p>
          </div>
        </div>
        ${isPlan && thread.plan_full
          ? `<div class="chat-head-actions">
               <button class="icon-btn" type="button" data-action="chat-plan" data-id="${thread.plan_full.id}" aria-label="Ver plan">${ico("calendar")}</button>
               <button class="icon-btn" type="button" data-action="chat-leave" data-plan="${thread.plan_full.id}" aria-label="${thread.plan_full.my_status === "host" ? "Cancelar plan" : "Salir del plan"}">${ico("logout")}</button>
             </div>`
          : `<button class="icon-btn" type="button" data-action="create-plan" aria-label="Crear plan">${ico("plus")}</button>`}
      </header>
      <div class="chat-body" id="chat-messages">${messagesHTML(thread)}</div>
      <div class="quick-row">
        ${(isPlan ? QUICK_PLAN : QUICK_MATCH).map((text) => `<button class="chip" type="button" data-action="quick-message" data-text="${esc(text)}">${esc(text)}</button>`).join("")}
      </div>
      <form class="composer" id="chat-form">
        <textarea id="chat-input" rows="1" maxlength="1000" placeholder="Escribe algo…" aria-label="Mensaje"></textarea>
        <button class="send-btn" type="submit" aria-label="Enviar">${ico("send")}</button>
      </form>
    </div>`;
}

async function openChat(threadId) {
  const id = Number(threadId);
  if (!id) return;
  S.chat = { id, data: null };
  const layer = document.createElement("div");
  layer.className = "chat-layer";
  layer.id = "chat-layer";
  layer.innerHTML = `<div class="chat-panel">
    <header class="chat-head"><button class="chat-back" type="button" data-action="close-chat">${ico("back")}</button><div class="chat-user"><div><h3>Cargando chat…</h3></div></div></header>
    <div class="chat-body"><div class="chat-empty">Un momento…</div></div>
  </div>`;
  layer.addEventListener("click", (event) => { if (event.target === layer) closeChat(); });
  openLayer(layer);
  try {
    const data = await api(`/threads/${id}`);
    if (!S.chat || S.chat.id !== id) return;
    S.chat.data = data;
    if (S.data) {
      const thread = S.data.threads.find((item) => item.id === id);
      if (thread) thread.unread = 0;
      S.data.unread_messages = S.data.threads.reduce((sum, item) => sum + item.unread, 0);
      updateChrome();
    }
    layer.innerHTML = chatPanelHTML(data);
    const box = $("#chat-messages");
    if (box) box.scrollTop = box.scrollHeight;
    const input = $("#chat-input");
    if (input) input.focus({ preventScroll: true });
  } catch (error) {
    toast(error.message, "error");
    closeChat();
  }
}

async function refreshChat() {
  if (!S.chat) return;
  const id = S.chat.id;
  try {
    const data = await api(`/threads/${id}`);
    if (!S.chat || S.chat.id !== id) return;
    S.chat.data = data;
    const box = $("#chat-messages");
    if (!box) { renderChatPanel(); return; }
    const nearBottom = box.scrollHeight - box.scrollTop - box.clientHeight < 140;
    box.innerHTML = messagesHTML(data);
    if (nearBottom) box.scrollTop = box.scrollHeight;
  } catch { /* chat may be gone */ }
}

function renderChatPanel() {
  if (!S.chat?.data) return;
  const layer = $("#chat-layer");
  if (!layer) return;
  layer.innerHTML = chatPanelHTML(S.chat.data);
  const box = $("#chat-messages");
  if (box) box.scrollTop = box.scrollHeight;
}

function closeChat() {
  const layer = $("#chat-layer");
  if (layer) closeLayer(layer);
  S.chat = null;
  if (S.data) {
    S.data.unread_messages = S.data.threads.reduce((sum, item) => sum + (item.unread || 0), 0);
    updateChrome();
  }
}

async function sendChatMessage(text) {
  if (!S.chat?.data) return;
  const thread = S.chat.data;
  const input = $("#chat-input");
  const body = String(text ?? input?.value ?? "").trim();
  if (!body) return;
  if (input) {
    input.value = "";
    input.style.height = "auto";
  }
  const box = $("#chat-messages");
  const temp = document.createElement("div");
  temp.className = "msg me";
  temp.innerHTML = `<div class="msg-bubble">${esc(body)}</div><span class="msg-time">${timeLabel(new Date().toISOString().slice(0, 16))}</span>`;
  if (box) {
    box.append(temp);
    box.scrollTop = box.scrollHeight;
  }
  try {
    await api(`/threads/${thread.id}/messages`, { method: "POST", body: { body } });
    const data = await api(`/threads/${thread.id}`);
    if (!S.chat || S.chat.id !== thread.id) return;
    S.chat.data = data;
    if (box) {
      box.innerHTML = messagesHTML(data);
      box.scrollTop = box.scrollHeight;
    }
    loadState({ preserveScroll: true, skipChat: true }).catch(() => {});
  } catch (error) {
    temp.remove();
    if (input) input.value = body;
    toast(error.message, "error");
  }
}

/* ------------------------------------------------------------- profile */
function profileView() {
  const me = S.data.me;
  const stats = S.data.stats;
  const wallet = S.data.wallet || { coins: me.coins || 0, daily_available: false, like_cost: LIKE_COST };
  return `
    <section class="profile-hero">
      <div class="profile-top">
        <span class="profile-avatar-wrap avatar-wrap">
          ${avatarHTML(me, "")}
          <span class="online"></span>
        </span>
        <div class="profile-info">
          <h1>${esc(firstName(me.name))} <span>${me.age}</span></h1>
          <div class="handle">@${esc(me.username)}</div>
          <div class="loc">${ico("pin")} ${esc(me.city)}${me.zone ? ` · ${esc(me.zone)}` : ""} · ${esc(me.online ? "activo ahora" : "hace un rato")}</div>
        </div>
      </div>
      ${me.status_note ? `<span class="profile-status">${esc(me.status_note)}</span>` : ""}
      <p class="profile-bio">${esc(me.bio || "Añade una bio para que la gente sepa qué plan te apetece.")}</p>
      <div class="profile-stats">
        <div class="profile-stat"><b>${stats.plans}</b><span>planes</span></div>
        <div class="profile-stat"><b>${stats.matches}</b><span>matches</span></div>
        <div class="profile-stat"><b>${stats.connections}</b><span>conexiones</span></div>
      </div>
    </section>

    <section class="profile-section">
      <div class="section-head"><h2 class="section-title">Mi vibe <span class="count">${me.interests.length}</span></h2><button class="link-btn" type="button" data-action="edit-profile">${ico("edit")} Editar</button></div>
      <div class="interest-list">
        ${me.interests.length ? me.interests.map((interest) => `<span class="tag">${esc(interest)}</span>`).join("") : `<span class="muted" style="font-size:12px">Aún no has elegido intereses.</span>`}
      </div>
      ${me.looking_for ? `<div class="share-box" style="margin-top:10px">${ico("sparkles")} <span>Buscas: <b style="color:var(--text);font-weight:600">${esc(me.looking_for)}</b></span></div>` : ""}
    </section>

    <section class="profile-section">
      <div class="section-head"><h2 class="section-title">Ajustes</h2></div>
      <div class="settings">
        <button class="setting" type="button" data-action="wallet">
          <span class="setting-ico" style="color:var(--amber)">${ico("coin")}</span>
          <span class="setting-main"><strong>Mis monedas</strong><span>${wallet.daily_available ? "Recompensa diaria disponible" : "Cada like cuesta " + (wallet.like_cost ?? LIKE_COST)}</span></span>
          <span class="wallet-mini">${ico("coin")} ${num(wallet.coins)}</span>
        </button>
        <button class="setting" type="button" data-action="location">
          <span class="setting-ico">${ico("locate")}</span>
          <span class="setting-main"><strong>Mi ubicación</strong><span>${esc(me.city)}${me.zone ? ` · ${esc(me.zone)}` : ""} · radio ${km(me.max_distance)}</span></span>
          <span class="arrow">›</span>
        </button>
        <button class="setting" type="button" data-action="edit-profile">
          <span class="setting-ico">${ico("edit")}</span>
          <span class="setting-main"><strong>Editar perfil</strong><span>Nombre, avatar, bio e intereses</span></span>
          <span class="arrow">›</span>
        </button>
        <button class="setting" type="button" data-action="location">
          <span class="setting-ico" style="color:var(--accent-2)">${ico("locate")}</span>
          <span class="setting-main"><strong>Ubicación</strong><span>${me.location_exact ? `Exacta · ${esc(me.city)}` : `Ciudad · ${esc(me.city)}`}</span></span>
          <span class="arrow">›</span>
        </button>
        <button class="setting" type="button" data-action="export-data">
          <span class="setting-ico" style="color:var(--cyan)">${ico("download")}</span>
          <span class="setting-main"><strong>Mis datos</strong><span>Descarga tu perfil, planes, chats y monedas</span></span>
          <span class="arrow">›</span>
        </button>
        <button class="setting" type="button" data-action="filters">
          <span class="setting-ico">${ico("filter")}</span>
          <span class="setting-main"><strong>Descubrimiento</strong><span>${km(me.max_distance)} · ${me.age_min}-${me.age_max} años</span></span>
          <span class="arrow">›</span>
        </button>
        <button class="setting" type="button" data-action="notifications">
          <span class="setting-ico">${ico("bell")}</span>
          <span class="setting-main"><strong>Notificaciones</strong><span>${S.data.unread_notifications ? `${S.data.unread_notifications} sin leer` : "Todo al día"}</span></span>
          <span class="arrow">›</span>
        </button>
        <button class="setting" type="button" data-action="how-it-works">
          <span class="setting-ico">${ico("shield")}</span>
          <span class="setting-main"><strong>Cómo funciona Ronda</strong><span>Reglas, match y planes</span></span>
          <span class="arrow">›</span>
        </button>
        <button class="setting" type="button" data-action="logout">
          <span class="setting-ico">${ico("logout")}</span>
          <span class="setting-main"><strong>Cerrar sesión</strong><span>@${esc(me.username)}</span></span>
          <span class="arrow">›</span>
        </button>
      </div>
      <div class="share-box" style="margin-top:10px">${ico("shield")} <span>Tu cuenta y tus chats se guardan en la base de datos de Ronda. Cierra y vuelve a abrir cuando quieras: siguen ahí. Descarga una copia en <b style="color:var(--text)">Mis datos</b>.</span></div>
    </section>

    <section class="profile-section">
      <div class="section-head"><h2 class="section-title">Tema</h2></div>
      <div class="theme-row">
        ${THEMES.map((theme) => `
          <button class="swatch ${S.theme === theme.key ? "active" : ""}" type="button" data-action="theme" data-theme-choice="${theme.key}" style="--sw-bg:${theme.bg};--sw-dot:${theme.dot};--sw-dot2:${theme.dot2}">
            <i></i><span>${theme.label}</span>
          </button>`).join("")}
      </div>
    </section>

    <p class="sheet-note" style="margin-top:26px">Ronda · Hackathon 26-27 · Hecho en España</p>`;
}

function renderProfile() {
  $("#view").innerHTML = profileView();
}

/* ------------------------------------------------------------- location */
function nearestCity(lat, lon) {
  let best = null;
  let bestDistance = Infinity;
  for (const city of S.catalog.cities || []) {
    const distance = haversineKm(lat, lon, city.lat, city.lon);
    if (distance < bestDistance) {
      bestDistance = distance;
      best = city;
    }
  }
  return best || cityByName("Madrid");
}

function nearestArea(lat, lon, cityName) {
  const venues = (S.catalog.venues || []).filter((venue) => venue.city === cityName);
  let best = null;
  let bestDistance = Infinity;
  for (const venue of venues) {
    const distance = haversineKm(lat, lon, venue.lat, venue.lon);
    if (distance < bestDistance) {
      bestDistance = distance;
      best = venue;
    }
  }
  return best && bestDistance <= 15 ? best.area : "";
}

function cityListHTML(query = "") {
  const me = S.data.me;
  const normalized = foldText(query);
  const cities = (S.catalog.cities || [])
    .map((city) => ({ ...city, distance: cityDistance(city) }))
    .sort((a, b) => a.distance - b.distance)
    .filter((city) => !normalized ||
      foldText(city.name).includes(normalized) ||
      foldText(city.province || "").includes(normalized))
    .sort((a, b) => {
      if (!normalized) return a.distance - b.distance;
      const aExact = foldText(a.name) === normalized ? 0 : 1;
      const bExact = foldText(b.name) === normalized ? 0 : 1;
      return aExact - bExact || a.distance - b.distance;
    });
  if (!cities.length) {
    return `<p class="venue-empty">${ico("search")} No encontramos esa ciudad. Prueba con otra.</p>`;
  }
  return cities.map((city) => {
    const current = city.name === me.city;
    const province = city.province && city.province !== city.name ? city.province : "";
    const distanceText = city.distance < 1 ? "aquí" : `a ${km(city.distance)}`;
    return `
      <button class="city-row ${current ? "current" : ""}" type="button" data-action="set-city" data-city="${esc(city.name)}">
        <span class="city-pin">${ico("pin")}</span>
        <span class="city-main">
          <strong>${esc(city.name)}</strong>
          <span>${province ? `${esc(province)} · ` : ""}${distanceText}</span>
        </span>
        ${current ? `<span class="city-now">${ico("check")} Actual</span>` : `<span class="city-go">›</span>`}
      </button>`;
  }).join("");
}

function showLocation() {
  const me = S.data.me;
  const nearby = (S.data.venues || []).filter((venue) => venue.distance_km <= (me.max_distance || 20)).length;
  openSheet({
    title: "Tu ubicación",
    content: `
      <div class="sheet-body">
        <div class="location-current">
          <span class="location-orb">${ico("locate")}</span>
          <div class="location-copy">
            <span class="eyebrow">${me.location_exact ? "Ubicación exacta activa" : "Ubicación aproximada"}</span>
            <strong>${esc(me.city)}${me.zone ? ` · ${esc(me.zone)}` : ""}</strong>
            <span>Radio ${km(me.max_distance)} · ${nearby} locales cerca</span>
          </div>
          <button class="icon-btn" type="button" data-action="filters" aria-label="Cambiar radio">${ico("filter")}</button>
        </div>

        <button class="btn btn-primary btn-block gps-btn" type="button" data-action="ask-gps">
          ${ico("locate")} ${me.location_exact ? "Actualizar mi ubicación exacta" : "Usar mi ubicación exacta"}
        </button>
        <p class="sheet-note" style="margin-top:8px">Te pediremos permiso antes de usar el GPS. Solo sirve para calcular distancias: el resto ve kilómetros, nunca tus coordenadas.</p>
        ${me.location_exact ? `<button class="link-btn location-revoke" type="button" data-action="clear-location">Dejar de usar mi ubicación exacta</button>` : ""}

        <div class="field" style="margin-top:18px">
          <label for="city-search">O elige cualquier ciudad de España</label>
          <div class="search-box">
            ${ico("search")}
            <input id="city-search" type="text" placeholder="Busca Madrid, Sevilla, Bilbao…" autocomplete="off">
          </div>
        </div>
        <div class="city-list" id="city-list">${cityListHTML("")}</div>
      </div>`,
    foot: `<button class="btn btn-soft" type="button" data-action="venues">${ico("store")} Locales cerca</button>
           <button class="btn btn-soft" type="button" data-action="close-layer">Cerrar</button>`,
  });
}

function askGps() {
  if (!window.isSecureContext) {
    openSheet({
      title: "Ubicación exacta no disponible",
      content: `<div class="sheet-body">
        <div class="empty-state" style="margin-top:4px">
          <div class="empty-art">${ico("lock", "")}</div>
          <h3>Este navegador pide HTTPS</h3>
          <p>Chrome, Edge y Safari solo permiten el GPS en conexiones seguras (HTTPS) o en localhost. En una dirección de red local puedes seguir usando Ronda eligiendo tu ciudad.</p>
          <button class="btn btn-primary btn-sm" type="button" data-action="location">Elegir mi ciudad</button>
        </div>
      </div>`,
      foot: `<button class="btn btn-soft" type="button" data-action="close-layer">Entendido</button>`,
    });
    return;
  }
  if (!navigator.geolocation) {
    return toast("Tu navegador no permite geolocalización", "error");
  }
  confirmSheet({
    title: "¿Autorizas tu ubicación exacta?",
    message: "Ronda usará la ubicación de este dispositivo solo para calcular distancias y ordenar planes cerca de ti. No se muestra a otras personas ni se comparte con terceros. El navegador te pedirá permiso justo después y puedes desactivarla cuando quieras.",
    confirmLabel: "Permitir ubicación",
    onConfirm: async () => {
      await useGps();
      closeAllLayers();
    },
  });
}

async function useGps(button = null) {
  if (!navigator.geolocation) {
    return toast("Tu navegador no permite geolocalización", "error");
  }
  const original = button?.innerHTML;
  if (button) {
    button.disabled = true;
    button.textContent = "Localizando…";
  }
  try {
    const position = await new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(resolve, reject, {
        enableHighAccuracy: true,
        timeout: 12000,
        maximumAge: 60000,
      });
    });
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    const city = nearestCity(lat, lon);
    const area = nearestArea(lat, lon, city.name);
    await api("/profile", {
      method: "PATCH",
      body: { city: city.name, lat, lon, zone: area, location_exact: true },
    });
    closeAllLayers();
    S.filters.when = "near";
    await loadState();
    renderView();
    toast(`Ubicación exacta activada: ${city.name}${area ? ` · ${area}` : ""} 📍`);
  } catch (error) {
    const message = error?.code === 1
      ? "Permiso de ubicación denegado. Actívalo en el navegador o elige una ciudad."
      : error?.message || "No pudimos obtener tu ubicación";
    toast(message, "error");
    if (button) {
      button.disabled = false;
      button.innerHTML = original;
    }
  }
}

async function clearExactLocation() {
  try {
    await api("/profile", { method: "PATCH", body: { location_exact: false } });
    closeAllLayers();
    await loadState();
    renderView();
    toast("Ubicación exacta desactivada. Usamos solo tu ciudad.");
  } catch (error) {
    toast(error.message, "error");
  }
}

async function downloadMyData() {
  try {
    const data = await api("/me/export");
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    const date = new Date().toISOString().slice(0, 10);
    link.href = url;
    link.download = `ronda-${S.data.me.username}-${date}.json`;
    document.body.append(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1500);
    toast("Copia de tus datos descargada 📥");
  } catch (error) {
    toast(error.message, "error");
  }
}

async function setCity(name) {
  if (!cityByName(name)) return toast("Esa ciudad no está disponible", "error");
  try {
    await api("/profile", { method: "PATCH", body: { city: name, zone: "" } });
    closeAllLayers();
    S.filters.when = "near";
    S.filters.cat = "all";
    await loadState();
    renderView();
    toast(`Ahora estás en ${name}. Esto es lo que hay cerca 📍`);
  } catch (error) {
    toast(error.message, "error");
  }
}

function showVenues() {
  const me = S.data.me;
  const venues = (S.data.venues || []).filter((venue) => venue.distance_km <= (me.max_distance || 20));
  openSheet({
    title: `Locales cerca de ${me.city}`,
    content: `
      <div class="sheet-body">
        ${venues.length ? `
          <p class="screen-sub" style="margin-bottom:12px">Sitios a menos de ${km(me.max_distance)}. Toca uno para montar un plan allí mismo.</p>
          <div class="venue-list">${venues.map(venueCardHTML).join("")}</div>
        ` : `
          <div class="empty-state" style="margin-top:8px">
            <div class="empty-art">${ico("store", "")}</div>
            <h3>Todavía no hay locales aquí</h3>
            <p>Puedes crear un plan y escribir el sitio a mano. También puedes cambiar de ciudad o ampliar el radio.</p>
            <div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap">
              <button class="btn btn-soft btn-sm" type="button" data-action="location">${ico("locate")} Cambiar ciudad</button>
              <button class="btn btn-primary btn-sm" type="button" data-action="create-plan">Crear plan</button>
            </div>
          </div>`}
      </div>`,
    foot: `<button class="btn btn-soft" type="button" data-action="location">${ico("locate")} Cambiar ciudad</button>
           <button class="btn btn-soft" type="button" data-action="close-layer">Cerrar</button>`,
  });
}

/* ------------------------------------------------------------- sheets: create plan */
function defaultPlanDate() {
  const date = new Date();
  date.setDate(date.getDate() + 1);
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
}

function defaultPlanTime() {
  const date = new Date(Date.now() + 2 * 3600 * 1000);
  date.setMinutes(Math.round(date.getMinutes() / 5) * 5, 0, 0);
  return `${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}`;
}

function venueSuggestionsHTML(city, selectedId = null) {
  const cityInfo = cityByName(city);
  const originCity = cityInfo || cityByName(S.data.me.city) || { lat: 40.4168, lon: -3.7038 };
  const origin = city === S.data.me.city ? myCoords() : [originCity.lat, originCity.lon];
  const venues = (S.catalog.venues || [])
    .filter((venue) => venue.city === city)
    .map((venue) => ({ ...venue, local_km: haversineKm(origin[0], origin[1], venue.lat, venue.lon) }))
    .sort((a, b) => a.local_km - b.local_km)
    .slice(0, 6);
  if (!venues.length) {
    return `<p class="venue-empty">${ico("store")} Aún no tenemos locales guardados en ${esc(city)}. Escribe el sitio y publicamos el plan igual.</p>`;
  }
  return `
    <div class="venue-suggestions">
      ${venues.map((venue) => `
        <button class="venue-suggestion ${Number(selectedId) === venue.id ? "active" : ""}" type="button" data-action="pick-venue" data-id="${venue.id}">
          <span class="venue-suggestion-emoji">${venue.emoji || "📍"}</span>
          <span><strong>${esc(venue.name)}</strong><span>${esc(venue.area)} · ${km(venue.local_km)}</span></span>
        </button>`).join("")}
    </div>`;
}

function showCreatePlan(prefill = {}) {
  const me = S.data.me;
  const categories = S.catalog.categories;
  const today = new Date().toISOString().slice(0, 10);
  const vibeOptions = [...new Set([...S.catalog.interests.slice(0, 20)])];
  const prefillVenue = prefill.venue || null;
  const city = prefillVenue?.city || me.city || "Madrid";
  const area = prefillVenue?.area || (city === me.city ? me.zone : "") || "";
  const venueName = prefillVenue?.name || "";
  const category = prefillVenue?.category || "cañas";
  S.planVenueId = prefillVenue?.id || null;
  openSheet({
    title: "Crear un plan",
    content: `
      <form class="sheet-body" id="create-form">
        <div class="field">
          <label for="plan-title">¿Qué plan es?</label>
          <input id="plan-title" name="title" type="text" maxlength="70" placeholder="Ej. Concierto + birras después" required>
        </div>
        <div class="field">
          <label>Categoría</label>
          <div class="category-picker" id="cat-picker">
            ${categories.map((cat) => `<button class="cat-option ${cat.key === category ? "active" : ""}" type="button" data-action="pick-cat" data-value="${cat.key}"><span>${cat.emoji}</span><b>${esc(cat.label)}</b></button>`).join("")}
          </div>
        </div>
        <div class="form-grid">
          <div class="field">
            <label for="plan-date">Día</label>
            <input id="plan-date" name="date" type="date" value="${defaultPlanDate()}" min="${today}" required>
          </div>
          <div class="field">
            <label for="plan-time">Hora</label>
            <input id="plan-time" name="time" type="time" value="${defaultPlanTime()}" required>
          </div>
        </div>
        <div class="form-grid">
          <div class="field">
            <label for="plan-city">Ciudad</label>
            <select id="plan-city" name="city">${cityOptions(city)}</select>
          </div>
          <div class="field">
            <label for="plan-area">Zona / barrio <span class="label-hint">opcional</span></label>
            <input id="plan-area" name="zone" type="text" maxlength="60" value="${esc(area)}" placeholder="Ej. Malasaña">
          </div>
        </div>
        <div class="field">
          <label for="plan-venue">Sitio <span class="label-hint">opcional</span></label>
          <input id="plan-venue" name="venue" type="text" maxlength="80" value="${esc(venueName)}" placeholder="Ej. La Riviera" autocomplete="off">
          <input type="hidden" id="plan-venue-id" name="venue_id" value="${prefillVenue?.id || ""}">
          <div id="venue-suggestions">${venueSuggestionsHTML(city, prefillVenue?.id)}</div>
        </div>
        <div class="field">
          <label>¿Cuánta gente buscas?</label>
          <div class="stepper">
            <button type="button" data-action="spots-minus" aria-label="Quitar">${ico("minus")}</button>
            <span class="stepper-value" id="spots-value">2</span>
            <button type="button" data-action="spots-plus" aria-label="Añadir">${ico("plus")}</button>
            <span class="stepper-suffix" id="spots-suffix">faltan 2 personas</span>
          </div>
          <input type="hidden" name="spots" id="plan-spots" value="2">
        </div>
        <div class="field">
          <label for="plan-desc">Cuéntalo <span class="label-hint">opcional</span></label>
          <textarea id="plan-desc" name="description" rows="3" maxlength="400" placeholder="Nivel, horario, qué llevar… lo que te gustaría saber si te apuntaras."></textarea>
        </div>
        <div class="field">
          <label>Vibe del plan <span class="label-hint">hasta 5</span></label>
          <div class="chip-wrap" id="vibe-picker">
            ${vibeOptions.map((vibe) => `<button class="chip chip-toggle" type="button" data-action="vibe-toggle" data-value="${esc(vibe)}">${esc(vibe)}</button>`).join("")}
          </div>
        </div>
        <div class="field" style="margin-bottom:4px">
          <label class="switch">
            <input type="checkbox" id="plan-approval" name="approval">
            <span class="switch-track"></span>
            <span class="switch-label">Revisar quién se apunta<br><span style="color:var(--faint)">Tú apruebas cada solicitud</span></span>
          </label>
        </div>
      </form>`,
    foot: `<button class="btn btn-primary" type="submit" form="create-form">Publicar plan</button>`,
  });
}

function pickVenue(button) {
  const venue = venueById(button.dataset.id);
  if (!venue) return;
  S.planVenueId = venue.id;
  const venueInput = $("#plan-venue");
  const areaInput = $("#plan-area");
  const hidden = $("#plan-venue-id");
  if (venueInput) venueInput.value = venue.name;
  if (areaInput) areaInput.value = venue.area || "";
  if (hidden) hidden.value = String(venue.id);
  $$("#cat-picker .cat-option").forEach((el) => el.classList.toggle("active", el.dataset.value === venue.category));
  $$("#venue-suggestions .venue-suggestion").forEach((el) => el.classList.toggle("active", Number(el.dataset.id) === venue.id));
}

function updateVenueSuggestions(city) {
  S.planVenueId = null;
  const hidden = $("#plan-venue-id");
  if (hidden) hidden.value = "";
  const venueInput = $("#plan-venue");
  if (venueInput) venueInput.value = "";
  const areaInput = $("#plan-area");
  if (areaInput) areaInput.value = "";
  const root = $("#venue-suggestions");
  if (root) root.innerHTML = venueSuggestionsHTML(city);
}

async function submitCreatePlan(form) {
  const button = form.querySelector("button[type=submit]");
  const data = new FormData(form);
  const selectedCat = $("#cat-picker .cat-option.active")?.dataset.value || "planes";
  const vibes = $$("#vibe-picker .chip.active").map((el) => el.dataset.value);
  const payload = {
    title: data.get("title"),
    category: selectedCat,
    date: data.get("date"),
    time: data.get("time"),
    city: data.get("city"),
    zone: data.get("zone"),
    venue: data.get("venue"),
    venue_id: data.get("venue_id") ? Number(data.get("venue_id")) : null,
    description: data.get("description"),
    spots: Number(data.get("spots")),
    approval: data.get("approval") === "on",
    vibe: vibes,
  };
  if (!payload.title || !payload.date || !payload.time) return toast("Completa el título, el día y la hora", "error");
  setBusy(button, true, "Publicando…");
  try {
    await api("/plans", { method: "POST", body: payload });
    closeAllLayers();
    S.tab = "plans";
    await loadState();
    setTab("plans");
    toast("Plan publicado. Que empiece la ronda 🎉");
  } catch (error) {
    toast(error.message, "error");
  } finally {
    setBusy(button, false);
  }
}

/* ------------------------------------------------------------- sheets: filters */
function showFilters() {
  const me = S.data.me;
  openSheet({
    title: "Ajustar descubrimiento",
    content: `
      <form class="sheet-body" id="filters-form">
        <div class="share-box" style="margin-bottom:14px">
          ${ico("locate")}
          <span>Buscando en <b style="color:var(--text)">${esc(me.city)}</b> · <button class="inline-link" type="button" data-action="location">Cambiar ciudad</button></span>
        </div>
        <div class="field">
          <label for="filter-distance">Distancia máxima <b id="distance-label" style="color:var(--text)">${km(me.max_distance)}</b></label>
          <input type="range" id="filter-distance" name="max_distance" min="1" max="40" value="${me.max_distance}" style="--pct:${(me.max_distance / 40) * 100}%">
          <div class="muted" style="font-size:10.5px;display:flex;justify-content:space-between"><span>1 km</span><span>40 km</span></div>
        </div>
        <div class="form-grid">
          <div class="field"><label for="filter-min">Edad mínima</label><input type="number" id="filter-min" name="age_min" min="18" max="80" value="${me.age_min}"></div>
          <div class="field"><label for="filter-max">Edad máxima</label><input type="number" id="filter-max" name="age_max" min="18" max="80" value="${me.age_max}"></div>
        </div>
        <div class="share-box" style="margin-top:4px">${ico("sparkles")} <span>El mazo prioriza a quien comparte intereses contigo. Cuantos más elijas en tu perfil, mejor el match.</span></div>
        <div style="margin-top:18px;border-top:1px solid var(--line);padding-top:14px">
          <button class="btn btn-soft btn-block btn-sm" type="button" data-action="reset-deck">${ico("refresh")} Volver a ver perfiles descartados</button>
        </div>
      </form>`,
    foot: `<button class="btn btn-primary" type="submit" form="filters-form">Guardar ajustes</button>`,
  });
}

async function submitFilters(form) {
  const data = new FormData(form);
  const payload = {
    max_distance: Number(data.get("max_distance")),
    age_min: Number(data.get("age_min")),
    age_max: Number(data.get("age_max")),
  };
  try {
    await api("/profile", { method: "PATCH", body: payload });
    closeAllLayers();
    await loadState();
    renderView();
    toast("Ajustes guardados");
  } catch (error) {
    toast(error.message, "error");
  }
}

/* ------------------------------------------------------------- plan detail */
function findPlan(id) {
  const planId = Number(id);
  return S.data?.plans.find((plan) => plan.id === planId) ||
    S.data?.my_plans.find((plan) => plan.id === planId) ||
    (S.chat?.data?.plan_full?.id === planId ? S.chat.data.plan_full : null);
}

function spotDotsHTML(plan) {
  const total = plan.capacity;
  return `<span class="spots-dots">${Array.from({ length: total }, (_, index) => {
    const person = plan.members[index];
    const isMe = person?.id === S.data.me.id;
    return `<span class="spot-dot ${person ? "on" : ""} ${isMe ? "me" : ""}"></span>`;
  }).join("")}</span>`;
}

function showPlanDetail(id) {
  const plan = findPlan(id);
  if (!plan) return toast("Ese plan ya no está disponible", "error");
  const color = CAT_COLORS[plan.category] || "var(--accent)";
  const mine = plan.my_status;
  const canChat = plan.thread_id;
  let actions = "";
  if (mine === "host") {
    actions = `${canChat ? `<button class="btn btn-primary" type="button" data-action="open-chat" data-id="${plan.thread_id}">${ico("message")} Chat del plan</button>` : ""}
      <button class="btn btn-danger" type="button" data-action="cancel-plan" data-id="${plan.id}">Cancelar</button>`;
  } else if (mine === "joined") {
    actions = `${canChat ? `<button class="btn btn-primary" type="button" data-action="open-chat" data-id="${plan.thread_id}">${ico("message")} Chat del plan</button>` : ""}
      <button class="btn btn-soft" type="button" data-action="leave-plan" data-id="${plan.id}">Salir</button>`;
  } else if (mine === "pending") {
    actions = `<button class="btn btn-soft" type="button" data-action="leave-plan" data-id="${plan.id}">Cancelar solicitud</button>`;
  } else if (plan.status === "full" || plan.spots_left <= 0) {
    actions = `<button class="btn btn-soft" disabled>Plan completo</button>`;
  } else {
    actions = `<button class="btn btn-primary" type="button" data-action="join-plan" data-id="${plan.id}">${plan.approval ? "Solicitar sitio" : "Me apunto"} ${ico("sparkles")}</button>`;
  }

  const pendingHTML = plan.pending?.length ? `
    <div class="section" style="margin-top:16px">
      <div class="section-head"><h3 class="section-title">Solicitudes <span class="count">${plan.pending.length}</span></h3></div>
      <div class="member-list">
        ${plan.pending.map((person) => `
          <div class="member-row">
            ${avatarHTML(person)}
            <div class="who"><strong>${esc(person.name)}</strong><span>${esc(person.city)}${person.zone ? ` · ${esc(person.zone)}` : ""} · ${person.age} años</span></div>
            <div class="mini-actions">
              <button type="button" class="ok" data-action="resolve-request" data-plan="${plan.id}" data-user="${person.id}" data-verdict="accept" aria-label="Aceptar">${ico("check")}</button>
              <button type="button" class="no" data-action="resolve-request" data-plan="${plan.id}" data-user="${person.id}" data-verdict="reject" aria-label="Rechazar">${ico("close")}</button>
            </div>
          </div>`).join("")}
      </div>
    </div>` : "";

  openSheet({
    title: "Detalle del plan",
    content: `
      <div class="sheet-body">
        <div class="plan-detail-hero" style="--cat-color:${color}">
          <span class="emoji">${plan.emoji}</span>
          <div>
            <h3>${esc(plan.title)}</h3>
            <p>${esc(plan.category_label)} · ${esc(plan.distance_km ? km(plan.distance_km) : "tu zona")}</p>
          </div>
        </div>
        <div class="detail-meta">
          <div><span>Cuándo</span><strong>${ico("calendar")} ${esc(fullWhen(plan.start_at))}</strong></div>
          <div><span>Dónde</span><strong>${ico("pin")} ${esc(plan.venue || plan.zone)}${plan.venue && plan.zone ? ` · ${esc(plan.zone)}` : ""} · ${esc(plan.city)}</strong></div>
          <div><span>Distancia</span><strong>${ico("map")} ${km(plan.distance_km)}</strong></div>
          <div><span>Entrada</span><strong>${plan.approval ? ico("lock") + " Con aprobación" : ico("users") + " Abierto"}</strong></div>
        </div>
        <p class="detail-desc">${esc(plan.description || "El anfitrión no ha añadido más detalles. Pregúntale en el chat.")}</p>
        ${plan.vibe?.length ? `<div class="chip-wrap" style="margin-bottom:14px">${plan.vibe.map((vibe) => `<span class="tag">${esc(vibe)}</span>`).join("")}</div>` : ""}
        <div class="section" style="margin-top:8px">
          <div class="section-head"><h3 class="section-title">Quién va <span class="count">${plan.member_count}</span></h3><span class="spots-pill ${plan.spots_left ? "" : "full"}">${plan.spots_left ? `Faltan ${plan.spots_left}` : "Completo"}</span></div>
          <div class="member-list">
            ${plan.members.map((person) => `
              <div class="member-row">
                ${avatarHTML(person, "", true)}
                <div class="who"><strong>${esc(person.name)}${person.id === S.data.me.id ? " (tú)" : ""}</strong><span>${esc(person.city)}${person.zone ? ` · ${esc(person.zone)}` : ""} · ${person.age} años${person.id === plan.host.id ? " · anfitrión" : ""}</span></div>
                ${person.id === plan.host.id ? `<span class="pill-state host">Host</span>` : ""}
              </div>`).join("")}
          </div>
        </div>
        ${pendingHTML}
        ${mine === "host" || mine === "joined" ? `<p class="sheet-note">Los chats de plan incluyen a todo el grupo. Nada de grupos paralelos.</p>` : ""}
      </div>`,
    foot: actions,
  });
}

/* ------------------------------------------------------------- edit profile */
function showEditProfile() {
  const me = S.data.me;
  S.edit = { interests: [...me.interests], avatar: me.avatar, variant: me.variant % 8 };
  openSheet({
    title: "Editar perfil",
    content: `
      <form class="sheet-body" id="edit-form">
        <div class="form-grid">
          <div class="field"><label for="edit-name">Nombre</label><input id="edit-name" name="name" type="text" maxlength="40" value="${esc(me.name)}" required></div>
          <div class="field"><label for="edit-age">Edad</label><input id="edit-age" name="age" type="number" min="18" max="99" value="${me.age}" required></div>
        </div>
        <div class="field"><label for="edit-city">Ciudad</label><select id="edit-city" name="city">${cityOptions(me.city)}</select></div>
        <div class="field"><label for="edit-area">Zona / barrio <span class="label-hint">opcional</span></label><input id="edit-area" name="zone" type="text" maxlength="60" value="${esc(me.zone)}" placeholder="Ej. Malasaña"></div>
        <div class="field"><label for="edit-status">Tu estado de hoy <span class="label-hint">máx. 80</span></label><input id="edit-status" name="status_note" type="text" maxlength="80" value="${esc(me.status_note)}" placeholder="Ej. Terraza y cañas después del curro ☀️"></div>
        <div class="field"><label for="edit-looking">Qué buscas</label><input id="edit-looking" name="looking_for" type="text" maxlength="120" value="${esc(me.looking_for)}" placeholder="Ej. Gente para conciertos y planes de día"></div>
        <div class="field"><label for="edit-bio">Bio <span class="label-hint">máx. 200</span></label><textarea id="edit-bio" name="bio" rows="3" maxlength="200">${esc(me.bio)}</textarea></div>
        <div class="field">
          <label>Avatar</label>
          <div class="avatar-picker" id="edit-avatars">
            ${S.catalog.avatars.map((emoji, index) => `<button class="avatar-pick ${emoji === me.avatar ? "active" : ""}" type="button" data-action="edit-avatar" data-value="${esc(emoji)}" data-index="${index}">${esc(emoji)}</button>`).join("")}
          </div>
        </div>
        <div class="field">
          <label>Intereses <span class="label-hint">máx. 8</span></label>
          <div class="chip-wrap chip-wrap-form" id="edit-interests">
            ${S.catalog.interests.map((interest) => `<button class="chip chip-toggle ${me.interests.includes(interest) ? "active" : ""}" type="button" data-action="edit-interest" data-value="${esc(interest)}">${esc(interest)}</button>`).join("")}
          </div>
        </div>
      </form>`,
    foot: `<button class="btn btn-primary" type="submit" form="edit-form">Guardar perfil</button>`,
  });
}

function toggleEditInterest(button) {
  if (!S.edit) return;
  const value = button.dataset.value;
  if (S.edit.interests.includes(value)) S.edit.interests = S.edit.interests.filter((item) => item !== value);
  else {
    if (S.edit.interests.length >= 8) return toast("Máximo 8 intereses");
    S.edit.interests.push(value);
  }
  button.classList.toggle("active", S.edit.interests.includes(value));
}

function pickEditAvatar(button) {
  if (!S.edit) return;
  S.edit.avatar = button.dataset.value;
  S.edit.variant = Number(button.dataset.index || 0) % 8;
  $$("#edit-avatars .avatar-pick").forEach((el) => el.classList.toggle("active", el === button));
}

async function submitEditProfile(form) {
  const button = form.querySelector("button[type=submit]");
  const data = new FormData(form);
  const payload = {
    name: data.get("name"),
    age: Number(data.get("age")),
    city: data.get("city"),
    zone: data.get("zone"),
    status_note: data.get("status_note"),
    looking_for: data.get("looking_for"),
    bio: data.get("bio"),
    avatar: S.edit?.avatar,
    variant: S.edit?.variant,
    interests: S.edit?.interests,
  };
  setBusy(button, true, "Guardando…");
  try {
    await api("/profile", { method: "PATCH", body: payload });
    closeAllLayers();
    await loadState();
    renderView();
    toast("Perfil actualizado");
  } catch (error) {
    toast(error.message, "error");
  } finally {
    setBusy(button, false);
  }
}

/* ------------------------------------------------------------- notifications */
function notificationIcon(kind) {
  return { match: "💘", message: "💬", request: "🙋", join: "🎉", accept: "✅", reject: "😔", cancel: "🚫", plan: "✨" }[kind] || "🔔";
}

function showNotifications() {
  const items = S.data.notifications;
  const layer = document.createElement("div");
  layer.className = "notif-layer";
  layer.innerHTML = `
    <div class="notif-panel" role="dialog" aria-modal="true" aria-label="Notificaciones">
      <div class="sheet-grab"></div>
      <div class="notif-head">
        <h2>Notificaciones</h2>
        <button class="sheet-close" type="button" data-action="close-layer" aria-label="Cerrar">${ico("close")}</button>
      </div>
      <div class="notif-list">
        ${items.length ? items.map((item) => `
          <button class="notif ${item.read ? "" : "unread"}" type="button" data-action="open-notification" data-kind="${esc(item.kind)}" data-plan="${item.plan_id || ""}" data-thread="${item.thread_id || ""}">
            <span class="notif-ico ${esc(item.kind)}">${notificationIcon(item.kind)}</span>
            <span class="notif-main"><p>${esc(item.text)}</p><span>${ago(item.created_at)}</span></span>
            ${item.read ? "" : '<span class="unread-dot"></span>'}
          </button>`).join("") : `<div class="empty-state" style="margin:14px"><div class="empty-art">🌙</div><h3>Todo tranquilo</h3><p>Cuando haya matches, mensajes o solicitudes, aparecerán aquí.</p></div>`}
      </div>
    </div>`;
  layer.addEventListener("click", (event) => { if (event.target === layer) closeLayer(layer); });
  openLayer(layer);
  api("/notifications/read", { method: "POST", body: {} }).then(() => {
    S.data.notifications.forEach((item) => { item.read = 1; });
    S.data.unread_notifications = 0;
    updateChrome();
  }).catch(() => {});
}

/* ------------------------------------------------------------- wallet */
function showWallet() {
  const wallet = S.data?.wallet || {
    coins: S.data?.me?.coins || 0,
    daily_available: false,
    daily_amount: DAILY_COINS,
    like_cost: LIKE_COST,
    welcome_amount: WELCOME_COINS,
    transactions: [],
  };
  const dailyAmount = wallet.daily_amount ?? DAILY_COINS;
  const likeCost = wallet.like_cost ?? LIKE_COST;
  const welcomeAmount = wallet.welcome_amount ?? WELCOME_COINS;
  const ledgerIcons = { welcome: "🎁", daily: "🪙", like: "💘", superlike: "⭐" };
  const transactions = wallet.transactions || [];
  openSheet({
    title: "Tus monedas",
    content: `<div class="sheet-body">
      <div class="wallet-hero">
        <span class="wallet-coin">${ico("coin")}</span>
        <div><b>${num(wallet.coins)}</b><span>monedas disponibles</span></div>
      </div>

      <div class="daily-card">
        <span class="daily-ico">${wallet.daily_available ? "🎁" : "✅"}</span>
        <div>
          <strong>Recompensa diaria</strong>
          <span>${wallet.daily_available ? `+${dailyAmount} monedas · Disponible hoy` : "Ya la has reclamado · Vuelve mañana"}</span>
        </div>
        ${wallet.daily_available
          ? `<button class="btn btn-lime btn-sm" type="button" data-action="claim-daily">Reclamar +${dailyAmount}</button>`
          : `<button class="btn btn-soft btn-sm" type="button" disabled>Hecho</button>`}
      </div>

      <div class="wallet-help">
        <div><span class="dotline"></span><span><b>+${welcomeAmount} de bienvenida</b> al entrar por primera vez.</span></div>
        <div><span class="dotline"></span><span><b>+${dailyAmount} cada día</b> desde esta cartera.</span></div>
        <div><span class="dotline"></span><span><b>-${likeCost} por like o superlike.</b> Pasar de perfil es gratis.</span></div>
      </div>

      <div class="section" style="margin-top:4px">
        <div class="section-head"><h3 class="section-title">Movimientos <span class="count">${transactions.length}</span></h3></div>
        <div class="ledger">
          ${transactions.length ? transactions.map((item) => `
            <div class="ledger-row">
              <span class="ledger-ico">${ledgerIcons[item.kind] || "🪙"}</span>
              <span class="ledger-main"><strong>${esc(item.note || "Movimiento")}</strong><span>${ago(item.created_at)} · saldo ${num(item.balance_after)}</span></span>
              <span class="ledger-delta ${item.delta < 0 ? "neg" : ""}">${item.delta > 0 ? "+" : ""}${num(item.delta)}</span>
            </div>`).join("") : `<div class="ledger-empty">Todavía no hay movimientos. Tu primer like estrena la lista.</div>`}
        </div>
      </div>
    </div>`,
    foot: `<button class="btn btn-primary" type="button" data-action="close-layer">Entendido</button>`,
  });
}

async function claimDaily(button) {
  if (!S.data) return;
  setBusy(button, true, "Reclamando…");
  try {
    const result = await api("/economy/daily", { method: "POST", body: {} });
    if (result.wallet) S.data.wallet = result.wallet;
    else {
      S.data.wallet.coins = result.coins;
      S.data.wallet.daily_available = false;
    }
    S.data.me.coins = result.coins;
    updateChrome();
    toast(`+${result.amount} monedas. A seguir con la ronda 🪙`);
    closeAllLayers();
    await loadState();
    showWallet();
  } catch (error) {
    toast(error.message, "error");
    setBusy(button, false);
  }
}

/* ------------------------------------------------------------- info sheet */
function showHowItWorks() {
  openSheet({
    title: "Cómo funciona Ronda",
    content: `<div class="sheet-body">
      <div class="auth-step" style="margin-bottom:16px"><span>01</span><div><strong>Un plan abierto</strong><p style="color:var(--muted);font-size:12.5px;line-height:1.5">Alguien propone un plan, elige ciudad y sitio y dice cuánta gente falta. Puedes apuntarte al instante o pedir plaza si el anfitrión revisa solicitudes.</p></div></div>
      <div class="auth-step" style="margin-bottom:16px"><span>02</span><div><strong>Gente con tu vibe</strong><p style="color:var(--muted);font-size:12.5px;line-height:1.5">En Gente deslizas perfiles. Si a los dos os interesa, hacéis match y se abre un chat privado. Los intereses compartidos suben en el mazo.</p></div></div>
      <div class="auth-step" style="margin-bottom:16px"><span>03</span><div><strong>Chats con contexto</strong><p style="color:var(--muted);font-size:12.5px;line-height:1.5">Cada match tiene su conversación. Cada plan, su chat de grupo con todos los apuntados. Nada se pierde en grupos de WhatsApp.</p></div></div>
      <div class="auth-step" style="margin-bottom:6px"><span>04</span><div><strong>Sal</strong><p style="color:var(--muted);font-size:12.5px;line-height:1.5">El plan se completa, la ronda empieza. Ronda no sustituye a tus amigos: te presenta a los que faltaban.</p></div></div>
      <div class="share-box" style="margin-top:18px">${ico("coin")}<span>Monedas: <b style="color:var(--text)">+${WELCOME_COINS} de bienvenida</b>, <b style="color:var(--text)">+${DAILY_COINS} cada día</b> y <b style="color:var(--text)">-${LIKE_COST} por like</b>. Nunca bajan de cero.</span></div>
      <div class="share-box" style="margin-top:10px">${ico("locate")}<span>Ciudad y GPS: cambia de ciudad cuando quieras o usa tu ubicación. Verás gente, planes y locales a la distancia real.</span></div>
      <div class="share-box" style="margin-top:10px">${ico("shield")}<span>Sin spam: solo recibes avisos de matches, mensajes y planes en los que participas.</span></div>
    </div>`,
    foot: `<button class="btn btn-primary" type="button" data-action="close-layer">Entendido</button>`,
  });
}

/* ------------------------------------------------------------- actions */
async function handleAction(action, element) {
  try {
    switch (action) {
      case "demo-login": {
        const username = element.dataset.username;
        const original = element.innerHTML;
        element.disabled = true;
        element.innerHTML = `<span class="avatar"><span>⏳</span></span><span><strong>Entrando…</strong></span>`;
        try {
          await doLogin(username, "demo1234");
        } catch (error) {
          toast(error.message, "error");
          element.disabled = false;
          element.innerHTML = original;
        }
        break;
      }
      case "reg-interest":
        toggleRegChip(element);
        break;
      case "reg-avatar":
        pickRegAvatar(element);
        break;
      case "plan-detail":
        showPlanDetail(element.dataset.id);
        break;
      case "join-plan":
        await joinPlan(Number(element.dataset.id), element);
        break;
      case "leave-plan":
        leavePlan(Number(element.dataset.id));
        break;
      case "cancel-plan":
        cancelPlan(Number(element.dataset.id));
        break;
      case "resolve-request":
        await resolveRequest(Number(element.dataset.plan), Number(element.dataset.user), element.dataset.verdict);
        break;
      case "refresh-plan":
        S.busy = false;
        await loadState();
        showPlanDetail(element.dataset.id);
        break;
      case "spot-minus":
        updateSpots(-1);
        break;
      case "spot-plus":
        updateSpots(1);
        break;
      case "pick-cat":
        $$("#cat-picker .cat-option").forEach((el) => el.classList.toggle("active", el === element));
        break;
      case "vibe-toggle":
        toggleLimitedChip(element, "#vibe-picker .chip.active", 5);
        break;
      case "edit-interest":
        toggleEditInterest(element);
        break;
      case "edit-avatar":
        pickEditAvatar(element);
        break;
      case "edit-profile":
        showEditProfile();
        break;
      case "filters":
        showFilters();
        break;
      case "location":
        showLocation();
        break;
      case "use-gps":
        await useGps(element);
        break;
      case "ask-gps":
        askGps();
        break;
      case "clear-location":
        await clearExactLocation();
        break;
      case "set-city":
        await setCity(element.dataset.city);
        break;
      case "venues":
        showVenues();
        break;
      case "pick-venue":
        pickVenue(element);
        break;
      case "plan-from-venue": {
        const venue = venueById(element.dataset.id);
        closeAllLayers();
        if (venue) {
          await wait(60);
          showCreatePlan({ venue });
        }
        break;
      }
      case "create-plan":
        showCreatePlan();
        break;
      case "swipe":
        await applySwipe(element.dataset.dir || "like");
        break;
      case "reset-deck":
        await resetDeck();
        break;
      case "open-chat":
        closeLayer(element.closest(".sheet-layer, .notif-layer"));
        await openChat(element.dataset.id);
        break;
      case "close-chat":
        closeChat();
        break;
      case "chat-plan": {
        const planId = element.dataset.id;
        closeChat();
        await wait(80);
        showPlanDetail(planId);
        break;
      }
      case "chat-leave": {
        const planId = Number(element.dataset.plan);
        const plan = findPlan(planId) || S.chat?.data?.plan_full;
        if (!plan) return toast("Ese plan ya no está disponible", "error");
        if (plan.my_status === "host") cancelPlan(planId);
        else leavePlan(planId);
        break;
      }
      case "confirm-pending":
        await runPendingConfirm(element);
        break;
      case "quick-message":
        await sendChatMessage(element.dataset.text);
        break;
      case "match-chat":
        closeAllLayers();
        await openChat(element.dataset.thread);
        break;
      case "notifications":
        showNotifications();
        break;
      case "export-data":
        await downloadMyData();
        break;
      case "wallet":
        showWallet();
        break;
      case "claim-daily":
        await claimDaily(element);
        break;
      case "open-notification": {
        const threadId = element.dataset.thread;
        const planId = element.dataset.plan;
        closeLayer(element.closest(".notif-layer"));
        if (threadId) await openChat(threadId);
        else if (planId) showPlanDetail(planId);
        break;
      }
      case "theme":
        setTheme(element.dataset.themeChoice);
        break;
      case "how-it-works":
        showHowItWorks();
        break;
      case "logout":
        confirmSheet({
          title: "¿Cerrar sesión?",
          message: "Tus planes y chats se quedan guardados. Puedes volver cuando quieras.",
          confirmLabel: "Cerrar sesión",
          danger: true,
          onConfirm: async () => {
            closeAllLayers();
            await logout();
          },
        });
        break;
      case "close-layer":
        closeLayer(element.closest(".sheet-layer, .notif-layer, .match-layer"));
        break;
      default:
        break;
    }
  } catch (error) {
    toast(error.message || "No se pudo completar la acción", "error");
  }
}

async function joinPlan(planId, button) {
  setBusy(button, true, "Enviando…");
  try {
    const result = await api(`/plans/${planId}/join`, { method: "POST", body: {} });
    closeAllLayers();
    if (result.pending) {
      toast("Solicitud enviada. El anfitrión decide ✨");
    } else {
      toast("¡Estás dentro! Ya podéis organizarlo 🎉");
    }
    S.busy = false;
    await loadState();
    if (S.tab === "plans") renderView();
    if (result.joined && result.thread_id) {
      await wait(450);
      openChat(result.thread_id);
    }
  } catch (error) {
    toast(error.message, "error");
  } finally {
    setBusy(button, false);
  }
}

function leavePlan(planId) {
  confirmSheet({
    title: "¿Salir del plan?",
    message: "Tu plaza se libera y el grupo verá que has salido. Puedes volver si todavía hay sitio.",
    confirmLabel: "Salir",
    danger: true,
    onConfirm: async () => {
      await api(`/plans/${planId}/leave`, { method: "POST", body: {} });
      closeAllLayers();
      await loadState();
      toast("Has salido del plan");
    },
  });
}

function cancelPlan(planId) {
  confirmSheet({
    title: "¿Cancelar el plan?",
    message: "Todo el grupo recibirá un aviso. Esta acción no se puede deshacer.",
    confirmLabel: "Cancelar plan",
    danger: true,
    onConfirm: async () => {
      await api(`/plans/${planId}/cancel`, { method: "POST", body: {} });
      closeAllLayers();
      await loadState();
      if (S.tab !== "plans") setTab("plans");
      else renderView();
      toast("Plan cancelado");
    },
  });
}

async function resolveRequest(planId, userId, verdict) {
  try {
    await api(`/plans/${planId}/members/${userId}/resolve`, { method: "POST", body: { action: verdict } });
    closeAllLayers();
    await loadState();
    toast(verdict === "accept" ? "Solicitud aceptada. Ya está en el chat 🎉" : "Solicitud rechazada");
    showPlanDetail(planId);
  } catch (error) {
    toast(error.message, "error");
  }
}

async function resetDeck() {
  try {
    await api("/swipes/reset", { method: "POST", body: {} });
    closeAllLayers();
    await loadState();
    if (S.tab === "discover") renderView();
    toast("Mazos reiniciados. A ver si hay suerte 🍀");
  } catch (error) {
    toast(error.message, "error");
  }
}

function updateSpots(delta) {
  const valueEl = $("#spots-value");
  const input = $("#plan-spots");
  if (!valueEl || !input) return;
  const next = Math.min(8, Math.max(1, Number(valueEl.textContent) + delta));
  valueEl.textContent = String(next);
  input.value = String(next);
  const suffix = $("#spots-suffix");
  if (suffix) suffix.textContent = next === 1 ? "falta 1 persona" : `faltan ${next} personas`;
}

function toggleLimitedChip(button, activeSelector, limit) {
  if (button.classList.contains("active")) {
    button.classList.remove("active");
    return;
  }
  if ($$(activeSelector).length >= limit) return toast(`Elige hasta ${limit}`);
  button.classList.add("active");
}

/* ------------------------------------------------------------- events */
function bindEvents() {
  document.addEventListener("click", (event) => {
    const authTab = event.target.closest("[data-auth-tab]");
    if (authTab) return setAuthTab(authTab.dataset.authTab);

    const tab = event.target.closest("[data-tab]");
    if (tab) {
      event.preventDefault();
      return setTab(tab.dataset.tab);
    }

    const filterCat = event.target.closest("[data-filter-cat]");
    if (filterCat) {
      S.filters.cat = filterCat.dataset.filterCat;
      renderView({ preserveScroll: true });
      return;
    }
    const filterWhen = event.target.closest("[data-filter-when]");
    if (filterWhen) {
      S.filters.when = filterWhen.dataset.filterWhen;
      renderView({ preserveScroll: true });
      return;
    }

    const actionEl = event.target.closest("[data-action]");
    if (actionEl) {
      event.preventDefault();
      handleAction(actionEl.dataset.action, actionEl);
      return;
    }

    const theme = event.target.closest("[data-theme-choice]");
    if (theme) setTheme(theme.dataset.themeChoice);
  });

  document.addEventListener("submit", (event) => {
    const form = event.target;
    if (!(form instanceof HTMLFormElement)) return;
    if (form.id === "login-form") {
      event.preventDefault();
      submitLogin(form);
    } else if (form.id === "register-form") {
      event.preventDefault();
      submitRegister(form);
    } else if (form.id === "create-form") {
      event.preventDefault();
      submitCreatePlan(form);
    } else if (form.id === "filters-form") {
      event.preventDefault();
      submitFilters(form);
    } else if (form.id === "edit-form") {
      event.preventDefault();
      submitEditProfile(form);
    } else if (form.id === "chat-form") {
      event.preventDefault();
      sendChatMessage();
    }
  });

  document.addEventListener("change", (event) => {
    const target = event.target;
    if (target.id === "plan-city") {
      updateVenueSuggestions(target.value);
    }
  });

  document.addEventListener("input", (event) => {
    const target = event.target;
    if (target.id === "city-search") {
      const list = $("#city-list");
      if (list) list.innerHTML = cityListHTML(target.value);
    }
    if (target.id === "plan-venue") {
      const selected = venueById(S.planVenueId);
      if (!selected || selected.name !== target.value.trim()) {
        S.planVenueId = null;
        const hidden = $("#plan-venue-id");
        if (hidden) hidden.value = "";
        $$("#venue-suggestions .venue-suggestion").forEach((el) => el.classList.remove("active"));
      }
    }
    if (target.id === "filter-distance") {
      const label = $("#distance-label");
      if (label) label.textContent = km(Number(target.value));
      target.style.setProperty("--pct", `${(Number(target.value) / 40) * 100}%`);
    }
    if (target.id === "chat-input") {
      target.style.height = "auto";
      target.style.height = `${Math.min(120, target.scrollHeight)}px`;
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      const layers = $$("#layers > *");
      if (layers.length) {
        event.preventDefault();
        closeTopLayer();
      }
    }
    if (event.key === "Enter" && !event.shiftKey && event.target.id === "chat-input") {
      event.preventDefault();
      sendChatMessage();
    }
  });

  window.addEventListener("beforeunload", () => S.source?.close());
}

/* ------------------------------------------------------------- boot */
async function boot() {
  setTheme(S.theme);
  bindEvents();
  renderAuthCatalog();
  const params = new URLSearchParams(location.search);
  const testMode = params.get("nosw") === "1";
  if (params.get("theme") && THEMES.some((theme) => theme.key === params.get("theme"))) {
    setTheme(params.get("theme"));
  }

  if (params.get("demo")) {
    try {
      const data = await api("/auth/login", {
        method: "POST",
        body: { username: params.get("demo"), password: "demo1234" },
      });
      S.token = data.token;
      localStorage.setItem("ronda.token", data.token);
    } catch {
      S.token = null;
      localStorage.removeItem("ronda.token");
    }
  }

  try {
    const [demo, catalog] = await Promise.allSettled([api("/demo-accounts"), api("/catalog")]);
    if (catalog.status === "fulfilled") S.catalog = { ...FALLBACK_CATALOG, ...catalog.value };
    if (demo.status === "rejected") {
      // api() is fine, demo fallback is rendered by renderAuthCatalog
    }
    $$("#reg-interests, #reg-avatars").forEach((el) => { el.dataset.ready = ""; });
    const regCity = $("#reg-city");
    if (regCity) regCity.innerHTML = "";
    renderAuthCatalog();
  } catch { /* offline */ }

  if (S.token) {
    try {
      S.suppressChat = true;
      await loadState();
      S.suppressChat = false;
      showApp();
      renderView();
      if (!testMode) connectEvents();
      const tab = params.get("tab");
      if (["plans", "discover", "chats", "profile"].includes(tab)) setTab(tab);
      if (params.get("action") === "create") setTimeout(() => showCreatePlan(), 250);
    } catch (error) {
      S.suppressChat = false;
      S.token = null;
      localStorage.removeItem("ronda.token");
      showAuth();
    }
  } else {
    showAuth();
  }

  if ("serviceWorker" in navigator && !testMode) {
    navigator.serviceWorker.register("/sw.js").catch(() => {});
  }
}

boot();
