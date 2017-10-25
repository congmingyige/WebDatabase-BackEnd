# get ready to import other models
import sys
sys.path.append('..')

from django.db import models
from user.models import User

class Comment(models.Model):
    '''Table of comment

    The model of comment data, designed for the comments under the article.

    Attributes:
        ID: unique key to identify
        content: the main content of this comment
        author: an User object (foreign key)
        time: when to post
        article: declare the relationship with the corresponding article
    '''

    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment_data'
        # bind them together to build the primary key
        unique_together = (("author", "content"),)

    def __str__(self):
        return '<Comment %r@%r>' % (self.author,self.id)

    def __repr__(self):
        return '<Comment %r@%r>' % (self.author,self.id)


class Article(models.Model):
    '''Table of article

    The model of article data, designed for acticle storage.

    Attributes:
        (ID): unique key to identify
        title: title of the article
        author: an User object (foreign key)
        time: when to post
        text: the content of the main body
        comments: All the comments in this article (a ManyToMany relationship)
        views: number of people who have viewed this article
        liked: number of people who liked this acticle
    '''

    title = models.CharField(max_length=64)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField(null=True)
    comments = models.ManyToManyField(Comment)
    views = models.PositiveIntegerField(null=True)
    liked = models.PositiveIntegerField(null=True)

    class Meta:
        db_table = 'article_data'
        # bind them together to build the primary key
        unique_together = (("title", "author"),)

    def __str__(self):
        return '<Article %r@%r>' % (self.title,self.author)

    def __repr__(self):
        return '<Article %r@%r>' % (self.title,self.author)
