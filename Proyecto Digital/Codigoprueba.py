# Importar las bibliotecas necesarias
import cv2  # OpenCV para captura y manipulación de video
from ultralytics import YOLO  # YOLOv8 para detección de objetos
from googletrans import Translator  # Traductor para la traducción en tiempo real

# Crear un objeto traductor
translator = Translator()

# Cargar el modelo YOLOv8 preentrenado (versión más ligera para optimizar rendimiento)
model = YOLO('yolov8n.pt')  # Cambiar a la versión nano para mejorar velocidad

# Inicializar la cámara (índice 0 generalmente es la cámara por defecto)
cap = cv2.VideoCapture(0)

# Reducir la resolución de la cámara (por ejemplo, 640x480)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Definir el área del cuadro central (incrementamos el tamaño a 70% del ancho y alto del video)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Definir el cuadro central en coordenadas (70% del ancho y alto del video para una mayor área)
box_width = int(frame_width * 0.7)
box_height = int(frame_height * 0.7)
x_center = frame_width // 2
y_center = frame_height // 2
box_x1 = x_center - box_width // 2
box_y1 = y_center - box_height // 2
box_x2 = x_center + box_width // 2
box_y2 = y_center + box_height // 2

# Variable para almacenar el nombre del objeto detectado
detected_object = ""

# Iniciar un bucle que se ejecutará mientras la cámara esté abierta
while cap.isOpened():
    # Leer un fotograma de la cámara
    ret, frame = cap.read()
    if not ret:  # Si no se lee el fotograma correctamente, se sale del bucle
        break

    # Dibujar el cuadro verde en el centro del video
    cv2.rectangle(frame, (box_x1, box_y1), (box_x2, box_y2), (0, 255, 0), 2)  # Verde con grosor 2

    # Mostrar el nombre del objeto detectado en pantalla si existe
    if detected_object:
        cv2.putText(frame, detected_object, (box_x1, box_y1 - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Mostrar el video con el cuadro central
    cv2.imshow('YOLOv8 Object Detection (Cuadro Central)', frame)

    # Detectar si se ha presionado la tecla 'C'
    if cv2.waitKey(1) & 0xFF == ord('c'):
        # Ejecutar la detección de objetos
        results = model(frame)

        # Recorrer los objetos detectados
        detected_object = ""  # Reiniciar el objeto detectado
        for result in results[0].boxes:
            # Extraer las coordenadas de la caja delimitadora
            x1, y1, x2, y2 = map(int, result.xyxy[0])

            # Verificar si la caja detectada está dentro del cuadro verde (al menos un 80% del objeto debe estar en el cuadro)
            if (x1 >= box_x1 and y1 >= box_y1 and x2 <= box_x2 and y2 <= box_y2):
                # Extraer la clase del objeto detectado
                label = result.cls[0]
                class_name = model.names[int(label)]  # Obtener el nombre de la clase en inglés

                # Traducir el nombre de la clase al español usando Google Translate
                translation = translator.translate(class_name, src='en', dest='es')
                class_name_es = translation.text  # Obtener el texto traducido

                # Guardar el nombre del objeto detectado para mostrarlo en pantalla
                detected_object = f'Objeto: {class_name_es}'
                break  # Salir del bucle después de detectar un objeto dentro del cuadro

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos de la cámara y cerrar las ventanas de OpenCV
cap.release()
cv2.destroyAllWindows()
