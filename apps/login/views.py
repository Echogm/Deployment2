# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login
from .models import Users, Quotes, Favorites
from django.contrib import messages
# Create your views here.
def home(request):
    return render(request, "login/index.html")

def login(request):
    if request.method == 'POST':
        valid = Users.userManager.login(
            request.POST["email"],
            request.POST["password"],
        )
        if valid[0]:
            request.session["email"] = {
                "id": valid[1].id,
                "name": valid[1].name
            }
            return redirect("/quotes")
        else:
            for errors in valid[1]:
                messages.add_message(request, messages.ERROR, errors)
        return redirect("/")
    if request.method == 'GET':
        return render(request, "")

def register(request):
    if request.method == 'POST':
        valid = Users.userManager.register(
            request.POST['name'],
            request.POST['last'],
            request.POST['email'],
            request.POST['password'],
            request.POST['confirmation']
        )
        if valid[0]:
            request.session["email"] = {
            "id": valid[1].id,
            "name": valid[1].name
            }
            return redirect('/quotes')
        else:
            for errors in valid[1]:
                messages.add_message(request, messages.ERROR, errors)
            return redirect('/')
    elif request.method == 'GET':
        return render(request, "login/index.html")

def logout(request):
    request.session.clear()
    return redirect("/")

def quotes(request):
    if 'email' not in request.session:
        return redirect('/')
    if request.method == 'POST':
        valid = Quotes.quotesManager.quote(
            author = request.POST["author"],
            message = request.POST["message"],
            creator = request.session["email"]["id"]
        )
        if valid[0]:
            return redirect('/quotes')
        else:
            for errors in valid[1]:
                messages.add_message(request, messages.ERROR, errors)
            return redirect('/quotes')
    elif request.method == "GET":
        quotess = Quotes.quotesManager.all()
        favoritess = Favorites.objects.filter(quote_id = request.session["email"]["id"])
        for favorites in favoritess:
            quotess = quotess.exclude(id = favorites.id)
        context = {
            "Quotes": quotess,
            "Favorites": favoritess
        }
        return render(request, "login/quotes.html", context)

def favorite(request, id):
        joins = Favorites.objects.filter(post_id = id).filter(quote_id = request.session["email"]["id"])
        if len(joins) == 0:
            Favorites.objects.create(
                quote_id = request.session["email"]["id"],
                post_id = id
            )
        return redirect("/quotes")

def unfavorite(request, id):
    query = Favorites.objects.filter(id = id)
    query.delete()
    return redirect("/quotes")

def info(request, id):
    if 'email' not in request.session:
        return redirect('/')
    context = {
        "Quotes": Quotes.quotesManager.filter(creator_id = id),
        "Favorites": Favorites.objects.filter(quote_id = id),
    }
    return render(request, "login/info.html", context)
