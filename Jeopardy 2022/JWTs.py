"""Can you find the valid (on the 2022-06-01 at 12:00) JWT?"""

# tshark -r file.pcap -Y 'http contains "Bearer "' -T fields -e http.authorization > jwt_tokens.txt
# grep -oP 'eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+' jwt_tokens.txt > cleaned_jwts.txt


import base64
import json

def decode_jwt(jwt):
    try:
        payload_encoded = jwt.split('.')[1]
        payload_encoded += '=' * ((4 - len(payload_encoded) % 4) % 4)
        return json.loads(base64.urlsafe_b64decode(payload_encoded))
    except:
        return None

target_time = 1654084800  # 2022-06-01 12:00 UTC

with open("cleaned_jwts.txt", "r") as f:
    for line in f:
        jwt = line.strip()
        if not jwt:
            continue
        payload = decode_jwt(jwt)
        if not payload:
            continue
        
        # Controlla se il token era valido al target_time
        valid = True
        if 'nbf' in payload and payload['nbf'] > target_time:
            valid = False  # Non ancora valido
        if 'exp' in payload and payload['exp'] < target_time:
            valid = False  # Già scaduto
        
        if valid:
            print(f"✅ Token valido il 2022-06-01 12:00 UTC:")
            print(f"   JWT: {jwt}")
            print(f"   Payload: {json.dumps(payload, indent=2)}")
            if 'flag' in payload:
                print(f"   🔥 Flag nel payload: {payload['flag']}")