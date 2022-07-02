from django.db import models
from django.core.validators import FileExtensionValidator
from rest_framework.exceptions import ValidationError


# Gallery
from apps.accounts.models import Account


class GalleryImg(models.Model):
    post = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='gallery_img')
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post}"


class GalleryVideo(models.Model):
    post = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='gallery_video')
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post}"

#  IMG


def upload_status_image(instance, filename):
    return "update/{gallery}/{filename}".format(gallery=instance.gallery, filename=filename)


class PostImg(models.Model):
    gallery = models.ForeignKey(GalleryImg, on_delete=models.CASCADE, related_name='img')
    image = models.ImageField(upload_to=upload_status_image)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if PostImg.objects.filter(gallery_id=self.gallery).count() < 50:
            super(PostImg, self).save(*args, **kwargs)
        else:
            raise ValidationError('The pools are all full.')

    # def __unicode__(self):
    #     return unicode(self.id)  # unicode methods should return unicode

    def __str__(self):
        return f"{self.gallery}"


#  Video

def upload_status_video(instance, filename):
    return "update/{gallery}/{filename}".format(gallery=instance.gallery, filename=filename)


class PostVideo(models.Model):
    gallery = models.ForeignKey(GalleryVideo, on_delete=models.CASCADE, related_name='video')
    video = models.FileField(
                             upload_to=upload_status_video,
                             validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
                             )
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if PostVideo.objects.filter(gallery_id=self.gallery).count() < 2:
            super(PostVideo, self).save(*args, **kwargs)
        else:
            raise ValidationError('The pools are all full.')

    # def __unicode__(self):
    #     return unicode(self.id)  # unicode methods should return unicode

    def __str__(self):
        return f"{self.gallery}"



