🖼️ Image to GIF Creator

Image to GIF Creator is a Python-based graphical application that allows users to upload, sort, resize, and convert images into an animated GIF. The app provides options for controlling image quality, compression, resolution, and frame durations.

🏆 Features
🚀 Upload multiple images and sort them for GIF creation.
🖼️ Live preview of selected images in customizable resolution.
✂️ Crop and resize images while maintaining aspect ratio.
🎨 Adjust image quality, compression level, and frame duration.
💾 Save GIF with custom settings (loop, resolution, duration per frame).
🔧 Installation
To run the Image to GIF Creator, ensure you have the following dependencies installed:

Prerequisites
Python 3.x
Pillow (PIL)
Tkinter (bundled with most Python installations)
ttkbootstrap
Install Dependencies
bash
Copy code
pip install Pillow ttkbootstrap
🚀 How to Use
Clone this repository to your local machine:

bash
Copy code
git clone https://github.com/achrefelouafi/image-gif-creator.git
Navigate to the project directory:

bash
cd image-gif-creator
Run the application:

bash
Copy code
python main.py
Usage Flow
Upload Images: Click the Upload Images button and select your image files.
Sort & Remove: Arrange your images using the Move Up and Move Down buttons. Remove unwanted images by selecting and pressing Remove.
Set Dimensions: Adjust width/height manually or choose from preset resolutions.
Quality & Compression: Use sliders to set image quality and compression level.
Set Frame Duration: Adjust the frame duration (ms) for each image in the GIF.
Preview: Preview your image before GIF creation.
Create GIF: Click Create GIF to save your animated GIF.

🖼️ UI Preview
⚙️ Commands
Upload Images: Select and upload images.
Sort Images: Use Move Up and Move Down buttons to reorder the images.
Remove Images: Click Remove to delete selected images.
Preview: Displays the image in the preview window.
Adjust Resolution: Manually input or select preset resolutions.
Set Quality: Use the quality slider to adjust image quality (1-100).
Set Compression: Adjust compression from 0 (none) to 9 (maximum).
Set Duration: Adjust the frame duration using the slider (in milliseconds).
Create GIF: Save the final GIF with the specified settings.

📦 Project Structure
bash
image-gif-creator/
│
├── main.py              # Main application script
├── requirements.txt     # Dependencies
├── README.md            # Project documentation
└── assets/              # Images and icons for the UI

🤝 Contributing
Feel free to fork this project, make your changes, and submit a pull request. We welcome all improvements!

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -m 'Add new feature').
Push to the branch (git push origin feature-branch).
Create a new Pull Request.

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

