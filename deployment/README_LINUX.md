# Deploying Bit-Bot to Ubuntu

## 1. Transfer Files
Copy your entire project folder to your Ubuntu machine (e.g., to `/home/youruser/bitbot`).

## 2. Install System Dependencies
Run this on your Ubuntu terminal:
```bash
sudo apt update
sudo apt install python3-venv python3-pip -y
```

## 3. Setup Python Environment
Inside the bot folder on Ubuntu:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 4. Configure Service
1.  Open `deployment/start.sh` and `deployment/bitbot.service`.
2.  Change `/home/youruser/bitbot` to the **actual path** on your Ubuntu machine.
3.  Change `youruser` to your **actual username**.
4.  Make the script executable:
    ```bash
    chmod +x deployment/start.sh
    ```

## 5. Enable Auto-Restart
Copy the service file and enable it:
```bash
sudo cp deployment/bitbot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable bitbot
sudo systemctl start bitbot
```

## 6. Check Status
```bash
sudo systemctl status bitbot
```
If it says **active (running)**, you are good to go!
It will now automatically restart if it crashes or if the PC reboots.
