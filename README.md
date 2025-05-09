
Frontend
From root folder
./start-frontend.sh

Backend
From root folder
./start-backend.sh

rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt


Select Correct Python Interpreter

Press Cmd + Shift + P (Mac) or Ctrl + Shift + P (Windows/Linux)
Type and Select: Python: Select Interpreter

If you see something like "./backend/venv/bin/python" select it
Else, click Enter interpreter path
/Users/pratyakshsharma/VSCodeProjects/harmony-hr/backend/venv/bin/python
