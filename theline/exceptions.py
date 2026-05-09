from rest_framework.exceptions import APIException
from rest_framework import status

class EstoqueInsuficiente(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Não temos estoque suficiente para este produto.'
    default_code = 'estoque_insuficiente'