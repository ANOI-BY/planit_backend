from typing import Annotated

from fastapi import Header, HTTPException


async def get_token_header(authorization: Annotated[str, Header()]):
    print(authorization)
    if authorization == '':
        raise HTTPException(status_code=400, detail="authorization header invalid")