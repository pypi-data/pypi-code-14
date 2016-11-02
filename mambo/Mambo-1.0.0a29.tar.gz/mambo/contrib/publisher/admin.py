import os
import datetime
import uuid
from mambo import (Mambo, models, nav_menu, page_meta, init_app,
                         route, get_config, session, request, redirect,
                         url_for, get, post, flash, flash_data, flash_success, flash_error,
                         abort, recaptcha, storage, get_flash_data)

from flask_login import fresh_login_required
from mambo.exceptions import AppError
from mambo import utils
import json
from mambo.contrib.auth import (current_user, authenticated, is_authenticated,
                                not_authenticated)


def main(**kwargs):

    options = kwargs.get("options", {})
    nav_kwargs = kwargs.get("nav_menu", {})

    @nav_menu(title=nav_kwargs.pop("title", "Publisher Admin") or "Publisher Admin",
              visible=is_authenticated,
              css_id=nav_kwargs.pop("css_id", "publisher-admin-menu"),
              css_class=nav_kwargs.pop("css_class", "publisher-admin-menu"),
              order=nav_kwargs.pop("order", 20),
              **nav_kwargs)
    class PublisherAdmin(Mambo):
        base_route = kwargs.get("route") or "/publisher/"
        decorators = Mambo.decorators + [authenticated] + kwargs.get("decorators")

        @nav_menu("All Posts")
        def index(self):
            """
            List all posts
            """
            page_meta(title="All Posts")
            per_page = get_config("PAGINATION_PER_PAGE", 25)
            page = request.args.get("page", 1)
            id = request.args.get("id", None)
            slug = request.args.get("slug", None)
            status = request.args.get("status", "all")
            type_id = request.args.get("type_id", None)
            category_id = request.args.get("category_id", None)
            tag_id = request.args.get("tag_id", None)

            reorder_post = request.args.get("reorder_post")

            posts = models.PublisherPost.query()
            types = models.PublisherType.query().order_by("name asc")
            types_options = [(t.id, t.name) for t in types]

            selected_type = None
            if type_id:
                selected_type = models.PublisherType.get(type_id)

            if id:
                posts = posts.filter(models.PublisherPost.id == id)
            if slug:
                posts = posts.filter(models.PublisherPost.slug == slug)
            if type_id:
                type_id = int(type_id)
                posts = posts.filter(models.PublisherPost.type_id == type_id)
            if category_id:
                posts = posts.join(models.PublisherCategoryMap) \
                    .join(models.PublisherCategory) \
                    .filter(models.PublisherCategory.id == category_id)
            if tag_id:
                posts = posts.join(models.PublisherTagMap) \
                    .join(models.PublisherTag) \
                    .filter(models.PublisherTag.id == tag_id)
            if status == "publish":
                posts = posts.filter(models.PublisherPost.is_published == True)
            elif status == "draft":
                posts = posts.filter(models.PublisherPost.is_draft == True)
            elif status == "revision":
                posts = posts.filter(models.PublisherPost.is_revision == True)

            posts = posts.order_by(models.PublisherPost.id.desc())
            posts = posts.paginate(page=page, per_page=per_page)

            return dict(posts=posts,
                        types=types,
                        types_options=types_options,
                        search=False,
                        query_vars={
                            "id": id,
                            "slug": slug,
                            "type_id": type_id,
                            "status": status
                        },
                        selected_type=selected_type)

        @nav_menu("Post Preview", endpoint="PublisherAdmin:preview", visible=False)
        def preview(self, id):
            """
            Read Post
            """
            post = models.PublisherPost.get(id)
            if not post:
                abort(404, "Post doesn't exist")

            page_meta(title="Read: %s " % post.title)

            return dict(post=post)

        @nav_menu("Edit Post", endpoint="PublisherAdmin:edit", visible=False)
        @nav_menu("New Post", endpoint="PublisherAdmin:new", order=2)
        @get("/new/", defaults={"id": None}, endpoint="PublisherAdmin:new")
        @get("/edit/<id>/", endpoint="PublisherAdmin:edit")
        def edit(self, id):
            """
            Create / Edit Post
            """
            page_meta(title="Edit Post")

            types = [(t.id, t.name) for t in
                     models.PublisherType.query().order_by(models.PublisherType.name.asc())]
            categories = [(c.id, c.name) for c in
                          models.PublisherCategory.query().order_by(
                              models.PublisherCategory.name.asc())]
            checked_cats = []

            type_id = request.args.get("type_id", None)

            # data to pass to view
            post = {
                "id": 0,
                "title": "",
                "content": "",
                "slug": "",
                "is_public": True,
                "is_sticky": False,
                "is_featured": False,
                "type_id": 0 if not type_id else int(type_id),
                "options": {}
            }

            # saved in session
            flashed_data = get_flash_data()
            if request.args.get("error") and flashed_data:
                post = flashed_data
                checked_cats = post["post_categories"]

            elif id:
                post = models.PublisherPost.get(id)
                if not post or post.is_revision:
                    abort(404, "Post doesn't exist")
                checked_cats = [c.id for c in post.categories]

            images = models.PublisherAssets.query() \
                .filter(models.PublisherAssets.type == "IMAGE") \
                .order_by(models.PublisherAssets.name.asc())

            images_list = [{"id": img.id, "url": img.object_url} for img in images]
            return dict(post=post,
                        types=types,
                        categories=categories,
                        checked_categories=checked_cats,
                        images_list=images_list)

        @post()
        def save_post(self):
            id = request.form.get("id")
            title = request.form.get("title")
            slug = request.form.get("slug")
            content = request.form.get("content")
            description = request.form.get("description")
            summary = request.form.get("summary")
            keywords = request.form.get("keywords")
            type_id = request.form.get("type_id")
            post_categories = request.form.getlist("post_categories")
            published_date = request.form.get("published_date")
            status = request.form.get("status", "draft")
            is_published = True if status == "publish" else False
            is_draft = True if status == "draft" else False
            is_public = True if request.form.get("is_public") == "y" else False
            is_sticky = True if request.form.get("is_sticky") == "y" else False
            is_featured = True if request.form.get("is_featured") == "y" else False
            featured_image = request.form.get("featured_image")
            featured_embed = request.form.get("featured_embed")
            featured_media_top = request.form.get("featured_media_top", "")
            social_options = request.form.getlist("social_options")
            tags = list(set(request.form.get("tags", "").split(",")))

            now_dt = datetime.datetime.now()
            data = {
                "title": title,
                "content": content,
                "description": description,
                "summary": summary,
                "keywords": keywords,
                "featured_image": featured_image,
                "featured_embed": featured_embed,
                "featured_media_top": featured_media_top,
                "type_id": type_id,
                "is_sticky": is_sticky,
                "is_featured": is_featured,
                "is_public": is_public
            }

            if status in ["draft", "publish"] and (not title or not type_id):
                if not title:
                    flash_error("Post Title is missing ")
                if not type_id:
                    flash_error("Post type is missing")

                data.update({
                    "published_date": published_date,
                    "post_categories": post_categories,
                    "options": {"social_options": social_options},
                })
                flash_data(data)

                if id:
                    url = url_for(self.edit, id=id, error=1)
                else:
                    url = url_for(self.new, error=1)
                return redirect(url)

            published_date = datetime.datetime.strptime(published_date,
                                                        "%Y-%m-%d %H:%M:%S") \
                if published_date else now_dt

            if id and status in ["delete", "revision"]:
                post = models.PublisherPost.get(id)
                if not post:
                    abort(404, "Post '%s' doesn't exist" % id)

                if status == "delete":
                    post.delete()
                    flash_success("Post deleted successfully!")
                    return redirect(self.index)

                elif status == "revision":
                    data.update({
                        "parent_id": id,
                        "is_revision": True,
                        "is_draft": False,
                        "is_published": False,
                        "is_public": False
                    })
                    post = models.PublisherPost.create(**data)
                    return jsonify({"revision_id": post.id})

            elif status in ["draft", "publish"]:
                data.update({
                    "is_published": is_published,
                    "is_draft": is_draft,
                    "is_revision": False,
                    "is_public": is_public
                })

                if id:
                    post = models.PublisherPost.get(id)
                    if not post:
                        abort(404, "Post '%s' doesn't exist" % id)
                    elif post.is_revision:
                        abort(403, "Can't access this post")
                    else:
                        if is_sticky and not post.is_sticky:
                            data["sticky_at"] = now_dt
                        if is_featured and not post.is_featured:
                            data["featured_at"] = now_dt
                        post.update(**data)
                else:
                    if is_published:
                        data["published_at"] = published_date
                    if is_sticky:
                        data["sticky_at"] = now_dt
                    if is_featured:
                        data["featured_at"] = now_dt
                    post = models.PublisherPost.create(**data)

                # prepare tags
                _tags = []
                for tag in tags:
                    tag = tag.strip().lower()
                    _tag = models.PublisherTag.get_by_slug(name=tag)
                    if tag and not _tag:
                        _tag = models.PublisherTag.new(name=tag)
                    if _tag:
                        _tags.append(_tag.id)
                post.update_tags(_tags)

                post.set_slug(slug or title)
                post.update_categories(map(int, post_categories))
                post.set_options("social", social_options)

                if post.is_published and not post.published_at:
                    post.update(published_at=published_date)

                flash_success("Post saved successfully!")

                return redirect(self.edit, id=post.id)

            else:
                abort(400, "Invalid post status")

        @nav_menu("Categories", order=4)
        @get()
        @post()
        def categories(self):
            page_meta(title="Post Categories")
            if request.method == "POST":
                id = request.form.get("id", None)
                action = request.form.get("action")
                name = request.form.get("name")
                slug = request.form.get("slug", None)
                ajax = request.form.get("ajax", False)
                try:
                    if not id:
                        cat = models.PublisherCategory.new(name=name, slug=slug)
                        if ajax:
                            return jsonify({
                                "id": cat.id,
                                "name": cat.name,
                                "slug": cat.slug,
                                "status": "OK"
                            })
                        flash_success("New category '%s' added" % name)
                    else:
                        post_cat = models.PublisherCategory.get(id)
                        if post_cat:
                            if action == "delete":
                                post_cat.delete()
                                flash_success("Category '%s' deleted successfully!" % post_cat.name)
                            else:
                                post_cat.update(name=name, slug=slug)
                                flash_success("Category '%s' updated successfully!" % post_cat.name)
                except Exception as ex:
                    if ajax:
                        return jsonify({
                            "error": True,
                            "error_message": ex.message
                        })

                    flash_error("Error: %s" % ex.message)
                return redirect(self.categories)

            else:
                cats = models.PublisherCategory.query().order_by(
                    models.PublisherCategory.name.asc())
                return dict(categories=cats)

        @nav_menu("Tags", order=5)
        @get()
        @post()
        def tags(self):
            page_meta(title="Post Tags")
            if request.method == "POST":
                id = request.form.get("id", None)
                action = request.form.get("action")
                name = request.form.get("name")
                slug = request.form.get("slug", None)
                ajax = request.form.get("ajax", False)
                try:
                    if not id:
                        tag = models.PublisherTag.new(name=name, slug=slug)
                        if ajax:
                            return jsonify({
                                "id": tag.id,
                                "name": tag.name,
                                "slug": tag.slug,
                                "status": "OK"
                            })
                        flash_success("New Tag '%s' added" % name)
                    else:
                        post_tag = models.PublisherTag.get(id)
                        if post_tag:
                            if action == "delete":
                                post_tag.delete()
                                flash_success("Tag '%s' deleted successfully!" % post_tag.name)
                            else:
                                post_tag.update(name=name, slug=slug)
                                flash_success("Tag '%s' updated successfully!" % post_tag.name)
                except Exception as ex:
                    if ajax:
                        return jsonify({
                            "error": True,
                            "error_message": ex.message
                        })

                    flash_error("Error: %s" % ex.message)
                return redirect(self.tags)

            else:
                tags = models.PublisherTag.query().order_by(models.PublisherTag.name.asc())
                return dict(tags=tags)

        @nav_menu("Types", order=6)
        @get()
        @post()
        def types(self):
            page_meta(title="Post Types")
            if request.method == "POST":
                try:
                    id = request.form.get("id", None)
                    action = request.form.get("action")
                    name = request.form.get("name")
                    slug = request.form.get("slug", None)
                    if not id:
                        models.PublisherType.new(name=name, slug=slug)
                        flash_success("New type '%s' added" % name)
                    else:
                        post_type = models.PublisherType.get(id)
                        if post_type:
                            if action == "delete":
                                post_type.delete()
                                flash_success("Type '%s' deleted successfully!" % post_type.name)
                            else:
                                post_type.update(name=name, slug=slug)
                                flash_success("Type '%s' updated successfully!" % post_type.name)
                except Exception as ex:
                    flash_error("Error: %s" % ex.message)
                return redirect(self.types)
            else:
                types = models.PublisherType.query().order_by(models.PublisherType.name.asc())
                return dict(types=types)

        @nav_menu("Images", order=3)
        @get()
        @post()
        def images(self):
            page_meta(title="Images")
            if request.method == "POST":
                id = request.form.get("id", None)
                action = request.form.get("action")
                description = request.form.get("description")
                if id:
                    image = models.PublisherAssets.get(id)
                    if image:
                        if action == "delete":
                            image.delete()
                            obj = storage.get(image.name)
                            if obj:
                                obj.delete()
                            flash_success("Image deleted successfully!")
                        else:
                            image.update(description=description)
                            flash_success("Image updated successfully!")
                else:
                    abort(404, "No image ID provided")
                return redirect(self.images)

            else:
                page = request.args.get("page", 1)
                per_page = get_config("PAGINATION_PER_PAGE", 25)
                images = models.PublisherAssets.query() \
                    .filter(models.PublisherAssets.type == "IMAGE") \
                    .order_by(models.PublisherAssets.name.asc())
                images = images.paginate(page=page, per_page=per_page)
                return dict(images=images)

        @post()
        def upload_image(self):
            """
            Placeholder for markdown
            """
            try:
                ajax = request.form.get("ajax", False)
                allowed_extensions = ["gif", "png", "jpg", "jpeg"]

                if request.files.get("file"):
                    _file = request.files.get('file')
                    obj = storage.upload(_file,
                                         prefix="uploads/publisher/",
                                         allowed_extensions=allowed_extensions,
                                         public=True)

                    if obj:
                        description = os.path.basename(obj.name)
                        description = description.replace(".%s" % obj.extension, "")
                        description = description.split("__")[0]
                        upload_object = models.PublisherAssets.create(name=obj.name,
                                                                      provider=obj.provider_name,
                                                                      container=obj.container.name,
                                                                      extension=obj.extension,
                                                                      type=obj.type,
                                                                      object_path=obj.path,
                                                                      object_url=obj.url,
                                                                      size=obj.size,
                                                                      description=description)
                        if ajax:
                            return jsonify({
                                "id": upload_object.id,
                                "url": upload_object.object_url
                            })
                        else:
                            flash_success("Image '%s' uploaded successfully!" % upload_object.name)
                else:
                    flash_error("Error: Upload object file is invalid or doesn't exist")
            except Exception as e:
                flash_error("Error: %s" % e.message)
            return redirect(self.images)

    return PublisherAdmin
