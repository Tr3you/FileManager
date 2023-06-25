from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
import firebase_admin
from firebase_admin import credentials
from datetime import datetime
from tempfile import gettempdir
from firebase_admin import storage
from .models import File, User

cred = credentials.Certificate("./firebase_key.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'filesadmin.appspot.com'})

@require_http_methods(['GET', 'POST'])
def login(request):
    return HttpResponse('Pagina login')

@require_http_methods(['GET', 'POST'])
def register(request):
    return HttpResponse('Pagina signup')

@require_http_methods(['GET', 'POST'])
def my_files(request):
    files = list(File.objects.filter(user=1, is_deleted=False))
    return render(request, 'files.html', {
        'file_id': None,
        'files': files
    })

@require_http_methods(['GET', 'POST'])
def upload(request):
    if request.method == 'POST':
        bucket = storage.bucket()
        blob = bucket.blob('user_1/' + request.FILES["file"].name)
        blob.upload_from_file(request.FILES["file"])
        File.objects.create(
            name=request.FILES["file"].name.split('.')[0], 
            size= request.FILES["file"].size,
            type=request.FILES["file"].content_type,
            last_modified=datetime.fromtimestamp(int(request.POST['last_modified']) / 1000).date().isoformat(),
            date_deleted=None,
            date_updated=datetime.now().date().isoformat(),
            download_url='user_1/' + request.FILES["file"].name,
            is_favorite=False,
            is_deleted=False,
            user= User.objects.get(id=1)
        )

        return redirect('files')
    else:
        return render(request, 'upload.html')

@require_http_methods(['GET', 'POST'])
def favorites(request):
    files = list(File.objects.filter(user=1, is_favorite=True, is_deleted=False))
    return render(request, 'favorites.html', {
        'file_id': None,
        'files': files
    })

@require_http_methods(['GET', 'POST'])
def trash_bin(request):
    files = list(File.objects.filter(user=1, is_deleted=True))
    return render(request, 'trash.html', {
        'file_id': None,
        'files': files
    })

@require_http_methods(['GET', 'POST'])
def load_file_info(request, file_id, page_id):
    page = 'files.html' if page_id == 0 else 'favorites.html' if page_id == 1 else 'trash.html'
    if page_id == 0:
        page = 'files.html'
        files = files = list(File.objects.filter(user=1))
    elif page_id == 1:
        page = 'favorites.html'
        files = list(File.objects.filter(user=1, is_favorite=True))
    elif page_id == 2:
        page = 'trash.html'
        files = list(File.objects.filter(user=1, is_deleted=True))

    select_file = File.objects.get(id=file_id)
    return render(request, page,{
        'file_id': file_id,
        'files': files,
        'file_info':{
            'name': select_file.name if len(select_file.name) <= 20 else select_file.name[:21]+ '...',
            'type': select_file.type if len(select_file.type) <= 25 else select_file.type[:26]+ '...',
            'size': str(int(select_file.size / 1000)) + 'KB' if select_file.size < 1000000 else str(round(select_file.size / 1000000, 2)) + "MB",
            'last_modified': select_file.last_modified,
            'date_updated': select_file.date_updated,
        }
    })

@require_http_methods(['GET', 'POST'])
def download_file(request, path):
    file_path = path
    bucket = storage.bucket()
    blob = bucket.blob(file_path)
    file = blob.download_as_bytes()
    response = HttpResponse(file, content_type=blob.content_type)
    response['Content-Disposition'] = f'attachment; filename="{path.split("/")[1]}"'
    return response

@require_http_methods(['GET', 'POST'])
def mark_as_favorite(request, file_id, page_id):
    file = File.objects.get(id=file_id);
    file.is_favorite = not file.is_favorite
    file.save()
    if page_id == 0 and file.is_favorite == False:
        return redirect("files")
    else:
        return redirect("favorites")
    
@require_http_methods(['GET', 'POST'])
def mark_as_deleted(request, file_id, page_id):
    file = File.objects.get(id=file_id);
    file.is_deleted = not file.is_deleted
    file.save()
    if page_id == 0:
        return redirect("trash")
    elif page_id == 2:
        return redirect("files")