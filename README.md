# piVA
Raspberry Pi powered Vision Assistant

### WIP Draft
```
sudo dphys-swapfile swapoff

sudo nano /etc/dphys-swapfile
CONF_SWAPSIZE=1024

sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

```
sudo apt install espeak ffmpeg
pip3 install torch==2.1.1 torchvision==0.16.1 --index-url https://download.pytorch.org/whl/cpu --no-cache-dir
```

```
# Automatically load overlays for detected cameras
#start_x=1
dtoverlay=imx219
```
