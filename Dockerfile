FROM mullenkamp/wrf-wps-debian:1.0

WORKDIR /app

# RUN uv tool install toml-cli

COPY requirements.txt .
RUN uv pip install --no-cache-dir -r requirements.txt

COPY *.py .

# CMD ["uv", "run", "python", "-u", "main.py"]

CMD ["/bin/bash"]