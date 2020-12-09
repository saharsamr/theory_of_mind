def find_common_unique_object(visited_pair, other_pair):

    common, unique = None, None
    for object in visited_pair:
        if object in other_pair:
            common = object
            break

    unique = visited_pair[0] if common != visited_pair[0] else visited_pair[1]

    return common, unique
