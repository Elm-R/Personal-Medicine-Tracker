# Personal Medicine Inventory Tracker

## Description

A Python-based tool to manage your personal medicine inventory with essential tracking features and integration with AWS for secure storage, automation, and notifications.

This project helps you keep track of your medicines, monitor expiry dates, and securely back up or interact with your inventory using AWS services like S3, SES, Lambda
and EventBridge.

It also includes Terraform for infrastructure as code, Docker for containerization of components, and Kubernetes for orchestration and job execution.


## Core Features (Local)
- Add a medicine  
- List all medicines  
- Update quantity  
- Delete medicine  
- Show items expiring in X days  
- Show expired medicines  

## AWS Features
- Upload inventory CSV to AWS S3 bucket 
- Send expiry alert email via AWS SES with a list of medicines expiring in the next 10 days
- Automate expiry checks and sending emails every 10 days using AWS Lambda and Amazon EventBridge 
- Sent the required metrics to CloudWatch
- (Planned) Visualize expiry trends with Grafana using CloudWatch metrics

## Infrastructure as code (IaC)
- Use Terraform to manage AWS resources, making deployment reproducible and version-controlled

## Docker Setup
- The project uses Docker to containerize all components
- Each application (local tracker, Lambda-based email sender, cloud-based file) has its own Dockerfile stored in a dedicated folder
- The CSV file is stored in the project root and copied into each container at build time
- A single docker-compose.yml manages all three containers

## Kubernetes Setup
- Each application runs as a Kubernetes Job executing Python scripts to completion
- CSV included in the image (optionally shared via PersistentVolumeClaim)
- AWS credentials via Secrets, non-sensitive config via ConfigMaps, accessed as environment variables



