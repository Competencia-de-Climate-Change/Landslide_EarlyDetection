from dataloader import DataLoader
PATH_TO_DATASET = '/home/jupyter/data-step/clean_dataset/'

def main():

    dl = DataLoader()

    positive_data = dl.create_positive_dataset()
    torch.save(positive_data, PATH_TO_DATASET + 'positive_dataset.pt')

    negative_data = dl.create_negative_dataset()
    torch.save(negative_data, PATH_TO_DATASET * 'negative_dataset.pt')
    
if __name__ == "__main__":
    main()
