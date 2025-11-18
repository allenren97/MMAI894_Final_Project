import os
import pandas as pd
from sklearn.model_selection import train_test_split

def split_dataset(input_csv_path, output_dir, test_size = 0.1, val_size = 0.1, random_state = 42):
    # Load the dataset
    df = pd.read_csv(input_csv_path)

    # First split into train+val and test
    train_val_df, test_df = train_test_split(df, test_size=test_size, random_state=random_state)

    # Then split train+val into train and val
    val_relative_size = val_size / (1 - test_size)  # Adjust validation size relative to train+val
    train_df, val_df = train_test_split(train_val_df, test_size=val_relative_size, random_state=random_state)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save the splits to CSV files
    train_df.to_csv(os.path.join(output_dir, 'train.csv'), index=False)
    val_df.to_csv(os.path.join(output_dir, 'validation.csv'), index=False)
    test_df.to_csv(os.path.join(output_dir, 'test.csv'), index=False)

    print(f"Dataset split completed. Files saved to {output_dir}")
    
    return train_df, val_df, test_df