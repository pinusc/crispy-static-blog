"""
Simple script using the jinja2 engine to render templates.
Receives the path of the file to convert as the only argument, and outputs the
compiled text to STDIN.
"""
import sys
import os
import glob
from jinja2 import Environment, FileSystemLoader, select_autoescape, Markup
import markdown
from config import config

def get_compiled_path(file_name, new_ext='.html'):
    fname, _ = os.path.splitext(file_name)
    return fname + new_ext


def get_envar():
    def get_posts():
        return [get_compiled_path(i) for i in glob.glob("posts/*")]
    def get_post_name(path):
        fname, _ = os.path.splitext(path.split('/')[-1])
        return fname

    envar = {}
    envar['posts'] = os.listdir(config['posts_dir'])
    envar['get_posts'] = get_posts
    envar['get_post_name'] = get_post_name
    return envar

def main():
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    envar = get_envar()
    # env.filters['markdown'] = lambda text: jinja2.Markup(md.convert(text))
    # env.globals['meta'] = lambda var: md.Meta[var][0]
    # env.trim_blocks = True
    # env.lstrip_blocks = True
    # print(env.list_templates())
    template = env.get_template('default.html')
    content=None
    meta = lambda _: False
    with open(sys.argv[1], 'r') as input_file:
        text = input_file.read()
    fname, ext = os.path.splitext(sys.argv[1])
    if ext in ['.md', '.markdown']:
        md = markdown.Markdown(extensions=['markdown.extensions.meta'])
        meta = lambda t: md.Meta[t][0] if t in md.Meta else False
        content = Markup(md.convert(text))
        if meta('template'):
            template = env.get_template(meta('template')+'.html')
    elif ext in ['.html']:
        template = env.from_string(text)
    else:
        content = Markup(text)
    print(template.render(content=content,meta=meta,**config,**envar))
    # print('title meta-data is retrieved from the content:', file=sys.stderr)

if __name__ == "__main__":
    print(sys.argv, file=sys.stderr)
    main()