class Obj:
    def __init__(self,filename,color = [1,1,1]):
        self.filename = filename
        self.vertex_format = [(b'v_pos', 3, 'float'),
                              (b'v_normal', 3, 'float'),
                              (b'v_tc0', 2, 'float'),
                              (b'color', 3, 'float')]
        self.vertices = []
        self.indices = []
        self.color = color 
        self.parseFile()
        
    def parseFile(self, *args):
        with open(self.filename, 'r') as o:
            objData = o.read()
        for line in objData.split('\n'):
            if line.startswith('v '):
                for v in line.split(' ')[1:]:
                    self.vertices.append(float(v))
                for v in [0,0,0, 0,0, self.color[0], self.color[1], self.color[2] ]:
                    self.vertices.append(v)
            elif line.startswith('f '):
                for f in line.split(' ')[1:]:
                    self.indices.append(int(f.split('/')[0])-1)
        
        self.indices = resize(self.indices)
                
def resize(l):
    m = []
    for i in l:
        m.append( i - sorted(l)[0] )
    return m
                    
            