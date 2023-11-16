# MunmudBlog

## Overview

This web application is a feature-rich platform developed for smooth code management, build, and deployment. The project includes functionalities such as custom codeforces rank viewing, blog posting, and email notification. The application is hosted on AWS and leverages various AWS services, including RDS (Postgres) for the database and S3 for image storage.

## Key Features

- **Custom Codeforces Rank Viewing:** Users can Codeforces ranks based on specific criteria.
- **Blog Posting:** Users can read blog posts within the application.
- **Integrated Email:** Seamless integration with email notification of their local rank (countrywise, universitywise).

## Deployment and Infrastructure

- **Continuous Integration/Continuous Deployment (CI/CD):** The project follows a CI/CD pipeline for automated code management, build, and deployment. 
- **AWS RDS:** The application uses Amazon RDS for the PostgreSQL database.
- **AWS S3:** Amazon S3 is utilized for storing and retrieving images in the application.

## Dockerization

The application is Dockerized, allowing for easy deployment and scalability.

## Automated Rank Updates

A Cron Job is implemented to automate the process of updating ranks at specified intervals.

## Security

- **SSL Certificate:** Secure communication is ensured through the implementation of an SSL certificate.
- **AWS Hosted Zone:** The application is hosted in an AWS hosted zone for enhanced security and reliability.

## Getting Started

To get started with the project, follow the command
```cmd
git clone https://github.com/Munmud/Community-Detection-Modularity.git
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Secreats Variable 
in .env use
```env
SECRET_KEY = ''
DEBUG=1
ALLOWED_HOSTS= '127.0.0.1,http://127.0.0.1' 
PRODUCTION=1

DATABASE_NAME= ''
DATABASE_USER= ''
DATABASE_PASSWORD= ''

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

EMAIL_OF_ADMIN = ''
'
```
