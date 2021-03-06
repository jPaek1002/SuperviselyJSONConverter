import json
import os
from datetime import datetime


class json_obj:
    def __init__(self, filename=""):
        self.filename = filename
        self.filepath = os.path.join(os.path.dirname(os.getcwd()), 'data', filename)
        self.num_points = []
        self.keypoints = []
        self.keyids = ['nose', 'left_eye', 'right_eye', 'left_ear', 'right_ear',
                       'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist',
                       'left_hip', 'right_hip', 'left_knee', 'right_knee', 'left_ankle', 'right_ankle']
        self.image_id = ""
        self.iscrowd = []
        self.dimensions = {"height": 0, "width": 0}
        self.nodes = []
        self.bbox = []

    # converts supervisely json format to coco format
    # only converts keypoints, size, and iscrowd
    # must call sv_get_nodes before
    # other values are constant
    def sv_to_coco(self, out_name="coco.json"):
        # loads the file and assigns fields to values based on supervisely style json file
        with open(self.filepath) as f:
            data = json.load(f)

        self.dimensions = data['size']

        objects = data["objects"]

        for object in objects:
            # set the keypoints
            if object["geometryType"] == "graph":
                nodes = object["nodes"]
                count = 0;
                # each node will have an id and a location, create keypoint list
                kpoints = []
                for node in nodes:
                    keypoint = nodes[node]["loc"]

                    if keypoint == [0, 0]:
                        keypoint.append(0)
                    else:
                        keypoint.append(1)
                        count += 1
                    kpoints.extend(keypoint)
                self.keypoints.append(kpoints)
                self.iscrowd = len(objects) > 1
                self.num_points.append(count)
            elif object["geometryType"] == "rectangle":
                self.bbox.append(object["points"]["exterior"][0] + object["points"]["exterior"][1])
                self.bbox = [self.bbox[0][0],self.bbox[0][1],self.bbox[0][2]-self.bbox[0][0],self.bbox[0][3]-self.bbox[0][1]]
        # make sure to change this to an int
        id = int(os.path.splitext(self.filename)[0])
        # convert code
        now = datetime.now()
        coco_json = {"info": {}, "licenses": [], "images": [], "annotations": [], "categories": []}
        info = {"description": "MindsLab DataSet", "url": "https://mindslab.ai/", "version": "1.0", "year": 2021,
                "contributor": "MindsLabAI", "date_created": now.strftime("%Y/%m/%d")}
        img = [{"license": 1, "file_name": self.filename, "height": self.dimensions["height"],
                "width": self.dimensions["width"], "date_captured": now.strftime("%Y/%m/%d %H:%M:%S"), "id": id}]
        ann = {"segmentation": [], "num_keypoints": 0, "area": 0, "iscrowd": self.iscrowd,
               "keypoints": [], "image_id": id, "bbox": self.bbox, "category_id": 1, "id": 201376}
        coco_json["info"] = info
        coco_json["images"] = img
        coco_json["annotations"] = []
        coco_json["categories"] = {"supercategory": "person", "id": 1, "name": "person",
                                   "keypoints": ["nose", "left_eye", "right_eye", "left_ear", "right_ear",
                                                 "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
                                                 "left_wrist", "right_wrist", "left_hip", "right_hip", "left_knee",
                                                 "right_knee", "left_ankle", "right_ankle"],
                                   "skeleton": [[16, 14], [14, 12], [17, 15], [15, 13], [12, 13], [6, 12], [7, 13],
                                                [6, 7], [6, 8], [7, 9], [8, 10], [9, 11], [2, 3], [1, 2], [1, 3],
                                                [2, 4], [3, 5], [4, 6], [5, 7]]}
        i = 0
        print(self.num_points)
        for kpoints in self.keypoints:
            temp = ann.copy()
            temp["num_keypoints"] = self.num_points[i]
            temp["keypoints"] = kpoints
            coco_json["annotations"].append(temp)
            i += 1
        json_string = json.dumps(coco_json)
        coco = open(out_name, "w")
        coco.write(json_string)

    # converts coco format to supervisely json format
    # only converts keypoints and size
    # other values are constant
    def coco_to_sv(self, out_name="sv.json"):
        # loads the file and assigns fields to values based on coco-style json file
        with open(self.filepath) as f:
            data = json.load(f)

        dim = data["images"][0]
        self.dimensions["height"] = dim["height"]
        self.dimensions["width"] = dim["width"]

        imgs = data["images"]
        annotations = data["annotations"]
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
                    self.iscrowd.append(annotation["iscrowd"])
                    self.bbox.append(annotation["bbox"])
            self.coco_create(fname)
            b += 1
            if b == 1:
                break

    # creates sv json file. note: creates file in src
    def coco_create(self, out_name="sv.json"):
        out_name = os.path.join(os.path.dirname(os.getcwd()), 'data', out_name)
        # create code
        now = datetime.now()
        supervisely_json = {"description": "", "tags": [], "size": self.dimensions, "objects": []}
        objects = {"id": self.image_id, "classId": 6926590, "description": "", "geometryType": "graph",
                   "labelerLogin": "MindsLabAI", "createdAt": now.strftime("%Y/%m/%d %H:%M:%S"),
                   "updatedAt": now.strftime("%Y/%m/%d %H:%M:%S"), "tags": [], "classTitle": "person", "nodes": {}}
        bbox = {"id": self.image_id, "classId": 6926591, "description": "", "geometryType": "rectangle",
                "labelerLogin": "MindsLabAI", "createdAt": now.strftime("%Y/%m/%d %H:%M:%S"),
                "updatedAt": now.strftime("%Y/%m/%d %H:%M:%S"), "tags": [], "classTitle": "bbox",
                "points": {"exterior": [], "interior": []}}
        i = 0
        for points in self.keypoints:
            obj = objects.copy()
            nodes = obj["nodes"]
            for j in range(0, int(len(points) / 2)):
                nodes[self.nodes[j]] = {"loc": [points[j * 2], points[j * 2 + 1]]}
            box = bbox.copy()
            box["points"]["exterior"] = [self.bbox[i][0],self.bbox[i][1]],[self.bbox[i][0]+self.bbox[i][2],self.bbox[i][1]+self.bbox[i][3]]
            supervisely_json["objects"].append(box)
            supervisely_json["objects"].append(obj)
        json_string = json.dumps(supervisely_json)
        sv = open(out_name, "w")
        sv.write(json_string)
        print()

    # reads nodes of meta.json file to make sv json
    def sv_get_nodes(self, fname="meta.json"):
        with open(fname) as f:
            data = json.load(f)
        nodes = data['classes'][0]['geometry_config']['nodes']
        for key in nodes:
            self.nodes.append(key)
        print(len(self.nodes))
