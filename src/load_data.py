## load the data 
# process it 
## save the csv to raw

import os 
import argparse
from get_data import get_data, read_params

def load_and_save(config_path):
    config = read_params(config_path)
    df = get_data(config_path)
    raw_data_path = config['load_data']['raw_dataset_csv']
    new_cols = [col.replace(' ', '_') for col in df.columns]
    df.to_csv(raw_data_path, sep=',', index=False, header=new_cols)


if __name__=='__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--config', default='params.yaml')
    parse_arg = args.parse_args()
    load_and_save(config_path=parse_arg.config)
