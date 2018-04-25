# from django.utils import timezone
# from .models import Post
# from django.shortcuts import render, get_object_or_404, redirect
# from .forms import PostForm
# from django.http import HttpResponse, JsonResponse
import datetime
# from django.template import Template, Context
# from django.template.loader import get_template, render_to_string
from FinexAPI import *
from cmc import *
from scrap import *
# from django.views.decorators.csrf import csrf_exempt
import json
import random

def message(data):
    if data == 'JPY_Exchange':
        response_message_jpy = jpy_rate()
        response_message_jpy_1 = response_message_jpy[0]
    if data == 'JPY_Exchange':
        return response_message_jpy_1

a = message('JPY_Exchange')
print(a)
