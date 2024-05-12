import csv
import io
import os

from django import forms
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext


class MsgForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    f = forms.FileField()


def home(request):
    print("SETTING", settings.SOME_VALUE)
    subject = None
    message = None
    fname = None
    fsize = 0
    print("META", request.META)
    if request.POST:
        form = MsgForm(request.POST, request.FILES)
        print("FILES", request.FILES)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            f = request.FILES["f"]
            fsize = f.size
            fname = f.name
    else:
        form = MsgForm()

    return render(
        request,
        "home.html",
        {
            "form": form,
            "subject": subject,
            "message": message,
            "fsize": fsize,
            "fname": fname,
        },
    )


def acsv(request):
    rows = [{"a": 1, "b": 2}, {"a": 3, "b": 3}]

    response = HttpResponse(mimetype="text/csv")
    response["Content-Disposition"] = "attachment; filename=report.csv"

    writer = csv.writer(response)
    writer.writerow(["a", "b"])

    for r in rows:
        writer.writerow([r["a"], r["b"]])

    return response
