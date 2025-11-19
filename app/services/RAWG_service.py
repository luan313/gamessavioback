
from dotenv import load_dotenv
import math
import requests
import time
from app.core.config import settings
from datetime import datetime
from app.models.game import Game
from app.models.categoria import Categoria
from app.models.game_categoria import GameCategoria
from app.models.plataforma import Plataforma
from app.models.game_plataforma import GamePlataforma
load_dotenv()

class rawg_service:        
    @staticmethod
    def __import_game_from_response(game_data: dict, db):
        print(f"Importando: {game_data['name']}...")
        
        if game_data.get("released"):
            try:
                release_date = datetime.strptime(game_data["released"], "%Y-%m-%d").date()
            except ValueError:
                pass
        rawg_id = game_data.get("id")
        game = db.query(Game).filter(Game.rawg_id == rawg_id).first()
        
        if not game:
            game = Game(
                nome=game_data.get("name"), 
                slug=game_data.get("slug"),
                rawg_id=rawg_id,
                metacritic=game_data.get("metacritic"),
                imagem_capa=game_data.get("background_image"),
                data_lancamento=release_date,
                descricao=f"Released: {game_data.get('released')}"
            )
            db.add(game)
            db.flush()
        else:
            game.nome = game_data.get("name") 
            game.metacritic = game_data.get("metacritic")
            game.imagem_capa = game_data.get("background_image")
            game.updated_at = datetime.now()
        
        if "genres" in game_data:
            for genre_data in game_data["genres"]:
                cat_nome = genre_data["name"]
                cat_slug = genre_data.get("slug")
                categoria = db.query(Categoria).filter(Categoria.nome == cat_nome).first()
                
                if not categoria:
                    categoria = Categoria(nome=cat_nome, slug=cat_slug)
                    db.add(categoria)
                    db.flush()
                    
                link_existente = db.query(GameCategoria).filter_by(
                    game_id=game.id, 
                    categoria_id=categoria.id
                ).first()
                
                if not link_existente:
                    novo_link = GameCategoria(game_id=game.id, categoria_id=categoria.id)
                    db.add(novo_link)
                    
        if "platforms" in game_data:            
            for p_wrapper in game_data["platforms"]:
                p_data = p_wrapper["platform"]
                plat_nome = p_data["name"]
                plat_slug = p_data.get("slug")
                
                plataforma = db.query(Plataforma).filter(Plataforma.nome == plat_nome).first()
                if not plataforma:
                    plataforma = Plataforma(nome=plat_nome, slug=plat_slug)
                    db.add(plataforma)
                    db.flush()
                    
                link_plat_existente = db.query(GamePlataforma).filter_by(
                    game_id=game.id, 
                    plataforma_id=plataforma.id
                ).first()
                
                if not link_plat_existente:
                    novo_link_plat = GamePlataforma(game_id=game.id, plataforma_id=plataforma.id)
                    db.add(novo_link_plat)
        
        try:
            db.commit()
            print(f"✅ Sucesso: {game.nome} salvo/atualizado!")
            return game
        except Exception as e:
            db.rollback()
            print(f"❌ Erro ao salvar {game_data['name']}: {e}")
            raise e
                  
        
    @staticmethod                 
    def seed_games_by_amount(db, amount=80):
        page_size = 40
        total_importado = 0
        total_pages = math.ceil(amount / page_size)
        print(f"--- Iniciando Carga de {amount} jogos ({total_pages} requisições) ---")

        for page in range(1, total_pages + 1):
            print(f"Requisitando página {page}/{total_pages}...")
                
            params = {
                "key": settings.RAWG_API_KEY,
                "page_size": page_size,
                "ordering": "-added",
                "page": page
            }
                
            try:
                resp = requests.get(settings.RAWG_BASE_URL, params=params)
                    
                if resp.status_code == 429:
                    print("Rate Limit atingido! Esperando 10 segundos...")
                    time.sleep(10)
                    continue 
                        
                if resp.status_code != 200:
                    print(f"Erro API: {resp.status_code}")
                    break

                data = resp.json()
                results = data.get("results", [])
                    
                if not results:
                    print("Fim dos resultados na API.")
                    break

                for game_json in results:
                    try:
                        print(rawg_service.__import_game_from_response(game_json, db))
                        total_importado += 1
                            
                    except Exception as e_db:
                        print(f"Skipping {game_json.get('name')}: {e_db}")
                            
                    time.sleep(0.5)

            except Exception as e:
                print(e)
        
        print(f"--- ✅ Carga Finalizada! Total processado: {total_importado} jogos ---")
        return {"status": "success", "total": total_importado}


