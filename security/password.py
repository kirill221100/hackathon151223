from passlib.context import CryptContext

pass_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_pass(plain, hashed):
    return pass_context.verify(plain, hashed)


def hash_password(password):
    return pass_context.hash(password)
