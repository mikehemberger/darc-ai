import os
import logging
import torch
from torch.utils.data import DataLoader
import pandas as pd
import numpy as np
from datasets import load_dataset, load_from_disk, Image, Dataset, DatasetDict
from transformers import Blip2Processor, Blip2ForConditionalGeneration


def add_image_path(example):
    example['file_name'] = example['image'].filename.split("/")[-1]
    example["show_name"] = example['image'].filename.split("/")[-2]
    example["relative_path"] = "./data/" + "/".join(example['image'].filename.split("data/")[-1].split("/")[:-1])
    return example


torch.set_grad_enabled(False)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

logging.info(f"GPU: {device}")

def darc_imagefolder_textcaption_generation(image_folder, language_model, batch_size, num_workers):
    
    data_dir = f"./data/images/{image_folder}/"
    try:
        ds = load_from_disk(data_dir)
    except:
        ds = load_dataset('imagefolder', data_dir=data_dir, drop_labels=False)
        ds = ds.map(add_image_path)
    
    # Large Language Model
    blip_processor = Blip2Processor.from_pretrained(language_model)
    blip_model = Blip2ForConditionalGeneration.from_pretrained(language_model)  #, torch_dtype=torch.float16)
    blip_model.to(device)
    
    # loop over to subset into episodes
    classes = np.unique(ds["train"]["label"])
    class_labels = np.unique(ds["train"]["relative_path"])

    for c, label in zip(classes, class_labels):
            idx = np.where([1 if x == c else 0 for x in ds["train"]["label"]])[0]
            
            ds_subset = ds["train"].select(idx)
            print("NUMBER OF ROWS IN THE SUB-DATASET=", ds_subset.num_rows)

            ds_subset.set_format("torch", columns=["image", "label"])  #ds_subset = ds_subset.cast_column("image", Image(decode=True))
            dataloader = DataLoader(ds_subset, batch_size=batch_size, num_workers=num_workers)

            # CAPTION GENERATION
            captions = list()
            for batch in dataloader:
                inputs = blip_processor([im for im in batch['image']], do_resize=True, return_tensors='pt')
                inputs.to(device)
                with torch.no_grad():
                    outputs = blip_model.generate(**inputs, max_new_tokens=20)
                captions.append(blip_processor.batch_decode(outputs, skip_special_tokens=True))

            # Save feature vectors
            df = pd.DataFrame()
            df["caption"] = [txt.strip() for txt in captions]
            df.to_csv(f"./data/images/{image_folder}/dataframe.csv", index=False) # f"{label}/dataframe.csv"
    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Genenerate text captions from images')
    parser.add_argument('--image_folder', type=str, required=True, help='Path towards folder of images')
    parser.add_argument('--language_model', type=str, default="Salesforce/blip2-opt-2.7b", help='image feature extractor')
    parser.add_argument('--batch_size', type=int, default=2, help='batch size')
    parser.add_argument('--num_workers', type=int, default=2, help='num workers')
    
    args = parser.parse_args()
    darc_imagefolder_textcaption_generation(
         args.image_folder, args.language_model,
         args.batch_size, args.num_workers)