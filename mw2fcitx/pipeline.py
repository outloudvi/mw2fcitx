# pylint: disable=import-outside-toplevel

import json
import os
import sys

from .fetch import fetch_all_titles
from .utils import dedup
from .logger import console


class MWFPipeline():
    """
    A pipeline for converting title lists to dictionaries.
    """

    def __init__(self, api_path=""):
        self.api_path = api_path
        self.titles = []
        self.words = []
        self.exports = ""
        self.dict = ""

    def load_titles(self, titles, limit=-1, replace=False):
        if isinstance(titles, str):
            titles = titles.split("\n")
        if limit >= 0:
            titles = titles[:limit]
        if replace:
            self.titles = titles
        else:
            self.titles.extend(titles)
        console.debug(f"{len(titles)} title(s) imported.")
        self.words = self.titles

    def write_titles_to_file(self, filename):
        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write("\n".join(self.titles))
        except Exception as e:
            console.error(f"File {filename} is not writable: {str(e)}")
            sys.exit(1)

    def post_load(self, **kwargs):
        if kwargs.get("output"):
            self.write_titles_to_file(kwargs.get("output"))

    def load_titles_from_file(self, filename, **kwargs):
        limit = kwargs.get("file_title_limit") or kwargs.get(
            "title_limit") or -1
        if not os.access(filename, os.R_OK):
            console.error(
                f"File {filename} is not readable; "
                "remove this parameter (\"file_path\") or provide a readable file"
            )
            sys.exit(1)
        with open(filename, "r", encoding="utf-8") as fp:
            self.load_titles(fp.read(), limit=limit)

    def fetch_titles(self, **kwargs):
        titles = fetch_all_titles(self.api_path, **kwargs)
        self.load_titles(titles)
        self.post_load(**kwargs)

    def reset_words(self):
        self.words = self.titles

    def convert_to_words(self, pipelines):
        console.debug(f"Running {len(pipelines)} pipelines")
        cnt = 0
        if callable(pipelines):
            pipelines = [pipelines]
        titles = self.titles
        for i in pipelines:
            cnt += 1
            console.debug(
                f"Running pipeline {cnt}/{len(pipelines)} ({i.__name__ or 'anonymous function'}')"
            )
            titles = i(titles)
        console.debug(f"Deduplicating {len(titles)} items")
        self.words = dedup(titles)
        console.debug(
            f"Deduplication completed. {len(self.words)} items left.")

    def export_words(self, converter="pypinyin", **kwargs):
        # "opencc" is an alias for backward compatibility
        if converter in ("pypinyin", "opencc"):
            console.debug(f"Exporting {len(self.words)} words with OpenCC")
            from mw2fcitx.exporters.pypinyin import export
            fixfile_path = kwargs.get('fixfile')
            if fixfile_path is not None:
                with open(fixfile_path, "r", encoding="utf-8") as fp:
                    kwargs["fix_table"] = json.load(fp)
            self.exports = export(self.words, **kwargs)
        elif callable(converter):
            console.debug(
                f"Exporting {len(self.words)} words with custom converter")
            self.exports = converter(self.words, **kwargs)
        else:
            console.error(f"No such exporter: {converter}")

    def generate_dict(self, generator="pinyin", **kwargs):
        if generator == "pinyin":
            from mw2fcitx.dictgen import pinyin
            dest = kwargs.get("output")
            if not dest:
                console.error(
                    "Dictgen 'pinyin' can only output to files.\n" +
                    "Please give the file path in the 'output' argument.")
                return
            pinyin(self.exports, **kwargs)
        elif generator == "rime":
            from mw2fcitx.dictgen import rime
            self.dict = rime(self.exports, **kwargs)
        else:
            console.error(f"No such dictgen: {generator}")
