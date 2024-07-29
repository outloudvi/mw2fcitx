def is_libime_used(config):
    generators = config.get('generator') or []
    for i in generators:
        if i.get("use") == "pinyin":
            return True
    return False
