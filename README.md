# crispy-static-blog
Crispy is a static blog generator written overnight with Python, Jinja2, SASS and Markdown, with an emphasis on absolute minimalism, both of UI and code. Due to its simplicity, it is incredibly easy to extend.

# Dependencies
The project uses:
- `python3`
- `make`
- `markdown` (`pip install markdown`)
- `jinja2` (`pip install jinja2`)
- `sass` (installation depends on platform; I used the ruby sass implementation)

# Usage
Just modify `index.html` et similia to change the way the page is structured. 
The style files are in `sass/`, they all get compiled in one big css file. 
Put your posts in `posts`, prefereably following the format: `yyyy-mm-dd-title-lorem-ipsum.md`. 
The markdown flavor is plain markdown plus metadata: add a block at the beginning of each file with content as follows:

    ---
    title: Lorem ipsum
    template: post
    date: 2018-03-17
    ---
    And here goes the text of the post...

Finally, run `make` to make the project! The site will be built in the `output` folder, which can be delete by issuing `make clean`.

For development purposes, you can locally host the websites by cd'ing in `output/` and running `python3 -m http.server`, then navigating to `localhost:8000` in your browser of choice.

# Contributing
Just clone the repo and play around! Pull requests are more than welcome. Keep in mind, however, that this should stay as minimalistic as possible.

# Roadmap
The project is almost ready to be used, apart from a few minor changes:
- Basic media queries should be implemented to resize the text according to screen size
- The generator should allow adding non-post pages (for example nav pages) in a more seamless way
- A 404.html page is missing
- It would be nice if the initial work of `detemplater.py` could be shared across al future instances (i.e. generate the posts list and the site map) but I'm not sure how to do that.
