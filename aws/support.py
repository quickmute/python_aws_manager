## This is a helper function to parse the tags for easier to read
def parse_tags(tag_dict):
    my_dict = {}
    for tag in tag_dict:
        for item in tag:
            if item == 'Key':
                ## this is Key
                key = tag[item]
            else:
                ## this is Value
                value = tag[item]
        my_dict[key]= value
    return my_dict