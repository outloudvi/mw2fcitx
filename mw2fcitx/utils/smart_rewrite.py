def smart_rewrite(config_object):

    # If `generator` is not a list, make it a list
    generators = config_object["generator"]
    if not isinstance(generators, list):
        config_object["generator"] = [generators]

    # If `title_file_path` is not a list, make it a list
    title_file_path = config_object["source"].get("file_path")
    if isinstance(title_file_path, str):
        config_object["source"].set('file_path', [title_file_path])

    return config_object
