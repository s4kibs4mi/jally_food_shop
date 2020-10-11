import jwt


def encode(user_id):
    return jwt.encode({'user_id': user_id}, 'secret', algorithm='HS256')


def decode(token):
    return jwt.decode(token, 'secret', algorithms='HS256')
