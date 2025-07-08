import os
from deepface import DeepFace
import shutil
from tqdm import tqdm
import gc

# Get script directory to always work relative to script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Paths
input_folder = os.path.join(script_dir, 'images')
men_folder = os.path.join(script_dir, 'men')
women_folder = os.path.join(script_dir, 'women')
unknown_folder = os.path.join(script_dir, 'unknown')

# Create output folders if they don't exist
os.makedirs(men_folder, exist_ok=True)
os.makedirs(women_folder, exist_ok=True)
os.makedirs(unknown_folder, exist_ok=True)

# List all image files
image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

print("Current working directory:", os.getcwd())
print(f"Found {len(image_files)} images to process.")

# Batch size: adjust based on your RAM
batch_size = 50

# Counters
count_men = 0
count_women = 0
count_unknown = 0
count_errors = 0

for i in range(0, len(image_files), batch_size):
    batch = image_files[i:i+batch_size]
    print(f"\nProcessing batch {i//batch_size + 1} with {len(batch)} images...")

    for image_file in tqdm(batch):
        img_path = os.path.join(input_folder, image_file)

        # Skip if already exists in target folders
        if (os.path.exists(os.path.join(men_folder, image_file)) or
            os.path.exists(os.path.join(women_folder, image_file)) or
            os.path.exists(os.path.join(unknown_folder, image_file))):
            continue

        try:
            objs = DeepFace.analyze(img_path=img_path, actions=['gender'], enforce_detection=False)
            result = objs[0] if isinstance(objs, list) else objs

            # check if face detected
            region = result.get('region', {})
            w, h = region.get('w', 0), region.get('h', 0)

            if w == 0 or h == 0:
                target_folder = unknown_folder
                count_unknown += 1
            else:
                gender_dict = result['gender']
                predicted_gender = max(gender_dict, key=gender_dict.get)

                if predicted_gender == 'Man':
                    target_folder = men_folder
                    count_men += 1
                elif predicted_gender == 'Woman':
                    target_folder = women_folder
                    count_women += 1
                else:
                    target_folder = unknown_folder
                    count_unknown += 1

            shutil.copy(img_path, os.path.join(target_folder, image_file))

        except Exception as e:
            print(f"Error processing {image_file}: {e}")
            count_errors += 1
            continue

    # Free memory after each batch
    gc.collect()

print("\n✅ Done!")
print(f"Total men: {count_men}")
print(f"Total women: {count_women}")
print(f"Total unknown/no-face: {count_unknown}")
print(f"Total errors: {count_errors}")
