import time
import json
import ast
import argparse
from pathlib import Path
from threading import Thread
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from reweld.parsers.source_to_ast import SourceToAST
from reweld.parsers.ast_to_uml import ASTToUML
from reweld.parsers.uml_to_json import UMLToJSON
from reweld.parsers.json_to_uml import JSONToUML
from reweld.parsers.uml_to_ast import UMLToAST
from reweld.parsers.ast_to_source import ASTToSource


class DiagramSync:
    def __init__(self, source_path: str, diagram_path: str):
        self.source_path = Path(source_path)
        self.diagram_path = Path(diagram_path)
        self._last_source_mtime = None
        self._last_diagram_mtime = None

    def start(self):
        event_handler = _FileChangeHandler(self)
        observer = Observer()
        observer.schedule(event_handler, str(self.source_path.parent), recursive=False)
        observer.schedule(event_handler, str(self.diagram_path.parent), recursive=False)
        observer.start()
        print(f"Watching:\n- Source: {self.source_path}\n- Diagram: {self.diagram_path}")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    def sync_from_source(self):
        print(f"Detected source file change, updating diagram {self.diagram_path}")
        source_code = self.source_path.read_text(encoding="utf-8")
        try:
            ast_tree = SourceToAST.parse(source_code)
        except SyntaxError as e:
            print(f"Warning: Source code not valid yet, skipping update. ({e})")
            return
        uml_classes = ASTToUML.convert(ast_tree)
        uml_json = UMLToJSON.convert(uml_classes)
        self.diagram_path.write_text(uml_json, encoding="utf-8")
        print("Diagram updated from source.")


    def sync_from_diagram(self):
        print(f"Detected diagram file change, updating source {self.source_path}")
        try:
            uml_json = json.loads(self.diagram_path.read_text(encoding="utf-8"))
            uml_classes = JSONToUML.convert(uml_json)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Warning: Diagram JSON not valid yet, skipping update. ({e})")
            return

        ast_tree = UMLToAST.convert(uml_classes)
        source_code = ASTToSource.convert(ast_tree)
        self.source_path.write_text(source_code, encoding="utf-8")
        print("Source updated from diagram.")



class _FileChangeHandler(FileSystemEventHandler):
    def __init__(self, syncer: DiagramSync):
        self.syncer = syncer

    def on_modified(self, event):
        if event.is_directory:
            return
        filepath = Path(event.src_path)
        if filepath == self.syncer.source_path:
            self.syncer.sync_from_source()
        elif filepath == self.syncer.diagram_path:
            self.syncer.sync_from_diagram()


def main():
    parser = argparse.ArgumentParser(description="Sync Python source file and UML JSON diagram.")
    parser.add_argument("source", help="Path to the Python source file to watch")
    parser.add_argument("diagram", help="Path to the UML JSON diagram file to watch")
    args = parser.parse_args()

    syncer = DiagramSync(args.source, args.diagram)
    syncer.start()


if __name__ == "__main__":
    main()
