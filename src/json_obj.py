import json

class json_obj:
    def __init__(self, filename = ""):
        self.filename = filename
        self.filepath = os.path.join(os.path.dirname(os.getcwd()) , 'data', filename)
        self.keypoints = []
        self.keyids = ['nose','left_eye','right_eye','left_ear','right_ear',
                       'left_shoulder','right_shoulder','left_elbow','right_elbow','left_wrist','right_wrist',
                       'left_hip','right_hip','left_knee','right_knee','left_ankle','right_ankle']
        self.iscrowd = False
        self.dimensions = []

    def get_json(self):
        with open(filename) as f:
            return json.load(f)

    def supervisely_load(self):
        data = get_json(self)


    def supervisely_to_coco(self):
        coco_json = {}


    def supervisely_getobjects(self):
        data = self.get_json()
        return json.loads(str(data['objects'])[1:-1].replace("'", "\""))

    def supervisely_getkeypoints(self):
        # objects tag
        objects = self.supervisely_getobjects()

        # label object
        nodes = json.loads(str(objects[list(objects)[9]]).replace("'", "\""))

        # each node will have an id and a location, create keypoint list
        for node in nodes:
            keypoint = json.loads(str(nodes[node]).replace("'", "\""))['loc']
            keypoint.append(1)
            self.keypoints.extend(keypoint)

    def supervisely_check_iscrowd(self):
        # objects tag
        return len(self.supervisely_getobjects()['objects'])>1



    def coco_load(self):
        return

    def coco_to_supervisely(self):
        supervisely_json = {}
