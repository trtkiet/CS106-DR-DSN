import subprocess

if __name__ == '__main__':
    datasets = {'summe', 'tvsum'}
    name = 'd-dsn-wo-lambda'
    split_ids = {0, 1, 2, 3, 4}
    for dataset in datasets:
        for split_id in split_ids:
            split_file = f'datasets/{dataset}_splits.json'
            print(dataset)
            if dataset == 'summe':
                dataset_path = 'datasets/eccv16_dataset_summe_google_pool5.h5'
            elif dataset == 'tvsum':
                dataset_path = 'datasets/eccv16_dataset_tvsum_google_pool5.h5'
            cmd = f"python main.py -d {dataset_path} -s {split_file} --split-id {split_id} -m {dataset} --save-results --save-dir log/{name}/{dataset}/split_{split_id}/"
            print(f"Running command: {cmd}")
            subprocess.run(cmd, shell=True)