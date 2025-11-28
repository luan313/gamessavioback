Examples
========

Exemplos práticos de como interagir com a API GamesSavio.

Autenticação
------------

Para acessar endpoints protegidos, você primeiro precisa obter um token de acesso.

**Login**

.. code-block:: bash

    curl -X 'POST' \
      'http://localhost:8000/auth/login' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "email": "user@example.com",
      "password": "password123"
    }'

**Resposta de Sucesso:**

.. code-block:: json

    {
      "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
      "refresh_token": "eyJhbGciOiJIUzI1NiIsIn...",
      "token_type": "bearer"
    }

Buscar Jogos
------------

Você pode buscar jogos por nome.

**Requisição**

.. code-block:: bash

    curl -X 'GET' \
      'http://localhost:8000/game/search?name=Elden' \
      -H 'accept: application/json'

**Resposta:**

.. code-block:: json

    {
      "items": [
        {
          "id": "550e8400-e29b-41d4-a716-446655440000",
          "nome": "Elden Ring",
          "slug": "elden-ring",
          "nota_media": 4.8
        }
      ],
      "total": 1,
      "page": 1,
      "size": 20
    }

Criar Alerta de Preço
---------------------

Monitorar o preço de um jogo específico. Requer autenticação.

**Requisição**

.. code-block:: bash

    curl -X 'POST' \
      'http://localhost:8000/monitoramentos/create' \
      -H 'accept: application/json' \
      -H 'Authorization: Bearer SEU_ACCESS_TOKEN' \
      -H 'Content-Type: application/json' \
      -d '{
      "game_id": "550e8400-e29b-41d4-a716-446655440000",
      "preco_alvo": 150.00,
      "ativo": true
    }'

**Resposta:**

.. code-block:: json

    {
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "game_id": "550e8400-e29b-41d4-a716-446655440000",
      "preco_alvo": 150.00,
      "ativo": true,
      "created_at": "2024-11-27T12:00:00"
    }
