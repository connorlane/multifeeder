sudo systemctl disable cloud9.service
sudo systemctl disable gateone.service
sudo systemctl disable bonescript.service
sudo systemctl disable bonescript.socket
sudo systemctl disable bonescript-autorun.service
sudo systemctl disable avahi-daemon.service
sudo systemctl disable gdm.service
sudo systemctl disable mpd.service

# Install dependencies
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install device-tree-compiler -y
sudo apt-get install python-pip -y
pip install web.py
pip install python-uinput

# Compile and copy RS485 device tree overlay
dtc -o devicetree/LAMP-RS485-00A0.dtbo -b 0 -@ devicetree/LAMP-RS485-00A0.dts
sudo cp devicetree/LAMP-RS485-00A0.dtbo /lib/firmare

# Install display autostart
sudo cp scripts/autostart /etc/xdg/lxsession/LXDE/autostart
sudo chmod +x /etc/xdg/lxsession/LXDE/autostart

# Copy server dependencies & data files
sudo cp -ar data/* /srv/multifeeder_server/
sudo cp -ar drivers/ /usr/local/lib/python2.7/site-packages/
sudo cp feederbus.py /usr/local/lib/python2.7/site-packages/

# Main server executable
sudo cp multifeeder_server.py /usr/bin/
sudo chmod +x /usr/bin/multifeeder_server.py

# Main server daemon script
sudo cp daemon_scripts/multifeeder_server.sh /etc/init.d/
sudo chmod +x /etc/init.d/multifeeder_server.sh

# Touch driver
sudo cp touch.py /usr/bin/
sudo chmod +x /usr/bin/touch.py

# Touch driver daemon script
sudo cp daemon_scripts/touch.sh /etc/init.d/
sudo chmod +x /etc/init.d/touch.sh

# Register the daemons
sudo update-rc.d multifeeder_server.sh defaults
sudo update-rc.d touch.sh defaults
