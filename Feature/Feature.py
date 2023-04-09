import cv2
import fingerprint_feature_extractor
img = cv2.imread('tarit2.bmp', 0)
FeaturesTerminations, FeaturesBifurcations = fingerprint_feature_extractor.extract_minutiae_features(img, spuriousMinutiaeThresh=10, invertImage=False, showResult=False, saveResult=True)

for i in FeaturesBifurcations:
    print(i)