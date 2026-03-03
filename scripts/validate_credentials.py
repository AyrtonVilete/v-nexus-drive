import json
import sys

REQUIRED_KEYS = ["type", "project_id", "private_key", "client_email"]

def load_env(path='.env'):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip().startswith('GOOGLE_CREDENTIALS_JSON='):
                    # split at first '=' and take remainder
                    _, val = line.split('=', 1)
                    # If value starts with { assume JSON inline, else accumulate following lines
                    val = val.strip()
                    if val.startswith('{') and val.endswith('}'):
                        return val
                    # Otherwise read until closing brace
                    if val.startswith('{'):
                        buffer = [val]
                        for l in f:
                            buffer.append(l.rstrip('\n'))
                            if l.strip().endswith('}'): break
                        return '\n'.join(buffer)
        return None
    except FileNotFoundError:
        print('.env not found')
        return None


def main():
    raw = load_env()
    if not raw:
        print('GOOGLE_CREDENTIALS_JSON not found in .env')
        sys.exit(2)
    try:
        obj = json.loads(raw)
    except Exception as e:
        print('Invalid JSON:', e)
        sys.exit(3)
    missing = [k for k in REQUIRED_KEYS if k not in obj]
    if missing:
        print('Missing keys:', missing)
        sys.exit(4)
    # basic checks
    pk = obj.get('private_key','')
    if 'BEGIN PRIVATE KEY' not in pk or 'END PRIVATE KEY' not in pk:
        print('private_key does not look like a PEM block')
        sys.exit(5)
    print('GOOGLE_CREDENTIALS_JSON looks valid. Keys:', list(obj.keys()))
    sys.exit(0)

if __name__ == '__main__':
    main()
