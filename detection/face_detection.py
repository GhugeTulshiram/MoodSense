import cv2


# ==========================================
# FACE DETECTOR CLASS
# ==========================================
class FaceDetector:

    def __init__(self):
        # OpenCV Haar Cascade face detector
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades +
            "haarcascade_frontalface_default.xml"
        )

    # ==========================================
    # DETECT FACES FROM IMAGE
    # ==========================================
    def detect_faces(self, frame):

        # Convert image into grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(80, 80)
        )

        return faces

    # ==========================================
    # DRAW FACE RECTANGLES
    # ==========================================
    def draw_faces(self, frame, faces):

        for (x, y, w, h) in faces:

            # Draw rectangle around face
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (255, 255, 255),
                2
            )

            # Display label
            cv2.putText(
                frame,
                "Face Detected",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

        return frame