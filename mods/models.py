from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.encoding import python_2_unicode_compatible
from ckeditor.fields import RichTextField


class Post(models.Model, HitCountMixin):
    title = models.CharField(max_length=40)
    content = RichTextField(max_length=20000)
    description = models.CharField(max_length=80)
    tags = models.CharField(max_length=300, blank=True)
    thumbnail = models.ImageField(upload_to="thumbnails")
    likes = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    CATEGORY_CHOICES = (
        ('1', 'Combat'),
        ('2', 'Food'),
        ('3', 'Storage'),
        ('4', 'Magic'),
        ('5', 'World Gen'),
        ('6', 'API and Library'),
        ('7', 'Mobs and Creatures'),
        ('8', 'Armor, Tools and Weapons'),
        ('9', 'Cosmetic'),
        ('10', 'Technology'),
        ('11', 'Miscellaneous'),
        ('12', 'Other'),
    )
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default="Other")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    MOD_VERSION = (
        ('0', '1.15'),
        ('1', '1.14.4'),
        ('2', '1.14'),
        ('3', '1.13.2'),
        ('4', '1.12.2'),
        ('5', '1.11.2'),
        ('6', '1.10.2'),
        ('7', '1.9.4'),
        ('8', '1.8.9'),
        ('9', '1.7.10'),
        ('10', '1.7.2'),
        ('11', '1.6.4'),
        ('12', 'Other (Description)'),
    )
    version = models.CharField(max_length=2, choices=MOD_VERSION)
    download = models.CharField(max_length=500)
    website = models.CharField(max_length=500, blank=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
