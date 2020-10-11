from django.http.response import JsonResponse
from rest_framework import status
from rest_api import jwt
from jwt import exceptions


class AuthMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.path)

        if self.protected_routes(request.path):
            authenticated, user = self.is_authenticated(request)
            print(authenticated)
            print(user)

            if not authenticated:
                return JsonResponse({}, status=status.HTTP_403_FORBIDDEN)
            else:
                request.session['user_id'] = user

        return self.get_response(request)

    def protected_routes(self, current_route):
        routes = [
            'orders',
        ]

        for r in routes:
            print(r)
            print(current_route)

            if r in current_route:
                return True
        return False

    def is_authenticated(self, request):
        print("++ ", request.headers)

        try:
            token = request.headers['Authorization'].strip("Bearer").strip(" ")
            print(token)
            pld = jwt.decode(token)
            print("-- ", pld)
            return True, pld['user_id']
        except KeyError as e:
            print("-- ", e)
            return False, None
        except exceptions.InvalidSignatureError as e:
            print("-- ", e)
            return False, None
