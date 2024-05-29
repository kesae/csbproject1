from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Message
import sqlite3
import markdown
import bleach
from .forms import UserForm

# Views

def format_messages(raw_messages):
    messages = []
    TAGS = bleach.ALLOWED_TAGS | {'p','h1','h2','h3','h4','h5','h6'}
    for message in raw_messages:
        # Comment out the next line and uncomment the line after that to fix the XSS vulnerability
        content = markdown.markdown(message[1])
        # content = bleach.clean(markdown.markdown(message[1]), tags=TAGS)
        messages.append({"author": message[0], "content": content})
    return messages


def index(request):
    messageobjects = Message.objects.all()
    raw_messages = [(m.author, m.content) for m in messageobjects]
    messages = format_messages(raw_messages)
    return render(request, 'pages/index.html', {'msgs': messages})

def search(request):
    query = request.GET.get('q','')
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    results = []
    if query:
        # Comment out the next two lines and uncomment the following two to fix the injection vulnerability
        sql = f"select U.username, M.content from messageapp_message as M JOIN auth_user AS U ON M.author_id =U.id WHERE M.content LIKE '%{query}%';"
        results = cursor.execute(sql).fetchall()
        # sql2 = "select U.username, M.content from messageapp_message as M JOIN auth_user AS U ON M.author_id =U.id WHERE M.content LIKE ?"
        # results = cursor.execute(sql2, (f"%{query}%",)).fetchall()
    results = format_messages(results)
    return render(request, 'pages/search.html', {'results': results})

@login_required
def post(request):
    content = request.POST.get('content')
    message = Message(content=content, author = request.user )
    message.save()
    return redirect('/')

@login_required
def user(request, uid):
    # Uncomment next two lines to fix the broken access control vulnerability
    # if request.user.id != uid:
    #   return redirect('/')
    form = UserForm()
    user = User.objects.get(id=uid)
    return render(request, 'pages/user.html', {'user': user, "form": form})


# Comment out the following line as part of a fix for the CSRF flaw
@csrf_exempt
@login_required
def setuserdata(request):
    form = UserForm(request.POST)
    if form.is_valid():
        request.user.email = form.cleaned_data['email']
        request.user.save()
    return redirect('user', uid=request.user.id)

