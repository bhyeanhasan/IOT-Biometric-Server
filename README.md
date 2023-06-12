
```
pip install djangorestframework
python manage.py runserver 0.0.0.0:8000
http://192.168.43.62:8000/
```

### Connection:
 * Biometric module green wire to Arduino Pin 2
 * Biometric module yellow wire to Arduino Pin 3
 * Biometric module red wire to Arduino Pin 5v
 * Biometric module black wire to Arduino Pin Gnd

### For capturing the raw fingerprint data to the PC :

* Import the ``FPM.zip`` library to IDE
* Then upload image_to_pc.ino to the board
* Now install the requirements.txt
* launch the django web application using ```python manage.py runserver```

* source: [https://github.com/brianrho/FPM]()
