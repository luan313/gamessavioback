from fastapi import APIRouter, Request
from app.core.auth_config import oauth  

router = APIRouter()

@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for('auth_google')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/google")
async def auth_google(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        
        user_info = token.get('userinfo')
        
        request.session['user'] = user_info
        
        return {"status": "sucesso", "user": user_info}


    except Exception as e:
        return {"error": str(e)}