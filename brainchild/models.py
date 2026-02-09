from django.db import models


class PubCategory(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Pub(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    pub_path = models.CharField(max_length=300)
    category = models.ForeignKey(
        PubCategory, on_delete=models.CASCADE, related_name='publications')

    @property
    def blog_content_path(self):
        return f"{self.pub_path}/dev/promo/{self.name}-blog.md"

    def __str__(self):
        return self.name

    # add a Pub record if it doesn't already exist

    @classmethod
    def add_pub(cls, name, title, pub_path, category, author=None):
        cat, _ = PubCategory.objects.get_or_create(name=category)
        pub = cls.objects.get_or_create(
            name=name,
            title=title,
            author=author,
            pub_path=pub_path,
            category=cat
        )
        return pub


class BlogPost(models.Model):
    pub = models.ForeignKey(
        Pub, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return f"{self.title} ({self.pub.name})"


class BlogPage(models.Model):
    post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name='pages')
    order = models.IntegerField(default=0)

    @property
    def blog_page_path(self):
        return f"/public/{self.post.pub.category.name}/blog/{self.order}.md"

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} ({self.post.title})"
