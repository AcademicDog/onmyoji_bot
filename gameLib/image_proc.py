import cv2


def match_img_knn(queryImage, trainingImage, thread=0):
    sift = cv2.xfeatures2d.SIFT_create()  # 创建sift检测器
    kp1, des1 = sift.detectAndCompute(queryImage, None)
    kp2, des2 = sift.detectAndCompute(trainingImage, None)
    #print(len(kp1))
    # 设置Flannde参数
    FLANN_INDEX_KDTREE = 1
    indexParams = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    searchParams = dict(checks=50)
    flann = cv2.FlannBasedMatcher(indexParams, searchParams)
    matches = flann.knnMatch(des1, des2, k=2)

    good = []

    # 设置好初始匹配值
    matchesMask = [[0, 0] for i in range(len(matches))]
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.7*n.distance:  # 舍弃小于0.7的匹配结果
            matchesMask[i] = [1, 0]
            good.append(m)

    s = sorted(good, key=lambda x: x.distance)
    '''
    drawParams=dict(matchColor=(0,0,255),singlePointColor=(255,0,0),matchesMask=matchesMask,flags=0) #给特征点和匹配的线定义颜色
    resultimage=cv2.drawMatchesKnn(queryImage,kp1,trainingImage,kp2,matches,None,**drawParams) #画出匹配的结果
    cv2.imshow('res',resultimage)
    cv2.waitKey(0)
    '''
    #print(len(good))
    if len(good) > thread:
        maxLoc = kp2[s[0].trainIdx].pt
        #print(maxLoc)
        return (int(maxLoc[0]), int(maxLoc[1]))
    else:
        return (0, 0)


if __name__ == "__main__":
    queryImage = cv2.imread("img\\exp.png", 1)
    trainingImage = cv2.imread("1.png", 1)  # 读取要匹配的灰度照片
    match_img_knn(queryImage, trainingImage)
