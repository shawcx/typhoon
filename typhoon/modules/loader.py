
# this will fail and instead import sys as a random name
try:
    import sys_R_ as sys_R_
except:
    import sys as sys_R_

# decode the command-line provided key into into integer values
# NOTE: strings that start with '__ ' and end with ' __' are not ciphered
sys_R_.argv[-1] = [ord(k_R_) for k_R_ in sys_R_.argv[-1].decode('__ hex __')]

# our cipher function XORs the string with the key + the offset
# e.g. "AAAA" with a key of "\x00" becomes "A@CB" and "A@CB" becomes "AAAA"
def cipher_R_(string_R_, key_R_ = sys_R_.argv[-1]):
    return '__  __'.join(chr(ord(v_R_) ^ ((i_R_ + key_R_[i_R_ % len(key_R_)]) % 256)) for i_R_, v_R_ in enumerate(string_R_))

# decode the string table (injected by typhoon)
for i_R_,v_R_ in enumerate(strings_R_):
    strings_R_[i_R_] = cipher_R_(v_R_)

# obfuscate a bunch of builtin functions
getattr_R_  = eval('getattr')
builtins_R_ = eval('__builtins__')
eval_R_     = getattr_R_(builtins_R_, 'eval')
import_R_   = getattr_R_(builtins_R_, '__import__')
setattr_R_  = getattr_R_(builtins_R_, 'setattr')

# obfuscated importer
class MetaLoader_R_(object):
    def find_module_R_(self_R_, name_R_, path_R_=None):
        return self_R_ if name_R_.startswith('__') else None

    def load_module_R_(self_R_, name_R_):
        # TODO: obfuscate 'decode' reference
        return import_R_(cipher_R_(name_R_[2:].decode_E_('hex')))

# sys.meta_path allows for customer importers
meta_path_R_ = getattr_R_(sys_R_, 'meta_path')
# fix up the references
setattr_R_(MetaLoader_R_, 'find_module', MetaLoader_R_.find_module_R_)
# append MetaLoader_R_ to sys.meta_path
append_R_ = getattr_R_(meta_path_R_, 'append')
append_R_(MetaLoader_R_())
# rearranged just because
setattr_R_(MetaLoader_R_, 'load_module', MetaLoader_R_.load_module_R_)
