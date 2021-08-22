from json_obj import json_obj
import json
import os

if __name__ == "__main__":
    test = json_obj("person_keypoints_val2017.json")
    test.sv_get_nodes()
    test.coco_to_sv()

