# Personal Medicine Inventory Tracker

## Description

A Python-based tool to manage your personal medicine inventory with essential tracking features and integration with AWS for secure storage, automation, and notifications.

This project helps you keep track of your medicines, monitor expiry dates, and securely back up or interact with your inventory using AWS services like S3, SES, Lambda, EventBridge and CloudWatch.

It also includes Terraform for infrastructure as code, Docker for containerization of components, and Kubernetes for orchestration and job execution.


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
- (in edit mode to apply the new changes) Each module (Database service, Cloud integration, Messaging & Emails, Lambda-based email sender) has its own Dockerfile stored in a dedicated folder
- The MySQL database runs as a Docker service, replacing the previous CSV-only approach
- A single docker-compose.yml manages all three containers

## Kubernetes Setup
- Each application runs as a Kubernetes Job executing Python scripts to completion
- CSV included in the image (optionally shared via PersistentVolumeClaim)
- AWS credentials via Secrets, non-sensitive config via ConfigMaps, accessed as environment variables



