from json_obj import json_obj
import json
import os

if __name__ == "__main__":
    test = json_obj("coco.json")
    test.coco_load()
    test.coco_to_supervisely()

