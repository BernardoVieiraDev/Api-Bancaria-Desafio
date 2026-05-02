import jwt
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

payload = {
    "user_id": 123,
    "username": "johndoe",
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1) # Expires in 1 hour
}

# 3. Generate the token
token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM) # type: ignore

print(token)