import pickle
import face_recognition
from PIL import Image, ImageDraw
from cv2 import cv2
from deepface import DeepFace


def face_create():
    face_img = face_recognition.load_image_file("img/maks1.jpg")
    face_location = face_recognition.face_locations(face_img)
    justice_league_img = face_recognition.load_image_file("img/slava.jpg")
    justice_league_faces_locations = face_recognition.face_locations(justice_league_img)
    # print(face_location)
    # print(justice_league_faces_locations)
    # print(f"Found {len(face_location)} face(s) in this image")
    # print(f"Found {len(justice_league_faces_locations)} face(s) in this image")
    pil_img1 = Image.fromarray(face_img)
    draw1 = ImageDraw.Draw(pil_img1)

    for (top, right, bottom, left) in face_location:
        draw1.rectangle(((left, top), (right, bottom)), outline=(255, 255, 0), width=4)

    del draw1
    pil_img1.save("img/new_maks1.jpg")

    pil_img2 = Image.fromarray(justice_league_img)
    draw2 = ImageDraw.Draw(pil_img2)

    for (top, right, bottom, left) in justice_league_faces_locations:
        draw2.rectangle(((left, top), (right, bottom)), outline=(255, 255, 0), width=4)

    del draw2
    pil_img2.save("img/new_slava.jpg")


def extracting_faces(img_path):
    count = 1
    faces = face_recognition.load_image_file(img_path)
    faces_locations = face_recognition.face_locations(faces)

    for face_location in faces_locations:
        top, right, bottom, left = face_location

        face_img = faces[top:bottom, left:right]
        pil_img = Image.fromarray(face_img)
        pil_img.save(f"img/{count}_face_img.jpg")
        count += 1

    return f"Found {count} face(s) in this photo"


def compare_faces(img1_path, img2_path):
    img1 = face_recognition.load_image_file(img1_path)
    img1_encodings = face_recognition.face_encodings(img1)[0]
    # print(img1_encodings)

    img2 = face_recognition.load_image_file(img2_path)
    img2_encodings = face_recognition.face_encodings(img2)[0]

    result = face_recognition.compare_faces([img1_encodings], img2_encodings,)
    # print(result)

    if result[0]:
        print("Welcome to the club! :*")
    else:
        print("Sorry, not today... Next!")
    return result[0]


def detect_person_in_video():
    data = pickle.loads(open("Lena04ka_encodings.pickle", "rb").read())
    video = cv2.VideoCapture("video/video2.mp4")

    while True:
        ret, image = video.read()

        locations = face_recognition.face_locations(image)
        encodings = face_recognition.face_encodings(image, locations)

        for face_encoding, face_location in zip(encodings, locations):
            result = face_recognition.compare_faces(data["encodings"], face_encoding)
            match = None

            if True in result:
                match = data["name"]
                print(f"Match found! {match}")
            else:
                print("Фото человека нет в бд")
                break

            left_top = (face_location[3], face_location[0])
            right_bottom = (face_location[1], face_location[2])
            color = [0, 255, 0]
            cv2.rectangle(image, left_top, right_bottom, color, 4)

            left_bottom = (face_location[3], face_location[2])
            right_bottom = (face_location[1], face_location[2] + 20)
            cv2.rectangle(image, left_bottom, right_bottom, color, cv2.FILLED)
            cv2.putText(
                image,
                match,
                (face_location[3] + 10, face_location[2] + 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                4
            )

        cv2.imshow("detect_person_in_video is running", image)

        k = cv2.waitKey(20)
        if k == ord("q"):
            print("Q pressed, closing the app")
            break


def ff(img_path):
    try:
        result = DeepFace.analyze(img_path=img_path, actions=('emotion', 'age', 'gender', 'race'))
        return result
    except Exception as _ex:
        return _ex



if __name__ == '__main__':
    # print(extracting_faces("img/maks1.jpg"))
    compare_faces("img/zhenia.jpg", "img/cam.jpg")
    # detect_person_in_video()

