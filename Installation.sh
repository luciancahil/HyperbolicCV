conda create -n HCNN python=3.8 pip
conda activate HCNN
conda install pytorch torchvision cpuonly -c pytorch
pip install -r requirements.txt

conda install -c conda-forge "libtiff<4.5"
