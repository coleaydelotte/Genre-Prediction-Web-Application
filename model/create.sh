sudo mkdir -p ./uploads
sudo mkdir -p ./data
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r ./model/requirements.txt
chmod +x ./model/upload_cleaner_script.sh
nohup python3 ./model/api.py > ./model/api.log 2>&1 &
./model/upload_cleaner_script.sh
