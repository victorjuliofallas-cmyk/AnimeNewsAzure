import requests
import json
import time

# El disfraz para que la API no nos bloquee
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# --- FUNCIÓN DE TRADUCCIÓN/SINOPSIS EN ESPAÑOL ---
# Esto es necesario porque la API nos da todo en inglés.
def obtener_sinopsis_espanol(titulo_anime):
    t = titulo_anime.lower()

    # Aquí definimos sinopsis cortas y bonitas para los más probables
    if "frieren" in t:
        return "La elfa Frieren y sus compañeros derrotaron al Rey Demonio. Ahora, ella emprende un nuevo viaje para comprender a los humanos, cuyo tiempo de vida es mucho más corto que el suyo."
    elif "jujutsu kaisen" in t:
        return "Yuji Itadori es un estudiante con una fuerza física increíble. Para salvar a sus amigos de una maldición, se come el dedo de Sukuna, convirtiéndose en el recipiente del Rey de las Maldiciones."
    elif "jigokuraku" in t:
        return "Gabimaru, un ninja legendario condenado a muerte, recibe una última oportunidad: viajar a una isla misteriosa para encontrar el Elixir de la Inmortalidad para el Shogun."
    elif "demon slayer" in t or "kimetsu" in t:
        return "Tanjiro Kamado emprende un viaje peligroso para encontrar una cura para su hermana Nezuko, quien fue convertida en demonio tras el asesinato de su familia."
    elif "attack on titan" in t or "shingeki" in t:
        return "La humanidad vive aterrada por los Titanes. Eren Yeager y sus amigos se unen al Cuerpo de Exploración para exterminarlos y recuperar su libertad."

    # Si es un anime que no conocemos, usamos este mensaje genérico:
    return "¡Un emocionante anime de esta temporada! Visita MyAnimeList para leer la sinopsis completa en inglés y ver más detalles sobre este gran estreno."

def actualizar_estrenos():
    print("🤖 Bot: Buscando estrenos de la temporada...")
    # Esta es la API de Jikan (MyAnimeList)
    url = "https://api.jikan.moe/v4/seasons/now"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        datos = response.json()

        lista_estrenos = []

        # Tomamos los primeros 4 animes populares para la web
        for anime in datos.get('data', [])[:4]:
            titulo = anime.get('title', 'Sin título')
            print(f"   - Procesando: {titulo}")

            # ¡AQUÍ ESTÁ LA MAGIA! Obtenemos la sinopsis en español
            sinopsis_espanol = obtener_sinopsis_espanol(titulo)

            estreno = {
                "titulo": titulo,
                "imagen": anime.get('images', {}).get('jpg', {}).get('large_image_url', ''),
                "sinopsis": sinopsis_espanol, # Usamos la versión en español
                "link": anime.get('url', '#')
            }
            lista_estrenos.append(estreno)

        # Creamos el archivo que leerá la página web
        with open('estrenos.json', 'w', encoding='utf-8') as f:
            json.dump(lista_estrenos, f, ensure_ascii=False, indent=4)

        print("✅ Archivo estrenos.json actualizado con éxito con datos en español.")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    actualizar_estrenos()