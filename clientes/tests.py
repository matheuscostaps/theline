from django.urls import reverse # Importe o reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Cliente

class ClienteAPITest(APITestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nome="Ana Silva", 
            cpf="98765432100", 
            email="ana@teste.com"
        )

        self.url = reverse('cliente-list') 

    def test_get_lista_clientes(self):
        """Garante que a API retorna status 200 ao listar clientes"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)