import json
import os
from datetime import datetime


class json_obj:
    def __init__(self, filename=""):
        self.filename = filename
        self.filepath = os.path.join(os.path.dirname(os.getcwd()), 'data', filename)
        self.num_points = 0
        self.keypoints = []
        self.keyids = ['nose', 'left_eye', 'right_eye', 'left_ear', 'right_ear',
                       'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist',
                       'left_hip', 'right_hip', 'left_knee', 'right_knee', 'left_ankle', 'right_ankle']
        self.image_id = ""
        self.iscrowd = False
        self.dimensions = {"height": 0, "width": 0}

    # converts supervisely json format to coco format
    # only converts keypoints, size, and iscrowd
    # other values are constant
    def supervisely_to_coco(self, out_name="coco.json"):
        # loads the file and assigns fields to values based on supervisely style json file
        with open(self.filepath) as f:
            data = json.load(f)

        self.dimensions = data['size']

        objects = data["objects"]
        for object in objects:
        # set the keypoints
            nodes = object["nodes"]

            # each node will have an id and a location, create keypoint list
            for node in nodes:
                keypoint = nodes[node]["loc"]
                keypoint.append(1)
                self.keypoints.extend(keypoint)

            self.iscrowd = len(objects) > 1
        #make sure to change this to an int
        id = file_ext = os.path.splitext(self.filename)[0]
        print(id)
        # convert code
        now = datetime.now()
        coco_json = {"info": {}, "licenses": [], "images": [], "annotations": [], "categories": []}
        info = {"description": "MindsLab DataSet", "url": "https://mindslab.ai/", "version": "1.0", "year": 2021,
                "contributor": "MindsLabAI", "date_created": now.strftime("%Y/%m/%d")}
        img = [{"license": 1, "file_name": self.filename, "height": self.dimensions["height"],
                "width": self.dimensions["width"], "date_captured": now.strftime("%Y/%m/%d %H:%M:%S"), "id": id}]
        ann = [{"segmentation": [], "num_keypoints": 17, "area": 0, "iscrowd": self.iscrowd,
                "keypoints": self.keypoints, "image_id": 000000, "bbox": [0, 0, 0, 0], "category_id": 1, "id": 201376}]
        coco_json["info"] = info
        coco_json["images"] = img
        coco_json["annotations"] = ann
        coco_json["categories"] = {"supercategory": "person", "id": 1, "name": "person",
                                   "keypoints": ["nose", "left_eye", "right_eye", "left_ear", "right_ear",
                                                 "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
                                                 "left_wrist", "right_wrist", "left_hip", "right_hip", "left_knee",
                                                 "right_knee", "left_ankle", "right_ankle"],
                                   "skeleton": [[16, 14], [14, 12], [17, 15], [15, 13], [12, 13], [6, 12], [7, 13],
                                                [6, 7], [6, 8], [7, 9], [8, 10], [9, 11], [2, 3], [1, 2], [1, 3],
                                                [2, 4], [3, 5], [4, 6], [5, 7]]}
        json_string = json.dumps(coco_json)
        coco = open(out_name, "w")
        coco.write(json_string)

    # converts coco format to supervisely json format
    # only converts keypoints and size
    # other values are constant
    def coco_to_supervisely(self, out_name="sv.json"):
        # loads the file and assigns fields to values based on coco-style json file
        with open(self.filepath) as f:
            data = json.load(f)

        # create meta_json first
        obj = data["categories"][0]
        dim = data["images"][0]
        self.dimensions["height"] = dim["height"]
        self.dimensions["width"] = dim["width"]

        imgs = data["images"]
        annotations = data["annotations"]
        unpaired = []
        b = 0
        for img in imgs:
            self.keypoints.clear()
            self.image_id = img["id"]
            for annotation in annotations:
                fname = str(self.image_id) + ".json"
                if annotation["image_id"] == self.image_id:
                    kpoints = annotation["keypoints"]
                    count = 1
                    temp = []
                    for i in kpoints:
                        if count % 3 != 0:
                            temp.append(i)
                        count += 1
                    self.keypoints.append(temp)
                    self.iscrowd = annotation["iscrowd"]
            self.coco_create(fname)
            b += 1
            if b == 1:
                break

    def coco_create(self, out_name="sv.json"):
        # create code
        now = datetime.now()
        supervisely_json = {"description": "", "tags": [], "size": self.dimensions, "objects": []}
        objects = {"id": self.image_id, "classId": 3893107, "description": "", "geometryType": "graph",
                   "labelerLogin": "MindsLabAI", "createdAt": now.strftime("%Y/%m/%d %H:%M:%S"),
                   "updatedAt": now.strftime("%Y/%m/%d %H:%M:%S"), "tags": [], "classTitle": "Pose", "nodes": {}}
        i = 0
        for points in self.keypoints:
            obj = objects.copy()
            nodes = obj["nodes"]
            for j in range(0, len(points), 2):
                # str(j / 2) is the id of the node
                nodes[j] = {"loc": [points[j], points[j + 1]]}
                print(nodes[j])
            i += 1
            supervisely_json["objects"].append(obj)
            if i == 1:
                break

        json_string = json.dumps(supervisely_json)
        sv = open(out_name, "w")
        sv.write(json_string)
        print()
