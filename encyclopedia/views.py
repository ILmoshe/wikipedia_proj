from random import randint
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse
import markdown2

from . import util


# Main page


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.get_list_entries()
    })


# Entry page
def entry(request, entry_name):
    print(request)
    text = util.get_entry(entry_name)
    if text is None:
        # When DEBUG=TRUE best to do as follow, for debugging propose. When set
        # to false better to create a nice template, indicating Error as occurred.
        # raise Http404("For debugging propose")
        return HttpResponseNotFound('<h1 style="color:red;">Page not found</h1>')
    return render(request, "encyclopedia/entry.html", {
        "title": entry_name,
        "page_content": markdown2.markdown(text)
    })


def article_search(request):
    """This function redirect to entry() if the request is in our entries

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """

    query_dict = request.GET  # This is a dictionary
    query = query_dict.get("q")
    if query in util.get_list_entries():
        return entry(request, query)
    else:
        all_items = util.get_list_entries()  # All entries as a list.
        sub_str = [item for item in all_items if query in item]
        empty = len(sub_str) == 0
        return render(request, "encyclopedia/search.html",
                      {
                          "sub_str": sub_str,
                          "empty": empty,
                      })


# Simple form for the new page
class NewPage(forms.Form):
    title = forms.CharField(max_length=20, label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Maintext")


def create_new(request):

    # If user clicks submit:
    if request.method == 'POST':
        form = NewPage(request.POST)
        if form.is_valid():  # is valid cleaning the cleaned_data dict
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if title not in util.get_list_entries():  # Check if title not already exist
                util.save_entry(title, content)  # saving our new entry
                # redirecting to the new page
                return entry(request, title)
            else:  # page already exists
                return HttpResponseNotFound('<h1 style="color:red;">Page already exists</h1>')

    # If user go to the newpage URL
    return render(request, "encyclopedia/newpage.html", {
        "text": NewPage()
    })


def edit(request, entry_name):

    # If user clicked submit:
    if request.method == 'POST':
        form = NewPage(request.POST)
        if form.is_valid():  # is valid cleaning the cleaned_data dict
            util.save_entry(
                form.cleaned_data["title"], form.cleaned_data["content"])
            return entry(request, form.cleaned_data["title"])

    # If method is GET:
    text = util.get_entry(entry_name)
    # Setting init value according to the entry name
    fields = NewPage(initial={"title": entry_name, "content": text})

    return render(request, "encyclopedia/edit.html", {
        "text": fields,
        "title": entry_name})


def random(request):
    lst = util.get_list_entries()
    random = lst[randint(0, len(lst) - 1)]
    return entry(request, random)
