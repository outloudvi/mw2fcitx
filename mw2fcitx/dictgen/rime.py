import re
import yaml


from ..logger import console


def gen(text, **kwargs):
    name = kwargs.get("name") or "unnamed_dict"
    version = kwargs.get("version") or "0.1"
    sort = kwargs.get("sort") or "by_weight"
    text = re.sub(r'[ ][ ]*', '\t', text)
    text = text.replace("\t0", "")
    text = text.replace("'", " ")
    header = yaml.dump({
        "name": name,
        "version": version,
        "sort": sort
    })
    text = f'---\n{header.strip()}\n...\n' + text
    if kwargs.get("output"):
        with open(kwargs.get("output"), "w", encoding="utf-8") as file:
            file.write(text)
    else:
        print(text)
    console.info("Dictionary generated.")
    return text
