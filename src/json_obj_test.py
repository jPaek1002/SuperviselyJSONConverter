from json_obj import json_obj
import json
import os

if __name__ == "__main__":
    test = json_obj("sv.json")
    test.supervisely_to_coco()

