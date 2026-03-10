import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def obtener_sinopsis_espanol(titulo_anime):
    t = titulo_anime.lower()
    if "frieren" in t: return "La elfa Frieren y sus compañeros derrotaron al Rey Demonio. Ahora, ella emprende un nuevo viaje para comprender a los humanos."
    elif "jujutsu kaisen" in t: return "Yuji Itadori es un estudiante con una fuerza increíble. Para salvar a sus amigos, se come el dedo de Sukuna."
    elif "jigokuraku" in t: return "Gabimaru, un ninja legendario condenado a muerte, recibe una última oportunidad: viajar a una isla misteriosa."
    elif "demon slayer" in t or "kimetsu" in t: return "Tanjiro Kamado emprende un viaje peligroso para encontrar una cura para su hermana Nezuko."
    return "¡Un emocionante anime de esta temporada! Visita MyAnimeList para leer la sinopsis completa."

def actualizar_estrenos():
    url = "https://api.jikan.moe/v4/seasons/now"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        datos = response.json()
        lista = []
        for anime in datos.get('data', [])[:4]:
            titulo = anime.get('title', 'Sin título')
            lista.append({
                "titulo": titulo,
                "imagen": anime.get('images', {}).get('jpg', {}).get('large_image_url', ''),
                "sinopsis": obtener_sinopsis_espanol(titulo),
                "link": anime.get('url', '#')
            })
        with open('estrenos.json', 'w', encoding='utf-8') as f:
            json.dump(lista, f, ensure_ascii=False, indent=4)
    except Exception as e: print(f"Error: {e}")

def actualizar_trailers():
    url = "https://api.jikan.moe/v4/seasons/upcoming"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        datos = response.json()
        lista = []
        for anime in datos.get('data', []):
            t_info = anime.get('trailer')
            if t_info and isinstance(t_info, dict):
                yt_id = t_info.get('youtube_id')
                if yt_id:  # <--- ESTO ES LO QUE FALTABA EN TU LÍNEA 47
                    lista.append({"titulo": anime.get('title', 'Anime'), "youtube_id": yt_id})
            if len(lista) >= 3: break
        with open('trailers.json', 'w', encoding='utf-8') as f:
            json.dump(lista, f, ensure_ascii=False, indent=4)
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    actualizar_estrenos()
    actualizar_trailers()