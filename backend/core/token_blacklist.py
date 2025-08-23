blacklist=set()

def blacklist_token(token: str) -> None:
    blacklist.add(token)

def token_in_blacklist(token: str) -> bool:
    return token in blacklist