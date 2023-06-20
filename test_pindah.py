import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")

        # Membuat tombol "Buka Folder"
        self.button_open_folder = tk.Button(root, text="Buka Folder", command=self.open_folder)
        self.button_open_folder.pack()

        # Membuat tombol "Buka Gambar"
        self.button_open_image = tk.Button(root, text="Buka Gambar", command=self.open_image, state=tk.DISABLED)
        self.button_open_image.pack()

        # Membuat label untuk menampilkan gambar
        self.image_label = tk.Label(root)
        self.image_label.pack()

        # Menyimpan path folder yang sedang dibuka
        self.current_folder_path = None

        # Menyimpan list path gambar dalam folder
        self.image_paths = []
        self.current_image_index = 0

    def open_folder(self):
        # Memilih folder menggunakan file dialog
        folder_path = filedialog.askdirectory()

        if folder_path:
            # Mendapatkan semua path gambar dalam folder
            self.image_paths = self.get_image_paths(folder_path)
            self.current_image_index = 0

            if self.image_paths:
                # Menampilkan gambar pertama dalam folder
                self.display_image()

                # Mengaktifkan tombol "Buka Gambar"
                self.button_open_image.config(state=tk.NORMAL)

            else:
                # Menonaktifkan tombol "Buka Gambar" jika tidak ada gambar dalam folder
                self.button_open_image.config(state=tk.DISABLED)

            # Menyimpan path folder yang sedang dibuka
            self.current_folder_path = folder_path

    def get_image_paths(self, folder_path):
        # Mendapatkan semua path gambar dalam folder
        image_extensions = (".jpg", ".jpeg", ".png", ".gif")
        image_paths = []

        for root_dir, _, file_names in os.walk(folder_path):
            for file_name in file_names:
                if file_name.lower().endswith(image_extensions):
                    image_paths.append(os.path.join(root_dir, file_name))

        return image_paths

    def open_image(self):
        if self.current_folder_path and self.image_paths:
            # Menampilkan gambar saat ini dalam folder
            self.display_image()

    def display_image(self):
        # Mendapatkan path gambar saat ini
        image_path = self.image_paths[self.current_image_index]

        # Menampilkan gambar menggunakan PIL
        image = Image.open(image_path)
        image.thumbnail((800, 600))  # Mengubah ukuran gambar agar sesuai dengan layar
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def next_image(self):
        if self.current_image_index < len(self.image_paths) - 1:
            # Menampilkan gambar berikutnya
            self.current_image_index += 1
            self.display_image()

    def previous_image(self):
        if self.current_image_index > 0:
            # Menampilkan gambar sebelumnya
            self.current_image_index -= 1
            self.display_image()

# Membuat instance Tkinter
root = tk.Tk()

# Membuat instance ImageViewer
image_viewer = ImageViewer(root)
root.mainloop()
