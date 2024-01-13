import bcrypt


def generate_password(password):
    dec_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(dec_password, salt)
    return hashed_password

def check_password(password, hashed_password):
    result = bcrypt.checkpw(
        password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )
    return result
