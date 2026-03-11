import requests
import json
import time

# Encabezados para que los sitios no nos bloqueen como "bots"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def obtener_sinopsis_espanol(titulo_anime):
    """Traduce o asigna sinopsis en español para los animes principales."""
    t = titulo_anime.lower()
    if "frieren" in t:
        return "La elfa Frieren y sus compañeros derrotaron al Rey Demonio. Ahora, ella emprende un nuevo viaje para comprender a los humanos."
    elif "jujutsu kaisen" in t:
        return "Yuji Itadori es un estudiante con una fuerza increíble. Para salvar a sus amigos, se come el dedo de Sukuna."
    elif "jigokuraku" in t:
        return "Gabimaru, un ninja legendario condenado a muerte, recibe una última oportunidad: viajar a una isla misteriosa."
    elif "demon slayer" in t or "kimetsu" in t:
        return "Tanjiro Kamado emprende un viaje peligroso para encontrar una cura para su hermana Nezuko."
    
    return "¡Un emocionante anime de esta temporada! Visita MyAnimeList para leer la sinopsis completa."

def actualizar_estrenos():
    print("Actualizando estrenos de la temporada...")
    url = "https://api.jikan.moe/v4/seasons/now"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        datos = response.json()
        lista = []
        
        # Tomamos los primeros 4 animes para no saturar la página
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
        print("✅ estrenos.json actualizado con éxito.")

    except Exception as e:
        print(f"❌ Error al actualizar estrenos: {e}")

def actualizar_trailers():
    print("Actualizando nuevos trailers...")
    # Usamos el endpoint de 'upcoming' (próximos) para obtener trailers de novedades
    url = "https://api.jikan.moe/v4/seasons/upcoming"
    try:
        # Esperamos un poco antes de la siguiente petición para no estresar el router
        time.sleep(2) 
        
        response = requests.get(url, headers=headers, timeout=10)
        datos = response.json()
        lista = []
        
        # Buscamos animes que tengan video de YouTube
        for anime in datos.get('data', []):
            trailer_url = anime.get('trailer', {}).get('url')
            if trailer_url and len(lista) < 3: # Solo ocupamos 3 trailers
                lista.append({
                    "titulo": anime.get('title', 'Próximo estreno'),
                    "video": trailer_url,
                    "imagen": anime.get('images', {}).get('jpg', {}).get('large_image_url', '')
                })
        
        with open('trailers.json', 'w', encoding='utf-8') as f:
            json.dump(lista, f, ensure_ascii=False, indent=4)
        print("✅ trailers.json actualizado con éxito.")

    except Exception as e:
        print(f"❌ Error al actualizar trailers: {e}")

if __name__ == "__main__":
    actualizar_estrenos()
    actualizar_trailers()
    print("\n--- Proceso terminado. Todos los archivos JSON están listos. ---")
