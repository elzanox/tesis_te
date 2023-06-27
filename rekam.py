import cv2

# Inisialisasi video capture
video_capture = cv2.VideoCapture(0)  # 0 menandakan penggunaan webcam default

# Mendapatkan properti frame width dan height
frame_width = int(video_capture.get(3))
frame_height = int(video_capture.get(4))

# Membuat objek video writer
video_writer = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (640, 480))

while True:
    # Membaca frame dari webcam
    ret, frame = video_capture.read()

    # Menulis frame ke objek video writer
    video_writer.write(frame)

    # Menampilkan frame
    cv2.imshow('Video', frame)

    # Jika tombol 'q' ditekan, hentikan rekaman
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Melepaskan sumber daya
video_capture.release()
video_writer.release()
cv2.destroyAllWindows()
