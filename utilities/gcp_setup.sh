# set up Google Cloud Platform

## presetting for static ip address here:
# https://towardsdatascience.com/running-jupyter-notebook-in-google-cloud-platform-in-15-min-61e16da34d52

## update ubuntu
sudo apt-get update
sudo apt-get upgrade

## download Anaconda
wget https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh
chmod +x Anaconda3-2019.10-Linux-x86_64.sh
./Anaconda3-2019.10-Linux-x86_64.sh

## set up jupyter notebook
jupyter notebook --generate-config # creates confing file
## set jupyter confing (port 8000)
echo -e "c = get_config()\nc.NotebookApp.ip = '*'\nc.NotebookApp.open_browser = False\nc.NotebookApp.port = 8000" >> ~/.jupyter/jupyter_notebook_config.py
## run jupyter
#jupyter-notebook --no-browser --port=8000


## install GCSFUSE to mount Google buckets
export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s`
echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

sudo apt-get update
sudo apt-get install gcsfuse

## install git

sudo apt install git

git config --global user.email "@gmail.com"
git config --global user.name ""
