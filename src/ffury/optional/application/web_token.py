import jwt

def encode(secret: str, **kwargs) -> str:
    return jwt.encode(dict(**kwargs),
                      key=secret,
                      algorithm="HS256")
