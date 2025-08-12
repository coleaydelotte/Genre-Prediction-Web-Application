sudo mkdir -p ./uploads
sudo mkdir -p ./data
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r ./model/requirements.txt
chmod +x ./model/upload_cleaner_script.sh
./model/upload_cleaner_script.sh & python3 ./model/api.py
