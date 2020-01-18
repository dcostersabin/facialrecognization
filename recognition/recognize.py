import imutils
import numpy as np
import pickle
import cv2
import face_recognition
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def recognize():
    encoding = BASE_DIR + "/data/trainedData/encoding1.pickle"
    data = pickle.loads(open(encoding, "rb").read())
    print(data)
    cap = cv2.VideoCapture(0)

    if cap.isOpened:
        ret, frame = cap.read()
    else:
        ret = False
    while ret:
        ret, frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb = imutils.resize(frame, width=400)
        r = frame.shape[1] / float(rgb.shape[1])

        boxes = face_recognition.face_locations(rgb, model="hog")
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        for encoding in encodings:
            matches = face_recognition.compare_faces(np.array(encoding), np.array(data["encodings"]))
            name = "Unknown"

            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                    name = max(counts, key=counts.get)
            names.append(name)

        for ((top, right, bottom, left), name) in zip(boxes, names):
            top = int(top * r)
            right = int(right * r)
            bottom = int(bottom * r)
            left = int(left * r)
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, "Name:" + name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.69, (0, 255, 0), 2)
            cv2.putText(frame, " Press Esc If Recognized", (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255))
        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()
    cap.release()

    return name
