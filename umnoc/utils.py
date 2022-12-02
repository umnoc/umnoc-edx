import os
import time
import uuid
from Levenshtein import distance

def generate_new_filename(instance, filename):
    f, ext = os.path.splitext(filename)
    filename = '%s_%s%s' % (uuid.uuid4().hex, instance.user.email, ext)
    fullpath = "verified_profile/{subdir}/{filename}".format(
        subdir=time.strftime('%Y-%m'),
        filename=filename
    )
    return fullpath


def rough_search(dct, key):
    res = [None, 9999]
    for k in dct.keys():
        l_dis = distance(str(key), str(k))
        if l_dis < res[1]:
            res[0] = k
    return dct.get(res[0])


