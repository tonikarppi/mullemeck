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

## Interacting with the server

The development server runs on localhost:5000 by default.

When the server is running, the website where the builds can be browsed is available at the server root.

The server accepts JSON webhook requests from Github at the /webhook route.

## Testing the project

This project uses pytest for its testing framework.

```
pytest tests/
```

## Documentation

The documentation for this project is available [here](https://tonikarppi.github.io/mullemeck/).

## Contributions

This section contains a list of the contribution by the authors of this project.

### Alexander Westberg-Bladh (xobust)

-   Implemented:
    -   Configuration v1
    -   Email sending and templates
-   Setup production environment
-   Various fixes and reviews

### Alexis Hubert (SandstormVR)

-   Implemented :
    -   functions clone_repo, build_static_checks and build_tests
    -   function that runs the whole build and create a new entry in the database
    -   tests for the build functions
    -   some of the actions started when a webhooks is received
-   Various fixes
-   Active participation in reviewing other contributors' code.

### Isak Peterson (Isak-P)

-   Implemented :
    -   Various sections of the frontend
    -   Various sections of the frontend database logic
-   Various fixes
-   Active participation in reviewing other contributors' code.

### Lars Lundin (Larsrat)

### Toni Karppi (tonikarppi)

-   Implemented
    -   The Github webhook endpoint + HMAC verification
    -   Dockerfile
    -   Travis CI integration
    -   ORM
-   Added instructions for setting up the project in the README.
