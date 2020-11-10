
# TODO: use meta loader to load _E_ modules cleanly

import struct as struct_R_

def crypt_R_(key1_R_, iv1_R_, data_R_):
    def keygen_R_(key2_R_, iv2_R_):
        while True:
            v0_R_,v1_R_ = struct_R_.unpack("!2L", iv2_R_)
            k_R_ = struct_R_.unpack("!4L", key2_R_)
            sum_R_,delta_R_,mask_R_ = eval('(0,0x61c88646,0xffffffff)')

            for round in xrange(45):
                v0_R_ = (v0_R_ + (((v1_R_<<4 ^ v1_R_>>5) + v1_R_) ^ (sum_R_ + k_R_[sum_R_ & 3]))) & mask_R_
                sum_R_ = (sum_R_ + delta_R_) & mask_R_
                v1_R_ = (v1_R_ + (((v0_R_<<4 ^ v0_R_>>5) + v0_R_) ^ (sum_R_ + k_R_[sum_R_>>11 & 3]))) & mask_R_

            iv2_R_ = struct_R_.pack("!2L", v0_R_, v1_R_)

            for k_R_ in iv2_R_:
                yield ord(k_R_)

    return ''.join(chr(x^y) for (x,y) in zip(map(ord, data_R_), keygen_R_(key1_R_,iv1_R_)))


if __name__ == "__main__":
    import sys
    import os

    key = os.urandom(16)
    iv  = os.urandom(8)

    clear = ' '.join(sys.argv)
    crypted = crypt_R_(key, iv, clear)
    print repr(crypted)
    print repr(crypt_R_(key, iv, crypted))
