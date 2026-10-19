from html.parser import HTMLParser

class ParagraphParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_p = False
        self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag == "p": self.in_p = True
    def handle_endtag(self, tag):
        if tag == "p": self.in_p = False
    def handle_data(self, data):
        if self.in_p: self.parts.append(data)
            
         
        