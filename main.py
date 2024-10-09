import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import ttkbootstrap as ttk

class ImageGifCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to GIF Creator")
        self.root.geometry("800x600")  # Adjusted window size for better layout
        
        self.image_list = []  # Store uploaded images and their durations
        self.selected_resolution = ttk.StringVar(value="Original")
        self.quality = ttk.IntVar(value=75)
        self.compression = ttk.IntVar(value=0)
        self.current_duration = ttk.IntVar(value=100)  # Duration for each frame (in ms)
        self.current_preview = None
        self.ref_aspect_ratio = (1, 1)  # Aspect ratio of the first image
        
        # UI Elements
        self.create_widgets()
    
    def create_widgets(self):
        # Upload Button
        upload_btn = ttk.Button(self.root, text="Upload Images", command=self.upload_images, bootstyle="primary")
        upload_btn.pack(pady=10)
        
        # Sort Images
        sort_frame = ttk.Frame(self.root)
        sort_frame.pack(pady=10)
        up_btn = ttk.Button(sort_frame, text="Move Up", command=self.move_up, bootstyle="info-outline")
        down_btn = ttk.Button(sort_frame, text="Move Down", command=self.move_down, bootstyle="info-outline")
        remove_btn = ttk.Button(sort_frame, text="Remove", command=self.remove_image, bootstyle="danger-outline")
        up_btn.grid(row=0, column=0, padx=5)
        down_btn.grid(row=0, column=1, padx=5)
        remove_btn.grid(row=0, column=2, padx=5)

        # Image List Display
        self.image_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, width=50, bg="#333", fg="white", relief=tk.FLAT)
        self.image_listbox.pack(pady=10)
        self.image_listbox.bind("<<ListboxSelect>>", self.preview_image)

        # Manual Dimension Input
        self.width_entry = ttk.Entry(self.root, width=10)
        self.height_entry = ttk.Entry(self.root, width=10)

        self.width_label = ttk.Label(self.root, text="Width:")
        self.height_label = ttk.Label(self.root, text="Height:")
        
        self.width_label.pack()
        self.width_entry.pack(pady=5)
        self.height_label.pack()
        self.height_entry.pack(pady=5)

        self.width_entry.bind("<KeyRelease>", self.update_height)
        self.height_entry.bind("<KeyRelease>", self.update_width)

        # Resolution, Quality, Compression, and Duration settings
        res_label = ttk.Label(self.root, text="Choose Resolution:")
        res_label.pack()
        res_options = ["Original", "640x480", "800x600", "1024x768"]
        res_menu = ttk.OptionMenu(self.root, self.selected_resolution, *res_options)
        res_menu.pack()

        quality_label = ttk.Label(self.root, text="Quality (1-100):")
        quality_label.pack()
        quality_scale = ttk.Scale(self.root, from_=1, to=100, orient=tk.HORIZONTAL, variable=self.quality, bootstyle="success")
        quality_scale.pack()

        compression_label = ttk.Label(self.root, text="Compression Level (0-9):")
        compression_label.pack()
        compression_scale = ttk.Scale(self.root, from_=0, to=9, orient=tk.HORIZONTAL, variable=self.compression, bootstyle="success")
        compression_scale.pack()

        duration_label = ttk.Label(self.root, text="Duration per Frame (ms):")
        duration_label.pack()
        self.duration_scale = ttk.Scale(self.root, from_=10, to=1000, orient=tk.HORIZONTAL, variable=self.current_duration, bootstyle="warning")
        self.duration_scale.pack()

        # Duration Label
        self.duration_value_label = ttk.Label(self.root, text="Duration: 100 ms")
        self.duration_value_label.pack()

        # Bind scale value change to update label
        self.duration_scale.bind("<Motion>", self.update_duration_label)
        self.duration_scale.bind("<ButtonRelease-1>", self.update_duration_label)

        # Create GIF Button
        create_gif_btn = ttk.Button(self.root, text="Create GIF", command=self.create_gif, bootstyle="success")
        create_gif_btn.pack(pady=20)
        
        # Image Preview Frame
        self.preview_frame = ttk.Frame(self.root)
        self.preview_frame.pack(pady=10)
        self.preview_label = ttk.Label(self.preview_frame, text="Image Preview", bootstyle="info-inverse")
        self.preview_label.pack()
        self.preview_canvas = tk.Canvas(self.preview_frame, width=320, height=240, bg="black")
        self.preview_canvas.pack()

    def update_duration_label(self, event=None):
        duration_value = self.current_duration.get()
        self.duration_value_label.config(text=f"Duration: {duration_value} ms")
        
        selected_idx = self.image_listbox.curselection()
        if selected_idx:
            idx = selected_idx[0]
            self.image_list[idx][2] = duration_value  # Update duration for the selected image

    def upload_images(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
        if not file_paths:
            return
        
        for path in file_paths:
            image = Image.open(path)
            self.image_list.append([image, path, self.current_duration.get()])  # Append duration
            self.image_listbox.insert(tk.END, os.path.basename(path))
        
        # Update width and height entries based on the first image
        if self.image_list:
            first_img = self.image_list[0][0]
            self.ref_aspect_ratio = (first_img.width, first_img.height)
            self.width_entry.delete(0, tk.END)
            self.height_entry.delete(0, tk.END)
            self.width_entry.insert(0, str(first_img.width))
            self.height_entry.insert(0, str(first_img.height))

    def move_up(self):
        selected_idx = self.image_listbox.curselection()
        if selected_idx:
            idx = selected_idx[0]
            if idx > 0:
                self.image_list[idx], self.image_list[idx - 1] = self.image_list[idx - 1], self.image_list[idx]
                self.update_listbox(idx, idx - 1)

    def move_down(self):
        selected_idx = self.image_listbox.curselection()
        if selected_idx:
            idx = selected_idx[0]
            if idx < len(self.image_list) - 1:
                self.image_list[idx], self.image_list[idx + 1] = self.image_list[idx + 1], self.image_list[idx]
                self.update_listbox(idx, idx + 1)

    def remove_image(self):
        selected_idx = self.image_listbox.curselection()
        if selected_idx:
            idx = selected_idx[0]
            self.image_listbox.delete(idx)
            del self.image_list[idx]
            self.preview_canvas.delete("all")  # Clear preview
            self.current_duration.set(100)  # Reset duration to default

    def update_listbox(self, old_idx, new_idx):
        self.image_listbox.delete(0, tk.END)
        for _, path, _ in self.image_list:
            self.image_listbox.insert(tk.END, os.path.basename(path))
        self.image_listbox.select_set(new_idx)

    def update_height(self, event=None):
        """Update height based on width while maintaining aspect ratio."""
        try:
            width = float(self.width_entry.get())
            aspect_ratio = self.ref_aspect_ratio[0] / self.ref_aspect_ratio[1]
            height = width / aspect_ratio
            self.height_entry.delete(0, tk.END)
            self.height_entry.insert(0, str(int(height)))
        except ValueError:
            pass

    def update_width(self, event=None):
        """Update width based on height while maintaining aspect ratio."""
        try:
            height = float(self.height_entry.get())
            aspect_ratio = self.ref_aspect_ratio[1] / self.ref_aspect_ratio[0]
            width = height * aspect_ratio
            self.width_entry.delete(0, tk.END)
            self.width_entry.insert(0, str(int(width)))
        except ValueError:
            pass

    def crop_and_resize(self, img, target_width, target_height):
        """Crop and resize the image based on target dimensions, centering the image."""
        img_aspect = img.width / img.height
        target_aspect = target_width / target_height

        if img_aspect > target_aspect:
            # Image is wider than target
            new_height = target_height
            new_width = int(target_height * img_aspect)
        else:
            # Image is taller than target
            new_width = target_width
            new_height = int(target_width / img_aspect)

        img = img.resize((new_width, new_height), Image.LANCZOS)

        # Crop to fit the target size
        left = (new_width - target_width) // 2
        top = (new_height - target_height) // 2
        right = (new_width + target_width) // 2
        bottom = (new_height + target_height) // 2

        img = img.crop((left, top, right, bottom))
        return img

    def preview_image(self, event):
        selected_idx = self.image_listbox.curselection()
        if selected_idx:
            idx = selected_idx[0]
            img, path, duration = self.image_list[idx]
            
            # Get the selected resolution
            resolution = self.selected_resolution.get()

            # Clear previous images from the canvas
            self.preview_canvas.delete("all")
            
            if resolution != "Original":
                width, height = map(int, resolution.split('x'))
            else:
                width, height = img.size

            img_preview = self.crop_and_resize(img, width, height)

            # Centering the image for preview
            img_preview.thumbnail((320, 240), Image.LANCZOS)  # Maintain aspect ratio
            
            # Create a PhotoImage for preview
            self.current_preview = ImageTk.PhotoImage(img_preview)
            x = (320 - self.current_preview.width()) // 2
            y = (240 - self.current_preview.height()) // 2
            self.preview_canvas.create_image(x, y, image=self.current_preview, anchor=tk.NW)  # Centered preview
            
            # Update duration scale for the selected image
            self.current_duration.set(duration)  # Set duration
            self.duration_value_label.config(text=f"Duration: {duration} ms")

    def create_gif(self):
        if not self.image_list:
            messagebox.showerror("Error", "No images selected")
            return
        
        quality = self.quality.get()
        compression = self.compression.get()

        gif_images = []
        
        # Reference dimensions based on the first image
        ref_width, ref_height = self.ref_aspect_ratio
        
        for img, path, duration in self.image_list:
            target_width = int(self.width_entry.get())
            target_height = int(self.height_entry.get())

            img_resized = self.crop_and_resize(img, target_width, target_height)  # Resize the image
            img_resized = img_resized.convert("P", palette=Image.ADAPTIVE)
            gif_images.append((img_resized, duration))  # Store image and its duration

        save_path = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF", "*.gif")])
        if save_path:
            gif_images[0][0].save(
                save_path, save_all=True, append_images=[img[0] for img in gif_images[1:]], optimize=True, 
                quality=quality, compress_level=compression, duration=[img[1] for img in gif_images], loop=0
            )
            messagebox.showinfo("Success", "GIF created successfully!")
        else:
            messagebox.showerror("Error", "Save operation canceled")

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = ImageGifCreator(root)
    root.mainloop()
