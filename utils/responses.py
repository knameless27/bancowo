from rest_framework.response import Response
from rest_framework import status

def api_response(success=True, message="", data=None, code=status.HTTP_200_OK, errors=None):
    return Response({
        "success": success,
        "message": message,
        "data": data,
        "errors": errors
    }, status=code)
