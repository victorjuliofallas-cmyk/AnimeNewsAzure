def actualizar_trailers():
    url = "https://api.jikan.moe/v4/seasons/upcoming"
    try:
        time.sleep(2) 
        response = requests.get(url, headers=headers, timeout=10)
        datos = response.json()
        lista = []
        for anime in datos.get('data', []):
            trailer_url = anime.get('trailer', {}).get('url')
            
            if trailer_url and len(lista) < 6:
                # MAGIA: Convertimos el link normal a link de EMBED
                # De: https://www.youtube.com/watch?v=abc
                # A: https://www.youtube.com/embed/abc
                video_id = ""
                if "v=" in trailer_url:
                    video_id = trailer_url.split("v=")[1].split("&")[0]
                elif "youtu.be/" in trailer_url:
                    video_id = trailer_url.split("youtu.be/")[1].split("?")[0]
                
                embed_link = f"https://www.youtube.com/embed/{video_id}"

                lista.append({
                    "titulo": anime.get('title', 'Próximo estreno'),
                    "video": embed_link,
                    "imagen": anime.get('images', {}).get('jpg', {}).get('large_image_url', '')
                })
        
        with open('trailers.json', 'w', encoding='utf-8') as f:
            json.dump(lista, f, ensure_ascii=False, indent=4)
        print("✅ trailers.json actualizado con links REALES y funcionales.")
    except Exception as e:
        print(f"Error: {e}")
