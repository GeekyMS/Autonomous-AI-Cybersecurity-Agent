import pandas as pd

def load_raw_data(filename):
    
    try:
        df = pd.read_csv(filename)
        
        required_columns = [' Flow Duration', ' Total Fwd Packets', ' Total Backward Packets', 
                            ' Flow Packets/s', 'Total Length of Fwd Packets', 
                            ' Total Length of Bwd Packets', 'Flow Bytes/s', ' Label']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
            
        print(f"Loaded dataset: {len(df)} rows, {len(df.columns)} columns")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"File {filename} not found.")
    except Exception as e:
        raise Exception(f"Error reading file {filename}: {e}")

def engineer_features(df):
    
    new_df = pd.DataFrame()
    new_df['flow_duration'] = df[' Flow Duration']
    new_df['total_packets'] = df[' Total Fwd Packets'] + df[' Total Backward Packets']
    new_df['packets_per_second'] = df[' Flow Packets/s']
    new_df['total_bytes'] = df['Total Length of Fwd Packets'] + df[' Total Length of Bwd Packets']   
    new_df['bytes_per_second'] = df['Flow Bytes/s']
    new_df['Label'] = df[' Label']

    new_df['packets_per_second'] = new_df['packets_per_second'].clip(upper=1e6)
    new_df['bytes_per_second'] = new_df['bytes_per_second'].clip(upper=1e8)

    new_df = new_df[new_df['packets_per_second'] >= 0]
    new_df = new_df[new_df['bytes_per_second'] >= 0]
    new_df = new_df[new_df['total_packets'] >= 0]

    return new_df


def convert_to_binary_labels(df):
    
    new_df = df.copy()
    label_map = {"BENIGN":0}
    new_df['binary_label'] = new_df['Label'].map(label_map).fillna(1)
    new_df = new_df.dropna(subset=['binary_label'])
    return new_df

def save_preprocessed_data(df, filename="preprocessed_data.csv"):
    try:
        df.to_csv(filename, index=False)
        print(f"Preprocessed data saved to {filename}")
    except Exception as e:
        raise Exception(f"Error saving preprocessed data: {e}")
