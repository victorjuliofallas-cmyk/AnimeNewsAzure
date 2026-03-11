import requests
import json
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

def obtener_sinopsis_espanol(titulo):
    t = titulo.lower()

    sinopsis = {
        "frieren": "La elfa Frieren viaja después de derrotar al Rey Demonio recordando a sus antiguos compañeros.",
        "jujutsu": "Yuji Itadori entra al mundo de las maldiciones tras ingerir un objeto maldito.",
        "demon slayer": "Tanjiro lucha contra demonios para salvar a su hermana Nezuko.",
        "one punch": "Saitama derrota enemigos de un solo golpe pero busca un rival digno."
    }

    for clave in sinopsis:
        if clave in t:
            return sinopsis[clave]

    return "Uno de los animes destacados de la temporada actual."

# --------------------------------------------------

def actualizar_estrenos():

    url = "https://api.jikan.moe/v4/seasons/now"

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print("Error API:", response.status_code)
            return

        datos = response.json()

        lista = []

        for anime in datos.get("data", [])[:24]:

            lista.append({
                "titulo": anime.get("title", "Sin título"),
                "imagen": anime.get("images", {}).get("jpg", {}).get("large_image_url", ""),
                "sinopsis": obtener_sinopsis_espanol(anime.get("title", "")),
                "link": anime.get("url", "#")
            })

        with open("estrenos.json", "w", encoding="utf-8") as f:
            json.dump(lista, f, ensure_ascii=False, indent=4)

        print("Estrenos actualizados")

    except Exception as e:
        print("Error en estrenos:", e)

# --------------------------------------------------

def actualizar_trailers():

    url = "https://api.jikan.moe/v4/seasons/upcoming"

    try:

        time.sleep(1)

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print("Error API trailers:", response.status_code)
            return

        datos = response.json()

        lista = []

        for anime in datos.get("data", []):

            trailer = anime.get("trailer")

            if trailer and trailer.get("embed_url"):

                lista.append({
                    "titulo": anime.get("title", "Próximo estreno"),
                    "video": trailer.get("embed_url"),
                    "imagen": anime.get("images", {}).get("jpg", {}).get("large_image_url", "")
                })

            if len(lista) >= 4:
                break

        with open("trailers.json", "w", encoding="utf-8") as f:
            json.dump(lista, f, ensure_ascii=False, indent=4)

        print("Trailers actualizados")

    except Exception as e:
        print("Error en trailers:", e)

# --------------------------------------------------

if __name__ == "__main__":

    actualizar_estrenos()

    time.sleep(2)

    actualizar_trailers()