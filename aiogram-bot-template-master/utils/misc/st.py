from stegano import lsb


def photo_use(photo, password):
    secret = lsb.hide(photo, str(password))
    secret.save("1.jpeg")
    return secret


def decode(photo):
    secret = lsb.reveal(photo)
    return secret

