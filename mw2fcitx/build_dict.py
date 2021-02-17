import logging
import sys

from pipeline import MWFPipeline


def build(config):
    config["source"] = config["source"] or {}
    config["tweaks"] = config["tweaks"] or []
    config["converter"] = config["converter"] or {}
    config["generator"] = config["generator"] or []
    pipeline = MWFPipeline(config["source"].get("api_path"))
    if config["source"].get("api_path") is None:
        title_file_path = config["source"].get("file_path")
        if title_file_path is None:
            logging.error("No api_path or file_path provided. Stop.")
            sys.exit(1)
        pipeline.load_titles_from_file(title_file_path,
                                       **config["source"].get("kwargs"))
    else:
        pipeline.fetch_titles(**config["source"].get("kwargs"))
    pipeline.convert_to_words(config["tweaks"])
    pipeline.export_words(config["converter"].get("use"),
                          **config["converter"].get("kwargs"))
    generators = config["generator"]
    if not isinstance(generators, list):
        generators = [generators]
    for gen in generators:
        pipeline.generate_dict(gen.get("use"), **gen.get("kwargs"))
    return pipeline.dict
