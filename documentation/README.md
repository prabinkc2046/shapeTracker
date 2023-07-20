# ShapeTracker Deployment Guide

This guide will walk you through the steps to deploy the ShapeTracker application on a Linode server using Docker Compose, Nginx, and Let's Encrypt SSL/TLS certificates.

## Prerequisites

Before starting the deployment process, make sure you have the following:

1. A Linode server with Ubuntu installed and SSH access configured.
2. Docker and Docker Compose installed on your Linode server.
3. A registered domain name with DNS configured to point to your Linode server's IP address.

### Step 1: Setting up linode server, secure access and firewall considerations
	1. set up linode virtual machine as your requirements

	2. update and upgrade to the latest version
```
		apt update -y && apt upgrade -y
```
	3. create a user and add it to the sudo group

```
		adduser prabin
```

```
		usermod -aG sudo prabin
```

	4. set up hostname

```
		hostnamectl set-hostname shapetracker
```
```
		add shapetracker to /etc/hosts 
```

	4. reboot
```
		sudo reboot
```

	5. login as new user and update the server
```
		ssh user@server_IP
```

	6. create a ssh-key on the local machine or use existing one and transfer it to the remote server

```
		mkdir .ssh @remote server
```
```		scp path_to_ssh_public_key prabin@remote_server:path_to_.ssh_directory
		sudo chmod 700 .ssh/
		sudo chmod 600 .ssh/*
```

	7. login with ssh key
```
		ssh prabin@serverIP
```

	8. disable root login and password login

	9. install ufw firewall and set up following rules
```
		sudo apt install ufw
		sudo ufw default allow outgoing
		sudo ufw default deny incoming
		sudo ufw allow 5000
		sudo ufw allow ssh
		sudo ufw allow 80/tcp
		sudo ufw allow 443/tcp
		suod ufw reload
```

### Step 2: Clone the Repository

	Clone the ShapeTracker repository to your Linode server using Git.
```
	git clone <https://github.com/prabinkc2046/ShapeTrack.git>
```

### Step 3: Build and Start the Containers

	Use Docker Compose to build and start the application and database containers.

```
	docker-compose up -d
```
	
	This command will create two containers - one for the ShapeTracker application and another for the MySQL database.

### Step 4: Set Up Nginx as Reverse Proxy

	Install Nginx on your Linode server.

```
	sudo apt update
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
	sudo nginx -t
	sudo systemctl restart nginx
```

### Step 6: Obtain SSL/TLS Certificate

	Install Certbot on your Linode server.

```
		sudo apt install certbot python3-certbot-nginx
```

	Obtain a Let's Encrypt SSL/TLS certificate for your domain.

```
		sudo certbot --nginx -d your_domain_or_server_ip
```
	
	Follow the on-screen instructions to complete the certificate installation.

### Step 7: Update DNS Records

	Update your DNS records to point to your Linode server's IP address. Add an A record for shapetracker.your_domain_or_server_ip to your domain's DNS settings.

### Step 8: Access Your Application

	Once the DNS changes have propagated, you can access your ShapeTrack application at http://shapetracker.your_domain_or_server_ip. The application will automatically redirect to HTTPS (https://shapetracker.your_domain_or_server_ip) due to the Let's Encrypt SSL/TLS certificate.

# Conclusion

	Congratulations! You have successfully deployed the ShapeTrack application on your Linode server with Docker Compose, Nginx, and Let's Encrypt SSL/TLS certificates. You can now access your application securely over HTTPS.
	Thank you.

Happy tracking and stay healthy! 🏋️‍♀️🥦🏃‍♂️




