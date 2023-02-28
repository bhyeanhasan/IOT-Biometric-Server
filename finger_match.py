import os
from aiohttp import Fingerprint
import cv2

sample = cv2.imread("noyon2.bmp")

best_score = counter = 0
filename = image = kp1 = kp2 = mp = None
for file in os.listdir("finger_prints/"):

    counter += 1

    fingerprint_img = cv2.imread("finger_prints/" + file)
    # cv2.imshow("ok",fingerprint_img)
    # cv2.waitKey(0)

    sift = cv2.SIFT_create()
    keypoints_1, des1 = sift.detectAndCompute(sample, None)
    keypoints_2, des2 = sift.detectAndCompute(fingerprint_img, None)
    # print(kp1, des1)
    # print(kp2, des2)
    # print(len(kp1), len(kp2))
    # print(len(des1), len(des2))
    # print(des1[0], des2[0])\
    # fast library for approx best match KNN
    matches = cv2.FlannBasedMatcher({"algorithm": 1, "trees": 10}, {}).knnMatch(des1, des2, k=2)

    match_points = []
    for p, q in matches:
        # if abs(p.distance - q.distance)<100:
        if abs(p.distance - q.distance) < 10:
            match_points.append(p)

    keypoints = 0
    if len(keypoints_1) <= len(keypoints_2):
        keypoints = len(keypoints_1)
    else:
        keypoints = len(keypoints_2)

    best_score = len(match_points) / keypoints * 100
    print(best_score)

print("Best score:  " + str(best_score))
