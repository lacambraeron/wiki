import random
import markdown2
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from . import util

# Homepage view
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Create a view that displays the encyclopedia entry
def display_content(request, title):
    entry = util.get_entry(title)
    if entry is None:
        message = "Error: Entry not found"
        entry = ""
        html = ""
    else:
        message = ""
        html = markdown2.markdown(entry)
        
    return render(request, "encyclopedia/displaycontent.html", {
        "html": html,
        "message": message,
        "title": title
    })

# Use search box to go to a page
def search(request):
    query = request.GET.get('q')
    if query is not None:
        listofentries = util.list_entries()
        if query in listofentries:
            return display_content(request, query)
        else:
            entries = [entry for entry in util.list_entries() if query.lower() in entry.lower()]
            return render(request, "encyclopedia/index.html", {
            "entries": entries
        })
    
    else:
        message = "Error: Input a keyword"
        html = ""
        return render(request, "encyclopedia/displaycontent.html", {
        "html": html,
        "message": message
        })

# Call on newpage.html to create a new entry
def newpage(request):
    return render(request, "encyclopedia/newpage.html")

# Using the form on newpage.html, add the entry into the list of entries
def save_entry(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse('entry', args=[title]))

# Function that returns a random element from the list  
def get_random_entry():
    entry_list = util.list_entries()
    return random.choice(entry_list)

# Function that displays content from the random element on the list
def random_entry_view(request):
    random_entry = get_random_entry()
    return display_content(request, random_entry)

# Edits entries, deletes the original entry while saving the new
def edit(request, title):
        oldcontent =  util.get_entry(title)
        if request.method == 'POST':
            newtitle = request.POST['newtitle']
            newcontent = request.POST['newcontent']
            filename = f"entries/{title}.md"
            default_storage.delete(filename)
            util.save_entry(newtitle, newcontent)
            return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
            })
        else:
            html = oldcontent
            return render(request, "encyclopedia/editpage.html", {
                "html": html,
                "title": title
            })