# ShapeTracker Deployment Guide

This guide will walk you through the steps to deploy the ShapeTracker application on a Linode server using Docker Compose, Nginx, and Let's Encrypt SSL/TLS certificates.

## Video Demo of Deployment

**Click on the below thumbnail for complete demo video of deployment on Linode**

[![Demo video of deployment of shapeTracker app](https://github.com/prabinkc2046/shapeTracker/blob/main/Screenshot/Screenshot%20from%202023-07-21%2013-50-11.png)](https://youtu.be/QfdKDJm3PkY)

## Prerequisites

1. A Linode server with Ubuntu installed and SSH access configured.
2. Docker and Docker Compose installed on your Linode server.
3. A registered domain name with DNS configured to point to your Linode server's IP address.

### Step 1: Setting up Linode server, Secure access and Firewall considerations

1. Set up linode virtual machine as your requirements

2. Update and upgrade to the latest version

```
apt update -y && apt upgrade -y
```

3. Create an user and add it to the sudo group

```
adduser <user name>
```

```
usermod -aG sudo <user name>
```

4. Set up hostname

```
hostnamectl set-hostname <hostname>
```

	Edit /etc/hosts file:
	
	# /etc/hosts
	127.0.0.1       localhost
	<IP of your server>	 <hostname>  <---  Add this line


5. Reboot

```
sudo reboot
```

6. Create a ssh-key on the local machine or use existing one and transfer it to the remote server

   if you don't have an existing ssh-key pair, create as follow:

```
ssh-keygen -t rsa -b 4096
```

   This above command will copy your public key to the appropriate location on the remote server, typically under the ~/.ssh/authorized_keys file.

```
ssh-copy-id <user name>@server_IP
```

7. Login

   if everythong goes well, you should be able to login without password:

```
ssh <user name>@serverIP
```

8. Disable root login and password login

	Edit /etc/ssh/sshd_config
	Set PermitRootLogin no
	PasswordAuthentication no

Restart ssh service

```
sudo systemctl reload ssh
```

9. Install ufw firewall and set up following rules

***Warning!!!***

Ensure you allow ssh access :)

```
sudo apt install ufw
```
```
sudo ufw default allow outgoing
```
```
sudo ufw default deny incoming
```
```
sudo ufw allow ssh
```
```
sudo ufw allow 80/tcp
```
```
sudo ufw allow 443/tcp
```
```
sudo ufw enable
```

10. Install Docker and Docker compose

Install Docker Engine on Ubuntu

```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```
```
sudo usermod -aG docker $USER
```
```
newgrp docker
```

Installing standalone docker-compose
```
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

```

```
sudo chmod +x /usr/local/bin/docker-compose

```

```
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

```

### Step 2: Clone the Repository

	Clone the ShapeTracker repository to your Linode server using Git.

```
git clone <https://github.com/prabinkc2046/shapeTracker.git>
```

### Step 3: Build and Start the Containers

Use Docker Compose to build and start the application and database containers.

```
cd shapeTracker
```

```
docker-compose up -d
```
	
This command will create two containers - one for the ShapeTracker application and another for the MySQL database.

### Step 4: Set Up Nginx as Reverse Proxy

Install Nginx on your Linode server.

```
sudo apt install nginx

```

Create a new Nginx configuration file for the ShapeTracker application.

```
sudo nano /etc/nginx/sites-available/shapetracker
```

Add the following Nginx configuration to the file:

```
server {
    listen 80;
    server_name your_domain_or_server_ip;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }	
}

```

Replace your_domain_or_server_ip with your domain name or server IP address. in my case, it is "shapetrack.prabinkc.com"

Enable the Nginx configuration and restart Nginx.

```
sudo ln -s /etc/nginx/sites-available/shapetracker /etc/nginx/sites-enabled/
```

```
sudo nginx -t
```
```
sudo systemctl restart nginx
```

### Step 5: Update DNS Records

	Update your DNS records to point to your Linode server's IP address. Add an A record for shapetracker.your_domain_or_server_ip to your domain's DNS settings.

### Step 6: Obtain SSL/TLS Certificate

Install Certbot on your Linode server.

```
sudo apt install certbot python3-certbot-nginx
```

Obtain a Let's Encrypt SSL/TLS certificate for your domain.

```
sudo certbot --nginx -d your_domain
```
	
Follow the on-screen instructions to complete the certificate installation.

### Step 7: Access Your Application

	Once the DNS changes have propagated, you can access your ShapeTrack application at http://shapetracker.your_domain_or_server_ip. The application will automatically redirect to HTTPS (https://shapetracker.your_domain_or_server_ip) due to the Let's Encrypt SSL/TLS certificate.

# Conclusion

	Congratulations! You have successfully deployed the ShapeTrack application on your Linode server with Docker Compose, Nginx, and Let's Encrypt SSL/TLS certificates. You can now access your application securely over HTTPS.
	Thank you.

Happy tracking and stay healthy! 🏋️‍♀️🥦🏃‍♂️




