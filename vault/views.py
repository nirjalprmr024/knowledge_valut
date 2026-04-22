from django.shortcuts import render, redirect

# Create your views here.
from .models import Note
from .forms import NoteForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


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

    if request.method == "POST":
        note.title = request.POST.get('title')
        note.content = request.POST.get('content')
        note.language = request.POST.get('language')
        note.tags = request.POST.get('tags')
        note.save()

        return redirect('note_list')

    return render(request, 'vault/edit_note.html', {'note': note})
@login_required
def delete_note(request, note_id):
    note = Note.objects.get(id=note_id, owner=request.user)

    note.delete()

    return redirect('note_list')

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        print("DEBUG:", username, email, password)

        # Check empty
        if not username or not password:
            return render(request, "registration/signup.html", {
                "error": "All fields are required"
            })

        # Duplicate check
        if User.objects.filter(username=username).exists():
            return render(request, "registration/signup.html", {
                "error": "Username already exists"
            })

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        print("USER CREATED:", user)

        return redirect("/accounts/login/")  # VERY IMPORTANT

    return render(request, "registration/signup.html")


from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Login successful ✅")
            return redirect("/")
        else:
            messages.error(request, "Invalid username or password ❌")

    return render(request, "login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        User.objects.create_user(username=username, email=email, password=password)
        return redirect("/login/")

    return render(request, "register.html")