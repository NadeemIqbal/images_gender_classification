# Gender Detection from Images

This project uses DeepFace to detect gender from images and sorts them into separate folders: `men`, `women`, and `unknown`.

## Features
- Batch processing of images for gender detection
- Uses DeepFace for face and gender analysis
- Automatically organizes images into folders based on detected gender
- Handles images with no detectable face

## Requirements
- Python 3.7+
- [DeepFace](https://github.com/serengil/deepface)
- tqdm

Install dependencies with:
```bash
pip install deepface tqdm
```

## Usage
1. Place your images in the `images/` folder (supported formats: .jpg, .jpeg, .png).
2. Run the script:
   ```bash
   python gender_detection.py
   ```
3. Processed images will be copied to `men/`, `women/`, or `unknown/` folders based on the detected gender.

## Notes
- The script will skip images already present in the output folders.
- No images or output folders are tracked by git (see `.gitignore`).
- No sensitive or personal data is included in this repository.

## Attribution
Any use of this code or its substantial portions must credit Nadeem Iqbal ([GitHub NadeemIqbal](https://github.com/NadeemIqbal)).

## License
See [LICENSE](LICENSE) for details. 