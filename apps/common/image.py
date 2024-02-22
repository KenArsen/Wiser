import sys
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


class ImageService(object):
    def compress_image(self, field, delete_source=False, max_width=1200, max_height=1200):
        image = getattr(self, field)
        img = Image.open(image)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        # compress image only if size is less than 1200 px on one side
        if image and (image.width > max_width or image.height > max_height):
            width = image.width if image.width < max_width else max_width
            height = image.height if image.height < max_height else max_height
            img.thumbnail((width, height), Image.ANTIALIAS)
        output = BytesIO()
        img.save(output, format='JPEG', quality=70, optimize=True,
                 progressive=True)
        output.seek(0)
        new_image = InMemoryUploadedFile(
            output, 'ImageField',
            f"{image.name.split('.')[0]}.jpg",
            'image/jpeg', sys.getsizeof(output), None
        )
        if delete_source:
            image.delete(False)
        setattr(self, field, new_image)
