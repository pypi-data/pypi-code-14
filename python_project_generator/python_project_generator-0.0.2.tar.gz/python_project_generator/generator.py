import os
import shutil
import argparse
import jinja2

project_dir = os.path.dirname(__file__)


class ProjectGenerator():
    def __init__(self, project_name, author_name, author_email, target_dir):
        self.project_name = project_name
        self.author_name = author_name
        self.author_email = author_email
        self.target_dir = target_dir
        self.template_dir = os.path.join(project_dir, "template")
        self.render_dict = {'author_name': self.author_name,
                            'author_email': self.author_email,
                            'project_name': self.project_name}

    def get_item_path(self, item):
        return os.path.join(self.template_dir, item)

    def get_target_path(self, item):
        temp = jinja2.Template(item)
        target_path = temp.render(self.render_dict)
        return os.path.join(self.target_dir, target_path)

    def template_items(self, top):
        for item in os.listdir(top):
            item_path = os.path.join(top, item)
            yield os.path.relpath(item_path, self.template_dir)
            if os.path.isdir(item_path):
                for x in self.template_items(item_path):
                    yield x

    def generate(self):
        for item in self.template_items(self.template_dir):
            item_path = self.get_item_path(item)
            target_path = self.get_target_path(item.replace('.tmpl', ''))

            if os.path.isdir(item_path):
                if not os.path.exists(target_path):
                    os.mkdir(target_path)
            else:
                shutil.copy(item_path, target_path)
                with open(item_path, 'r') as in_file:
                    content = in_file.read()
                    content = jinja2.Template(content).render(self.render_dict)
                    with open(target_path, 'w') as out_file:
                        out_file.write(content)


def main():
    gen = ProjectGenerator(**get_parser_args())
    gen.generate()


def get_parser_args():
    desc = "Args of Pyhton Project Generator"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--dir', dest='dir', action='store',
                        default=".",
                        help='''target dir of the project,
                        default is currentdir, it must be abspath path and
                        empty.''')
    parser.add_argument('--name', dest='name', action='store',
                        default="sample",
                        help="name of the project which you want generate")
    parser.add_argument('--author', dest='author', action='store',
                        default="author_name",
                        help="author of the project")
    parser.add_argument('--email', dest='email', action='store',
                        default='author_email#email.com',
                        help="email of the author")
    args = parser.parse_args()
    target_dir = os.path.abspath(args.dir)
    return {'project_name': args.name,
            'author_name': args.author,
            'author_email': args.email,
            'target_dir': target_dir}


if __name__ == '__main__':
    main()
