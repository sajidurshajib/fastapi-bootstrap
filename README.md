# FastAPI Bootstrap v1.0.1

Welcome to FastAPI Bootstrap! This repository is designed to give you a head start in building your next FastAPI project. With its well-organized structure and pre-configured settings, you can dive straight into development without wasting time setting up the basics.

## Why Use This Repository?

**Quick Start:** Save time by using this as a foundation for your FastAPI projects.

**Best Practices:** The repository follows standard coding conventions and scalable architecture.

**Customizable:** Easily tailor the structure to suit your project needs.

## Contributions Welcome!

If you have any suggestions to improve the structure or ideas for enhancing the codebase, feel free to open an issue or submit a pull request. Your feedback is invaluable in making this repository better for everyone!



## .env file

```
DB_USER=fastuser
DB_PASSWORD=fastpassword!
DB_HOST=pgdb
DB_NAME=fastdb
SECRET_KEY=p7dy3qua3jxkspo&=#0xd56t-3a7g0mnj_s5(2g=eh#)jd^!6y
ALGORITHM=HS256
```




## Build and Run (Docker)

I have written a Makefile to simplify the process. You can use the commands in the Makefile to save time, or you can skip those and manually run the commands.

**Makefile commands:**

1. **build**: `make build `
2. **run**: `make start`
3. **rebuild**: `make rebuild`
4. **restart**: `make restart`
5. **stop**: `make stop`
6. **remove docker image**: `make clean`
   
**For development**

1. **migration**: `make migrate m="your_comment_or_msg"`
2. **logs**: `make logs`
3. **shell**: `make shell`
