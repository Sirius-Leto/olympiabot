FROM python:3.11
# Copy all the files from the current directory to the container
COPY . /app
WORKDIR /app
# Copy the pyproject.toml and poetry.lock files to the container
# Upgrade pip
RUN pip install --upgrade pip
# Install poetry
RUN pip install poetry
# Install dependencies
RUN poetry install
# Print the current directory and its contents
RUN pwd && ls -la
# Add src to PYTHONPATH
RUN export PYTHONPATH="${PYTHONPATH}:/app/src"
# Run the app (src/bot.py)
ENTRYPOINT ["poetry", "run", "python", "src/bot.py"]
