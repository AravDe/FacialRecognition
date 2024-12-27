import cv2
import numpy as np
import traceback
import os
import albumentations as aug


class FacialRecognition:
    def __init__(self, dataset_path = "images", model_path = 'face_model.yml', target_size = (100,100),):
        
        self.faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

        self.dataset_path = dataset_path

        self.model_path = model_path

        self.target_size = target_size

        self.names = []

        
    def train_model(self):
        faces = []
        labels = []
        label_id = 0

        for person_name in os.listdir(self.dataset_path):
            print (os.listdir(self.dataset_path))
            person_path = os.path.join(self.dataset_path, person_name)
            if not os.path.isdir(person_path):
                continue

            for image_name in os.listdir(person_path):
                image_path = os.path.join(person_path, image_name)
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

                faces.append(image)
                labels.append(label_id)
            self.names.append(person_name)
            
            label_id += 1

        labelsfin = np.array(labels, dtype=np.int32)

        print(self.names)

        self.recognizer.train(faces, labelsfin)

        self.recognizer.save(self.model_path)

        self.recognizer.read(self.model_path)

    def generate_frames(self):
        try:
            print("Starting video capture...")

            # Open video capture
            cam = cv2.VideoCapture(0)
            if not cam.isOpened():
                raise Exception("Unable to access the webcam.")
            
            cam.set(cv2.CAP_PROP_FPS, 10)
            cam.set(cv2.CAP_PROP_BUFFERSIZE, 3)

            print("Camera opened successfully.")

            while True:
                try:
                    ret, frame = cam.read()
                    if not ret:
                        print("Failed to grab frame. Check your webcam connection.")
                        break

                    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    detected_faces = self.faceCascade.detectMultiScale(
                        grey_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
                    )

                    print(f"Faces detected: {len(detected_faces)}")

                    for (x, y, w, h) in detected_faces:
                        print(f"Face found at: x={x}, y={y}, w={w}, h={h}")
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (250, 0, 0), 2)
                        cropped_image = grey_frame[y:y+h, x:x+w]
                        resized_image = cv2.resize(cropped_image, self.target_size)
                        label, confidence = self.recognizer.predict(resized_image)

                        if confidence >= 60:
                            cv2.putText(frame, f"{self.names[label]}, {confidence}",(x, y -10), cv2.FONT_HERSHEY_COMPLEX, 0.9, (36,255,12),2)
                        if confidence < 60:
                            cv2.putText(frame, f"Unknown",(x, y -10), cv2.FONT_HERSHEY_COMPLEX, 0.9, (36,255,12),2)

                    # Display the video feed
                    cv2.imshow('Identity', frame)

                    # Break loop on 'q' key press
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print("Exiting...")
                        break
                except Exception as e:
                    print(f"Error inside loop: {e}")
                    traceback.print_exc()  
                    break  

            cam.release()
            cv2.destroyAllWindows()

        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()  
            input("Press Enter to exit.")
    def main(self):
        try:
            print("Starting face recognition...")
            self.face_recognition = FacialRecognition()
            print("Face recognition system is ready.")
            # Testing the webcam stream (uncomment below line to test directly with OpenCV)
            self.face_recognition.generate_frames()
        except Exception as e:
            print(f"An error occurred: {e}")

    if __name__ == "__main__":
        main()
        