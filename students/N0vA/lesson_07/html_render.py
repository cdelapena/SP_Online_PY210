#!/usr/bin/env python3

"""
A class-based system for rendering html.
"""

# This is the framework for the base class
class Element(object):

    tag = 'html'
    indent = '    '

    def __init__(self, content=None, **kwargs):
        
        self.attributes = kwargs
        if content is None:
            self.contents = []
        else:
            self.contents = [content]
        

    def append(self, new_content): # Add another string to content

       return self.contents.append(new_content)
        

    def _open_tag(self):

        open_tag = ["<{}".format(self.tag)]
        for key, value in self.attributes.items():
            open_tag.append(' {}="{}"'.format(key, value))
        open_tag.append(">")
        open_tag = ''.join(open_tag)

        return open_tag


    def _close_tag(self):
        
        close_tag = '</{}>'.format(self.tag)

        return close_tag


    def render(self, out_file, cur_ind=''):
        
        out_file.write(cur_ind + self._open_tag() + '\n')
        
        # loop through the list of contents:
        for content in self.contents:
            try:
                content.render(out_file, cur_ind + self.indent)
            except AttributeError:
                out_file.write(cur_ind + self.indent + content + '\n')
            
        out_file.write(cur_ind + self._close_tag() + '\n')
        

class Body(Element):

    tag = 'body'


class Html(Element):

    tag = 'html'

    def render(self, out_file, cur_ind=''):
        
        # Add doctype in file before html tag
        out_file.write(cur_ind + '<!DOCTYPE html>\n')
        super().render(out_file, cur_ind)


class P(Element):

    tag = 'p'

class Head(Element):

    tag = 'head'


class OneLineTag(Element):
    

    def render(self, out_file, cur_ind=''): # Render elements on one line
        
        out_file.write(cur_ind + self._open_tag())
        out_file.write(self.contents[0])
        out_file.write(self._close_tag() + '\n')


    def append(self, content):
        raise NotImplementedError


class Title(OneLineTag):

    tag = 'title'


class SelfClosingTag(Element):
    
    def __init__(self, content=None, **kwargs):
        if content is not None:
            raise TypeError("SelfClosingTag can not contain any content")
        super().__init__(content=content, **kwargs)

    def render(self, outfile, cur_ind=''):
        tag = self._open_tag()[:-1] + " />\n"
        outfile.write(cur_ind + tag)

    def append(self, *args):
        raise TypeError("You can not add content to a SelfClosingTag")


class Hr(SelfClosingTag):
    
    tag = "hr"


class Br(SelfClosingTag):
    
    tag = 'br'


class A(OneLineTag):
    
    tag = 'a'

    # Add argument for link in init call
    def __init__(self, link, content=None, **kwargs):
        kwargs['href'] = link
        super().__init__(content, **kwargs)


class Li(Element):
    
    tag = 'li'

class Ul(Element):
    
    tag = 'ul'


class Header(OneLineTag):

    tag = 'header'

    # Add level to init call
    def __init__(self, level, content=None, **kwargs):
        self.tag = 'header{}'.format(level)
        super().__init__(content, **kwargs)


class Meta(SelfClosingTag):
    
    tag = 'meta'
