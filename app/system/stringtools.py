def sanitize_title(string):
    return string\
            .lstrip()\
            .rstrip()\
            .lower()\
            .title()

def sanitize_lower(string):
    return string\
            .lstrip()\
            .rstrip()\
            .lower()
