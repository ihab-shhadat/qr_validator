import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import View
from .forms import ValidatorForm
import re


def validator(qrcode):
    fileName = open("results.txt", "a")

    qrcode_arr = re.match("^(0[123456789])(\d{14})(10)([\s\S]*?)(17)(\d{6})(21)([\s\S]*?)($)", qrcode)
    if (qrcode_arr is not None):
        fileName.write(qrcode + ":" + qrcode_arr.group(2) + ":" + qrcode_arr.group(4)
                       + ":" + qrcode_arr.group(6) + ":" + qrcode_arr.group(8) + "\n")
        return True, "QRCode: " + qrcode + "\nGTIN:" + qrcode_arr.group(2) + "\nBN:" + qrcode_arr.group(
            4) + "\nExpiry:" + qrcode_arr.group(
            6) + "\nSerial:" + qrcode_arr.group(8)
    qrcode_arr = re.match("^(0[123456789])(\d{14})(17)(\d{6})(10)([\s\S]*?)(21)([\s\S]*?)($)", qrcode)
    if (qrcode_arr is not None):
        fileName.write(qrcode + ":" + qrcode_arr.group(2) + ":" + qrcode_arr.group(6)
                       + ":" + qrcode_arr.group(4) + ":" + qrcode_arr.group(8) + "\n")
        return True, "QRCode: " + qrcode + "\nGTIN:" + qrcode_arr.group(2) + "\nBN:" + qrcode_arr.group(
            6) + "\nExpiry:" + qrcode_arr.group(
            4) + "\nSerial:" + qrcode_arr.group(8)
    qrcode_arr = re.match("^(0[123456789])(\d{14})(21)([\s\S]*?)(17)(\d{6})(10)([\s\S]*?)($)", qrcode)
    if (qrcode_arr is not None):
        fileName.write(qrcode + ":" + qrcode_arr.group(2) + ":" + qrcode_arr.group(8)
                       + ":" + qrcode_arr.group(6) + ":" + qrcode_arr.group(4) + "\n")
        return True, "QRCode: " + qrcode + "\nGTIN:" + qrcode_arr.group(2) + "\nBatch:" + qrcode_arr.group(
            8) + "\nExpiry:" + qrcode_arr.group(
            6) + "\nSerial:" + qrcode_arr.group(4) + "\n"
    qrcode_arr = re.match("^(21)([\s\S]*?)(01)(\d{14})(10)([\s\S]*?)(17)(\d{6})($)", qrcode)
    if (qrcode_arr is not None):
        fileName.write(qrcode + ":" + qrcode_arr.group(4) + ":" + qrcode_arr.group(6)
                       + ":" + qrcode_arr.group(8) + ":" + qrcode_arr.group(2) + "\n")
        return True, "QRCode: " + qrcode + "\nGTIN:" + qrcode_arr.group(4) + "\nBatch:" + qrcode_arr.group(
            6) + "\nExpiry:" + qrcode_arr.group(
            8) + "\nSerial:" + qrcode_arr.group(2)

    if (qrcode_arr is None):
        fileName.write(qrcode + ": Not able to parse this QR" + "\n")
        return False, " Not able to parse this QR"


class ValidatorView(View):
    template_name = 'index.html'
    form_class = ValidatorForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            status, value = validator(data['qr_code'])
        return render(request, self.template_name, {'form': self.form_class, 'status': status, 'value': value})
