
import os
import ast
import random

import typhoon

randset = []
randset.extend(chr(x) for x in range(0x41,0x5b)) # A - Z
randset.extend(chr(x) for x in range(0x61,0x7b)) # a - z
randset.append('_')
randset.extend(chr(x) for x in range(0x30,0x3a)) # 0 - 9

def randname(min=8,max=12):
    count = random.randrange(min,max)
    # pick a non-numeric character to start
    first = randset[random.randrange(len(randset) - 10)]
    return first + ''.join(randset[random.randrange(len(randset))] for x in range(count))

class Obfuscate(ast.NodeTransformer):
    def __init__(self, key, debug=False):
        super(Obfuscate, self).__init__()

        # table to track random names
        self.random = {}
        # table to track encrypted strings
        self.strings_R_ = []

        self.key = bytearray.fromhex(key)
        self.debug = debug

    def Randomize(self, name):
        'Generates a random name and caches the result'
        if name not in self.random:
            self.random[name] = randname()
        return self.random[name]

    def Cipher(self, string):
        ciphered = ''.join(chr(ord(v) ^ ((i + self.key[i % len(self.key)]) % 256)) for i,v in enumerate(string))
        try:
            idx = self.strings_R_.index(ciphered)
        except ValueError:
            idx = len(self.strings_R_)
            self.strings_R_.append(ciphered)
        return (idx,ciphered)

    @classmethod
    def Obfuscate(cls, program, key, debug=False):
        loader = os.path.join(typhoon.root, 'modules', 'loader.py')
        loader = open(loader, 'rb').read()
        loader = ast.parse(loader)

        tree = ast.parse(program)

        loader.body.extend(tree.body)

        obfuscate = cls(key, debug)

        tree = ast.fix_missing_locations(obfuscate.generic_visit(loader))

        strings_R_ = obfuscate.Randomize('strings_R_')
        strings_R_ = ast.parse(strings_R_ + '=' + repr(obfuscate.strings_R_)).body[0]
        tree.body.insert(0, strings_R_)

        code = compile(tree, obfuscate.Randomize('<string>'), 'exec')
        return code

    def visit_Import(self, node):
        for name in node.names:
            if name.name.endswith('_R_'):
                name.name = self.Randomize(name.name)
            elif name.name.endswith('_E_'):
                (idx,cipher) = self.Cipher(name.name[:-3])
                print('????', idx, cipher.__class__)
                name.name = '__' + cipher.encode('hex')

            if name.asname and name.asname.endswith('_R_'):
                name.asname = self.Randomize(name.asname)

        return self.generic_visit(node)

    def visit_ClassDef(self, node):
        if node.name.endswith('_R_'):
            node.name = self.Randomize(node.name)
        return self.generic_visit(node)

    def visit_FunctionDef(self, node):
        if node.name.endswith('_R_'):
            node.name = self.Randomize(node.name)
        return self.generic_visit(node)

    def visit_Name(self, node):
        if node.id.endswith('_R_'):
            node.id = self.Randomize(node.id)
        return self.generic_visit(node)

    def visit_Str(self, node):
        if node.s.startswith('__ ') and node.s.endswith(' __'):
            node.s = node.s[3:-3]
        else:
            idx = self.Cipher(node.s)[0]

            node = ast.copy_location(ast.Subscript(
                value = ast.Name(id=self.Randomize('strings_R_'), ctx=ast.Load()),
                slice = ast.Index(value=ast.Num(n=idx)),
                ctx = ast.Load()
                ), node)

        return self.generic_visit(node)

    def visit_Attribute(self, node):
        node = self.generic_visit(node)

        if node.attr.endswith('_R_'):
            node.attr = self.Randomize(node.attr)

        elif node.attr.endswith('_E_'):
            node.attr = node.attr[:-3]

            idx = self.Cipher(node.attr)[0]

            ref = ast.Subscript(
                value = ast.Name(id=self.Randomize('strings_R_'), ctx=ast.Load()),
                slice = ast.Index(value=ast.Num(n=idx)),
                ctx = ast.Load()
                )

            node = ast.copy_location(ast.Call(
                    func = ast.Name(id='getattr', ctx=ast.Load()),
                    args = [node.value, ref],
                    keywords = [],
                    starargs = None,
                    kwargs = None
                ), node)

        return node

    def visit_Print(self, node):
        if self.debug:
            return self.generic_visit(node)
        # This will crash if there are only print statements in a function
        return None
