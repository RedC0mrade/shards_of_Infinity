from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from config import settings

http_bearer = HTTPBearer(auto_error=False)