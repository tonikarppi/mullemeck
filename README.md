# Mullemeck

### Continous Integration Server

## Setting up the server

### Step 1. Set up your environment variables.

```
cp .env.example .env
```

Then for `GITHUB_SECRET` enter the secret value you specified when setting up the webhook for your repository.

For `GITHUB_URL` enter the URL for which the webhooks are running on. For example: https://github.com/tonikarppi/mullemeck would be the value for this repository.

### Step 2. Install the dependencies

This project uses [Poetry](https://github.com/sdispater/poetry) for dependency management. Install the project dependencies with.

```
poetry install
```

### Step 3. Source the virtual environment

Enter the following command to get shell access to the executables:

```
poetry shell
```

If this does not work, you'll have to manually source the virtual environment that Poetry created.

### Step 4. Setting up the database

```
python -m mullemeck create_tables
python -m mullemeck add_samples
```

### Step 5. Start the server

```
python -m mullemeck develop
```

## Documentation

The documentation for this project is available here (add link).

## Contributions

This section contains a list of the contribution by the authors of this project.

### Alexander Westberg-Bladh (xobust)

### Alexis Hubert (SandstormVR)

-   Implemented :
    -   functions clone_repo, build_static_checks and build_tests
    -   function that runs the whole build and create a new entry in the database
    -   tests for the build functions
    -   some of the actions started when a webhooks is received
-   Various fixes
-   Active participation in reviewing other contributors' code.

### Isak Peterson (Isak-P)

### Lars Lundin (Larsrat)

### Toni Karppi (tonikarppi)

-   Implemented
    -   The Github webhook endpoint + HMAC verification
    -   Dockerfile
    -   Travis CI integration
    -   ORM
-   Added instructions for setting up the project in the README.
