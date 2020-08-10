# RocketKite
Fly your kite around the planets in this little space simulator.

Android app available at: 
[https://play.google.com/store/apps/details?id=rocketkite.rocketkite](https://play.google.com/store/apps/details?id=rocketkite.rocketkite)

## Dependencies

- Python 3
- kivy 1.11.1


## Running locally using a virtual environment

```
# Create virtual env & install kivy
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
python main.py
```


## Compiling and running on Android

Tested on Ubuntu 18.04.5 LTS

```
# Install and activate the virtualenv (see above)

# Install Cython
pip install Cython

# Install any java compiler if you do not have one
sudo apt-get install openjdk-14-jdk

# Install buildozer
git clone https://github.com/kivy/buildozer.git
cd buildozer
python setup.py install
cd ..

# Connect your Android device via USB

# Build the apk, then deploy and run it on the device
# Customize buildozer.spec if required
# This takes a while on first run...
buildozer android debug deploy run

# Should you encounter any errors, debug using logcat
buildozer android debug deploy run logcat
```