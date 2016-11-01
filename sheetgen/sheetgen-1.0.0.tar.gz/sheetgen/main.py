import os
import sys
import argparse
import jinja2
import pdfkit

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TEMPLATE = os.path.join(BASE_DIR, 'templates', 'sheet.html')


def load_products(f):
    products = f.readlines()
    for product in products:
        ean, name = product.split("\t")
        yield {'ean': ean, 'name': name.strip()}


def render_html(products, template):
    path, filename = os.path.split(template.name)
    loader = jinja2.FileSystemLoader(path)
    env = jinja2.Environment(loader=loader)
    template = env.get_template(filename)
    return template.render(products=products)


def render_pdf(html_string, outfile):
    return pdfkit.from_string(html_string, outfile.name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('outfile', type=argparse.FileType('w'))
    parser.add_argument('--template', type=argparse.FileType('r'),
                        default=open(DEFAULT_TEMPLATE))
    parser.add_argument('--infile', type=argparse.FileType('r'),
                        default=sys.stdin)
    args = parser.parse_args()

    products = load_products(f=args.infile)
    html = render_html(products, args.template)
    render_pdf(html, args.outfile)


if __name__ == '__main__':
    main()
