from formMaker.helpers import generate_hash


def build_filename_with_hash(instance, filename):
    return filename + '-' + generate_hash()
