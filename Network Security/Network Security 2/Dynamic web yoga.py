def r(s: str, i: int) -> str:
    def shift(c):
        if c.isalpha():
            limit = ord('Z') if c.isupper() else ord('z')
            new_c = ord(c) + i
            return chr(new_c if new_c <= limit else new_c - 26)
        return c
    
    return ''.join(shift(c) for c in s)

print(r("qngn:grkg/synt;onfr64,D0AWIUgxo3qhq2SlMN==", 13))