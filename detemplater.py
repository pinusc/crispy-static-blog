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

class Post:
    """
    Abstracts the concept of Post. Efficiency-wise it is terrible and needs
    lazy-loading.
    """
    def __init__(self, path):
        self.path = path

    def _rawtext(self):
        with open(self.path, 'r') as f:
            rt = f.read()
            self._rawtext = lambda: rt
            return rt

    def _md(self):
        md = markdown.Markdown(extensions=['markdown.extensions.meta'])
        self._md = lambda: md
        return md

    def content(self):
        content = Markup(self._md().convert(self._rawtext()))
        self.content = lambda: content
        return content

    def title(self):
        return self.meta('title')

    def template(self):
        if self.meta('template'):
            return self.meta('template')+'.html'

    def meta(self, key):
        self.content() # in order for _md().Meta to exist
        return self._md().Meta[key][0] if key in self._md().Meta else False

    def get_compiled_path(self, new_ext='.html'):
        fname, _ = os.path.splitext(self.path)
        return fname + new_ext

    def __str__(self):
        return self.path

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.path == other.path

def posts():
    lposts = [Post(i) for i in glob.glob("posts/*")]
    posts = lambda: lposts
    return lposts

class macros():
    def add_post_in_dict(dic, key, post):
        print("APIND", file=sys.stderr)
        print(dic, file=sys.stderr)
        print(key, file=sys.stderr)
        print(post, file=sys.stderr)
        if key not in dic.keys():
            dic[key] = [post]
        else:
            dic[key] += [post]
        return dic


def main():
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    # env.filters['markdown'] = lambda text: jinja2.Markup(md.convert(text))
    # env.globals['meta'] = lambda var: md.Meta[var][0]
    # env.trim_blocks = True
    # env.lstrip_blocks = True
    # print(env.list_templates())
    template = env.get_template('default.html')
    post = None
    fname, ext = os.path.splitext(sys.argv[1])
    if ext in ['.md', '.markdown']:
        post = Post(sys.argv[1])
        template = env.get_template(post.template())
        print(template.render, file=sys.stderr)
    elif ext in ['.html']:
        with open(sys.argv[1], 'r') as f:
            template = env.from_string(f.read())
    else:
        pass
    print(template.render(**config, macros=macros, post=post, posts=posts))
    # print('title meta-data is retrieved from the content:', file=sys.stderr)

if __name__ == "__main__":
    print(sys.argv, file=sys.stderr)
    main()
