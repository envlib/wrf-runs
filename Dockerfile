FROM mullenkamp/wrf-wps-debian:1.0

WORKDIR /

COPY ./pyproject.toml ./
RUN uv sync --no-cache --no-install-project --no-default-groups

COPY *.py ./

CMD ["uv", "run", "python", "-u", "main.py"]

# CMD ["/bin/bash"]