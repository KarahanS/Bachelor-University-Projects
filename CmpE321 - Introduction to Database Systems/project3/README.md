#### To run the program: 

You can run the program on Windows PowerShell by following the steps provided below.

1) Clone this directory into your local workspace and open ```app``` folder.  
2) Create a virtual environment named as ```env```.
```cmd
 python -m venv env  
```
3) Activate your virtual environment:
```cmd
env\Scripts\activate
```
4) Install the necessary python packages listed in the ```requirements.txt```:
```cmd
pip install -r requirements.txt
```
5) Run the Flask application:
```cmd
flask run
```
6) You can test the application by using the website running on ```http://127.0.0.1:5000/```.


You can change the authentication credentials for your database using [db_config.json](https://github.com/KarahanS/University-Projects/blob/master/CmpE321%20-%20Introduction%20to%20Database%20Systems/project3/app/db_config.json).
