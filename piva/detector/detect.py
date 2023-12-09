import torch
from piva.detector.model import weights, model


def process(img):
    model.eval()

    preprocess = weights.transforms()
    prediction_classes = weights.meta["categories"]

    with torch.no_grad():
        prediction = model([preprocess(img)])[0]

        labels = [prediction_classes[i] for i in prediction["labels"]]
        bboxes = [bbox.numpy().astype("int").tolist() for bbox in prediction["boxes"]]
        score = [round(score.item(), 2) for score in prediction["scores"]]

        results = [{"class": labels[i], "bbox": bboxes[i], "conf": score[i]} for i in range(len(labels))]

        return results
