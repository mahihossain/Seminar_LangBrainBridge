# How to setup a virtual env and load the datasets

- Create a virtual env in this directory
  
  `{your_python_path}/python3 -m venv ./.venv`
- Clean the virstual env:
  
  `virtualenv --clear ./.venv`
- Install requirements
  
  `./.venv/bin/python3 -m pip install -r requirements.txt`

- To test the utilities download the "Harry Potter" dataset from https://drive.google.com/drive/folders/1Q6zVCAJtKuLOh-zWpkS3lH8LBvHcEOE8 (the 'fMRI' folder is sufficient) in the current folder

- Check the output of 
  `./.venv/bin/python3 ./Datasets/main_dataloader.py --dataset_name harry_potter --modality reading --subject_number H --dataset_location ./fMRI/`
  
  it should be `(1211, 24983)`

## Windows users (by Nursulu)

Download the git repository to the preferred location (I stored it in Downloads):

`{your_path_to_store_git_repo}> git clone https://github.com/subbareddy248/Naturalistic-Brain-Datasets.git`


- Create a virtual environment in the directory where your Python is. To find your Python directory, you can type in cmd:

`where python`


- Then go to the folder where your Python is in cmd, and type:


`{your_python_folder_path}> python -m venv .\venv`


- Activate the virtual environment (still being in the Python folder)


`{your_python_folder_path}> .\venv\Scripts\Activate`


- Clean (uninstall) the environment’s packages:


`{your_python_folder_path}> cd venv`


`{your_python_folder_path}\venv> for /f "delims=" %i in ('pip freeze') do pip uninstall -y %i`


- Install requirements (before that, make sure your environment is activated and you have “(venv)” written to the left of the screen, like in the image below):


`{your_python_folder_path}\venv> python -m pip install -r {your_path_to_store_git_repo}\requirements.txt`


- To test the utilities, download the "Harry Potter" dataset from https://drive.google.com/drive/folders/1Q6zVCAJtKuLOh-zWpkS3lH8LBvHcEOE8 (the 'fMRI' folder is sufficient) in the current folder (venv). I downloaded it to the git repo folder, doesn’t matter much (this path is further referred to as {your_datasets_path})


- Check the output of:
`{your_python_folder_path}\venv> python {your_path_to_store_git_repo}\main_dataloader.py --dataset_name harry_potter --modality reading --subject_number H --dataset_location {your_datasets_path}\fMRI\`

it should be (1211, 24983)
