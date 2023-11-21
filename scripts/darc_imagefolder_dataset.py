import os
import logging
import pandas as pd
import numpy as np
from datasets import load_dataset, load_from_disk

logging.info("CONSTRUCT HUGGINGFACE DATASET")

def add_image_path(example):
    example['file_name'] = example['image'].filename.split("/")[-1]
    example["show_name"] = example['image'].filename.split("/")[-2]
    example["relative_path"] = "./data/" + "/".join(example['image'].filename.split("data/")[-1].split("/")[:-1])
    return example


def darc_imagefolder_dataset(image_folder):

    data_dir = f"./data/images/{image_folder}/"
    try:
        ds = load_from_disk(data_dir)
    except:
        ds = load_dataset('imagefolder', data_dir=data_dir, drop_labels=False)
        ds = ds.map(add_image_path)
        #ds.save_to_disk(data_dir)
        #df = ds["train"].to_pandas()
        # df.to_csv(f'{data_dir.replace("images", "metadata")}/metadata.csv', index=False)

    logging.info(f"NUMBER OF ROWS IN THE DATASET=", ds.num_rows)

    # loop over to subset into episodes
    classes = np.unique(ds["train"]["label"])
    class_labels = np.unique(ds["train"]["relative_path"])

    for c, label in zip(classes, class_labels):
        idx = np.where([1 if x == c else 0 for x in ds["train"]["label"]])[0]
        
        ds_subset = ds["train"].select(idx)
        ds_subset.save_to_disk(label)
        print("NUMBER OF ROWS IN THE SUB-DATASET=", ds_subset.num_rows)

        # Save to df
        os.makedirs(label.replace("images", "metadata"), exist_ok=True)
        ds_subset.to_csv(f'{label.replace("images", "metadata")}/metadata.csv')
        #df = ds_subset.to_pandas()
        #df.to_csv(f'{label.replace("images", "metadata")}/metadata.csv', index=False)



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Generate a huggingface dataset per episode and show')
    parser.add_argument('--image_folder', type=str, required=True, help='Path towards folder of images')
    args = parser.parse_args()
    darc_imagefolder_dataset(args.image_folder)