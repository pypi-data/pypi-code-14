import mistune
import re 
import inspect
import copy
import urlparse
import posixpath  
"""
    guidemd
    ~~~~~~~
    An extension to mistune 
    :copyright: 2016 John Pickerill 
    
    Based on and dependant on mistune :copyright: (c) 2014 - 2015 by Hsiaoming Yang.
"""

#TODO disable embedded HTML ? 

 

__version__ = '0.0.2'
__author__ = 'John Pickerill <me@curiouscrab.com>'
__all__ = [
    'BlockGrammar', 'BlockLexer',
    'InlineGrammar', 'InlineLexer',
    'Renderer', 'Markdown',
    'markdown', 'escape',
]

span_class = {}
blk_class = {}

def url_for():
    return "<span>Unresolved Link</span>"
    
def set_styles(styles):
    global span_class
    for key,value in styles.iteritems():
        if value['span'] != "":
            span_class[value['span']] = value['class']
        if value['block'] != "":
            blk_class[value['block']] = value['class']

def output_drop(self):
    hdInd = hotdropIndex(self)
    if ((self.token['hdInd'] is None) or (not self.token['hdInd'].startswith("_") )):
        self.token['hdInd'] = hdInd
    md = Markdown(hn=self.token['hdInd'])
    cnt =  md(self.token['text']) 
    return self.renderer.drop(self.token['hdInd'],self.token['title'],self.token['level'],self.token['option'],cnt);    
       
def output_blk(self):
    md = Markdown()
    cnt =  md(self.token['text']) 
    return self.renderer.blk(self.token['option'],cnt);
    
def output_box(self):
    return self.renderer.box(self.token['option'],self.token['text']);    
    
    
def output_item(self):
    return self.renderer.item(self.token['item'],self.token['option'])


  
def  hotdropIndex(self):      
    self.hi = self.hi + 1
    return self.hn + "_" + str(self.hi)   

    
class Markdown(mistune.Markdown):

    elinks = []
    iLinks = []
    hi = 0
    hn = ""      

    def __init__(self, renderer=None, inline=None, block=None, hn="_drop", **kwargs):

        self.hn = hn
    
        if not renderer:
            renderer = Renderer(**kwargs)
        else:
            kwargs.update(renderer.options)
        self.renderer = renderer    
           
        if inline and inspect.isclass(inline):
            inline = inline(renderer, **kwargs)
        else:
            inline = InlineLexer(renderer, **kwargs)
            
        if block and inspect.isclass(block):
            block = block(**kwargs)   
        else:
            block = BlockLexer(**kwargs)
        
 
        if kwargs.get('styles'):
            set_styles(kwargs.get('styles'))
        
        Markdown.output_drop = output_drop
        Markdown.output_blk = output_blk
        Markdown.output_item = output_item
        Markdown.output_box = output_box           
        super(Markdown, self).__init__(renderer=renderer, inline=inline, block=block, **kwargs)         

    

class Renderer(mistune.Renderer):
    hn = "hd"
    hi = 0
    
    def __init__(self, hn="hdx" , **kwargs):
        if kwargs.get('url_for'):
            if inspect.isfunction(kwargs.get('url_for')):
                self.url_for = kwargs.get('url_for')
            else:
                self.url_for = url_for
        self.hn = hn
        super(Renderer,self).__init__(**kwargs)
        
    def box (self,option,text): 
        return '<pre><jpc>' + text + '</jpc></pre>'      

    def table(self, header, body):
        """Rendering table element. Wrap header and body in it.
        :param header: header part of the table.
        :param body: body part of the table.
        """
        return (
            '<table class="table table-striped table-bordered">\n<thead>%s</thead>\n'
            '<tbody>\n%s</tbody>\n</table>\n'
        ) % (header, body)           
         
    def spanFormat(self, option, text):
        return '<span class=%s>%s</span>' % (option, text)
     
    def anchor(self,name):
        return '<a id="%s"></a>' % (name)
       
    def blk (self,option,text): 
        return '<div class="' + option + '">' + text + '</div>'    
 
    def drop (self,hdInd,title,level,option,text):
        if level == 0: 
            stag = '<p>'
            etag = '</p>'
        else:
            stag ='<h' + str(level) + ' class="cc-drop-title">'
            etag = '</h' + str(level) + ' >'    
         
        options = "accordion"  
        opts = option.split()
        for o in opts:
            options += " cc-drop-%s" % (o)

        hd = '<div class="%s" id="info%s">\n<div class="accordion-group ">\n<div class="cc-drop-head">\n'  %(options,hdInd )  
        hd += '%s<a class="accordion-toggle collapsed" data-toggle="collapse" data-parent="#info%s" href="#%s">\n' %(stag,hdInd,hdInd) 
        hd += '%s</a>%s</div>\n'  % (title,etag)
        hd += '<div id="%s" class="accordion-body collapse">\n<div class="accordion-inner cc-drop-body">\n%s' %(hdInd, text)
        hd += '</div></div></div></div>\n <!--hd end-->'  

        return hd

 
        
    def item (self,item,option):
        it = '<< included item :' + item  +  ' >>'
        return it
 
    def wiki_link(self, text, link):
        # TODO this needs to be done at init time
        reSnippet = re.compile(r'@(\S{3}):(\S+)')
             
        matchObj= _reUrl.match(link)
        text = escape(text, quote=True)
        if matchObj is None: 
            #TODO shouldn't really be calling url_for from this module need to factor this out
            #TODO add snippet text here ?? lets say text beginning with @ is a snippet we need functions that return the html for a article link or a shippet    
            #url = '<a  target="_blank" href ="' + url_for("displayArticle",itemid = link.strip()) +'">' + text + '</a>'
            m = reSnippet.match(link)
            if m is None:
                url = '<a  target="_top" href ="' + url_for("displayArticle",itemid = link.strip).replace('%23','#') +'">' + text + '</a>'
            else:
                snipType = m.group(1)
                snipId = m.group(2)         
                url =  '<span class= "cc-snip"' 
                + ' data-type = "' + snipType 
                + '" data-url = "' + url_for("displaySnip", id = snipId, type=snipType) 
                + '">[snip:' + snipType + ':' + snipId +'] </span>'
        else:
            url = '<a target ="_self" href="%s">%s</a>' % (matchObj.group(), text)
        return url
 
 
 
 
    def link(self, link, title, text):
        """Rendering a given link with content and title.

        :param link: href link for ``<a>`` tag.
        :param title: title content for `title` attribute.
        :param text: text content for description.
        """     
        link = escape_link(link)
        matchObj= _reUrl.match(link)
        
        # If its a bare word then its an article to be rendered in the current browser tab
        # If its full url its external and should be rendered in a seperate browser tab
        # If its begins with a / then it should be fetched from the static content store and rendered in another browser tab
        
        if matchObj is None:           
            if ((len(link) > 0) and (link[0] != '/')):
                return '<a  target="_top" href ="' + url_for("displayArticle",itemid = link.strip).replace('%23','#') +'">' + text + '</a>'
            else: 
                link = urlparse.urljoin(app.config['KM_STATIC'], link[1:])
            
        if not title:
            return '<a target="_blank" href="%s">%s</a>' % (link, text)
        title = escape(title, quote=True)
        return '<a target="_blank" href="%s" title="%s">%s</a>' % (link, title, text)


 
    def image(self, src, title, alt_text):
        """Rendering a image with title and text.
        :param src: source link of the image.
        :param title: title text of the image.
        :param text: alt text of the image.
        """
        #TODO whats this about looks like it will fail the routine  
        if src.startswith('javascript:'):
            src = ''
        
#TODO refactor as common with wiki-link and pre-compile    
        # TODO should switch to 'https?:\/\/[^\s\/$.?#].[^\s]*$ as the one below fails www.english-heritage.uk
        #'https://mathiasbynens.be/demo/url-regex    

        #reUrl = re.compile(r'^https?:\/\/(-\.)?([^\s\/?\.#-]+\.?)+(\/[^\s]*)?$')
 
        matchObj= _reUrl.match(src)
        #TODO originally relative images were relative to an image directory, and did not have a leading /
        #TODO I am changing this so that relative paths for static server begin with a / and are relative to the base url not an image directory
        #TODO the code that is to maintain compatibility will need to be removed/changed once the content is re-exported from word.
        
        if matchObj is None: 
            if ((len(src) > 0) and (src[0] != '/')):
                src = urlparse.urljoin(app.config['KM_STATIC'], posixpath.join( "images",src))
            else: 
                src = urlparse.urljoin(app.config['KM_STATIC'], src[1:])
                
        text = escape(alt_text, quote=True)
        if title:
            title = escape(title, quote=True)
            html = '<img class="cc_img" src="%s" alt="%s" title="%s"' % (src, text, title)

        else:
            html = '<img class="cc_img" src="%s" alt="%s"' % (src, text)
        if self.options.get('use_xhtml'):
            return '%s />' % html
        return '%s>' % html
           
        
        
        
        
class InlineGrammar(mistune.InlineGrammar):
    wiki_link = re.compile(r'\[\[\s*([\S]+?)(?:\s*(?:\|| )([\s\S]+?))?\]\]')               # [[ link|text ]]          
    corres_tag = re.compile(r'<<') # pc corres indicators are actually <<.*>> but I think I can get away with just escaping the leading << - johnp 
    spanFormat = re.compile(r'^\!(\S)\!([\s\S]+?)\!:\!(?!\!)')
    anchor = re.compile(r'^\!\!\(([a-z,0-9]*)\)')

class InlineLexer(mistune.InlineLexer):      
    default_rules = copy.copy(mistune.InlineLexer.default_rules)
 
    default_rules.insert(1, 'wiki_link')
    default_rules.insert(1, 'corres_tag')
    default_rules.insert(1, 'spanFormat')
    default_rules.insert(1, 'anchor') 
    
    
    def __init__(self, renderer, rules=None, **kwargs):
        if rules is None:
            # use the inline grammar
            rules = InlineGrammar()					
        super(InlineLexer, self).__init__(renderer, rules, **kwargs) 
        

    def output_wiki_link(self, m):

        link = m.group(1)
        if m.group(2) is None:
            text = link
        else:    
            text = m.group(2)
        return self.renderer.wiki_link(text, link)
        
    def output_corres_tag(self, m):
        return "&lt&lt"
    
    def output_spanFormat(self,m):
        global span_class
        cl = m.group(1)
        if cl in span_class:
            cls = span_class[cl]
        else:
            cls = "g_default"
	
        text = m.group(2)
        text = self.output(text)
        return self.renderer.spanFormat(cls,text)
    
    def output_anchor(self,m):
        name = m.group(1)
        return self.renderer.anchor(name)        
        
        
        
        
class BlockGrammar(mistune.BlockGrammar):
    blk  = re.compile(r'(?:^|\n){{blk!([a-zA-Z0-9-_]+):\s*\n([\s\S]*?)\n(?:blk!\1)}}[^\n]*(?:\n|$)')
    box  = re.compile(r'(?:^|\n){{(box(?:![a-z]+)?):[ \t]*([a-zA-Z0-9 \t]*)\n([\s\S]*?)\n(?:\1)}}[^\n]*(?:\n|$)')
    drop = re.compile(r'(?:^|\n){{(drop\!?(?:(?<=\!)([_a-z0-9]+))?):[ \t]*([a-zA-Z0-9 \t]*)\n([^\n]*)\n([\s\S]*?)\n\1}}[^\n]*(?:\n|$)')
    #item = re.compile(r'(?:^|\n){{item:[ \t]*([\S]+)\s*(\S*)?\s*}}[^\n]*(?:\n|$)')       
    
class BlockLexer(mistune.BlockLexer):
    default_rules = copy.copy(mistune.BlockLexer.default_rules)
    default_rules.insert(1,'box')
    default_rules.insert(1,'blk')
    default_rules.insert(1,'drop')
    #default_rules.insert(1,'item')
    default_rules.insert(1,'box')
    
    def __init__(self,  rules=None, **kwargs):
        if rules is None:
            # use the inline grammar
            rules = BlockGrammar()
        super(BlockLexer, self).__init__(rules, **kwargs) 

    def parse_box(self, m):  
        src = m.group(0)
        option =  m.group(2) 
        textstr = m.group(3) 
        self.tokens.append({
            'type': 'box',
            'option': option,
            'text': textstr
        })          
 
    def parse_blk(self, m):
        src = m.group(0)
        if m.group(1) in blk_class:
            option = blk_class[m.group(1)]
        else:    
            option = "g_default"
        textstr = m.group(2) 
        self.tokens.append({
            'type': 'blk',
            'option': option,
            'text': textstr
        })        
               
    def parse_item(self, m):
        src = m.group(0)
        option = m.group(2)
        item = m.group(1) 
        self.tokens.append({
            'type': 'item',
            'option': option,
            'item': item
        })        
               
    def parse_drop(self, m):
        src = m.group(0)
        if ((len(m.group(4)) > 0 ) and (len(m.group(5)) > 0)):
            textstr = (m.group(5))
            #TODO pre compile this 
            r = re.compile(r'^ *(#{1,6}) *([^\n]+?) *#* *(?:\n+|$)')
            capt = r.match(m.group(4))

            if capt:
                level = len(capt.group(1))
                title = capt.group(2)
            else:
                level = 0
                title = m.group(4)          
 
            
            self.tokens.append({
                'hdInd' : m.group(2),
                'type': 'drop',
                'option': m.group(3),
                'level': level,
                'title': title,
                'text': textstr
            })
 
# fix for bug in mistune - submitted to lepture
    def parse_table(self, m):
        item = self._process_table(m)
        cells = re.sub(r' *\n$', '', m.group(3))    
        cells = cells.split('\n')
        for i, v in enumerate(cells):
            v = re.sub(r'^ *\| *| *\| *$', '', v)
            cells[i] = re.split(r' *\| *', v)

        item['cells'] = cells
        self.tokens.append(item)


def markdown(text, escape=True, **kwargs):
    """Render markdown formatted text to html.

    :param text: markdown formatted text content.
    :param escape: if set to False, all html tags will not be escaped.
    :param use_xhtml: output with xhtml tags.
    :param hard_wrap: if set to True, it will use the GFM line breaks feature.
    :param parse_block_html: parse text only in block level html.
    :param parse_inline_html: parse text only in inline level html.
    """

    return Markdown(escape=escape, **kwargs)(text) 
        


        
        
