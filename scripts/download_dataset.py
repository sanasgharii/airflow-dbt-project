import kagglehub
import shutil
import os


# Download dataset
path = kagglehub.dataset_download(
    "mehmettahiraslan/customer-shopping-dataset",
)

print("Downloaded to:", path)


# Move CSV into dbt seeds folder
source_file = os.path.join(
    path,
    "customer_shopping_data.csv",
)

destination_folder = os.path.join(
    "dbt",
    "my_project",
    "seeds",
)

destination_file = os.path.join(
    destination_folder,
    "customer_shopping_data.csv",
)

os.makedirs(destination_folder, exist_ok=True)
shutil.copy(source_file, destination_file)

print("Dataset moved to seeds folder.")