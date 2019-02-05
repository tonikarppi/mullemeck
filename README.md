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

## Documentation

The documentation for this project is available here (add link).

## Contributions

This section contains a list of the contribution by the authors of this project.

### Alexander Westberg-Bladh

### Alexis Hubert

### Isak Peterson

### Lars Lundin

### Toni Karppi
