# Personal Medicine Inventory Tracker

## Description

A Python-based tool to manage your personal medicine inventory with essential tracking features and integration with AWS for secure storage, automation, and notifications.

This project helps you keep track of your medicines, monitor expiry dates, and securely back up or interact with your inventory using AWS services like S3, SES, Lambda, EventBridge and CloudWatch.

This project uses the following technologies:

- Terraform: manages infrastructure as code for reproducible deployments.  
- Docker: containerizes all application components.    
- GitHub Actions (CI/CD): automatically builds Docker images, tags them with `latest` and the Git commit hash, and pushes them to Docker Hub.  
- Kubernetes: Kubernetes orchestrates jobs and runs a MySQL database as a Deployment for persistent storage.


## Core Features (Local)
- Add a medicine  
- List all medicines  
- Update quantity  
- Delete medicine  
- Show items expiring in X days  
- Show expired medicines  

## AWS Features
- (Planned) Back up the local MySQL database (running in a Docker container) to AWS S3 
- Send expiry alert email via AWS SES with a list of medicines expiring in the next 10 days
- Automate expiry checks and sending emails every 10 days using AWS Lambda and Amazon EventBridge 
- (Planned) Push custom metrics (e.g. number of expiring medicines) to CloudWatch
- (Planned) Visualize expiry trends with Grafana using CloudWatch metrics

## Infrastructure as code (IaC)
- Use Terraform to manage AWS resources, making deployment reproducible and version-controlled

## Docker Setup
- The project uses Docker to containerize all components
- Each module (Database service, Cloud integration, Messaging & Emails, Lambda-based email sender) has its own Dockerfile stored in a dedicated folder
- The MySQL database runs as a Docker service, replacing the previous CSV-only approach
- A single docker-compose.yml manages all four containers


## CI/CD Overview
- GitHub Actions workflow builds all Docker images using `docker-compose`  
- Each image is tagged with `latest` and the Git commit hash for versioned deployments  
- All images are automatically pushed to Docker Hub


## Kubernetes Setup
- Each application runs as a Kubernetes Job executing Python scripts to completion
- CSV included in the image (optionally shared via PersistentVolumeClaim)
- Replaced the CSV-only approach with a MySQL database deployed in Kubernetes for persistent storage.
- AWS credentials via Secrets, non-sensitive config via ConfigMaps, accessed as environment variables



