from django.shortcuts import render
import os
from django.conf import settings

def gallery_view(request, category=None):
    categories = ['flower', 'god', 'goddess']
    base_path = os.path.join(settings.BASE_DIR, 'gallery', 'static')

    if category in categories:
        folder = os.path.join(base_path, category)
        images = [f"{category}/{img}" for img in os.listdir(folder) if img.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    else:
        # Default: show all images from all categories
        images = []
        for cat in categories:
            folder = os.path.join(base_path, cat)
            for img in os.listdir(folder):
                if img.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    images.append(f"{cat}/{img}")

    return render(request, 'gallery/gallery.html', {
        'categories': categories,
        'images': images,
        'selected': category,
    })
