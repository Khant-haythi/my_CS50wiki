from django import forms
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse
import markdown,random
from . import util
from encyclopedia.models import Entry



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#For Entry Page
def topic(request, title):

    md_content = util.get_entry(title)

    if md_content:

        html_content = markdown.markdown(md_content)

        return render(request, 'encyclopedia/content.html', {'title': title, 'content': html_content})

    else:

        return render(request, 'encyclopedia/notfound.html' , {'title': title } )


#For Searching
def search(request):

    query = request.GET.get('q')

    if query:

        entries = util.list_entries()

        results = [entry for entry in entries if query.lower() in entry.lower()]

        
        if results:
            entry = util.get_entry(query)

            if entry:

                html_content = markdown.markdown(entry)

                return render(request, 'encyclopedia/content.html', {'title': query, 'content': html_content})
            
            else:

                return render(request, "encyclopedia/search.html", {"query": query, "results": results})
             
            
        else:

            return render(request, "encyclopedia/search.html", {"query": query, "results": results})


    else:

        return render(request, 'encyclopedia/index.html', {'entries': util.list_entries()})
    

#For create a New Page

def new_page(request):

    if request.method == "POST":

        title = request.POST.get('title')
        content = request.POST.get('content')
        
        my_entry = util.get_entry(title)
     
        if my_entry:

            error_message = "An entry with that title already exists."

            return render(request, 'encyclopedia/newPage.html', {'title': title, 'content': content, 'error_message': error_message})

        else:
            
            if content is not None:

                html_content = markdown.markdown(content)
                
            entry = util.save_entry(title, content)
                
            return render(request, 'encyclopedia/content.html', {'title': title, 'content': html_content})


    else:
        
        return render(request, 'encyclopedia/newPage.html')
    
#For Edit Page
def edit_page(request,title):
    "Edit an existing page in encyclopedia"
    entry = util.get_entry(title)

    if request.method == "POST":
        
        content = request.POST.get('content')

        if content is not None:

            html_content = markdown.markdown(content)

            util.save_entry(title, content)

            return render(request, 'encyclopedia/content.html', {'title': title, 'content': html_content})


    else:

        return render(request, 'encyclopedia/editPage.html', {'title': title, 'content': entry})

#For Random Page

def random_page(request):

    entries = util.list_entries()

    random_entry = random.choice(entries)

    return redirect('topic', title=random_entry)