# get ready to import other models
import sys
sys.path.append('..')

from django.db import models
from user.models import User
import json
from datetime import datetime

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

    # CharField : small     TextField : large, no limit
    content = models.TextField()
    # 要进行关联的表名 , 当删除关联表中的数据时，当前表与其关联的行的行为 : 删除关联数据，与之关联也删除
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 外键, 一对一
    # auto_now_add为添加时的时间，更新对象时不会有变动。
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment_data'
        # bind them together to build the primary key
        unique_together = (("author", "time"),)

    class TimeJsonEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            else:
                return json.JSONEncoder.default(self, obj)

    def __str__(self):
        return '<Comment %r@%r>' % (self.author, self.id)

    def __repr__(self):
        return '<Article %r@%r>' % (self.author, self.id)

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
        liked: number of people who liked this article
    '''

    title = models.CharField(max_length=64)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField(null=True)
    views = models.PositiveIntegerField(default=0)
    comments = models.ManyToManyField(Comment)  # 多对多
    liked = models.ManyToManyField(User, related_name='liked')
    collection = models.ManyToManyField(User, related_name='collection')
    comments_count = models.PositiveIntegerField(default=0)
    liked_count = models.PositiveIntegerField(default=0)
    collection_count = models.PositiveIntegerField(default=0)

    # 元数据
    class Meta:
        # 自定义数据库表名
        db_table = 'article_data'
        # bind them together to build the primary key
        unique_together = (("title", "author"),)

    class CJsonEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            else:
                return json.JSONEncoder.default(self, obj)

    def __str__(self):
        return '<Article %r@%r>' % (self.author, self.time)

    def __repr__(self):
        return '<Article %r@%r>' % (self.author, self.time)


class Moment(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    mode = models.PositiveIntegerField(default=0)
    # 1: article_create 2:article_update 3:article_delete 4:comment_create 5:comment_delete
    # 6: liked article 7:cancel liked article 8: collect article 9:cancel collect article
    time = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article')
    comment = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comment')

    class Meta:
        db_table = 'moment_data'
        unique_together = (("author", "time"),)

    class TimeJsonEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            else:
                return json.JSONEncoder.default(self, obj)

    def __str__(self):
        return '<Moment %r@%r>' % (self.author, self.id)

    def __repr__(self):
        return '<Moment %r@%r>' % (self.author, self.id)
