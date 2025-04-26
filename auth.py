from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from urllib.parse import parse_qs
import hmac
import hashlib

def verify_webapp_signature(bot_token: str, init_data: str) -> bool:
    try:
        parsed_data = parse_qs(init_data)
        hash_str = parsed_data.get('hash', [''])[0]
        data_check_str = '\n'.join(
            f"{key}={value[0]}" 
            for key, value in sorted(parsed_data.items()) 
            if key != 'hash'
        )

        secret_key = hmac.new(
            key=b"WebAppData",
            msg=bot_token.encode(),
            digestmod=hashlib.sha256
        ).digest()

        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=None,
        ).derive(secret_key)
        
        computed_hash = hmac.new(
            derived_key,
            data_check_str.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return computed_hash == hash_str
    except:
        return False