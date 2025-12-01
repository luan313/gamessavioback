
admin_responses = {
    401: {
        "description": "Não autenticado",
        "content": {
            "application/json": {
                "example": {"error": True, "message": "Não autenticado", "details": None}
            }
        }
    },
    403: {
        "description": "Proibido: Requer privilégios de Administrador",
        "content": {
            "application/json": {
                "example": {"error": True, "message": "Acesso negado", "details": None}
            }
        }
    }
}
