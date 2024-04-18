Source of installer: https://github.com/moonlight-stream/moonlight-qt


Pre reqs:
1. READ ALL OF THIS
2. Your pi must be connected to the internet to install
3 .Out of the box Moonlight requires a nvidia video card on your source PC
4. AMD Cards use https://github.com/LizardByte/Sunshine
5. Hardwire network your pi if possible
6. If you have any issues with moonlight like latency etc. Go to the moonlight subreddit.


Install Directions:
1. Unzip the files to your usb drive. you should now have roms/ports/moonlight
2. Scan for new games in rgbpi ui
3. Go to folder 
5. Run installmoonlight
6. Wait a few minutes while it downloads everything and installs (Installer deletes itself and with go away next time you scan for games)
7. Pi Reboots itself
8. Run Moonlight
	
Running directions:
1. Go into the moonlight settings (Y on my controller)
2. MUST DO - Change output resolution to Native (720x480). DO NOT USE 720p. The new script will auto swith from 240p to 480i, but you may still need to click on native one time.
3. If latency is an issue change the codec to x264
