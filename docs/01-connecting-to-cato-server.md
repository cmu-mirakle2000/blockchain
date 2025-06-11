# Remote Server Setup Guide for Blockchain Network

This guide will help you set up the blockchain application on an external server (like Cato) so that multiple students can interact with the network from different locations.

## Initial Server Setup

### Step 1: Access Your Server

1. Open a terminal on your laptop and connect to your server via SSH. Replace `server_ip` with the IP address of your server

   Where to get your server IP: https://console.cato.digital/compute/server   

```bash
  ssh -i "path/to/key.pem" cato-user@<server_ip>
  #Example
  ssh -i ~/.ssh/id_ecdsa.pem cato-user@192.168.5.6
```

### Step 2: Bypass the firewall

Run this on your remote server to bypass the firewall. You only need to do it ONCE on your server (not every time you login)

```bash
  sudo firewall-cmd --zone public --permanent --add-port=5000/tcp
  sudo firewall-cmd --reload
```

