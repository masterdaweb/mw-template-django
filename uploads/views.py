from urllib.parse import urlencode

from django.conf import settings
from django.core.files.storage import default_storage
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .models import Upload
from .texts import texts


def _probe(fn):
    try:
        return {'ok': True, 'detail': fn()}
    except Exception as e:  # each part reports its own failure
        return {'ok': False, 'detail': str(e).splitlines()[0][:160] if str(e) else type(e).__name__}


def _database():
    if connection.vendor != 'postgresql':
        raise RuntimeError('DATABASE_URL is empty: connect a database to this service')
    with connection.cursor() as cursor:
        cursor.execute('select version()')
        return ' '.join(cursor.fetchone()[0].split()[:2])


def _storage():
    bucket = settings.STORAGES['default']['OPTIONS']['bucket_name']
    if not bucket:
        raise RuntimeError('AWS_BUCKET is empty: connect a bucket to this service')
    default_storage.connection.meta.client.head_bucket(Bucket=bucket)
    return bucket


def checks():
    return {'database': _probe(_database), 'storage': _probe(_storage)}


def home(request):
    c = checks()
    uploads = list(Upload.objects.all()[:12]) if c['database']['ok'] else []
    t = texts(request)
    sent = request.GET.get('sent')
    error = request.GET.get('error')
    return render(request, 'uploads/home.html', {
        't': t,
        'lang': 'pt-BR' if t['title'].startswith('Seu') else 'en',
        'checks': [
            {'key': 'database', 'name': 'PostgreSQL', **c['database']},
            {'key': 'storage', 'name': 'Object Storage', **c['storage']},
        ],
        'uploads': uploads,
        'sent': t['sent'].format(name=sent) if sent else None,
        'error': (t['empty'] if error == 'empty' else t['failed']) if error else None,
    })


@require_POST
def upload(request):
    f = request.FILES.get('file')
    if not f or not f.size:
        return redirect('/?error=empty')
    try:
        Upload.objects.create(file=f, name=f.name, size=f.size)
    except Exception:
        import logging
        logging.getLogger(__name__).exception('upload failed')
        return redirect('/?error=failed')
    return redirect('/?' + urlencode({'sent': f.name}))


def health(_request):
    return JsonResponse({'ok': True})


def status(_request):
    c = checks()
    ok = all(v['ok'] for v in c.values())
    return JsonResponse({'ok': ok, 'checks': c}, status=200 if ok else 503)
