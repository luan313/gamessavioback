Overview
========

O **GamesSavioBack** é uma API robusta desenvolvida para servir como backend de uma plataforma de descoberta, avaliação e monitoramento de preços de jogos, inspirada no Letterboxd. O sistema permite que usuários acompanhem lançamentos, avaliem jogos, criem listas de monitoramento de preços e recebam alertas sobre promoções.

A aplicação integra-se com APIs externas renomadas (**RAWG** para metadados de jogos e **IsThereAnyDeal** para monitoramento de preços) para manter sua base de dados sempre atualizada.

Funcionalidades Principais
--------------------------

Usuários e Autenticação
~~~~~~~~~~~~~~~~~~~~~~~
- Registro e Login seguro com JWT (Access e Refresh Tokens).
- Gerenciamento de perfil.

Catálogo de Jogos
~~~~~~~~~~~~~~~~~
- Base de dados rica sincronizada com a **RAWG API**.
- Busca avançada por categorias, plataformas e popularidade (Hype Score).
- Detalhes completos: descrição, data de lançamento, metacritic, imagens, etc.

Avaliações e Social
~~~~~~~~~~~~~~~~~~~
- Sistema de notas (0-5) e comentários.
- Feed de últimas avaliações da comunidade.
- Média de notas por jogo.

Monitoramento de Preços
~~~~~~~~~~~~~~~~~~~~~~~
- Integração com **IsThereAnyDeal** para histórico de preços.
- Criação de alertas de preço personalizado.
- Notificação quando um jogo atinge o preço alvo.
- Integração via Webhook para processamento de alertas em lote.

Backoffice
~~~~~~~~~~
- Rotas administrativas para sincronização manual de jogos e preços.
- Gestão de dados mestres.

Arquitetura e Tecnologias
-------------------------

O projeto segue uma arquitetura em camadas visando desacoplamento e facilidade de manutenção:

- **Linguagem**: Python 3.12+
- **Framework Web**: FastAPI (Alta performance e validação automática)
- **Banco de Dados**: PostgreSQL
- **ORM**: SQLAlchemy (Async)
- **Migrações**: Alembic (implícito)
- **Autenticação**: PyJWT + Passlib (Bcrypt)
- **Monitoramento**: Uvicorn

Estrutura de Pastas
~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    app/
    ├── core/           # Configurações globais e segurança
    ├── database/       # Conexão com BD e sessões
    ├── models/         # Entidades do banco de dados (SQLAlchemy)
    ├── routers/        # Endpoints da API (Controllers)
    ├── schemas/        # Modelos de validação (Pydantic)
    ├── services/       # Regras de negócio e integração externa
    └── utils/          # Funções auxiliares
