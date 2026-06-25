from django.core.management.base import BaseCommand
from django.core.management import call_command
from theline.models import Produto

class Command(BaseCommand):
    help = 'Carrega dados iniciais se a base de dados estiver vazia e inicia o runserver'

    def handle(self, *args, **options):
        if not Produto.objects.exists():
            self.stdout.write(self.style.WARNING('Base de dados vazia. A carregar dados iniciais...'))
            call_command('loaddata', 'dados_iniciais.json') 
            self.stdout.write(self.style.SUCCESS('Dados carregados com sucesso!'))
        else:
            self.stdout.write(self.style.SUCCESS('Os dados já existem. A ignorar o carregamento.'))

        self.stdout.write(self.style.SUCCESS('A iniciar o servidor de desenvolvimento...'))
        
        call_command('runserver', '0.0.0.0:8000')