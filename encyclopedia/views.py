from django import forms
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse
import markdown
from . import util
from encyclopedia.models import Entry



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def topic(request, title):

    md_content = util.get_entry(title)

    if md_content:

        html_content = markdown.markdown(md_content)

        return render(request, 'encyclopedia/content.html', {'title': title, 'content': html_content})

    else:

        return render(request, 'encyclopedia/notfound.html' , {'title': title } )
    

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
class NewPageForm(forms.Form):

    title = forms.CharField(max_length=200)

    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 5}))


def new_page(request):

    if request.method == "POST":

        title = request.POST.get('title')

        content = request.POST.get('content')

        
        my_entry = util.get_entry(title)
      #  html_content = markdown.markdown(my_entry)
        if my_entry:

            error_message = "An entry with that title already exists."

            return render(request, 'encyclopedia/newPage.html', {'title': title, 'content': content, 'error_message': error_message})


        else:
            
            if content is not None:

                html_content = markdown.markdown(content)
                
            entry = util.save_entry(title, content)
                
            return render(request, 'encyclopedia/content.html', {'title': title, 'content': html_content})


    else:

        #form = NewPageForm()


        return render(request, 'encyclopedia/newPage.html')