# 🎮 GamesSavioBack - Letterboxd de Jogos

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=for-the-badge&logo=sqlalchemy&logoColor=white)

## 📋 Sobre o Projeto

O **GamesSavioBack** é uma API robusta desenvolvida para servir como backend de uma plataforma de descoberta, avaliação e monitoramento de preços de jogos, inspirada no Letterboxd. O sistema permite que usuários acompanhem lançamentos, avaliem jogos, criem listas de monitoramento de preços e recebam alertas sobre promoções.

A aplicação integra-se com APIs externas renomadas (**RAWG** para metadados de jogos e **IsThereAnyDeal** para monitoramento de preços) para manter sua base de dados sempre atualizada.

---

## 🚀 Funcionalidades Principais

### 👤 Usuários e Autenticação
- Registro e Login seguro com JWT (Access e Refresh Tokens).
- Gerenciamento de perfil.

### 🎮 Catálogo de Jogos
- Base de dados rica sincronizada com a **RAWG API**.
- Busca avançada por categorias, plataformas e popularidade (Hype Score).
- Detalhes completos: descrição, data de lançamento, metacritic, imagens, etc.

### ⭐ Avaliações e Social
- Sistema de notas (0-5) e comentários.
- Feed de últimas avaliações da comunidade.
- Média de notas por jogo.

### 💰 Monitoramento de Preços
- Integração com **IsThereAnyDeal** para histórico de preços.
- Criação de alertas de preço personalizado.
- Notificação quando um jogo atinge o preço alvo.

### 🛠️ Backoffice
- Rotas administrativas para sincronização manual de jogos e preços.
- Gestão de dados mestres.

---

## 🏗️ Arquitetura e Tecnologias

O projeto segue uma arquitetura em camadas visando desacoplamento e facilidade de manutenção:

- **Linguagem**: Python 3.12+
- **Framework Web**: FastAPI (Alta performance e validação automática)
- **Banco de Dados**: PostgreSQL
- **ORM**: SQLAlchemy (Async)
- **Migrações**: Alembic (implícito)
- **Autenticação**: PyJWT + Passlib (Bcrypt)
- **Monitoramento**: Uvicorn

### Estrutura de Pastas
```
app/
├── core/           # Configurações globais e segurança
├── database/       # Conexão com BD e sessões
├── models/         # Entidades do banco de dados (SQLAlchemy)
├── routers/        # Endpoints da API (Controllers)
├── schemas/        # Modelos de validação (Pydantic)
├── services/       # Regras de negócio e integração externa
└── utils/          # Funções auxiliares
```

---

## ⚡ Instalação e Execução

### Pré-requisitos
- Python 3.12+
- PostgreSQL
- Virtualenv

### 1. Clone o repositório
```bash
git clone https://github.com/luan313/gamessavioback.git
cd gamessavioback
```

### 2. Crie e ative o ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configuração do Ambiente (.env)
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Banco de Dados
DATABASE_URL=postgresql+asyncpg://usuario:senha@localhost:5432/nome_do_banco

# Segurança
SECRET_KEY=sua_chave_secreta_super_segura
REFRESH_SECRET_KEY=sua_chave_refresh_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Integrações Externas
RAWG_API_KEY=sua_api_key_rawg
RAWG_BASE_URL=https://api.rawg.io/api
ANY_DEAL_API_KEY=sua_api_key_isthereanydeal
ANY_DEAL_BASE_URL=https://api.isthereanydeal.com
BACKOFFICE_TOKEN=token_para_rotas_admin
```

### 5. Execute a aplicação
```bash
uvicorn app.main:app --reload
```
A API estará disponível em `http://localhost:8000`.

---

## 📖 Documentação da API

O FastAPI gera documentação interativa automaticamente. Após rodar o projeto, acesse:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Principais Rotas

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/auth/login` | Autenticação de usuário |
| `POST` | `/auth/register` | Cadastro de novo usuário |
| `GET` | `/game/hyped-games` | Listar jogos populares |
| `GET` | `/avaliacoes/last-five-avaliations` | Últimas avaliações da comunidade |
| `POST` | `/monitoramentos/` | Criar alerta de preço |
| `POST` | `/backoffice/sync-games` | Sincronizar jogos (Admin) |

---

## 🤝 Contribuição

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/MinhaFeature`)
3. Adicione suas mudanças (`git add .`)
4. Comite suas mudanças (`git commit -m ':sparkles: feature: Minha nova feature'`)
5. Faça o Push (`git push origin feature/MinhaFeature`)
6. Abra um Pull Request

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

Desenvolvido com 💜 por [Luis]
