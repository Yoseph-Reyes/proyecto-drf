from urllib import parse

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed



@database_sync_to_async
def get_user(token):
    auth = authentication.JWTAuthentication()
    try:
        token = auth.get_validated_token(token)
        user = auth.get_user(token)
    except (InvalidToken, AuthenticationFailed):
        return AnonymousUser()
    print("Logued in:", user.email)
    return user

class QueryAuthMiddleware(BaseMiddleware):

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_params = parse.parse_qs(scope['query_string'].decode())
        token_key = query_params.get('token', None)
        if token_key is not None:
            scope['user'] = await get_user(token_key[0])
        else:
            scope['user'] = AnonymousUser()
        return await super().__call__(scope, receive, send)
