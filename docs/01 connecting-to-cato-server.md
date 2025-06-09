# Remote Server Setup Guide for Blockchain Network

This guide will help you set up the blockchain application on an external server (like Cato) so that multiple students can interact with the network from different locations.

## Initial Server Setup

### Step 1: Access Your Server

1. Connect to your server via SSH:

```
ssh -i "path/to/key.pem" username@server_ip
```

Example:
   ```
   ssh -i "C:\Users\user\ecdsa-key-20250519.pem" cato-user@131.226.220.72
   ```

   Where to get your server IP: https://console.cato.digital/compute/server   


### Step 2: Bypass the firewall

Run the following command on your local machine first to see behavior when the server is not accessible:
 
```bash
$ curl http://<IP>:5000
>> curl: (7) Failed to connect to <IP> port 5000 after 2113 ms: Connection refused
```
Run this on your remote server to bypass the firewall:

```bash
sudo firewall-cmd --zone public --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
```

