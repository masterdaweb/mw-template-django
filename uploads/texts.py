"""The page in the visitor's language (Django's LocaleMiddleware picks it)."""

EN = {
    'title': 'Your Django app is live',
    'lead': 'PostgreSQL for the data and Object Storage for the files people send: what you upload below goes to the bucket through django-storages, and its row to the database.',
    'reaches': 'What this app reaches',
    'send': 'Send a file',
    'file': 'File',
    'submit': 'Send to Object Storage',
    'sent': '{name} was saved.',
    'empty': 'Choose a file first.',
    'failed': 'The file could not be saved. See the service logs.',
    'none': 'No files yet.',
    'next': 'Next steps',
    'step1': 'Make the code yours: in the console, open this project and follow “Your code” to copy it to your GitHub and connect it.',
    'step2': 'Create an admin user from the service’s Terminal tab: python manage.py createsuperuser — then sign in at /admin.',
    'step3': 'Change uploads/views.py and its template, then push: migrations run once, before the new version takes traffic.',
}

PT = {
    'title': 'Seu app Django está no ar',
    'lead': 'PostgreSQL para os dados e Object Storage para os arquivos que as pessoas enviam: o que você enviar abaixo vai para o bucket pelo django-storages, e a linha dele para o banco.',
    'reaches': 'O que este app alcança',
    'send': 'Envie um arquivo',
    'file': 'Arquivo',
    'submit': 'Enviar para o Object Storage',
    'sent': '{name} foi salvo.',
    'empty': 'Escolha um arquivo primeiro.',
    'failed': 'Não foi possível salvar o arquivo. Veja os logs do serviço.',
    'none': 'Nenhum arquivo ainda.',
    'next': 'Próximos passos',
    'step1': 'Torne o código seu: no console, abra este projeto e siga “Seu código” para copiá-lo para o seu GitHub e conectá-lo.',
    'step2': 'Crie um usuário de admin pela aba Terminal do serviço: python manage.py createsuperuser — e entre em /admin.',
    'step3': 'Altere uploads/views.py e o template dele e faça push: as migrações rodam uma vez, antes de a nova versão receber tráfego.',
}


def texts(request):
    return PT if getattr(request, 'LANGUAGE_CODE', 'en').startswith('pt') else EN
