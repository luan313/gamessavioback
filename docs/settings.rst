Settings
========

Configurações da aplicação definidas via variáveis de ambiente.

.. toctree::
   :maxdepth: 2

   app.core.config

Variáveis de Ambiente
---------------------

Crie um arquivo ``.env`` na raiz do projeto com as seguintes chaves:

Banco de Dados
~~~~~~~~~~~~~~

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Variável
     - Descrição
   * - ``DATABASE_URL``
     - URL de conexão com o PostgreSQL (ex: ``postgresql+asyncpg://user:pass@localhost/db``).
   * - ``REDIS_URL``
     - URL de conexão com o Redis (ex: ``redis://localhost:6379``).

Segurança
~~~~~~~~~

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Variável
     - Descrição
   * - ``SECRET_KEY``
     - Chave secreta para assinatura de tokens JWT.
   * - ``REFRESH_SECRET_KEY``
     - Chave secreta exclusiva para Refresh Tokens.
   * - ``ALGORITHM``
     - Algoritmo de criptografia (padrão: ``HS256``).
   * - ``ACCESS_TOKEN_EXPIRE_MINUTES``
     - Tempo de expiração do Access Token em minutos.
   * - ``REFRESH_TOKEN_EXPIRE_DAYS``
     - Tempo de expiração do Refresh Token em dias.

Integrações Externas
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Variável
     - Descrição
   * - ``RAWG_API_KEY``
     - Chave de API da RAWG (metadados de jogos).
   * - ``RAWG_BASE_URL``
     - URL base da API RAWG.
   * - ``ANY_DEAL_API_KEY``
     - Chave de API da IsThereAnyDeal (preços).
   * - ``ANY_DEAL_BASE_URL``
     - URL base da API IsThereAnyDeal.
   * - ``BACKOFFICE_TOKEN``
     - Token estático para proteger rotas administrativas.

Notificações (Email)
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Variável
     - Descrição
   * - ``EMAIL_HOST``
     - Servidor SMTP (ex: ``smtp.gmail.com``).
   * - ``EMAIL_PORT``
     - Porta do servidor SMTP (ex: ``587``).
   * - ``EMAIL_USER``
     - Email remetente.
   * - ``EMAIL_PASSWORD``
     - Senha de aplicativo do email.
