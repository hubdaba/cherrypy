class html_page:
    def __init__(self, filename):
        self.filename = filename
        self.html_src = None

    def _read(self):
        html_file = open(self.filename, 'r')
        self.html_src = html_file.read()
        
    def get_html(self):
        if self.html_src is None:
            self._read()
        return self.html_src
        
            
            
        
