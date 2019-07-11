from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.http import JsonResponse
from django.db import IntegrityError
from datetime import datetime, timezone
from reader.models import Series, Chapter, Group
import random
import os
import json
import zipfile


def series_data(request, series_slug):
    series = Series.objects.get(slug=series_slug)
    chapters = Chapter.objects.filter(series=series)
    chapters_dict = {}
    for chapter in chapters:
        chapter_media_path = os.path.join(settings.MEDIA_ROOT, "manga", series_slug, chapter.folder)
        ch_clean = Chapter.clean_chapter_number(chapter)
        if ch_clean in chapters_dict:
            chapters_dict[ch_clean]["groups"][str(chapter.group.id)] = sorted(os.listdir(chapter_media_path))
        else:
            chapters_dict[ch_clean] = {
                "volume": str(chapter.volume),
                "title": chapter.title,
                "folder": chapter.folder,
                "groups": {
                    str(chapter.group.id): sorted(os.listdir(chapter_media_path))
                }
            }
    data = {"slug": series_slug, "title": series.name, "chapters": chapters_dict}
    return HttpResponse(JsonResponse(data))


def get_groups(request, series_slug):
    groups = list(Chapter.objects.order_by().filter(series__slug=series_slug).values_list('group__name', flat=True).distinct())
    return HttpResponse(JsonResponse({"groups": groups}))


def random_chars():
    return ''.join(random.choices("0123456789abcdefghijklmnopqrstuvwxyz", k=8))


def upload_new_chapter(request, series_slug):
    if request.POST and request.user.is_staff:
        group = Group.objects.get(name=request.POST["scanGroup"])
        series = Series.objects.get(slug=series_slug)
        chapter_number = float(request.POST["chapterNumber"])
        existing_chapter = Chapter.objects.filter(chapter_number=chapter_number, series=series).first()
        chapter_folder_numb = f"{int(chapter_number):04}"
        chapter_folder_numb += f"-{str(chapter_number).rsplit('.')[1]}_" if not str(chapter_number).endswith("0") else "_"
        if not existing_chapter:
            uid = chapter_folder_numb + random_chars()
        else:
            if Chapter.objects.filter(chapter_number=chapter_number, series=series, group=group).first():
                return HttpResponse(JsonResponse({"response": "Error: This chapter by this group already exists! Click on edit next to the existing chapter for overwriting."}))
            else:
                uid = existing_chapter.folder
        ch_obj = Chapter.objects.create(chapter_number=chapter_number, group=group, series=series, folder=uid, page_count=0, title=request.POST["chapterTitle"], volume=request.POST["volumeNumber"], uploaded_on=datetime.utcnow().replace(tzinfo=timezone.utc))
        chapter_folder = os.path.join(settings.MEDIA_ROOT, "manga", series_slug, uid, str(group.id))
        if os.path.exists(chapter_folder):
            return HttpResponse(JsonResponse({"response": "Error: This chapter by this group already exists but wasn't recorded in the database. Chapter has been recorded but not uploaded."}))
        os.makedirs(chapter_folder)
        with zipfile.ZipFile(request.FILES["chapterPages"]) as zip_file:
            zip_file.extractall(path=chapter_folder)
        all_pages = os.listdir(chapter_folder)
        padding = len(str(len(all_pages)))
        for idx, page in enumerate(all_pages):
            extension = page.rsplit(".")[1]
            os.rename(os.path.join(chapter_folder, page), os.path.join(chapter_folder, f"{str(idx).zfill(padding)}.{extension}"))
        ch_obj.page_count = len(all_pages)
        ch_obj.save()
        return HttpResponse(json.dumps({"response": "success"}), content_type="application/json")