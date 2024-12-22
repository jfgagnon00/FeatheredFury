import jwt

def decode(secret: str, enocded_playload: str) -> dict:
    try:
        return jwt.decode(enocded_playload, 
                          key=secret,
                          algorithms=["HS256"])
    except:
        return None
