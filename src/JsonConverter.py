import json

with open('IMG_0663.jpg.json') as f:
  data = json.load(f)

#print(data)
#for i in data:
#    print(i, data[i])

#objects tag
objects = json.loads(str(data['objects'])[1:-1].replace("'","\""))

#label object
nodes = json.loads(str(objects[list(objects)[9]]).replace("'","\""))

#each node will have an id and a location, create keypoint list
keypoints = []
for node in nodes:
    keypoint = json.loads(str(nodes[node]).replace("'","\""))['loc']
    keypoint.append(1)
    keypoints.extend(keypoint)
print(keypoints)