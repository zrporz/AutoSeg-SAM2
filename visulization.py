import numpy as np
from PIL import Image, ImageEnhance
import os
from tqdm import tqdm
import cv2
import random
import argparse
import imageio


def images_to_video(input_folder, output_video, fps=30,max_width=1920, max_height=1080):
    images = [img for img in os.listdir(input_folder) if img.endswith(".png")]
    images.sort(key=lambda x: int(os.path.splitext(x)[0]))  

    if not images:
        print("No images found in the folder.")
        return

    frames = [imageio.imread(os.path.join(input_folder, img)) for img in images]
    imageio.mimwrite(output_video, frames, fps=30)
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_path",type=str,required=True)
    parser.add_argument("--output_dir",type=str,required=True)
    parser.add_argument("--level",choices=['default','small','middle','large'])
    args = parser.parse_args()

    level = args.level
    basedir = args.output_dir
    npybasedir = os.path.join(basedir,level,'final-output')
    imagebasedir = args.video_path
    savedir = os.path.join(basedir,level,'visualization','seperate')
    os.makedirs(savedir,exist_ok=True)
    image_name_list = os.listdir(imagebasedir)
    image_name_list.sort()

    npy_name_list = []
    for name in os.listdir(npybasedir):
        if 'npy' in name:
            npy_name_list.append(name)
    npy_name_list.sort()
    print(npy_name_list)
    npy_list = [np.load(os.path.join(npybasedir,name)) for name in npy_name_list]
    image_list = [Image.open(os.path.join(imagebasedir,name)) for name in image_name_list]
    assert len(npy_list) == len(image_name_list)
    print(len(npy_list))

    uid_dirs = {}
    for uid in range(npy_list[0].shape[0]):
        uid_dir = os.path.join(savedir, f"uid_{uid}")
        os.makedirs(uid_dir, exist_ok=True)
        uid_dirs[uid] = uid_dir


    for frame_id, (masks, image) in tqdm(enumerate(zip(npy_list,image_list))):
        dark_image = ImageEnhance.Brightness(image).enhance(0.3)
        dark_image_array = np.array(dark_image)
        highlighted_images = []
        mask_images = []
        for uid in range(masks.shape[0]):

            current_mask = masks[uid][0]
            image_array = np.array(image)

            highlighted_image_array = np.where(current_mask[:, :, np.newaxis], image_array, dark_image_array)
            highlighted_image = Image.fromarray(highlighted_image_array.astype('uint8'))

            bool_mask_array = (current_mask * 255).astype(np.uint8)
            bool_mask_image = Image.fromarray(bool_mask_array).convert("RGB")

            uid_frame = Image.new('RGB', (image.width, image.height * 2))
            uid_frame.paste(highlighted_image, (0, 0))
            uid_frame.paste(bool_mask_image, (0, image.height))
            uid_frame.save(os.path.join(uid_dirs[uid], f"{frame_id:05}.png"))

            highlighted_images.append(highlighted_image)
            mask_images.append(bool_mask_image)

        total_width = image.width * len(highlighted_images)
        max_height = image.height * 2

        final_image = Image.new('RGB', (total_width, max_height))

        for i, img in enumerate(highlighted_images):
            final_image.paste(img, (i * image.width, 0))

        for i, img in enumerate(mask_images):
            final_image.paste(img, (i * image.width, image.height))

        final_image.save(os.path.join(savedir,f"{frame_id:05}.png"))

    savedir = os.path.join(basedir,level,'visualization','full-mask-npy')
    video_path = os.path.join(basedir,level,'visualization',f'full-mask-{level}.mp4')
    os.makedirs(savedir,exist_ok=True)
    image_name_list = os.listdir(imagebasedir)
    image_name_list.sort()
    print(image_name_list)
    npy_name_list = []
    for name in os.listdir(npybasedir):
        if 'npy' in name:
            npy_name_list.append(name)
    npy_name_list.sort()
    print(npy_name_list)
    npy_list = [np.load(os.path.join(npybasedir,name)) for name in npy_name_list]
    image_list = [Image.open(os.path.join(imagebasedir,name)) for name in image_name_list]

    assert len(npy_list) == len(image_name_list)
    print(len(npy_list))
    # Generate a list of random colors
    def generate_random_colors(num_colors):
        colors = []
        for _ in range(num_colors):
            color = tuple(random.randint(0, 255) for _ in range(3))
            colors.append(color)
        return colors

    num_masks = max(len(masks) for masks in npy_list)
    colors = generate_random_colors(num_masks)

    video_frames = []
    output_path_list = []
    for frame_id, (masks, image) in tqdm(enumerate(zip(npy_list, image_list))):
        image_np = np.array(image)
        mask_combined = np.zeros_like(image_np, dtype=np.uint8)

        for i, mask in enumerate(masks):
            color = colors[i % len(colors)]
            # Ensure the mask is binary (0 or 1)
            mask_binary = (mask[0] > 0).astype(np.uint8)
            # Apply the mask color
            for j in range(3):  # For each channel in RGB
                mask_combined[:, :, j] += mask_binary * color[j]

        # Blend the original image with the colored masks
        mask_combined = np.clip(mask_combined, 0, 255)
        blended_image = cv2.addWeighted(image_np, 0.7, mask_combined, 0.3, 0)

        # Save each frame
        output_path = os.path.join(savedir, f"frame_{frame_id:04d}.png")
        output_path_list.append(output_path)

        Image.fromarray(blended_image).save(output_path)
        
    # Generate the video

    frames = [imageio.imread(img) for img in output_path_list]
    imageio.mimwrite(video_path, frames, fps=30)

    print(f"Video saved at {video_path}")


    output_video_dir = os.path.join(basedir,level,'visualization','seperate','videos')
    os.makedirs(output_video_dir,exist_ok=True)

    for uid in tqdm(range(len(uid_dirs))):
        uid_folder = uid_dirs[uid]
        images_to_video(uid_folder, os.path.join(output_video_dir,f"uid_{uid}.mp4"))