DEST          = /usr/local/remote-sw

PROGRAM       = app.py myfunc.py raspi.py
SYSTEMD       = raspi.service 

all:            $(PROGRAM)

install:        $(PROGRAM)
		apt-get update -y
		apt-get install python3-pip -y
		pip3 install RPi.GPIO flask
		mkdir $(DEST)
		install -m 0755 -o root -g root $(PROGRAM) $(DEST)
		install -m 0755 -o root -g root $(SYSTEMD) /etc/systemd/system
		systemctl enable raspi
		systemctl start raspi

