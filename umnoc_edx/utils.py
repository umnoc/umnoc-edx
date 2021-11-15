import os
import time
import uuid


def generate_new_filename(instance, filename):
    f, ext = os.path.splitext(filename)
    filename = '%s_%s%s' % (uuid.uuid4().hex, instance.user.email, ext)
    fullpath = "verified_profile/{subdir}/{filename}".format(
        subdir=time.strftime('%Y-%m'),
        filename=filename
    )
    return fullpath
