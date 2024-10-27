# Importar las bibliotecas necesarias
import cv2  # OpenCV para captura y manipulación de video
from ultralytics import YOLO  # YOLOv8 para detección de objetos

# Cargar el modelo YOLOv8 preentrenado
# 'yolov8lq.pt' es un modelo liviano; puedes usar otros como 'yolov8l.pt' para mayor precisión
model = YOLO('yolov8l.pt')

# Inicializar la cámara (índice 0 generalmente es la cámara por defecto)
cap = cv2.VideoCapture(0)

# Iniciar un bucle que se ejecutará mientras la cámara esté abierta
while cap.isOpened():
    # Leer un fotograma de la cámara
    ret, frame = cap.read()  
    if not ret:  # Si no se lee el fotograma correctamente, se sale del bucle
        break

    # Ejecutar la detección de objetos en el fotograma usando YOLOv8
    results = model(frame)

    # Recorrer las cajas delimitadoras (bounding boxes) detectadas
    for result in results[0].boxes:
        # Extraer coordenadas de la caja (x1, y1, x2, y2)
        x1, y1, x2, y2 = map(int, result.xyxy[0])
        # Extraer la confianza (confidence) del objeto detectado
        conf = result.conf[0]
        # Extraer la clase del objeto detectado (por ejemplo, 'person', 'car')
        label = result.cls[0]

        # Dibujar un rectángulo alrededor del objeto detectado
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Verde con grosor 2

        # Dibujar la etiqueta con el nombre del objeto y la confianza
        cv2.putText(frame, f'{label} ({conf:.2f})', (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Mostrar el video con las detecciones en una ventana
    cv2.imshow('YOLOv8 Object Detection', frame)

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos de la cámara y cerrar las ventanas de OpenCV
cap.release()
cv2.destroyAllWindows()
