.PHONY: all templ css clean
BUILDDIR=output
CSSDIR=$(BUILDDIR)/css
POSTS=$(patsubst %.md,$(BUILDDIR)/%.html,$(wildcard posts/*.md))

all: $(BUILDDIR) $(BUILDDIR)/index.html $(POSTS) $(CSSDIR)/style.css

clean:
	-rm -r $(BUILDDIR)

$(BUILDDIR):
	-mkdir $(BUILDDIR)
	-mkdir $(CSSDIR)
	-mkdir $(BUILDDIR)/posts

%.css: $(wildcard sass/** )
	sass sass/style.scss $(CSSDIR)/style.css

# $(BUILDDIR)/posts/%.html: $(POSTSRCDIR)/%.md
# 	python detemplater.py
$(BUILDDIR)/%.html: %.html templates/* templates/**/*
	python detemplater.py $< > $@

$(BUILDDIR)/%.html: %.md templates/* templates/**/*
	python detemplater.py $< > $@
