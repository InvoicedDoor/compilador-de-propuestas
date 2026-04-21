import bcrypt

def password_encryption(password: str):
    try:
        salt = bcrypt.gensalt()

        password_bytes = password.encode("utf-8")

        hashed = bcrypt.hashpw(password_bytes, salt)

        return hashed
    
    except:
        raise ValueError("Error al encriptar")


def validate_password(password: str, hashed_password: str):
    try:
        password_bytes = password.encode("utf-8")

        hashed_password_bytes = hashed_password.encode("utf-8")

        hashed = bcrypt.checkpw(password_bytes, hashed_password_bytes)

        return hashed
    except Exception as ex:
        raise ValueError("Error al comprobar la contraseña: ", ex)