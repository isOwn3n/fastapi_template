from datetime import datetime, timedelta
import pytz

from fastapi import HTTPException
from schema import JWTData

from settings import config
from jose import JWTError, jwt
from http import HTTPStatus

ALGORITHM = "HS256"


def token_generate(data: JWTData, expires_delta: timedelta | None = None) -> str:
    """Generate token"""
    to_encode = data.model_dump().copy()
    if expires_delta:
        expire = pytz.timezone("Asia/Tehran").localize(expires_delta)
    else:
        expire = (
            datetime.utcnow() + timedelta(hours=1)
        )
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, config.secret, algorithm=ALGORITHM)
    return encode_jwt


def token_validator(token: str) -> JWTData:
    """Validate token"""
    try:
        raw_data = jwt.decode(token, config.secret, ALGORITHM)
        return JWTData(roles=raw_data["roles"], user_id=raw_data["user_id"])
    except JWTError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
    except KeyError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

def token_exp_date(token: str):
    try:
        raw_data = jwt.decode(token, config.secret, ALGORITHM)
        return raw_data["exp"]
    except JWTError:
        raise HTTPException(
            HTTPStatus.UNAUTHORIZED,
            "Invalid Or Expired Token.",
        )
    except KeyError:
        raise HTTPException(
            HTTPStatus.UNAUTHORIZED,
            "Invalid Or Expired Token.",
        )
