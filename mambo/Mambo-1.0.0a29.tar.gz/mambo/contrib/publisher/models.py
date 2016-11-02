import datetime
import arrow
from mambo import db, utils
from mambo.exceptions import ModelError
import mambo.markdown_ext as markdown_ext
import json
import arrow


class SlugNameMixin(object):
    name = db.Column(db.String(255), index=True)
    slug = db.Column(db.String(255), index=True, unique=True)
    description = db.Column(db.String(255))
    image_url = db.Column(db.Text)

    @classmethod
    def get_by_slug(cls, slug=None, name=None):
        """
        Return a post by slug
        """
        if name and not slug:
            slug = utils.slugify(name)
        return cls.query().filter(cls.slug == slug).first()

    @classmethod
    def new(cls, name, slug=None):
        slug = utils.slugify(name if not slug else slug)
        return cls.create(name=name, slug=slug)

    def rename(self, name, slug=None):
        slug = utils.slugify(name if not slug else slug)
        return self.update(name=name, slug=slug)


class PublisherType(SlugNameMixin, db.Model):
    """
    Types
    """

    @property
    def total_posts(self):
        return PublisherPost.query().filter(
            PublisherPost.type_id == self.id).count()


class PublisherCategory(SlugNameMixin, db.Model):
    """
    Category
    """

    @property
    def total_posts(self):
        return PublisherCategoryMap.query() \
            .filter(PublisherCategoryMap.category_id == self.id) \
            .count()


class PublisherTag(SlugNameMixin, db.Model):
    """
    Tag
    """

    @property
    def total_posts(self):
        return PublisherTagMap.query() \
            .filter(PublisherTagMap.tag_id == self.id) \
            .count()


class PublisherTagMap(db.Model):
    """
    PostPostTag
    """
    post_id = db.Column(db.Integer, db.ForeignKey("publisher_post.id",
                                                  ondelete='CASCADE'))
    tag_id = db.Column(db.Integer,
                       db.ForeignKey(PublisherTag.id, ondelete='CASCADE'))

    @classmethod
    def add(cls, post_id, tag_id):
        c = cls.query().filter(cls.post_id == post_id) \
            .filter(cls.tag_id == tag_id) \
            .first()
        if not c:
            cls.create(post_id=post_id, tag_id=tag_id)

    @classmethod
    def remove(cls, post_id, tag_id):
        c = cls.query().filter(cls.post_id == post_id) \
            .filter(cls.tag_id == tag_id) \
            .first()
        if c:
            c.delete(hard_delete=True)


class PublisherCategoryMap(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey("publisher_post.id",
                                                  ondelete='CASCADE'))
    category_id = db.Column(db.Integer, db.ForeignKey(PublisherCategory.id,
                                                      ondelete='CASCADE'))

    @classmethod
    def add(cls, post_id, category_id):
        c = cls.query().filter(cls.post_id == post_id) \
            .filter(cls.category_id == category_id) \
            .first()
        if not c:
            cls.create(post_id=post_id, category_id=category_id)

    @classmethod
    def remove(cls, post_id, category_id):
        c = cls.query().filter(cls.post_id == post_id) \
            .filter(cls.category_id == category_id) \
            .first()
        if c:
            c.delete(hard_delete=True)


class PublisherPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey(PublisherType.id))

    title = db.Column(db.String(255))
    slug = db.Column(db.String(255), index=True)
    content = db.Column(db.Text)
    summary = db.Column(db.Text)
    description = db.Column(db.Text)
    keywords = db.Column(db.Text)
    featured_image = db.Column(db.Text)
    featured_embed = db.Column(db.Text)
    featured_media_top = db.Column(db.String(10))
    language = db.Column(db.String(255))
    expired_at = db.Column(db.DateTime,
                           default=None)  # Expired post will not be queried

    parent_id = db.Column(db.Integer, db.ForeignKey(
        'publisher_post.id'))  # If the post is derived from another post
    has_children = db.Column(db.Boolean, index=True, default=False)
    is_child = db.Column(db.Boolean, index=True, default=False)  #

    is_featured = db.Column(db.Boolean, index=True,
                            default=False)  # Feature post are limited
    featured_at = db.Column(db.DateTime)
    is_sticky = db.Column(db.Boolean, index=True,
                          default=False)  # A sticky post usually stay on top, no matter the count
    sticky_at = db.Column(db.DateTime)
    is_published = db.Column(db.Boolean, index=True, default=True)
    published_at = db.Column(db.DateTime)
    published_by = db.Column(db.Integer)
    is_revision = db.Column(db.Boolean, default=False)
    revision_id = db.Column(
        db.Integer)  # When updating the post, will auto-save
    is_public = db.Column(db.Boolean, index=True, default=False)
    is_draft = db.Column(db.Boolean, index=True, default=False)
    options_data = db.Column(db.Text, default="{}")
    menu_order = db.Column(db.Integer, default=0, index=True)

    type = db.relationship(PublisherType, backref="posts")
    categories = db.relationship(PublisherCategory,
                                 secondary=PublisherCategoryMap.__table__.name)
    tags = db.relationship(PublisherTag,
                           secondary=PublisherTagMap.__table__.name)
    parent = db.relationship('PublisherPost', remote_side=[id],
                             backref="children")

    @classmethod
    def _syncdb(cls):
        """
        Setup all models
        :return:
        """
        post_categories = ["Uncategorized"]
        post_types = ["Page", "Blog", "Document", "Other"]

        # Set types
        if not PublisherType.query().count():
            [PublisherType.new(t) for t in post_types]

        # Set categories
        if not PublisherCategory.query().count():
            [PublisherCategory.new(c) for c in post_categories]

        # Add some basic post
        if not PublisherPost.query().count():
            posts = [
                {
                    "title": "About Us",
                    "slug": "about",
                    "content": "**About Us**",
                    "type_slug": "document",
                    "is_published": True,
                },
                {
                    "title": "Terms of Service",
                    "slug": "tos",
                    "content": "**Terms of Service**",
                    "type_slug": "document",
                    "is_published": True,
                },
                {
                    "title": "Privacy",
                    "slug": "privacy",
                    "content": "**Privacy Policy**",
                    "type_slug": "document",
                    "is_published": True,
                },
                {
                    "title": "First Page",
                    "slug": "first-page",
                    "content": "**This is our First Page!**",
                    "type_slug": "page",
                    "is_published": True,
                },
                {
                    "title": "First Blog",
                    "slug": "first-blog",
                    "content": "**This is our First Blog!**",
                    "type_slug": "blog",
                    "is_published": True,
                }
            ]
            [PublisherPost.new(**post) for post in posts]

    @classmethod
    def new(cls, title, **kwargs):
        """
        Insert a new post
        """
        published_date = None
        is_revision = False
        is_published = False
        is_draft = False
        is_public = kwargs.get("is_public", True)
        parent_id = kwargs.get("parent_id", None)

        if kwargs.get("is_revision"):
            if not parent_id:
                raise ModelError("'parent_id' is missing for revision")
            is_revision = True
            is_public = False
        elif kwargs.get("is_draft"):
            is_draft = True
            is_public = False
        elif kwargs.get("is_published"):
            is_published = True
            published_date = datetime.datetime.now()

        slug = None
        if is_published or is_draft:
            slug = cls.create_slug(kwargs.get("slug", title))

        type_id = kwargs.get("type_id")
        if not type_id and kwargs.get("type_slug"):
            type_slug = kwargs.get("type_slug")
            _type = PublisherType.get_by_slug(slug=type_slug)
            if _type:
                type_id = _type.id

        data = {
            "title": title,
            "slug": slug,
            "content": kwargs.get("content"),
            "description": kwargs.get("description"),
            "is_published": is_published,
            "published_at": published_date,
            "is_draft": is_draft,
            "is_revision": is_revision,
            "is_public": is_public,
            "parent_id": parent_id,
            "type_id": type_id
        }
        return cls.create(**data)

    @classmethod
    def get_published(cls,
                      id=None,
                      slug=None,
                      types=[],
                      categories=[],
                      tags=[]):
        """
        Return published posts.
        If $id or $slug it will return a single post, else all

        :param id: int - the id of a post
        :param slug: string - the slug of a post
        :param types: list - list of types slugs
        :param categories: list - list of categories slug
        :param tags: list - list of tags slugs
        :return:
        """
        q = cls.query().filter(cls.is_published == True)

        # Query only a single post
        if id or slug:
            if id:
                q = q.filter(cls.id == id)
            elif slug:
                q = q.filter(cls.slug == slug)
            return q.first()

        # Query lists
        else:
            if types:
                q = q.join(PublisherType) \
                    .filter(PublisherType.slug.in_(types))
            if categories:
                q = q.join(PublisherCategoryMap) \
                    .join(PublisherCategory) \
                    .filter(PublisherCategory.slug.in_(categories))
            if tags:
                q = q.join(PublisherTag) \
                    .filter(PublisherTag.slug.in_(tags))
            return q

    @classmethod
    def create_slug(cls, title):
        slug = None
        slug_counter = 0
        _slug = utils.slugify(title).lower()
        while True:
            slug = _slug
            if slug_counter > 0:
                slug += str(slug_counter)
            slug_counter += 1
            if not cls.get_by_slug(slug):
                break
        return slug

    @classmethod
    def get_by_slug(cls, slug):
        """
        Return a post by slug
        """
        return cls.query().filter(cls.slug == slug).first()

    def publish(self, published_date=None, published_by_id=None):
        if self.is_draft:
            data = {
                "is_draft": False,
                "is_published": True,
                "published_at": published_date or datetime.datetime.now()
            }
            if published_by_id:
                data.update({
                    "published_by": published_by_id
                })

            self.update(**data)

    def expire(self, date=None):
        """
        Set the expiration date for the post
        :param date:
        :return:
        """
        if not date:
            self.update(expired_at=None)
        else:
            dt = arrow.get(date).datetime
            self.update(expired_at=dt)

    def set_slug(self, title):
        slug = utils.slugify(title)
        if title and slug != self.slug:
            slug = self.create_slug(slug)
            self.update(slug=slug)

    def update_categories(self, categories_list):
        """
        Update categories by replacing existing list with new list
        :param categories_list: list. The new list of category
        """
        cats = PublisherCategoryMap.query() \
            .filter(PublisherCategoryMap.post_id == self.id)
        cats_list = [c.category_id for c in cats]

        del_cats = list(set(cats_list) - set(categories_list))
        new_cats = list(set(categories_list) - set(cats_list))

        for dc in del_cats:
            PublisherCategoryMap.remove(post_id=self.id, category_id=dc)

        for nc in new_cats:
            PublisherCategoryMap.add(post_id=self.id, category_id=nc)

    def update_tags(self, tags_list):
        """
        Update tags by replacing existing list with new list
        :param tags_list: list. The new list of tags
        """
        tags = PublisherTagMap.query() \
            .filter(PublisherTagMap.post_id == self.id)
        tags_list_ = [c.tag_id for c in tags]

        del_tags = list(set(tags_list_) - set(tags_list))
        new_tags = list(set(tags_list) - set(tags_list_))

        for dc in del_tags:
            PublisherTagMap.remove(post_id=self.id, tag_id=dc)

        for nc in new_tags:
            PublisherTagMap.add(post_id=self.id, tag_id=nc)

    def delete_revisions(self):
        """
        Delete all revisions
        """
        try:
            PublisherPost.query() \
                .filter(PublisherPost.post_id == self.id) \
                .filter(PublisherPost.is_revision == True) \
                .delete()
            PublisherPost.db.commit()
        except Exception as ex:
            PublisherPost.db.rollback()

    def set_options(self, key, values):
        options = self.options
        options.update({key: values})
        self.update(options_data=json.dumps(options))

    def add_child(self, post):
        if post.id == self.id:
            raise ModelError("Post can't be its own parent... c'mon now!!!")
        if post.type_id != self.type_id:
            raise ModelError("Post Parent and Child must have the same type_id")

        old_parent = None
        if post.parent_id and post.parent_id != self.id:
            old_parent = self.get(post.parent_id, include_deleted=True)

        post.update(parent_id=self.id, is_child=True)
        self.update_parentage()
        if old_parent:
            old_parent.update_parentage()

    def remove_child(self, post):
        """
        Remove child from page
        :param post:
        :return:
        """
        post.update(parent_id=None, is_child=False)
        self.update_parentage()

    def update_parentage(self):
        """
        Update the parentage of this post
        :return:
        """
        self.update(has_children=True if self.children.count() else False)

    @property
    def options(self):
        return json.loads(self.options_data) if self.options_data else {}

    @property
    def excerpt(self):
        """
        Return description as excerpt, if empty,
        it will return the first paragraph
        :return: str
        """
        if self.description:
            return self.description
        else:
            return ""

    @property
    def top_image(self):
        """
        Return the top image
        Return the image url if exists, or it will get the first image
        Will get the first image from the markdown
        """
        if self.featured_image:
            return self.featured_image
        elif self.content:
            md_images = markdown_ext.extract_images(self.content)
            return md_images[0] if md_images else None

    @property
    def status(self):
        if self.is_published:
            return "Published"
        elif self.is_draft:
            return "Draft"
        elif self.is_revision:
            return "Revision"
        else:
            return ""

    @property
    def total_revisions(self):
        return PublisherPost.query() \
            .filter(PublisherPost.post_id == self.id) \
            .filter(PublisherPost.is_revision == True) \
            .count()


class PublisherAssets(db.Model):
    provider = db.Column(db.String(255))
    container = db.Column(db.String(255))
    local_path = db.Column(db.Text)
    name = db.Column(db.Text)
    description = db.Column(db.String(255))
    size = db.Column(db.Integer)
    extension = db.Column(db.String(10), index=True)
    type = db.Column(db.String(25), index=True)
    object_path = db.Column(db.Text)
    object_url = db.Column(db.Text)
    is_private = db.Column(db.Boolean, index=True, default=False)

