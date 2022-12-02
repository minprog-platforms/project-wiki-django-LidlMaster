from django.shortcuts import render
import markdown2
import random

from . import util

def convert(name):
    content = util.get_entry(name)
    markeddown = markdown2.markdown(content)
    if content == None:
        return None
    else:
        return markeddown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    page = convert(name)
    if page == None:
        return render(request, "encyclopedia/error.html", {
            "message": "404 Page not found"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "name": name, "content": page
            })

def search(request):
    searchresults= []
    entrylist= util.list_entries()
    if request.method == "POST":
        search = request.POST['q']
        page = convert(search)
        if page != None:
            return render(request, "encyclopedia/entry.html", {
               "name": search, "content": page
            })
        else:
            for entry in entrylist:
                if search.lower() in entry.lower():
                    searchresults.append(entry)
            return render(request, "encyclopedia/search.html", {
                "results": searchresults
            })

def new_page(request):
    if request.method == "GET":
        return render( request, "encyclopedia/new_page.html")
    else:
        entry_title = request.POST['entry_title']
        new_entry = request.POST['new_entry']
        if util.get_entry(entry_title) != None:
            return render(request, "encyclopedia/error.html",{
            "message": "This entry already exists"
            })
        else:
            util.save_entry(entry_title, new_entry)
            return render(request, "encyclopedia/entry.html", {
               "name": entry_title, "content": convert(entry_title)
            })

def edit(request, name):
    if request.method =="GET":
        name = request.GET[' entry_title']
        content = util.get_entry(name)
        return render(request, "encyclopedia/edit.html", {
           "name": name, "content": content
        })
# get_entry en zet in tekstbox

def save(request):
    if request.method == "POST":
        name = request.POST['title']
        content = request.POST['content']
        util.save_entry(name, content)
        return render(request, "encyclopedia/entry.html", {
           "name": name, "content": convert(name)
        })

def rand(request):
    entries = util.list_entries()
    randomized = random.choice(entries)
    return render(request, "encyclopedia/entry.html", {
       "name": randomized ,  "content": convert(randomized)
    })
