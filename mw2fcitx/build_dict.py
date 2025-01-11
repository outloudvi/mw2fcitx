import sys

from .pipeline import MWFPipeline
from .logger import console


def build(config):
    config["source"] = config["source"] or {}
    config["tweaks"] = config["tweaks"] or []
    config["converter"] = config["converter"] or {}
    config["generator"] = config["generator"] or []
    pipeline = MWFPipeline(config["source"].get("api_path"))
    has_contents = False
    if config["source"].get("api_path") is not None:
        has_contents = True
        pipeline.fetch_titles(**config["source"].get("kwargs"))
    if config["source"].get("file_path") is not None:
        has_contents = True
        title_file_path = config["source"].get("file_path")
        for i in title_file_path:
            source_kwargs = config["source"].get("kwargs")
            if source_kwargs is None:
                console.warning("source.kwargs does not exist; assuming null")
                source_kwargs = {}
            pipeline.load_titles_from_file(i, **source_kwargs)
    if not has_contents:
        console.error("No api_path or file_path provided. Stop.")
        sys.exit(1)
    pipeline.convert_to_words(config["tweaks"])
    pipeline.export_words(config["converter"].get("use"),
                          **config["converter"].get("kwargs"))
    generators = config["generator"]
    for gen in generators:
        pipeline.generate_dict(gen.get("use"), **gen.get("kwargs"))
    return pipeline.dict
