# Personal Medicine Inventory Tracker

## Description

A Python-based tool to manage your personal medicine inventory with essential tracking features and integration with AWS for secure storage, automation, and notifications.

This project helps you keep track of your medicines, monitor expiry dates, and securely back up or interact with your inventory using AWS services like S3, SES, Lambda
and EventBridge.


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

