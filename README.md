# simple_wallet
A simple wallet API built with python Flask (For AjoCard Job Test)


![alt text](https://github.com/trustedcoder/simple_wallet/blob/master/sample.png)

![alt text](https://github.com/trustedcoder/simple_wallet/blob/master/sample2.png)

# How to run
(1) clone the repository
(2) create a virtual environment in the project root directory
(3) install all dependencies. Open a terminal in the root project directory and type pip install -r requirements.txt
(4) Create database and tables by typing this in terminal
python manage.py db init
python manage.py db migrate
python manage.py db upgrade

(5) Then finall run the prject by typing this in terminal
python manage.py run

(6) Visit http://0.0.0.0:5000/ on your computer to see the documentation of the API

* Please ensure that port 5000 is not being used.
