from json_obj import json_obj
import json
import os

if __name__ == "__main__":
    test = json_obj("IMG_0663.jpg.json")
    print(test.supervisely_load())

