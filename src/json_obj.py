import json

class json_obj:
    def __init__(self, filename = ""):
        self.filename = filename
        self.keypoints = []
        self.keyids = ['nose','left_eye','right_eye','left_ear','right_ear',
                       'left_shoulder','right_shoulder','left_elbow','right_elbow','left_wrist','right_wrist',
                       'left_hip','right_hip','left_knee','right_knee','left_ankle','right_ankle']
        self.iscrowd = False


    def load_file(self):

    def coco_to_supervisely(self):
        supervisely_json = {}

    def supervisely_to_coco(self):
        coco_json = {}

    def supervisely_getkeywords(self):
        with open('IMG_0663.jpg.json') as f:
            data = json.load(f)

        # objects tag
        objects = json.loads(str(data['objects'])[1:-1].replace("'", "\""))

        # label object
        nodes = json.loads(str(objects[list(objects)[9]]).replace("'", "\""))

        # each node will have an id and a location, create keypoint list
        for node in nodes:
            keypoint = json.loads(str(nodes[node]).replace("'", "\""))['loc']
            keypoint.append(1)
            self.keypoints.extend(keypoint)
    def check_iscrowd(self):
        with open('IMG_0663.jpg.json') as f:
            data = json.load(f)

        # objects tag
        objects = json.loads(str(data['objects'])[1:-1].replace("'", "\""))
