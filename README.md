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

Place the following environment variables in your `.env` file before building and running the project. Adjust the values according to your needs. The `DB_HOST` value should match the `pgdb` service name specified in the `docker-compose.yml` file if you are running the project using **Docker**.



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


## Migration

When you create a new model, you should import it in `models/__init__.py`. After that, you can run the `make migrate` command. If you make any changes to a model or create a new one, those changes will be reflected in the database after restarting the application. This is because `script/start.sh` runs `alembic upgrade head` before starting the application.


## Seeds --

We seed roles when the application starts. The `roles_seeder.py` script in the seed directory handles this, fetching the data from `data/roles.json`. If you create any seeder script, remember to import it in `run.py`.


> Note: These commands build and run your project in Docker. If you find that your database tables are not created, use make restart. (This may happen the first time you run the project.)


## WeebSocket
```
wscat -c "ws://localhost:8000/ws/notifications/" -H "Authorization: Bearer YOUR_TOKEN"
```

## Logs
You will find error logs only in `logs` directory.


## Conclusion

FastAPI Bootstrap provides a solid foundation for quickly starting your FastAPI projects. With pre-configured settings, organized structure, and tools for migrations, seeding, and Docker integration, you can focus on building features instead of setting up the basics. Whether you’re a beginner or an experienced developer, this repository aims to streamline your development workflow.
