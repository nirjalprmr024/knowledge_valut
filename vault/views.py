from django.shortcuts import render, redirect

# Create your views here.
from .models import Note
from .forms import NoteForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


@login_required
def note_list(request):
    notes = Note.objects.filter(owner=request.user)
    return render(request, 'vault/note_list.html', {'notes': notes})

@login_required
def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)

        if form.is_valid():
            note = form.save(commit=False)
            note.owner = request.user
            note.save()
            return redirect('note_list')

    else:
        form = NoteForm()

    return render(request, 'vault/add_note.html', {'form': form})

@login_required
def note_detail(request, note_id):
    note = Note.objects.get(id=note_id, owner=request.user)

    return render(request, 'vault/note_detail.html', {'note': note})

@login_required
def edit_note(request, note_id):
    note = Note.objects.get(id=note_id, owner=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)

        if form.is_valid():
            form.save()
            return redirect('note_detail', note_id=note.id)

    else:
        form = NoteForm(instance=note)

    return render(request, 'vault/edit_note.html', {'form': form})

@login_required
def delete_note(request, note_id):
    note = Note.objects.get(id=note_id, owner=request.user)

    note.delete()

    return redirect('note_list')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})