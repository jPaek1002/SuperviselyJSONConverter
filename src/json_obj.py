import json
import os
from datetime import datetime


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

        self.dimensions = data['size']

        objects = data["objects"]
        # set the keypoints
        nodes = objects[0]["nodes"]

        # each node will have an id and a location, create keypoint list
        for node in nodes:
            keypoint = nodes[node]["loc"]
            keypoint.append(1)
            self.keypoints.extend(keypoint)

        self.iscrowd = len(objects) > 1

    # this function is for multiple supervisely jsons, do after
    def supervisely_loadjson(self):
        # Get input file names.
        filenames = []

    def supervisely_to_coco(self):
        now = datetime.now()
        coco_json = {"info": {}, "licenses": [], "images": [], "annotations": [], "categories": []}
        info = {"description": "MindsLab DataSet", "url": "https://mindslab.ai/", "version": "1.0", "year": 2021,
                "contributor": "MindsLabAI", "date_created": now.strftime("%Y/%m/%d")}
        img = [{"license": 1, "file_name": self.filename, "height": self.dimensions["height"],
                "width": self.dimensions["width"], "date_captured": now.strftime("%Y/%m/%d %H:%M:%S"), "id": 000000}]
        ann = [{"segmentation": [], "num_keypoints": 17, "area": 0, "iscrowd": self.iscrowd,
                "keypoints": self.keypoints, "image_id": 000000, "bbox": [0, 0, 0, 0], "category_id": 1, "id": 201376}]
        coco_json["info"] = info
        coco_json["images"] = img
        coco_json["annotations"] = ann
        json_string = json.dumps(coco_json)
        coco = open("coco.json", "w")
        coco.write(json_string)

    def coco_load(self):
        with open(self.filepath) as f:
            data = json.load(f)

        dim = data["images"][0]
        self.dimensions["height"] = dim["height"]
        self.dimensions["width"] = dim["width"]

        kpoints = data["annotations"][0]["keypoints"]
        count = 1
        for i in kpoints:
            if (count % 3 != 0):
                self.keypoints.append(i)
            count += 1

        self.iscrowd = data["annotations"][0]["iscrowd"]

    def coco_to_supervisely(self):
        now = datetime.now()
        supervisely_json = {"description": "", "tags": [], "size": {}, "objects": []}
        supervisely_json["size"] = self.dimensions
        objects = [{"id": 000000, "classId": 000000, "description": "", "geometryType": "graph",
                    "labelerLogin": "MindsLabAI", "createdAt": now.strftime("%Y/%m/%d %H:%M:%S"),
                    "updatedAt": now.strftime("%Y/%m/%d %H:%M:%S"), "tags": [], "classTitle": "Pose", "nodes": {}}]
        nodes = objects[0]["nodes"]
        for i in range(0,len(self.keypoints),2):
            nodes[str(i / 2)] = {"loc": [self.keypoints[i], self.keypoints[i+1]]}
            
        supervisely_json["objects"] = objects
        json_string = json.dumps(supervisely_json)
        sv = open("sv.json", "w")
        sv.write(json_string)