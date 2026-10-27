# Django na Master da Web

Um projeto Django 6 com PostgreSQL, os arquivos enviados no Object Storage (django-storages), Gunicorn e as migrações a cada deploy.

| Serviço | O que roda |
| --- | --- |
| `web` | Gunicorn; `python manage.py migrate` roda uma vez por deploy; `collectstatic` roda no build e o WhiteNoise serve o CSS do admin |

O banco chega como `DATABASE_URL`; o bucket público como `AWS_*`, os nomes que o django-storages lê; o `DJANGO_SECRET_KEY` foi gerado para você. Os arquivos do `FileField` vão para o bucket e são servidos pelo endereço público dele.

A página inicial envia arquivos e mostra cada um. Para o admin, crie um usuário pela aba Terminal do serviço: `python manage.py createsuperuser`, e entre em `/admin`.

## Torne o código seu

1. No console, abra o projeto e siga **Seu código**: copie este template
   para o seu GitHub e conecte a cópia ao projeto.
2. Altere `uploads/views.py` e `uploads/templates/` e faça push: cada push faz um deploy, sem tirar o
   app do ar.

## Rodar na sua máquina

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
export DJANGO_DEBUG=true DATABASE_URL=postgresql://app:app@localhost:5432/app
python manage.py migrate && python manage.py runserver
```

## Bom saber

- O banco é acessado pelo pooler em modo transação: `DISABLE_SERVER_SIDE_CURSORS` já está ligado.

*[English](README.en.md)*
