"""Domain helpers and demo data for Ronda."""
from __future__ import annotations

import hashlib
import json
import math
import secrets
from datetime import date, datetime, time, timedelta

from db import connect

FMT = "%Y-%m-%dT%H:%M"
DATE_FMT = "%Y-%m-%d"

ZONES = {
    "Malasaña": (40.4260, -3.7038),
    "Chueca": (40.4230, -3.6970),
    "Lavapiés": (40.4108, -3.7030),
    "La Latina": (40.4115, -3.7100),
    "Chamberí": (40.4350, -3.7040),
    "Salamanca": (40.4300, -3.6820),
    "Argüelles": (40.4270, -3.7170),
    "Delicias": (40.4050, -3.6930),
    "Tribunal": (40.4264, -3.7010),
    "Retiro": (40.4150, -3.6830),
    "Moncloa": (40.4350, -3.7190),
    "Sol": (40.4168, -3.7038),
}

EXTRA_AREAS = {
    "El Born": (41.3850, 2.1830),
    "Eixample": (41.3900, 2.1650),
    "El Cabanyal": (39.4700, -0.3300),
    "Indautxu": (43.2600, -2.9450),
    "Gros": (43.3220, -1.9780),
    "Born": (39.5710, 2.6490),
}

# All Spanish provincial capitals plus the main metropolitan and coastal cities.
CITY_DATA = [
    ("Madrid", "Madrid", 40.4168, -3.7038),
    ("Barcelona", "Barcelona", 41.3874, 2.1686),
    ("Valencia", "Valencia", 39.4699, -0.3763),
    ("Sevilla", "Sevilla", 37.3891, -5.9845),
    ("Zaragoza", "Zaragoza", 41.6488, -0.8891),
    ("Málaga", "Málaga", 36.7213, -4.4214),
    ("Murcia", "Murcia", 37.9922, -1.1307),
    ("Palma", "Illes Balears", 39.5696, 2.6502),
    ("Las Palmas de Gran Canaria", "Las Palmas", 28.1235, -15.4363),
    ("Bilbao", "Bizkaia", 43.2630, -2.9350),
    ("Alicante", "Alicante", 38.3452, -0.4815),
    ("Córdoba", "Córdoba", 37.8882, -4.7794),
    ("Valladolid", "Valladolid", 41.6523, -4.7245),
    ("Vigo", "Pontevedra", 42.2406, -8.7207),
    ("Gijón", "Asturias", 43.5322, -5.6611),
    ("A Coruña", "A Coruña", 43.3623, -8.4115),
    ("Vitoria-Gasteiz", "Álava", 42.8467, -2.6716),
    ("Granada", "Granada", 37.1773, -3.5986),
    ("Elche", "Alicante", 38.2699, -0.7011),
    ("Oviedo", "Asturias", 43.3614, -5.8593),
    ("Santa Cruz de Tenerife", "Santa Cruz de Tenerife", 28.4636, -16.2518),
    ("Badalona", "Barcelona", 41.4500, 2.2470),
    ("Cartagena", "Murcia", 37.6257, -0.9966),
    ("Terrassa", "Barcelona", 41.5632, 2.0099),
    ("Jerez de la Frontera", "Cádiz", 36.6850, -6.1261),
    ("Sabadell", "Barcelona", 41.5463, 2.1086),
    ("Móstoles", "Madrid", 40.3223, -3.8649),
    ("Alcalá de Henares", "Madrid", 40.4818, -3.3643),
    ("Pamplona", "Navarra", 42.8125, -1.6458),
    ("Fuenlabrada", "Madrid", 40.2842, -3.7942),
    ("Almería", "Almería", 36.8340, -2.4637),
    ("Leganés", "Madrid", 40.3272, -3.7635),
    ("San Sebastián", "Gipuzkoa", 43.3183, -1.9812),
    ("Burgos", "Burgos", 42.3439, -3.6969),
    ("Santander", "Cantabria", 43.4623, -3.8100),
    ("Castellón de la Plana", "Castellón", 39.9864, -0.0515),
    ("Albacete", "Albacete", 38.9943, -1.8585),
    ("Getafe", "Madrid", 40.3083, -3.7325),
    ("Salamanca", "Salamanca", 40.9701, -5.6635),
    ("Logroño", "La Rioja", 42.4627, -2.4449),
    ("Huelva", "Huelva", 37.2614, -6.9447),
    ("Badajoz", "Badajoz", 38.8786, -6.9703),
    ("Tarragona", "Tarragona", 41.1189, 1.2445),
    ("Lleida", "Lleida", 41.6176, 0.6200),
    ("Marbella", "Málaga", 36.5101, -4.8824),
    ("León", "León", 42.5987, -5.5671),
    ("Cádiz", "Cádiz", 36.5271, -6.2886),
    ("Jaén", "Jaén", 37.7796, -3.7849),
    ("Ourense", "Ourense", 42.3358, -7.8639),
    ("Lugo", "Lugo", 43.0097, -7.5567),
    ("Girona", "Girona", 41.9794, 2.8214),
    ("Cáceres", "Cáceres", 39.4753, -6.3724),
    ("Toledo", "Toledo", 39.8628, -4.0273),
    ("Guadalajara", "Guadalajara", 40.6320, -3.1667),
    ("Ciudad Real", "Ciudad Real", 38.9863, -3.9291),
    ("Cuenca", "Cuenca", 40.0704, -2.1374),
    ("Palencia", "Palencia", 42.0096, -4.5288),
    ("Zamora", "Zamora", 41.5035, -5.7440),
    ("Ávila", "Ávila", 40.6566, -4.6813),
    ("Segovia", "Segovia", 40.9429, -4.1088),
    ("Soria", "Soria", 41.7666, -2.4790),
    ("Teruel", "Teruel", 40.3457, -1.1065),
    ("Huesca", "Huesca", 42.1361, -0.4087),
    ("Ceuta", "Ceuta", 35.8894, -5.3213),
    ("Melilla", "Melilla", 35.2923, -2.9381),
    ("Santiago de Compostela", "A Coruña", 42.8782, -8.5448),
    ("Pontevedra", "Pontevedra", 42.4310, -8.6444),
    ("Ferrol", "A Coruña", 43.4896, -8.2198),
    ("Ibiza", "Illes Balears", 38.9067, 1.4206),
    ("Sitges", "Barcelona", 41.2370, 1.8050),
    ("Benidorm", "Alicante", 38.5411, -0.1225),
    ("Torrevieja", "Alicante", 37.9787, -0.6822),
    ("Estepona", "Málaga", 36.4260, -5.1460),
    ("Fuengirola", "Málaga", 36.5398, -4.6247),
    ("Ronda", "Málaga", 36.7423, -5.1669),
    ("Aranjuez", "Madrid", 40.0310, -3.6025),
    ("Ponferrada", "León", 42.5462, -6.5962),
    ("Sanlúcar de Barrameda", "Cádiz", 36.7784, -6.3539),
    ("Algeciras", "Cádiz", 36.1408, -5.4562),
    ("Motril", "Granada", 36.7450, -3.5170),
    ("Linares", "Jaén", 38.0930, -3.6350),
    ("Mérida", "Badajoz", 38.9160, -6.3430),
    ("Plasencia", "Cáceres", 40.0312, -6.0885),
    ("Talavera de la Reina", "Toledo", 39.9635, -4.8305),
    ("Antequera", "Málaga", 37.0194, -4.5610),
    ("Denia", "Alicante", 38.8408, 0.1057),
    ("Gandía", "Valencia", 38.9676, -0.1816),
    ("Sagunto", "Valencia", 39.6763, -0.2740),
    ("Alzira", "Valencia", 39.1500, -0.4333),
    ("Vilanova i la Geltrú", "Barcelona", 41.2243, 1.7256),
    ("Mataró", "Barcelona", 41.5380, 2.4450),
    ("Reus", "Tarragona", 41.1560, 1.1060),
    ("Figueres", "Girona", 42.2667, 2.9667),
    ("Blanes", "Girona", 41.6740, 2.7900),
    ("Lloret de Mar", "Girona", 41.6990, 2.8450),
    ("Calpe", "Alicante", 38.6440, 0.0440),
    ("Jávea", "Alicante", 38.7890, 0.1630),
    ("Mahón", "Illes Balears", 39.8885, 4.2658),
    ("Manresa", "Barcelona", 41.7280, 1.8230),
    ("Vic", "Barcelona", 41.9300, 2.2540),
    ("Olot", "Girona", 42.1820, 2.4890),
    ("Jaca", "Huesca", 42.5690, -0.5490),
    ("Calatayud", "Zaragoza", 41.3530, -1.6430),
    ("Tudela", "Navarra", 42.0640, -1.6060),
    ("Haro", "La Rioja", 42.5760, -2.8470),
    ("Aranda de Duero", "Burgos", 41.6700, -3.6890),
    ("Miranda de Ebro", "Burgos", 42.6860, -2.9460),
]

CITIES = {
    name: {"name": name, "province": province, "lat": lat, "lon": lon}
    for name, province, lat, lon in CITY_DATA
}

# name, city, area, category, lat, lon, blurb
VENUE_DATA = [
    ("La Riviera", "Madrid", "Delicias", "concierto", 40.4054, -3.6950, "Sala mítica junto al Manzanares para conciertos y noches largas."),
    ("Plaza del Dos de Mayo", "Madrid", "Malasaña", "cañas", 40.4268, -3.7050, "Terrazas, gente del barrio y la mejor previa de Malasaña."),
    ("Calle Cava Baja", "Madrid", "La Latina", "comida", 40.4120, -3.7095, "La ruta de tapas clásica: de bar en bar sin reserva."),
    ("Sala Equis", "Madrid", "Chueca", "cine", 40.4143, -3.7043, "Cine, terraza y planes que se alargan hasta la noche."),
    ("Mercado de la Paz", "Madrid", "Salamanca", "comida", 40.4315, -3.6835, "Brunch, puestos gourmet y domingos sin prisa."),
    ("Independance Club", "Madrid", "Malasaña", "baile", 40.4265, -3.7019, "Sala de conciertos y fiesta para bailar sin vergüenza."),
    ("Madrid Río · Matadero", "Madrid", "Delicias", "aire", 40.4040, -3.6970, "Paseos, bici y terrazas al lado del río."),
    ("Club Pádel Delicias", "Madrid", "Delicias", "deporte", 40.4000, -3.6900, "Pistas para partidos de nivel cero y risas garantizadas."),
    ("El Retiro", "Madrid", "Retiro", "aire", 40.4153, -3.6844, "El pulmón de Madrid: running, bici y tardes de manta."),
    ("Sala Canal de Isabel II", "Madrid", "Chamberí", "cultura", 40.4320, -3.6990, "Expos de fotografía y planes tranquilos de tarde."),
    ("Café Central", "Madrid", "Sol", "cultura", 40.4160, -3.7040, "Jazz en directo y cenas que empiezan tarde."),
    ("Teatro Barceló", "Madrid", "Tribunal", "concierto", 40.4275, -3.6990, "Conciertos, club y una de las pistas más conocidas de Madrid."),
    ("Razzmatazz", "Barcelona", "Poblenou", "concierto", 41.3975, 2.1910, "Cinco salas y noches que no terminan nunca."),
    ("Barceloneta", "Barcelona", "Barceloneta", "aire", 41.3784, 2.1925, "Playa, paseo y una cerveza mirando al mar."),
    ("Mercat de la Boqueria", "Barcelona", "El Raval", "comida", 41.3817, 2.1716, "Colores, tapas y un paseo por Las Ramblas después."),
    ("Sala Apolo", "Barcelona", "El Raval", "baile", 41.3744, 2.1689, "Sala histórica para conciertos y sesiones de madrugada."),
    ("Park Güell", "Barcelona", "Gràcia", "cultura", 41.4145, 2.1526, "Gaudí, vistas y un plan de día con paseo largo."),
    ("Cervecería Catalana", "Barcelona", "Eixample", "cañas", 41.3895, 2.1590, "Tapas de siempre y barra llena a cualquier hora."),
    ("Mercado Central", "Valencia", "Ciutat Vella", "comida", 39.4736, -0.3790, "Arquitectura modernista, producto y almuerzos largos."),
    ("Ruzafa", "Valencia", "Ruzafa", "cañas", 39.4610, -0.3730, "Terrazas, coctelerías y ambiente hasta tarde."),
    ("Ciudad de las Artes", "Valencia", "Quatre Carreres", "cultura", 39.4546, -0.3505, "Paseo, fotos y planes de tarde junto al Turia."),
    ("La Malvarrosa", "Valencia", "Malvarrosa", "aire", 39.4790, -0.3230, "Playa urbana para caminar, correr o tomar algo."),
    ("Sala Wah Wah", "Valencia", "Ruzafa", "concierto", 39.4632, -0.3760, "Conciertos indie y noches de barrio."),
    ("Bioparc", "Valencia", "Campanar", "aire", 39.4780, -0.4070, "Plan de día diferente, con paseo y naturaleza."),
    ("Triana", "Sevilla", "Triana", "cañas", 37.3830, -6.0030, "Cruzando el puente: cerámica, bares y río."),
    ("Plaza de España", "Sevilla", "Sur", "cultura", 37.3772, -5.9864, "El plan más fotogénico de Sevilla."),
    ("Alameda de Hércules", "Sevilla", "Alameda", "baile", 37.3977, -5.9955, "Terrazas y fiesta al aire libre hasta que aguante el cuerpo."),
    ("Mercado de Triana", "Sevilla", "Triana", "comida", 37.3860, -6.0070, "Tapas, flamenco y ambiente de mercado."),
    ("La Carbonería", "Sevilla", "Centro", "concierto", 37.3910, -5.9880, "Patio con música en directo y gente nueva cada noche."),
    ("Casco Viejo", "Bilbao", "Casco Viejo", "cañas", 43.2570, -2.9230, "Siete calles, pintxos y la mejor previa de Bilbao."),
    ("Guggenheim", "Bilbao", "Abando", "cultura", 43.2687, -2.9340, "Arte, arquitectura y paseo por la ría."),
    ("Azkuna Zentroa", "Bilbao", "Abando", "cultura", 43.2630, -2.9290, "Antigua alhóndiga con expos, cine y piscina."),
    ("Artxanda", "Bilbao", "Artxanda", "aire", 43.2720, -2.9430, "Funicular, vistas y merienda con calma."),
    ("Kafe Antzokia", "Bilbao", "Abando", "concierto", 43.2590, -2.9260, "Música en euskera, conciertos y noches de baile."),
    ("Plaza de la Merced", "Málaga", "Centro", "cañas", 36.7220, -4.4180, "Terrazas, historia y ambiente a cualquier hora."),
    ("Muelle Uno", "Málaga", "Centro", "aire", 36.7150, -4.4120, "Paseo marítimo, tiendas y helado al sol."),
    ("Alcazaba", "Málaga", "Centro", "cultura", 36.7210, -4.4150, "Murallas, vistas y una tarde de fotos."),
    ("La Malagueta", "Málaga", "La Malagueta", "aire", 36.7170, -4.4100, "Playa urbana y chiringuitos para el after."),
    ("Sala Paris 15", "Málaga", "Centro", "concierto", 36.7140, -4.4260, "Conciertos y fiesta en el centro de Málaga."),
    ("El Tubo", "Zaragoza", "Centro", "cañas", 41.6500, -0.8800, "La ruta de tapas más famosa de Zaragoza."),
    ("Basílica del Pilar", "Zaragoza", "Centro", "cultura", 41.6566, -0.8785, "Paseo por el Ebro y vistas desde el Puente de Piedra."),
    ("Parque Grande", "Zaragoza", "Romareda", "aire", 41.6370, -0.8870, "Running, bici y tardes de paseo."),
    ("La Casa del Loco", "Zaragoza", "Centro", "concierto", 41.6530, -0.8840, "Sala de conciertos con programación indie."),
    ("Albaicín", "Granada", "Albaicín", "cultura", 37.1800, -3.5940, "Calles blancas, teterías y vistas a la Alhambra."),
    ("Plaza Nueva", "Granada", "Centro", "cañas", 37.1770, -3.5940, "Tapas gratis con la bebida y ambiente universitario."),
    ("Mirador de San Nicolás", "Granada", "Albaicín", "aire", 37.1805, -3.5925, "El atardecer más famoso de Granada."),
    ("Sala El Tren", "Granada", "Centro", "baile", 37.1700, -3.6070, "Conciertos y fiesta hasta el cierre."),
    ("Plaza de María Pita", "A Coruña", "Centro", "cañas", 43.3710, -8.3960, "Terrazas, historia y ambiente atlántico."),
    ("Torre de Hércules", "A Coruña", "Torre", "cultura", 43.3860, -8.4060, "Paseo marítimo y el faro romano más famoso."),
    ("Riazor", "A Coruña", "Riazor", "aire", 43.3680, -8.4180, "Playa urbana para correr o pasear al atardecer."),
    ("Parte Vieja", "San Sebastián", "Parte Vieja", "comida", 43.3230, -1.9850, "Pintxos, txakoli y bares llenos de gente."),
    ("La Concha", "San Sebastián", "Centro", "aire", 43.3190, -1.9850, "La bahía más bonita para un paseo sin prisa."),
    ("Monte Igueldo", "San Sebastián", "Igueldo", "aire", 43.3210, -2.0100, "Funicular y vistas de toda la ciudad."),
    ("Kursaal", "San Sebastián", "Gros", "cultura", 43.3210, -1.9760, "Cine, congresos y conciertos frente al mar."),
    ("Santa Catalina", "Palma", "Santa Catalina", "cañas", 39.5720, 2.6370, "Mercado, tapas y terrazas con mucho ambiente."),
    ("Catedral de Mallorca", "Palma", "Centro", "cultura", 39.5670, 2.6480, "La Seu, paseo marítimo y casco antiguo."),
    ("Passeig del Born", "Palma", "Centro", "cañas", 39.5710, 2.6470, "Copas, tiendas y noches de Palma."),
    ("Cala Major", "Palma", "Cala Major", "aire", 39.5560, 2.6030, "Playa cercana para un plan de día."),
    ("Mezquita-Catedral", "Córdoba", "Centro", "cultura", 37.8790, -4.7790, "El monumento que hay que ver al menos una vez."),
    ("Judería", "Córdoba", "Judería", "cañas", 37.8780, -4.7830, "Calles estrechas, patios y tapas."),
    ("Puente Romano", "Córdoba", "Centro", "aire", 37.8770, -4.7780, "Paseo junto al Guadalquivir al atardecer."),
    ("Sala Impala", "Córdoba", "Centro", "concierto", 37.8840, -4.7890, "Conciertos y fiesta en el centro."),
    ("Castillo de Santa Bárbara", "Alicante", "Centro", "cultura", 38.3490, -0.4780, "Vistas al mar y paseo por la Explanada."),
    ("Playa del Postiguet", "Alicante", "Centro", "aire", 38.3440, -0.4770, "Playa urbana para después del trabajo."),
    ("El Barrio", "Alicante", "Centro", "cañas", 38.3450, -0.4860, "Tapas, terrazas y ambiente joven."),
    ("Plaza de las Flores", "Murcia", "Centro", "cañas", 37.9860, -1.1300, "Terrazas y tapas bajo los naranjos."),
    ("Catedral de Murcia", "Murcia", "Centro", "cultura", 37.9840, -1.1280, "Casco histórico y paseo por la ciudad."),
    ("Plaza Mayor", "Valladolid", "Centro", "cañas", 41.6520, -4.7280, "El corazón de Valladolid, lleno de terrazas."),
    ("Campo Grande", "Valladolid", "Centro", "aire", 41.6450, -4.7350, "Paseo, running y tardes de árboles."),
    ("Casco Vello", "Vigo", "Casco Vello", "cañas", 42.2390, -8.7260, "Calles de piedra, ostras y vino albariño."),
    ("Monte do Castro", "Vigo", "Castro", "aire", 42.2320, -8.7280, "Vistas a la ría y paseo al atardecer."),
    ("Cimadevilla", "Gijón", "Cimadevilla", "cañas", 43.5450, -5.6630, "El barrio marinero con más ambiente."),
    ("Playa de San Lorenzo", "Gijón", "Centro", "aire", 43.5400, -5.6550, "Paseo marítimo y surf."),
    ("Plaza Mayor", "Salamanca", "Centro", "cañas", 40.9650, -5.6640, "La plaza más bonita para empezar la noche."),
    ("Huerto de Calixto y Melibea", "Salamanca", "Centro", "cultura", 40.9610, -5.6660, "Jardín escondido y vistas a la catedral."),
    ("Plaza de Zocodover", "Toledo", "Centro", "cañas", 39.8590, -4.0210, "Punto de partida para perderse por el casco."),
    ("Mirador del Valle", "Toledo", "Valle", "aire", 39.8580, -4.0360, "La vista clásica de Toledo al atardecer."),
    ("La Caleta", "Cádiz", "La Caleta", "aire", 36.5290, -6.3000, "Playa urbana y paseo por el barrio de La Viña."),
    ("Plaza de la Catedral", "Cádiz", "Centro", "cañas", 36.5290, -6.2930, "Tapas, catedral y brisa atlántica."),
    ("Plaza del Castillo", "Pamplona", "Centro", "cañas", 42.8150, -1.6430, "El centro de la vida social pamplonica."),
    ("Ciudadela", "Pamplona", "Centro", "aire", 42.8100, -1.6490, "Murallas, paseo y planes al aire libre."),
    ("Plaza del Obradoiro", "Santiago de Compostela", "Centro", "cultura", 42.8805, -8.5457, "La meta de todos los caminos."),
    ("Parque de la Alameda", "Santiago de Compostela", "Centro", "aire", 42.8780, -8.5480, "Paseo con vistas a la catedral."),
    ("Dalt Vila", "Ibiza", "Dalt Vila", "cultura", 38.9080, 1.4320, "Murallas, calles blancas y vistas al puerto."),
    ("Playa de Talamanca", "Ibiza", "Talamanca", "aire", 38.9200, 1.4420, "Playa tranquila y chiringuitos."),
]



CATEGORIES = [
    {"key": "cañas", "label": "Cañas", "emoji": "🍻"},
    {"key": "concierto", "label": "Concierto", "emoji": "🎸"},
    {"key": "comida", "label": "Comida", "emoji": "🍜"},
    {"key": "cine", "label": "Cine", "emoji": "🎬"},
    {"key": "deporte", "label": "Deporte", "emoji": "⚡"},
    {"key": "baile", "label": "Baile", "emoji": "💃"},
    {"key": "cultura", "label": "Cultura", "emoji": "🎨"},
    {"key": "aire", "label": "Aire libre", "emoji": "🌿"},
    {"key": "planes", "label": "Otros", "emoji": "✨"},
]
CATEGORY_MAP = {c["key"]: c for c in CATEGORIES}

VENUES = [
    {
        "name": name, "city": city, "area": area, "category": category,
        "emoji": CATEGORY_MAP.get(category, CATEGORY_MAP["planes"])["emoji"],
        "lat": lat, "lon": lon, "blurb": blurb,
    }
    for name, city, area, category, lat, lon, blurb in VENUE_DATA
]

INTERESTS = [
    "Conciertos", "Música indie", "Terrazas", "Fotografía", "Brunch",
    "Cine", "Baile", "Gastronomía", "Viajes", "Bici", "Café", "Senderismo",
    "Running", "Arte", "Museos", "Cañas", "Tapas", "Fútbol", "Fiesta",
    "Cócteles", "Yoga", "Cerámica", "Pádel", "Gaming", "Rock", "Series",
    "Vinilos", "Moda", "Lectura", "Jazz", "Karaoke", "Ramen", "Skate",
    "Festivales", "Electrónica", "Teatro", "Playa", "Piscina", "Mercadillos",
    "Idiomas",
]

AVATARS = ["🦋", "🎸", "🍒", "🚲", "🌸", "🍻", "🪩", "🏓", "🏃", "🎨", "🍷", "🛹", "🎧", "🍜"]

WELCOME_COINS = 100
DAILY_COINS = 10
LIKE_COST = 10

DEMO_USERS = ["lucia", "hugo", "vera", "nico"]


# ------------------------------------------------------------------ time
def now() -> datetime:
    return datetime.now().replace(second=0, microsecond=0)


def now_str() -> str:
    return now().strftime(FMT)


def parse_dt(value):
    if not value:
        return None
    if isinstance(value, datetime):
        return value.replace(second=0, microsecond=0)
    if isinstance(value, date):
        return datetime.combine(value, time())
    for pattern in (FMT, "%Y-%m-%dT%H:%M:%S", DATE_FMT):
        try:
            return datetime.strptime(value.strip(), pattern)
        except (ValueError, AttributeError):
            continue
    return None


def fmt(dt: datetime) -> str:
    return dt.strftime(FMT)


def ago(minutes: int) -> str:
    return fmt(now() - timedelta(minutes=minutes))


def in_days(days: int, hour: int, minute: int = 0) -> str:
    stamp = (now() + timedelta(days=days)).replace(hour=hour, minute=minute, second=0, microsecond=0)
    if stamp < now():
        stamp += timedelta(days=1)
    return fmt(stamp)


# ------------------------------------------------------------------ auth
def hash_password(password: str, salt: str | None = None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 160_000)
    return digest.hex(), salt


def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    candidate, _ = hash_password(password, salt)
    return secrets.compare_digest(candidate, stored_hash)


def create_session(conn, user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    conn.execute(
        "INSERT INTO sessions(token, user_id, created_at) VALUES (?,?,?)",
        (token, user_id, now_str()),
    )
    return token


def user_by_token(conn, token: str | None):
    if not token:
        return None
    return conn.execute(
        "SELECT u.* FROM sessions s JOIN users u ON u.id = s.user_id WHERE s.token = ? LIMIT 1",
        (token,),
    ).fetchone()


def initials(name: str) -> str:
    parts = [p for p in name.replace(".", " ").split() if p]
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[1][0]).upper()


# ------------------------------------------------------------------ geography
def city_coords(city: str | None):
    item = CITIES.get(city or "") or CITIES["Madrid"]
    return item["lat"], item["lon"]


def haversine(lat1, lon1, lat2, lon2) -> float:
    lat1, lon1, lat2, lon2 = map(math.radians, (lat1, lon1, lat2, lon2))
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return round(2 * 6371 * math.asin(math.sqrt(h)), 1)


def _coords_of(value):
    """Coordinates from a user/plan row, city name, or (lat, lon) pair."""
    if value is None:
        return city_coords("Madrid")
    if isinstance(value, (tuple, list)):
        return float(value[0]), float(value[1])
    if hasattr(value, "keys"):
        keys = value.keys()
        lat = value["lat"] if "lat" in keys else None
        lon = value["lon"] if "lon" in keys else None
        if lat is not None and lon is not None:
            return float(lat), float(lon)
        city = value["city"] if "city" in keys else "Madrid"
        return city_coords(city)
    if isinstance(value, str):
        if value in ZONES:
            return ZONES[value]
        return city_coords(value)
    return city_coords("Madrid")


def distance_km(a, b) -> float:
    lat1, lon1 = _coords_of(a)
    lat2, lon2 = _coords_of(b)
    return haversine(lat1, lon1, lat2, lon2)


# ------------------------------------------------------------------ users
def load_json(value, fallback=None):
    try:
        data = json.loads(value or "")
    except (TypeError, ValueError):
        return fallback if fallback is not None else []
    return data


def public_user(row, me=None) -> dict:
    if row is None:
        return None
    interests = load_json(row["interests"])
    last_seen = parse_dt(row["last_seen"])
    online = bool(last_seen and (now() - last_seen).total_seconds() < 12 * 60)
    data = {
        "id": row["id"],
        "name": row["name"],
        "username": row["username"],
        "age": row["age"],
        "city": row["city"] if "city" in row.keys() else "Madrid",
        "zone": row["zone"],
        "bio": row["bio"],
        "avatar": row["avatar"],
        "variant": row["variant"] % 8,
        "interests": interests,
        "looking_for": row["looking_for"],
        "status_note": row["status_note"],
        "initials": initials(row["name"]),
        "online": online,
        "last_seen": row["last_seen"],
    }
    if me is not None:
        data["distance_km"] = 0.0 if row["id"] == me["id"] else distance_km(me, row)
        shared = [i for i in interests if i in load_json(me["interests"])]
        data["shared_interests"] = shared
    return data


def other_user(conn, thread_id: int, me_id: int):
    return conn.execute(
        """SELECT u.* FROM thread_members tm JOIN users u ON u.id = tm.user_id
           WHERE tm.thread_id = ? AND tm.user_id != ? LIMIT 1""",
        (thread_id, me_id),
    ).fetchone()


# ------------------------------------------------------------------ threads
def add_message(conn, thread_id: int, user_id, body: str, kind: str = "text", at: str | None = None) -> int:
    at = at or now_str()
    cur = conn.execute(
        "INSERT INTO messages(thread_id, user_id, body, kind, created_at) VALUES (?,?,?,?,?)",
        (thread_id, user_id, body, kind, at),
    )
    conn.execute("UPDATE threads SET last_at = ? WHERE id = ?", (at, thread_id))
    return cur.lastrowid


def add_notification(conn, user_id: int, kind: str, text: str, plan_id=None, thread_id=None, at=None):
    conn.execute(
        """INSERT INTO notifications(user_id, kind, text, plan_id, thread_id, read, created_at)
           VALUES (?,?,?,?,?,0,?)""",
        (user_id, kind, text, plan_id, thread_id, at or now_str()),
    )


def mark_read(conn, user_id: int, thread_id: int, upto: int | None = None):
    if upto is None:
        row = conn.execute("SELECT MAX(id) AS m FROM messages WHERE thread_id = ?", (thread_id,)).fetchone()
        upto = row["m"] or 0
    conn.execute(
        """INSERT INTO reads(user_id, thread_id, last_read_id) VALUES (?,?,?)
           ON CONFLICT(user_id, thread_id) DO UPDATE SET last_read_id = MAX(last_read_id, excluded.last_read_id)""",
        (user_id, thread_id, upto),
    )


def create_match(conn, user_a: int, user_b: int) -> int:
    a, b = sorted((int(user_a), int(user_b)))
    existing = conn.execute(
        "SELECT thread_id FROM matches WHERE user_a = ? AND user_b = ?", (a, b)
    ).fetchone()
    if existing:
        return existing["thread_id"]
    stamp = now_str()
    cur = conn.execute(
        "INSERT INTO threads(kind, title, created_at, last_at) VALUES ('match', '', ?, ?)",
        (stamp, stamp),
    )
    thread_id = cur.lastrowid
    conn.execute("INSERT INTO thread_members(thread_id, user_id) VALUES (?,?)", (thread_id, a))
    conn.execute("INSERT INTO thread_members(thread_id, user_id) VALUES (?,?)", (thread_id, b))
    conn.execute(
        "INSERT INTO matches(user_a, user_b, thread_id, created_at) VALUES (?,?,?,?)",
        (a, b, thread_id, stamp),
    )
    add_message(conn, thread_id, None, "¡Habéis hecho match! Ya podéis empezar a montar el plan ⚡", "system")
    return thread_id


def ensure_plan_thread(conn, plan_id: int):
    plan = conn.execute("SELECT * FROM plans WHERE id = ?", (plan_id,)).fetchone()
    if not plan:
        return None
    joined = conn.execute(
        """SELECT u.* FROM plan_members pm JOIN users u ON u.id = pm.user_id
           WHERE pm.plan_id = ? AND pm.status = 'joined'""",
        (plan_id,),
    ).fetchall()
    thread = conn.execute(
        "SELECT * FROM threads WHERE kind = 'plan' AND plan_id = ? LIMIT 1", (plan_id,)
    ).fetchone()
    if len(joined) < 2:
        if thread:
            # Keep the history but hide the chat until the plan has company again.
            conn.execute("DELETE FROM thread_members WHERE thread_id = ?", (thread["id"],))
        return None
    member_ids = {u["id"] for u in joined}
    if not thread:
        stamp = now_str()
        cur = conn.execute(
            "INSERT INTO threads(kind, plan_id, title, created_at, last_at) VALUES ('plan', ?, ?, ?, ?)",
            (plan_id, plan["title"], stamp, stamp),
        )
        thread_id = cur.lastrowid
        for user in joined:
            conn.execute("INSERT OR IGNORE INTO thread_members(thread_id, user_id) VALUES (?,?)", (thread_id, user["id"]))
        add_message(conn, thread_id, None, f"Chat del plan «{plan['title']}». Aquí se organiza todo 📍", "system")
        return thread_id
    thread_id = thread["id"]
    current = {
        r["user_id"]
        for r in conn.execute("SELECT user_id FROM thread_members WHERE thread_id = ?", (thread_id,)).fetchall()
    }
    for user_id in member_ids - current:
        conn.execute("INSERT OR IGNORE INTO thread_members(thread_id, user_id) VALUES (?,?)", (thread_id, user_id))
    for user_id in current - member_ids:
        conn.execute("DELETE FROM thread_members WHERE thread_id = ? AND user_id = ?", (thread_id, user_id))
    return thread_id


def unread_count(conn, user_id: int, thread_id: int) -> int:
    row = conn.execute(
        """SELECT COUNT(*) AS n FROM messages m
           WHERE m.thread_id = ? AND m.user_id IS NOT NULL AND m.user_id != ?
             AND m.id > COALESCE((SELECT last_read_id FROM reads WHERE user_id = ? AND thread_id = ?), 0)""",
        (thread_id, user_id, user_id, thread_id),
    ).fetchone()
    return row["n"] if row else 0


# ------------------------------------------------------------------ economy
def coin_balance(conn, user_id: int) -> int:
    row = conn.execute("SELECT coins FROM users WHERE id = ?", (user_id,)).fetchone()
    return row["coins"] if row else 0


def _ledger(conn, user_id: int, delta: int, kind: str, note: str, balance_after: int) -> None:
    conn.execute(
        """INSERT INTO coin_ledger(user_id, delta, kind, note, balance_after, created_at)
           VALUES (?,?,?,?,?,?)""",
        (user_id, delta, kind, note, balance_after, now_str()),
    )


def grant_welcome(conn, user_id: int):
    """Give the one-time welcome bonus. Returns the new balance, or None if already given."""
    cur = conn.execute(
        "UPDATE users SET coins = coins + ?, welcome_bonus = 1 WHERE id = ? AND welcome_bonus = 0",
        (WELCOME_COINS, user_id),
    )
    if cur.rowcount == 0:
        return None
    balance = coin_balance(conn, user_id)
    _ledger(conn, user_id, WELCOME_COINS, "welcome", "Regalo de bienvenida", balance)
    return balance


def claim_daily(conn, user_id: int):
    """Claim the once-per-calendar-day bonus. Returns the new balance, or None if already claimed."""
    today = now().strftime(DATE_FMT)
    cur = conn.execute(
        "UPDATE users SET coins = coins + ?, last_daily = ? WHERE id = ? AND COALESCE(last_daily, '') != ?",
        (DAILY_COINS, today, user_id, today),
    )
    if cur.rowcount == 0:
        return None
    balance = coin_balance(conn, user_id)
    _ledger(conn, user_id, DAILY_COINS, "daily", "Recompensa diaria", balance)
    return balance


def spend_coins(conn, user_id: int, amount: int, kind: str, note: str):
    """Atomically spend coins. Never goes below zero. Returns the new balance or None."""
    cur = conn.execute(
        "UPDATE users SET coins = coins - ? WHERE id = ? AND coins >= ?",
        (amount, user_id, amount),
    )
    if cur.rowcount == 0:
        return None
    balance = coin_balance(conn, user_id)
    _ledger(conn, user_id, -amount, kind, note, balance)
    return balance


# ------------------------------------------------------------------ demo seed
def seed_venues(conn) -> None:
    if conn.execute("SELECT 1 FROM venues LIMIT 1").fetchone():
        return
    for venue in VENUES:
        conn.execute(
            """INSERT OR IGNORE INTO venues(name, city, area, category, emoji, lat, lon, blurb)
               VALUES (?,?,?,?,?,?,?,?)""",
            (venue["name"], venue["city"], venue["area"], venue["category"], venue["emoji"],
             venue["lat"], venue["lon"], venue["blurb"]),
        )


def seed_demo() -> None:
    with connect() as conn:
        seed_venues(conn)
        if conn.execute("SELECT 1 FROM users LIMIT 1").fetchone():
            return
        ids: dict[str, int] = {}

        def add_user(username, name, age, zone, avatar, variant, bio, interests, looking_for, status_note,
                     minutes_online=0, city="Madrid", lat=None, lon=None):
            if lat is None or lon is None:
                if city == "Madrid" and zone in ZONES:
                    lat, lon = ZONES[zone]
                elif zone in EXTRA_AREAS:
                    lat, lon = EXTRA_AREAS[zone]
                else:
                    venue_area = next(
                        (venue for venue in VENUES if venue["city"] == city and venue["area"] == zone),
                        None,
                    )
                    if venue_area:
                        lat, lon = venue_area["lat"], venue_area["lon"]
                    else:
                        lat, lon = city_coords(city)
            digest, salt = hash_password("demo1234")
            last = fmt(now() - timedelta(minutes=minutes_online))
            cur = conn.execute(
                """INSERT INTO users(name, username, pass_hash, pass_salt, age, zone, city, lat, lon,
                   bio, avatar, variant, interests, looking_for, status_note, created_at, last_seen)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (name, username, digest, salt, age, zone, city, lat, lon,
                 bio, avatar, variant, json.dumps(interests, ensure_ascii=False),
                 looking_for, status_note, now_str(), last),
            )
            ids[username] = cur.lastrowid

        add_user("lucia", "Lucía Ferrer", 24, "Malasaña", "🦋", 0,
                 "Buscando plan a todas horas. Indie, terrazas y fotos malísimas.",
                 ["Música indie", "Terrazas", "Fotografía", "Conciertos", "Brunch"],
                 "Alguien para conciertos y terrazas infinitas",
                 "Hoy: terraza después del curro ☀️", 0)
        add_user("hugo", "Hugo Salas", 27, "Lavapiés", "🎸", 1,
                 "Guitarrista sin grupo. Siempre apunto a un concierto o a una birra.",
                 ["Música indie", "Cañas", "Conciertos", "Fútbol", "Vinilos"],
                 "Plan de conciertos y birras", "Buscando entrada para el sábado", 4)
        add_user("vera", "Vera Ortiz", 25, "Chueca", "🍒", 2,
                 "Salsa los jueves, cine de terror los domingos. Cenas que se alargan.",
                 ["Cine", "Baile", "Gastronomía", "Viajes", "Cócteles"],
                 "Cine, salsa y cenas largas", "Jueves de salsa 💃", 1)
        add_user("nico", "Nico Prieto", 29, "Tribunal", "🚲", 3,
                 "Rutas en bici, café de especialidad y perder tardes en El Retiro.",
                 ["Bici", "Café", "Senderismo", "Fotografía", "Running"],
                 "Rutas, café y aire libre", "Ruta en bici el domingo 🚴", 130)
        add_user("alba", "Alba Ríos", 22, "Salamanca", "🌸", 4,
                 "Expos, brunch y mercadillos. Nunca digo que no a un plan de día.",
                 ["Arte", "Brunch", "Museos", "Moda", "Fotografía"],
                 "Planes de día con arte y brunch", "Expo + brunch este finde", 0)
        add_user("dani", "Dani Cruz", 26, "La Latina", "🍻", 5,
                 "Ruta de bares sin pretensiones. Cuanto más largo el tapeo, mejor.",
                 ["Cañas", "Tapas", "Fútbol", "Música indie", "Idiomas"],
                 "Ruta de bares sin pretensiones", "Hoy toca La Latina 🍻", 3)
        add_user("emma", "Emma Vidal", 28, "Chamberí", "🪩", 6,
                 "Fiesta los sábados, yoga los domingos. Equilibrios.",
                 ["Fiesta", "Yoga", "Cerámica", "Baile", "Cócteles"],
                 "Noches locas y domingos de yoga", "Fiesta 90s el sábado 🪩", 2)
        add_user("ivan", "Iván Mena", 24, "Delicias", "🏓", 7,
                 "Pádel nivel cero y risas nivel diez. Gamer de tarde, rockero de noche.",
                 ["Pádel", "Gaming", "Rock", "Cañas", "Series"],
                 "Pádel nivel cero y risas", "Busco pareja de pádel malísima", 25)
        add_user("leo", "Leo Navarro", 30, "Retiro", "🏃", 1,
                 "Correr suave, café largo y pelis de domingo. Sin prisa.",
                 ["Running", "Cine", "Café", "Fotografía", "Viajes"],
                 "Correr, café y planes tranquilos", "Running suave mañana", 560)
        add_user("sara", "Sara Molina", 23, "Argüelles", "🎨", 2,
                 "Siempre con un plan en la cabeza. Expos, cines y cañas de después.",
                 ["Arte", "Cine", "Música indie", "Viajes", "Cañas"],
                 "Alguien con quien perderse en una expo", "Expo y café el jueves", 0)
        add_user("marta", "Marta Soler", 26, "Moncloa", "🍷", 2,
                 "Vino, libros y jazz. Prefiero una terraza a una discoteca.",
                 ["Vinilos", "Lectura", "Jazz", "Gastronomía", "Terrazas"],
                 "Cenas tranquilas y jazz en directo", "Jazz el viernes 🎷", 40)
        add_user("guille", "Guille Pardo", 28, "Lavapiés", "🛹", 3,
                 "Skate, grafitis y birras en la plaza. Madrid se ve mejor rodando.",
                 ["Skate", "Arte", "Cañas", "Fotografía", "Festivales"],
                 "Gente para rodar y tomar algo", "Rodada por Lavapiés al atardecer", 0)
        add_user("noa", "Noa Castro", 24, "Chueca", "🎧", 4,
                 " Electrónica, festivales y afterhours con cabeza. Playlist siempre lista.",
                 ["Electrónica", "Festivales", "Fiesta", "Baile", "Café"],
                 "Compañía para festivales y afters", "Buscando plan para el festival", 8)
        add_user("alex", "Álex Duarte", 27, "La Latina", "🍜", 5,
                 "Ramen, karaoke y anime. A veces todo en la misma noche.",
                 ["Ramen", "Karaoke", "Series", "Gastronomía", "Viajes"],
                 "Karaoke y cenas sin vergüenza", "Karaoke el viernes 🎤", 70)

        # People in the other cities so changing location actually finds a ronda.
        extra_people = [
            ("laia", "Laia Puig", 24, "Gràcia", "Barcelona", "🎨", 4,
             "Diseño de día, conciertos de noche. Gràcia me queda pequeña.",
             ["Conciertos", "Arte", "Café", "Fotografía", "Festivales"],
             "Gente para conciertos y vermuts", "Hoy: indie en Razzmatazz 🎸", 0),
            ("pau", "Pau Serra", 27, "El Born", "Barcelona", "🚲", 3,
             "Bici, playa y tapas. Si hay sol, hay plan.",
             ["Bici", "Playa", "Tapas", "Viajes", "Fotografía"],
             "Compañía para escapadas de fin de semana", "Ruta hasta la Barceloneta 🚲", 6),
            ("julia", "Júlia Bosch", 25, "Eixample", "Barcelona", "🍷", 2,
             "Vino natural, cenas largas y expos los domingos.",
             ["Gastronomía", "Arte", "Vinilos", "Cine", "Café"],
             "Cenas tranquilas y planes de día", "Vermut + expo este finde", 45),
            ("nerea", "Nerea Blasco", 26, "Ruzafa", "Valencia", "🌿", 5,
             "Ruzafa, playa y horchata. Valenciana de adopción.",
             ["Cañas", "Gastronomía", "Playa", "Música indie", "Yoga"],
             "Gente para tapas y playa", "Tapas en Ruzafa esta noche", 0),
            ("toni", "Toni Ferrer", 28, "El Cabanyal", "Valencia", "🎸", 1,
             "Guitarra, mar y conciertos pequeños. Nada de planes con prisa.",
             ["Conciertos", "Rock", "Playa", "Cañas", "Vinilos"],
             "Plan de conciertos y cervezas", "Concierto en Wah Wah 🎸", 22),
            ("carmen", "Carmen Ruiz", 23, "Triana", "Sevilla", "💃", 0,
             "Flamenco, tapas y puente. Sevilla se disfruta andando.",
             ["Baile", "Tapas", "Fiesta", "Música indie", "Arte"],
             "Alguien para bailar y tapear", "Flamenco en Triana 💃", 3),
            ("alvaro", "Álvaro Mesa", 29, "Alameda", "Sevilla", "🍻", 6,
             "Cervezas en la Alameda y partidos con amigos.",
             ["Cañas", "Fútbol", "Tapas", "Conciertos", "Idiomas"],
             "Ruta de bares sin pretensiones", "Cervezas en la Alameda 🍻", 14),
            ("ane", "Ane Etxeberria", 27, "Casco Viejo", "Bilbao", "🎧", 4,
             "Pintxos, música y monte. Bilbao de arriba abajo.",
             ["Gastronomía", "Electrónica", "Senderismo", "Cañas", "Festivales"],
             "Gente para pintxos y conciertos", "Pintxos por el Casco Viejo", 1),
            ("iker", "Iker Aramburu", 25, "Indautxu", "Bilbao", "🏃", 3,
             "Salgo a correr y acabo en una terraza. Siempre.",
             ["Running", "Café", "Cañas", "Fútbol", "Bici"],
             "Compañía para correr y tomar algo", "Ruta por Artxanda el domingo", 80),
            ("rocio", "Rocío León", 24, "Centro", "Málaga", "🍋", 4,
             "Sol, playa y tapas. No concibo un plan sin brisa.",
             ["Playa", "Tapas", "Fotografía", "Viajes", "Fiesta"],
             "Planes de playa y atardeceres", "Atardecer en La Malagueta 🌅", 0),
            ("mario", "Mario Vega", 28, "La Malagueta", "Málaga", "🍷", 2,
             "Vino, pescaíto y paseos por el puerto.",
             ["Gastronomía", "Cañas", "Playa", "Cine", "Música indie"],
             "Cenas y paseos sin prisa", "Tapas en la Merced esta noche", 32),
            ("pilar", "Pilar Gracia", 25, "El Tubo", "Zaragoza", "🎨", 0,
             "Tapas, expos y planes de última hora. Zaragoza mola.",
             ["Tapas", "Arte", "Cañas", "Cine", "Viajes"],
             "Gente para la ruta de tapas", "Ruta por El Tubo 🍢", 5),
            ("jorge", "Jorge Millán", 30, "Romareda", "Zaragoza", "🚴", 5,
             "Bici, parque y café. Planes sencillos que siempre salen bien.",
             ["Bici", "Café", "Running", "Gastronomía", "Fotografía"],
             "Compañía para planes al aire libre", "Paseo por el Parque Grande", 130),
            ("elena", "Elena Campos", 22, "Albaicín", "Granada", "🌸", 4,
             "Estudio arte y me pierdo por el Albaicín. Té y vistas.",
             ["Arte", "Museos", "Café", "Fotografía", "Viajes"],
             "Alguien para perderse por Granada", "Atardecer en San Nicolás 🌇", 2),
            ("david", "David Rueda", 26, "Centro", "Granada", "🎸", 1,
             "Tapas, conciertos y rutas por la Sierra.",
             ["Cañas", "Tapas", "Rock", "Senderismo", "Conciertos"],
             "Plan de tapas y música", "Tapas en Plaza Nueva", 55),
            ("uxia", "Uxía Varela", 24, "Centro", "A Coruña", "🌊", 4,
             "Mar, paseos y vino. Coruña tiene el mejor atardecer.",
             ["Playa", "Gastronomía", "Fotografía", "Viajes", "Café"],
             "Planes de mar y terraza", "Paseo hasta la Torre 🌊", 7),
            ("brais", "Brais Nogueira", 27, "Riazor", "A Coruña", "🏃", 3,
             "Corro por Riazor y luego invito a cañas. Equilibrio.",
             ["Running", "Cañas", "Playa", "Fútbol", "Música indie"],
             "Compañía para correr y tapear", "Cañas en María Pita", 90),
            ("maite", "Maite Agirre", 26, "Parte Vieja", "San Sebastián", "🍷", 2,
             "Pintxos, txakoli y playa. Lo simple, bien hecho.",
             ["Gastronomía", "Cañas", "Playa", "Cine", "Viajes"],
             "Gente para pintxos y paseos", "Pintxos en la Parte Vieja", 12),
            ("xabi", "Xabi Otaegi", 29, "Gros", "San Sebastián", "🎧", 3,
             "Música, surf y cenas que acaban en la playa.",
             ["Electrónica", "Playa", "Gastronomía", "Festivales", "Café"],
             "Plan de atardecer y música", "Atardecer en La Concha", 160),
            ("neus", "Neus Pons", 25, "Santa Catalina", "Palma", "🌸", 4,
             "Mercado, tapas y calas escondidas.",
             ["Tapas", "Playa", "Fotografía", "Gastronomía", "Viajes"],
             "Compañía para calas y tapas", "Tapas en Santa Catalina", 3),
            ("marc", "Marc Ferrer", 28, "Born", "Palma", "🚲", 5,
             "Bici por la isla y cervezas frente al mar.",
             ["Bici", "Playa", "Cañas", "Fotografía", "Música indie"],
             "Escapadas de fin de semana", "Cala Major y helado", 65),
        ]
        for username, name, years, area, city, emoji, variant, bio, interests, looking, status, minutes in extra_people:
            add_user(username, name, years, area, emoji, variant, bio, interests, looking, status,
                     minutes, city=city)

        for user_id in ids.values():
            grant_welcome(conn, user_id)

        def add_plan(host, title, category, description, start_at, zone, venue, spots,
                     members=(), pending=(), approval=0, vibe=(), city="Madrid"):
            meta = CATEGORY_MAP.get(category, CATEGORY_MAP["planes"])
            stamp = now_str()
            venue_row = conn.execute(
                "SELECT * FROM venues WHERE name = ? AND city = ?", (venue, city)
            ).fetchone()
            if venue_row:
                lat, lon = venue_row["lat"], venue_row["lon"]
                venue_id = venue_row["id"]
            else:
                lat, lon = city_coords(city)
                venue_id = None
            cur = conn.execute(
                """INSERT INTO plans(host_id, title, category, emoji, description, start_at, zone, city,
                   lat, lon, venue, venue_id, spots, approval, vibe, status, created_at, updated_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (ids[host], title, category, meta["emoji"], description, start_at, zone, city,
                 lat, lon, venue, venue_id, spots, 1 if approval else 0,
                 json.dumps(list(vibe), ensure_ascii=False), "open", stamp, stamp),
            )
            plan_id = cur.lastrowid
            conn.execute(
                """INSERT INTO plan_members(plan_id, user_id, role, status, joined_at)
                   VALUES (?,?,?,'joined',?)""",
                (plan_id, ids[host], "host", stamp),
            )
            for username in members:
                conn.execute(
                    """INSERT INTO plan_members(plan_id, user_id, role, status, joined_at)
                       VALUES (?,?,?,'joined',?)""",
                    (plan_id, ids[username], "member", stamp),
                )
            for username in pending:
                conn.execute(
                    """INSERT INTO plan_members(plan_id, user_id, role, status, note, joined_at)
                       VALUES (?,?,?,'pending','',?)""",
                    (plan_id, ids[username], "member", stamp),
                )
            joined = 1 + len(members)
            if joined >= spots + 1:
                conn.execute("UPDATE plans SET status = 'full' WHERE id = ?", (plan_id,))
            return plan_id

        plan_concert = add_plan(
            "hugo", "Vetusta Morla en La Riviera", "concierto",
            "Tengo una entrada de sobra y cero vergüenza. ¿Te vienes al concierto y nos tomamos algo después?",
            in_days(2, 21, 30), "Delicias", "La Riviera", 3,
            members=["vera", "lucia"], vibe=["indie", "concierto", "noche"],
        )
        plan_canas = add_plan(
            "dani", "Cañas y tapas por La Latina", "cañas",
            "Ruta de bares sin reserva y sin prisa. Gente nueva bienvenida, aquí nadie se queda fuera.",
            in_days(0, 20, 30), "La Latina", "Calle Cava Baja", 3,
            members=["lucia"], vibe=["cañas", "tapas", "buenrollo"],
        )
        add_plan(
            "nico", "Ruta en bici por Madrid Río", "aire",
            "Salida tranquila, parada a mitad para un café y vuelta antes de comer. Tengo una bici de sobra.",
            in_days(3, 11, 0), "Delicias", "Madrid Río · Matadero", 3,
            members=["alba"], vibe=["bici", "aire libre", "café"],
        )
        plan_cine = add_plan(
            "vera", "Cine de terror + pizza", "cine",
            "Maratón de terror en el salón con pizza casera. Nivel de sustos: alto. Nivel de vergüenza: cero.",
            in_days(1, 19, 30), "Chueca", "Sala Equis", 2,
            members=["lucia"], vibe=["cine", "pizza", "terror"],
        )
        add_plan(
            "ivan", "Pádel nivel cero", "deporte",
            "Partido relajado para gente que empieza. Yo llevo palas y pelotas; tú trae ganas de reírte.",
            in_days(4, 18, 0), "Delicias", "Club Pádel Delicias", 1,
            vibe=["pádel", "principiantes"],
        )
        add_plan(
            "alba", "Brunch + mercadillo", "comida",
            "Brunch largo y luego vuelta por el mercadillo. Sin horario, sin prisa, sin plan B.",
            in_days(2, 12, 30), "Salamanca", "Mercado de la Paz", 2,
            vibe=["brunch", "mercadillo", "domingo"],
        )
        add_plan(
            "emma", "Fiesta 90s", "baile",
            "Entradas para la fiesta de los 90. Dress code: brilli brilli. Bailar mal está permitido.",
            in_days(2, 23, 30), "Malasaña", "Independance Club", 4,
            members=["leo"], vibe=["fiesta", "90s", "baile"],
        )
        plan_terraza = add_plan(
            "lucia", "Terraceo after curro", "cañas",
            "Salgo a las 18:30 y no pienso irme a casa. Busco compañía de terraza, cañas y cotilleo sano.",
            in_days(1, 19, 30), "Malasaña", "Plaza del Dos de Mayo", 2,
            pending=["sara"], approval=1, vibe=["terrazas", "cañas", "afterwork"],
        )
        add_plan(
            "leo", "Running suave por El Retiro", "deporte",
            "5 km a ritmo de conversación y café al terminar. Si te quedas sin aire, se camina.",
            in_days(2, 9, 0), "Retiro", "Puerta de Alcalá", 3,
            vibe=["running", "principiantes", "café"],
        )
        add_plan(
            "sara", "Expo de fotografía + café", "cultura",
            "Expo pequeña, café largo y paseo. Me apetece conocer a alguien con quien comentar las fotos.",
            in_days(3, 17, 0), "Chamberí", "Sala Canal de Isabel II", 2,
            vibe=["fotografía", "expo", "café"],
        )

        # Plans in other cities. Changing location in the app surfaces these.
        extra_plans = [
            ("laia", "Noche indie en Razzmatazz", "concierto",
             "Entrada para la sala grande y previa en Poblenou. Busco gente que baile mal sin complejos.",
             in_days(2, 22, 0), "Barcelona", "Poblenou", "Razzmatazz", 3, ["pau"], ["indie", "concierto"]),
            ("pau", "Vermut y paseo por Gràcia", "cañas",
             "Vermut, sol y una vuelta por las plazas de Gràcia. Sin prisa y sin reserva.",
             in_days(1, 12, 30), "Barcelona", "Gràcia", "Park Güell", 3, [], ["vermut", "paseo"]),
            ("nerea", "Tapas en Ruzafa", "comida",
             "Ruta corta de tapas y después una copa. Ruzafa nunca falla.",
             in_days(1, 20, 30), "Valencia", "Ruzafa", "Ruzafa", 3, ["toni"], ["tapas", "cañas"]),
            ("toni", "Concierto en Wah Wah", "concierto",
             "Concierto pequeño y birras después. Llevo una entrada libre.",
             in_days(3, 21, 30), "Valencia", "Ruzafa", "Sala Wah Wah", 2, [], ["concierto", "indie"]),
            ("carmen", "Flamenco y tapas en Triana", "baile",
             "Tablao pequeño y tapas después. Nivel turista cero: vamos con locales.",
             in_days(2, 21, 0), "Sevilla", "Triana", "Triana", 3, [], ["flamenco", "tapas"]),
            ("alvaro", "Cervezas en la Alameda", "cañas",
             "Terrazas de la Alameda y partido si hay suerte. Plan sencillo, gente nueva.",
             in_days(1, 20, 0), "Sevilla", "Alameda", "Alameda de Hércules", 4, [], ["cañas", "fútbol"]),
            ("ane", "Pintxos por el Casco Viejo", "comida",
             "Ruta de pintxos por las Siete Calles. Tú eliges el siguiente bar.",
             in_days(1, 20, 0), "Bilbao", "Casco Viejo", "Casco Viejo", 3, [], ["pintxos", "cañas"]),
            ("iker", "Ruta por Artxanda", "aire",
             "Subimos en funicular, paseo y merienda con vistas. Nivel tranquilo.",
             in_days(3, 11, 0), "Bilbao", "Artxanda", "Artxanda", 3, [], ["senderismo", "vistas"]),
            ("rocio", "Atardecer en La Malagueta", "aire",
             "Manta, música y atardecer en la playa. Después cañas cerca.",
             in_days(1, 19, 30), "Málaga", "La Malagueta", "La Malagueta", 3, [], ["playa", "atardecer"]),
            ("mario", "Tapas en la Merced", "cañas",
             "Plaza, tapas y una vuelta por el centro. Sin reserva y sin drama.",
             in_days(2, 20, 30), "Málaga", "Centro", "Plaza de la Merced", 2, [], ["tapas", "cañas"]),
            ("pilar", "Ruta de tapas por El Tubo", "comida",
             "Cuatro bares, cuatro tapas y una copa final. El clásico de Zaragoza.",
             in_days(1, 20, 30), "Zaragoza", "El Tubo", "El Tubo", 4, [], ["tapas", "cañas"]),
            ("jorge", "Paseo por el Parque Grande", "aire",
             "Paseo, café y bici opcional. Plan de domingo sin madrugar.",
             in_days(2, 11, 0), "Zaragoza", "Romareda", "Parque Grande", 3, [], ["aire libre", "café"]),
            ("elena", "Atardecer en el Albaicín", "cultura",
             "Subimos al mirador y tomamos algo después. Llevo la cámara.",
             in_days(1, 19, 0), "Granada", "Albaicín", "Mirador de San Nicolás", 3, [], ["atardecer", "fotos"]),
            ("david", "Tapas en Plaza Nueva", "cañas",
             "Tapas y cañas en el centro. Después vemos dónde acaba la noche.",
             in_days(2, 21, 0), "Granada", "Centro", "Plaza Nueva", 2, [], ["tapas", "cañas"]),
            ("uxia", "Paseo por la Torre de Hércules", "aire",
             "Paseo marítimo hasta el faro y café al volver. El mejor plan de Coruña.",
             in_days(2, 18, 0), "A Coruña", "Torre", "Torre de Hércules", 3, [], ["paseo", "mar"]),
            ("brais", "Cañas en María Pita", "cañas",
             "Terrazas, cañas y partido. Si llueve, se cambia el bar y ya está.",
             in_days(1, 20, 30), "A Coruña", "Centro", "Plaza de María Pita", 3, [], ["cañas", "fútbol"]),
            ("maite", "Pintxos en la Parte Vieja", "comida",
             "Ruta de pintxos y txakoli. La Parte Vieja se recorre mejor con gente.",
             in_days(1, 20, 0), "San Sebastián", "Parte Vieja", "Parte Vieja", 4, [], ["pintxos", "gastronomía"]),
            ("xabi", "Atardecer en La Concha", "aire",
             "Paseo por la bahía y algo en Gros después. Llevo altavoz pequeño.",
             in_days(2, 19, 30), "San Sebastián", "Gros", "La Concha", 3, [], ["playa", "atardecer"]),
            ("neus", "Tapas en Santa Catalina", "comida",
             "Mercado, tapas y una vuelta por el barrio. Plan fácil de Palma.",
             in_days(1, 20, 30), "Palma", "Santa Catalina", "Santa Catalina", 3, [], ["tapas", "mercado"]),
            ("marc", "Cala Major y helado", "aire",
             "Bici hasta Cala Major, baño y helado. Vuelta antes de cenar.",
             in_days(2, 12, 0), "Palma", "Cala Major", "Cala Major", 2, [], ["bici", "playa"]),
        ]
        for host, title, category, description, start_at, city, area, venue, spots, members, vibe in extra_plans:
            add_plan(host, title, category, description, start_at, area, venue, spots,
                     members=members, vibe=vibe, city=city)

        # plan group chats
        for plan_id in (plan_concert, plan_canas, plan_cine):
            ensure_plan_thread(conn, plan_id)
        chat = conn.execute("SELECT id FROM threads WHERE kind='plan' AND plan_id = ?", (plan_canas,)).fetchone()["id"]
        add_message(conn, chat, ids["dani"], "Reservado a las 20:30 en Cava Baja 🍻", at=ago(190))
        add_message(conn, chat, ids["lucia"], "¿Queda sitio para alguien más?", at=ago(150))
        add_message(conn, chat, ids["dani"], "Sí, llevo a un colega del curro. Te presento 😄", at=ago(135))
        chat = conn.execute("SELECT id FROM threads WHERE kind='plan' AND plan_id = ?", (plan_concert,)).fetchone()["id"]
        add_message(conn, chat, ids["hugo"], "Entradas listas. Nos vemos a las 21:15 en la puerta 🎸", at=ago(330))
        add_message(conn, chat, ids["vera"], "Yo llevo la cámara 📸", at=ago(300))
        add_message(conn, chat, ids["lucia"], "Perfecto, allí estaré", at=ago(285))
        chat = conn.execute("SELECT id FROM threads WHERE kind='plan' AND plan_id = ?", (plan_cine,)).fetchone()["id"]
        add_message(conn, chat, ids["vera"], "Maratón de terror el viernes. Llevo la pizza 🍕", at=ago(95))
        chat = conn.execute("SELECT id FROM threads WHERE kind='plan' AND plan_id = ?", (plan_canas,)).fetchone()["id"]
        mark_read(conn, ids["lucia"], chat)

        # extra plan chats (host + member)
        bici = conn.execute("SELECT id FROM plans WHERE title LIKE 'Ruta en bici%'").fetchone()["id"]
        ensure_plan_thread(conn, bici)
        chat = conn.execute("SELECT id FROM threads WHERE kind='plan' AND plan_id = ?", (bici,)).fetchone()["id"]
        add_message(conn, chat, ids["alba"], "¿Alguien tiene una bici de sobra? La mía está en el pueblo 😅", at=ago(1440))
        add_message(conn, chat, ids["nico"], "Yo llevo una extra. Te la dejo, pero invitas al café 🚲", at=ago(1380))
        fiesta = conn.execute("SELECT id FROM plans WHERE title LIKE 'Fiesta 90s%'").fetchone()["id"]
        ensure_plan_thread(conn, fiesta)
        chat = conn.execute("SELECT id FROM threads WHERE kind='plan' AND plan_id = ?", (fiesta,)).fetchone()["id"]
        add_message(conn, chat, ids["emma"], "Dress code: brilli brilli ✨", at=ago(65))

        # matches + swipes
        def match(a, b):
            conn.execute(
                "INSERT OR IGNORE INTO swipes(from_user, to_user, action, created_at) VALUES (?,?,'like',?)",
                (ids[a], ids[b], ago(4000)),
            )
            conn.execute(
                "INSERT OR IGNORE INTO swipes(from_user, to_user, action, created_at) VALUES (?,?,'like',?)",
                (ids[b], ids[a], ago(3900)),
            )
            return create_match(conn, ids[a], ids[b])

        lucia_hugo = match("lucia", "hugo")
        add_message(conn, lucia_hugo, ids["hugo"], "¡ey! ¿al final vas al concierto del sábado? 🎸", at=ago(52))
        add_message(conn, lucia_hugo, ids["lucia"], "me lo estoy pensando… ¿tú vas?", at=ago(46))
        add_message(conn, lucia_hugo, ids["hugo"], "sí, tengo una entrada libre por si te animas 👀", at=ago(24))
        add_message(conn, lucia_hugo, ids["lucia"], "me lo vendes y te debo una caña", at=ago(18))
        add_message(conn, lucia_hugo, ids["hugo"], "trato. ¿te paso el link?", at=ago(7))
        first_hugo = conn.execute("SELECT MIN(id) FROM messages WHERE thread_id = ?", (lucia_hugo,)).fetchone()[0]
        mark_read(conn, ids["lucia"], lucia_hugo, upto=first_hugo + 3)

        lucia_vera = match("lucia", "vera")
        add_message(conn, lucia_vera, ids["vera"], "Vi que también te gusta el cine de terror 👀", at=ago(700))
        add_message(conn, lucia_vera, ids["lucia"], "mucho. ¿has visto la de Suspiria?", at=ago(660))
        add_message(conn, lucia_vera, ids["vera"], "mil veces. el viernes hago maratón, ¿te apuntas?", at=ago(640))
        mark_read(conn, ids["lucia"], lucia_vera)

        lucia_nico = match("lucia", "nico")
        add_message(conn, lucia_nico, ids["nico"], "¿Te gusta la bici o solo la foto? 🚴", at=ago(1600))
        add_message(conn, lucia_nico, ids["lucia"], "depende del día 😌", at=ago(1580))
        add_message(conn, lucia_nico, ids["nico"], "domingo 11:00, Madrid Río. te dejo una bici", at=ago(1540))
        mark_read(conn, ids["lucia"], lucia_nico)

        hugo_vera = match("hugo", "vera")
        add_message(conn, hugo_vera, ids["vera"], "¿Al final vas con alguien al concierto?", at=ago(200))
        add_message(conn, hugo_vera, ids["hugo"], "voy con Lucía, pero hay sitio en la previa 🍻", at=ago(190))
        add_message(conn, hugo_vera, ids["vera"], "me apunto a la previa", at=ago(180))
        mark_read(conn, ids["hugo"], hugo_vera)

        nico_emma = match("nico", "emma")
        add_message(conn, nico_emma, ids["emma"], "Te vi en la ruta del domingo, ¿vas siempre?", at=ago(900))
        add_message(conn, nico_emma, ids["nico"], "casi siempre. el domingo salimos a las 11", at=ago(880))
        mark_read(conn, ids["nico"], nico_emma)

        # incoming likes, so demo accounts get a match quickly
        incoming = {
            "lucia": ["alba", "ivan", "emma", "leo", "sara", "marta",
                      "laia", "pau", "nerea", "carmen", "ane", "rocio", "pilar", "elena", "uxia", "maite", "neus"],
            "hugo": ["alba", "marta", "noa", "sara"],
            "vera": ["dani", "guille", "alex", "leo"],
            "nico": ["sara", "noa", "marta", "alex"],
        }
        for target, senders in incoming.items():
            for sender in senders:
                conn.execute(
                    "INSERT OR IGNORE INTO swipes(from_user, to_user, action, created_at) VALUES (?,?,'like',?)",
                    (ids[sender], ids[target], ago(3000)),
                )

        # notifications
        add_notification(conn, ids["lucia"], "request", "Sara quiere apuntarse a «Terraceo after curro»", plan_id=plan_terraza, at=ago(22))
        add_notification(conn, ids["lucia"], "message", "Hugo te ha escrito: «trato. ¿te paso el link?»", thread_id=lucia_hugo, at=ago(7))
        add_notification(conn, ids["lucia"], "plan", "Nuevo plan de Emma: Fiesta 90s", plan_id=fiesta, at=ago(70))
        conn.execute("UPDATE notifications SET read = 1 WHERE user_id = ? AND kind = 'plan'", (ids["lucia"],))

        add_notification(conn, ids["hugo"], "message", "Lucía te ha escrito en el chat del concierto", thread_id=plan_concert, at=ago(285))
        add_notification(conn, ids["hugo"], "plan", "Vera se ha apuntado a «Vetusta Morla en La Riviera»", plan_id=plan_concert, at=ago(360))
        conn.execute("UPDATE notifications SET read = 1 WHERE user_id = ? AND kind = 'plan'", (ids["hugo"],))

        add_notification(conn, ids["vera"], "message", "Lucía te ha escrito: «me lo vendes y te debo una caña»", thread_id=lucia_vera, at=ago(18))
        add_notification(conn, ids["vera"], "match", "¡Nuevo match con Emma! Ya podéis hablar", thread_id=nico_emma, at=ago(900))
        conn.execute("UPDATE notifications SET read = 1 WHERE user_id = ? AND kind = 'match'", (ids["vera"],))

        add_notification(conn, ids["nico"], "plan", "Alba se ha apuntado a «Ruta en bici por Madrid Río»", plan_id=bici, at=ago(1440))
        add_notification(conn, ids["nico"], "message", "Emma te ha escrito: «Te vi en la ruta del domingo…»", thread_id=nico_emma, at=ago(900))
        conn.execute("UPDATE notifications SET read = 1 WHERE user_id = ? AND kind = 'message'", (ids["nico"],))

        # seeded conversations start read for their participants
        for thread in conn.execute("SELECT id FROM threads WHERE kind = 'plan'").fetchall():
            for member in conn.execute(
                "SELECT user_id FROM thread_members WHERE thread_id = ?", (thread["id"],)
            ).fetchall():
                mark_read(conn, member["user_id"], thread["id"])
