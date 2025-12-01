Installation
============

Como instalar e rodar o projeto GamesSavio.

Pré-requisitos
--------------
- Python 3.12+
- PostgreSQL
- Virtualenv

1. Clone o repositório
----------------------

.. code-block:: bash

    git clone https://github.com/luan313/gamessavioback.git
    cd gamessavioback

2. Crie e ative o ambiente virtual
----------------------------------

.. code-block:: bash

    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # ou
    venv\Scripts\activate     # Windows

3. Instale as dependências
--------------------------

.. code-block:: bash

    pip install -r requirements.txt

4. Configuração do Ambiente (.env)
----------------------------------

Crie um arquivo ``.env`` na raiz do projeto com as seguintes variáveis:

.. code-block:: text

    # Banco de Dados
    # Banco de Dados
    DATABASE_URL=postgresql+asyncpg://usuario:senha@localhost:5432/nome_do_banco

    # Nota: Certifique-se de criar o banco de dados 'nome_do_banco' no PostgreSQL antes de rodar a aplicação.


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

    # Email (Notificações)
    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_USER=seu_email@gmail.com
    EMAIL_PASSWORD=sua_senha_de_app

5. Execute a aplicação
----------------------

.. code-block:: bash

    uvicorn app.main:app --reload

A API estará disponível em ``http://localhost:8000``.
