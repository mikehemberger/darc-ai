import os
import logging
import torch
from torch.utils.data import DataLoader
import pandas as pd
import numpy as np
from datasets import load_dataset, load_from_disk, Image, Dataset, DatasetDict
from transformers import ViTFeatureExtractor, ViTModel


def add_image_path(example):
    example['file_name'] = example['image'].filename.split("/")[-1]
    example["show_name"] = example['image'].filename.split("/")[-2]
    example["relative_path"] = "./data/" + "/".join(example['image'].filename.split("data/")[-1].split("/")[:-1])
    return example


torch.set_grad_enabled(False)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

logging.info(f"GPU: {device}")

def darc_imagefolder_feature_extraction(image_folder, vision_model, batch_size, num_workers):

    data_dir = f"./data/images/{image_folder}/"
    try:
        ds = load_from_disk(data_dir)
    except:
        ds = load_dataset('imagefolder', data_dir=data_dir, drop_labels=False)
        ds = ds.map(add_image_path)

    # Vision model
    vit_feature_extractor = ViTFeatureExtractor.from_pretrained(vision_model)
    vit_model = ViTModel.from_pretrained(vision_model, return_dict=True)
    vit_model.to(device)
    
    # loop over to subset into episodes
    classes = np.unique(ds["train"]["label"])
    class_labels = np.unique(ds["train"]["relative_path"])

    features = list()
    for c, label in zip(classes, class_labels):
            idx = np.where([1 if x == c else 0 for x in ds["train"]["label"]])[0]
            
            ds_subset = ds["train"].select(idx)
            #ds_subset.save_to_disk(label)
            print("NUMBER OF ROWS IN THE SUB-DATASET=", ds_subset.num_rows)

            #ds_subset = ds_subset.cast_column("image", Image(decode=True))
            ds_subset.set_format("torch", columns=["image", "label"])
            dataloader = DataLoader(ds_subset, batch_size=batch_size, num_workers=num_workers)

            for batch in dataloader:
                inputs = vit_feature_extractor([im for im in batch['image']], do_resize=True, return_tensors='pt')
                inputs.to(device)

                with torch.no_grad():
                    outputs = vit_model(**inputs)

                features.append(outputs.pooler_output.detach().cpu().numpy())

            # Save feature vectors
            feature_vectors = np.concatenate(features)
            np.save(f"{label}/feature_vectors.npy", feature_vectors)
            # Save to df
            #os.makedirs(label.replace("images", "metadata"), exist_ok=True)
            #ds_subset.to_csv(f'{label.replace("images", "metadata")}/metadata.csv')


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Extract features from image frames')
    parser.add_argument('--image_folder', type=str, required=True, help='Path towards folder of images')
    parser.add_argument('--vision_model', type=str, default="google/vit-base-patch16-224-in21k", help='image feature extractor')
    parser.add_argument('--batch_size', type=int, default=2, help='batch size')
    parser.add_argument('--num_workers', type=int, default=2, help='num workers')
    
    args = parser.parse_args()
    darc_imagefolder_feature_extraction(
        args.image_folder, args.vision_model, args.batch_size, args.num_workers)