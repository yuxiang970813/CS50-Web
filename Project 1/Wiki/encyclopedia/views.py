from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
# from django.urls import reverse
from django import forms
from . import util

import markdown2
import random



# Global class
class NewQueryForm(forms.Form):
    # Get queries from user
    queries = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                'class': 'search',
                'placeholder': 'Search Encyclopedia'}))

class NewPage(forms.Form):
    # Define title
    title = forms.CharField(
        label="Enter title:",
        widget=forms.TextInput(
            attrs={'style':'width:25%;'}))
    # Define text area
    content = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={'placeholder': 'Enter the Markdown content for the page:'}))


# Create your views here.
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewQueryForm()})


# Show entry content when "wiki/title"
def entry(request, title):
    # Retrieve entry
    content = util.get_entry(title)
    # Check valid entry
    if not content:
        # Apologize if invalid
        return HttpResponse("Error! Requested page was not found!")
    else:
        # Show entry content
        return render(request, "encyclopedia/entry.html", {
            "form": NewQueryForm(),
            "title": title,
            # Convert md to html
            "content": markdown2.markdown(content)})


# Allow user type query to search for encyclopedia entry
def search(request):
    # Check request method
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = NewQueryForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            # Isolate the query from the 'cleaned' version of form data
            query = form.cleaned_data["queries"]
            # If query match, redirected to that entry's page
            entries = util.list_entries()
            if query in entries:
                return HttpResponseRedirect(f"/wiki/{query}")
            # If query doesn't match, display list of substring
            else:
                return render(request, "encyclopedia/search.html", {
                    "title": "Search",
                    "entries": entries,
                    "query": query,
                    "form": NewQueryForm()})


# Create new encyclopedia entry.
def new(request):
    # User visit the page
    if request.method == "GET":
        return render(request, "encyclopedia/new.html", {
            "title": "Create New Page",
            "form": NewQueryForm(),
            "new_page": NewPage()})
    # User submit the text
    else:
        new_page = NewPage(request.POST)
        # Check if form data is valid (server-side)
        if new_page.is_valid():
            # Isolate title and content
            title = new_page.cleaned_data["title"]
            content = new_page.cleaned_data["content"]
            # Error if entry already exists
            if title in util.list_entries():
                return HttpResponse("Error! Entry already exists!")
            # This is a brand new title! Save it!
            else:
                util.save_entry(title, content)
                # Redirect to the new page
                return HttpResponseRedirect(f"/wiki/{title}")


# Enable user edit entry's md content
def edit(request):
    # User request edit page
    if request.method == "GET":
        edit_title = request.GET["edit_title"]
        # Give user a edit text area form
        edit_content = util.get_entry(edit_title)
        return render(request, "encyclopedia/edit.html", {
            "title": "Edit Page",
            "edit_title": edit_title,
            'edit_content': edit_content})
    # User submit edited page
    else:
        # Get the edited title & content
        edited_title =  request.POST["edited_title"]
        edited_content = request.POST["edited_content"]
        # Update that entry
        util.save_entry(edited_title, edited_content)
        # Redirect to edited entry
        return HttpResponseRedirect(f"/wiki/{edited_title}")


# Take user to random entry
def random_page(request):
    # Get random page
    random_page = random.choice(util.list_entries())
    # Redirect to that random page
    return HttpResponseRedirect(f"/wiki/{random_page}")
