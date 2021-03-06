import cv2
import simpleaudio

#Modelos de reconocimiento de rostro y ojos
eye_cascPath = './haarcascade_eye_tree_eyeglasses.xml'
face_cascPath = './haarcascade_frontalface_alt.xml'
faceCascade = cv2.CascadeClassifier(face_cascPath)
eyeCascade = cv2.CascadeClassifier(eye_cascPath)

#Creación de la alarma como objeto para su reproducción
wave_obj = simpleaudio.WaveObject.from_wave_file("beep-01a.wav")

#Tiempo con los ojos cerrados
asleepTime = 0

#Captura de fotogramas, primero de un video y luego: directamente de la cámara
#cap = cv2.VideoCapture('ruta al video')
cap = cv2.VideoCapture(0)

while 1:
    #Procesamiento de un fotograma
    ret, img = cap.read()
    if ret:
        #Procesado como escala de grises para reducir problemas de iluminación
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detección de rostros en la imagen
        faces = faceCascade.detectMultiScale(
            frame,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            # flags = cv2.CV_HAAR_SCALE_IMAGE
        )
        if len(faces) > 0:
            # Dibujando un rectángulo alrededor de los rostros
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #Recortando la imagen al rectángulo anterior
            frame_tmp = img[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]:1, :]
            frame = frame[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]:1]
            #Detectando los ojos
            eyes = eyeCascade.detectMultiScale(
                frame,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                # flags = cv2.CV_HAAR_SCALE_IMAGESIMPLEX
            )
            #Aumenta el tiempo con los ojos cerrados si no detecta ojos en la imagen
            if len(eyes) == 0:
                asleepTime += 1
            #Reinicia el tiempo con los ojos cerrados si detecta ojos
            else:
                asleepTime = 0
            #Más de un segundo y menos de 4 implica adormecimiento
            if asleepTime > 1 and asleepTime < 4:
                cv2.putText(frame_tmp, "Adormecido", (30,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            #4 segundos o más implica dormido
            elif asleepTime > 3:
                cv2.putText(frame_tmp, "Dormido", (30,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            #Alarma de estado dormido detectado
                play_obj = wave_obj.play()
                play_obj.wait_done()
            #De lo contrario se asume despierto
            else:
                cv2.putText(frame_tmp, "Despierto", (30,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            #Definiendo propiedades de la ventana de la aplicación (el nombre de la ventana en inglés porque no permite tildes o ñ)
            frame_tmp = cv2.resize(frame_tmp, (700, 700), interpolation=cv2.INTER_LINEAR)
            cv2.imshow("Dream state detection", frame_tmp)
        waitkey = cv2.waitKey(1)
        #Deteniendo la ejecución si se detecta que el usuario presiona q/Q
        if waitkey == ord('q') or waitkey == ord('Q'):
            cv2.destroyAllWindows()
            break
