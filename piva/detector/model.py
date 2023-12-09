import torchvision.models.detection as models


weights = models.FasterRCNN_MobileNet_V3_Large_FPN_Weights.COCO_V1
model = models.fasterrcnn_mobilenet_v3_large_fpn(weights=weights, box_score_thresh=0.7)
