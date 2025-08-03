# Personal Medicine Inventory Tracker

## Description

A Python-based tool to manage your personal medicine inventory with essential tracking features and integration with AWS for secure storage, automation, and notifications.

This project helps you keep track of your medicines, monitor expiry dates, and securely back up or interact with your inventory using AWS services like S3, SES, and Lambda.


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
- (Planned) Automate expiry checks using AWS Lambda
- (Planned) Visualize expiry trends using Grafana and CloudWatch metrics

