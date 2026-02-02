from django.db import models


class PubCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Pub(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    pub_path = models.CharField(max_length=300)
    category = models.ForeignKey(
        PubCategory, on_delete=models.CASCADE, related_name='publications')

    @property
    def blog_content_path(self):
        return f"{self.pub_path}/dev/promo/{self.title}-blog.md"

    def __str__(self):
        return self.title

    # add a Pub record if it doesn't already exist

    @classmethod
    def add_pub(cls, title, subtitle=None, author=None, pub_path=None, category=None):
        category_obj, created = PubCategory.objects.get_or_create(
            name=category)
        pub = cls.objects.get_or_create(
            title=title,
            subtitle=subtitle,
            author=author,
            pub_path=pub_path,
            category=category_obj
        )
        return pub


class BlogPost(models.Model):
    pub = models.ForeignKey(
        Pub, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return f"{self.title} ({self.pub.title})"
