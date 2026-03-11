import requests
import json
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

def obtener_sinopsis_espanol(titulo_anime):
    t = titulo_anime.lower()
    if "frieren" in t:
        return "La elfa Frieren y sus compañeros derrotaron al Rey Demonio."
    elif "jujutsu" in t:
        return "Yuji Itadori es un estudiante con una fuerza increíble."
    return "¡Un emocionante anime! Visita MyAnimeList para más detalles."

def actualizar_estrenos():
    url = "https://api.jikan.moe/v4/seasons/now"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        datos = response.json()
        lista = []
        
        # ¡AQUÍ ESTÁ LA MAGIA! Cambié el [:4] por [:24] para que traiga 24 animes
        for anime in datos.get('data', [])[:24]:
            titulo = anime.get('title', 'Sin título')
            lista.append({
                "titulo": titulo,
                "imagen": anime.get('images', {}).get('jpg', {}).get('large_image_url', ''),
                "sinopsis": obtener_sinopsis_espanol(titulo),
                "link": anime.get('url', '#')
            })
        with open('estrenos.json', 'w', encoding='utf-8') as f:
            json.dump(lista, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error: {e}")

def actualizar_trailers():
    url = "https://api.jikan.moe/v4/seasons/upcoming"
    try:
        time.sleep(2) 
        response = requests.get(url, headers=headers, timeout=10)
        datos = response.json()
        lista = []
        for anime in datos.get('data', []):
            trailer_url = anime.get('trailer', {}).get('url')
            if trailer_url and len(lista) < 4:
                lista.append({
                    "titulo": anime.get('title', 'Próximo estreno'),
                    "video": trailer_url,
                    "imagen": ""
                })
        with open('trailers.json', 'w', encoding='utf-8') as f:
            json.dump(lista, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    actualizar_estrenos()
    actualizar_trailers()
