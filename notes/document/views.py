import uuid

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import Document


def index_view(request):
    if request.method != 'GET':
        return render(request, "errors/405.html", status=405)

    current_user = request.user
    documents = []
    if current_user.is_authenticated:
        documents = Document.objects.filter(creator=request.user)
    context = {
        'documents': documents,
        'user': current_user
    }
    return render(request, 'home.html', context=context)


def creator_view(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'creator.html', context=context)
    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        is_private = request.POST.get('is_private', False)
        creator_id = request.user
        document_id = uuid.uuid4()
        new_document = Document(id=document_id, title=title, content=content, is_private=is_private, creator=creator_id)
        new_document.save()

        return redirect(f'/note/{document_id}')
    else:
        return render(request, "errors/405.html", status=405)


@csrf_exempt
def editor_view(request, document_uid):
    print(request.method)
    if request.method == 'GET':
        print('got uid:', document_uid)
        document = Document.objects.filter(id=document_uid).first()
        if document is None:
            return render(request, "errors/404.html", status=404)
        context = {
            'document': document
        }
        return render(request, 'editor.html', context)

    if request.method == 'POST':
        document = Document.objects.get(pk=document_uid)
        current_user = request.user
        is_creator = current_user.is_authenticated and document.creator == current_user
        if not is_creator:
            return render(request, "errors/forbidden.html", status=405)
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        is_private = request.POST.get('is_private', False)
        document.title = title
        document.content = content
        document.is_private = is_private
        document.save()
        context = {
            'id': document_uid,
            'document': document,
        }
        return render(request, 'editor.html', context)

    if request.method == 'DELETE':
        document = Document.objects.get(pk=document_uid)
        current_user = request.user
        is_creator = current_user.is_authenticated and document.creator == current_user
        if not is_creator:
            return render(request, "errors/forbidden.html", status=405)
        document.delete()
        return "deleted successfully"
    else:
        return render(request, "errors/405.html", status=405)

