import json
import os
from datetime import date


class json_obj:
    def __init__(self, filename=""):
        self.filename = filename
        self.filepath = os.path.join(os.path.dirname(os.getcwd()), 'data', filename)
        self.keypoints = []
        self.keyids = ['nose', 'left_eye', 'right_eye', 'left_ear', 'right_ear',
                       'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist',
                       'left_hip', 'right_hip', 'left_knee', 'right_knee', 'left_ankle', 'right_ankle']
        self.iscrowd = False
        self.dimensions = {"height": 0, "width": 0}

    def supervisely_load(self):
        with open(self.filepath) as f:
            data = json.load(f)

        self.dimensions = data["size"]

        # set the keypoints
        objects = json.loads(str(data['objects'])[1:-1].replace("'", "\""))

        # label object
        nodes = json.loads(str(objects[list(objects)[9]]).replace("'", "\""))

        # each node will have an id and a location, create keypoint list
        for node in nodes:
            keypoint = json.loads(str(nodes[node]).replace("'", "\""))['loc']
            keypoint.append(1)
            self.keypoints.extend(keypoint)

        self.iscrowd = len(objects) > 1
        return self.keypoints

    # this function is for multiple supervisely jsons, do after
    def supervisely_loadjson(self):
        # Get input file names.
        filenames = []

    def supervisely_to_coco(self):
        now = date.now()
        coco_json = {"info": {}, "licenses": [], "images": [], "annotations": [], "categories": []}
        info = {"description": "MindsLab DataSet", "url": "https://mindslab.ai/", "version": "1.0", "year": 2021,
                "contributor": "MindsLabAI", "date_created": now.strftime("%Y/%m/%d")}
        img = [{"license": 1, "file_name": self.filename, "height": self.dimensions["height"],
                "width": self.dimensions["width"], "date_captured": now.strftime("%Y/%m/%d %H:%M:%S"), "id": 000000}]
        ann = [{"segmentation": [], "num_keypoints": 17, "area": 0, "iscrowd": self.iscrowd,
                "keypoints": self.keypoints,"image_id": 000000, "bbox": [0, 0, 0, 0], "category_id": 1, "id": 201376}]

    def coco_load(self):
        return

    def coco_to_supervisely(self):
        supervisely_json = {}
