from datasets import load_dataset
import pandas as pd
import os

#ds = load_dataset("bigbio/chemprot", "chemprot_bigbio_kb")

output_dir = "./Datasets/chemprot/Original"

os.makedirs(output_dir, exist_ok=True)

#print(ds)

#print(ds['train'][0])

#for split in ["train", "test", "validation"]:
  #  df = pd.DataFrame(ds[split])
  #  split_name = "dev" if split == "validation" else split
  #  df.to_csv(f"{output_dir}/{split_name}.csv", index=False)