from django.shortcuts import render
from django.shortcuts import redirect
from django import forms
import random
from markdown2 import Markdown
markdowner = Markdown()

from . import util

class NewSearchForm(forms.Form):
    search = {
        "class": "search",
        "type": "text",
        "name": "q",
        "placeholder": "Search Encyclopedia"
    }
    query = forms.CharField(label="",
                            widget=forms.TextInput(search))
    
def index(request):
    data = {
        "entries": util.list_entries(),
        "search": NewSearchForm()
    }
    return render(request, "encyclopedia/index.html", data)

def entry(request, entry):
    content = util.get_entry(entry)
    data = {
        "title": entry,
        "search": NewSearchForm()
    }
    
    if content == None:
        return render(request, "encyclopedia/404.html", data, 'text/html', 404)
    else:
        data["content"] = markdowner.convert(content)
        return render(request, "encyclopedia/entry.html", data)

def search(request):
    data = {
        "entries": util.list_entries(),
        "search": NewSearchForm(),
        "form": NewSearchForm(request.POST)
    }
    if request.method != "POST":
        return redirect("index")
    
    if data["form"].is_valid():
        data["query"] = data["form"].cleaned_data["query"]
        data["content"] = util.get_entry(data["query"])
        if data["content"] == None:
            def findEntries(entry):
                if entry.lower().find(data["query"].lower()) > -1:
                    return True
                return False
            data["results"] = filter(findEntries, data["entries"])
            return render(request, "encyclopedia/search.html", data)
        else:
            return redirect("entry", entry=data["query"])
    else:
        return render(request, "encyclopedia/404.html", data, 'text/html', 404)

class NewEntryForm(forms.Form):
    title = {
        "class": "search",
        "type": "text",
        "placeholder": "Title"
    }
    content = {
        "class": "search",
        "type": "textarea",
        "placeholder": "Type your markdown here"
    }
    entryTitle = forms.CharField(label="Title",
                                widget=forms.TextInput(title))
    entryContent = forms.CharField(label="Content",
                                widget=forms.Textarea(content))
    
def add(request):
    data = {
        "entryForm": NewEntryForm(),
        "title": "Create New Page",
        "search": NewSearchForm()
    }
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["entryTitle"]
            content = form.cleaned_data["entryContent"]
            if title in util.list_entries():
                form.add_error("entryTitle", forms.ValidationError(
                    ("'%(title)s' already exists. Please choose a different title"),
                    params={"title": title}
                ))
                data["entryForm"] = form
                return render(request, "encyclopedia/add.html", data)
            else:
                util.save_entry(
                    title,
                    content
                )
                return redirect("entry", entry=title)
        else:
            data["newEntry"] = form
            return render(request, "encyclopedia/add.html", data)
    # get
    return render(request, "encyclopedia/add.html", data)

class EditEntryForm(forms.Form):
    content = {
        "class": "search",
        "type": "textarea",
        "placeholder": "Type your markdown here"
    }
    entryContent = forms.CharField(label="Content",
                                widget=forms.Textarea(content))
    
def edit(request, entry):
    content = util.get_entry(entry)
    data = {
        "entryForm": EditEntryForm(initial={
            "entryContent": content
        }),
        "title": entry,
        "search": NewSearchForm()
    }

    # save
    if request.method == "POST":
        form = EditEntryForm(request.POST)

        if form.is_valid():
            title = entry
            content = form.cleaned_data["entryContent"]
            util.save_entry(
                title,
                content
            )
            return redirect("entry", entry=title)

    # Get
    if content == None:
        return render(request, "encyclopedia/404.html", data, 'text/html', 404)
    else:
        return render(request, "encyclopedia/edit.html", data)
    
def randomEntry(request):
    entries = util.list_entries();
    return redirect("entry", entry=entries[random.randint(0,len(entries)-1)])