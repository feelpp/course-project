# Course notebooks

1. Extract the ZIP and open the extracted `course-project` folder in VS Code.
2. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if needed.
3. In the VS Code terminal, run:

   ```sh
   uv sync --locked
   ```

   uv creates `.venv` using the supplied Python version and lockfile.
4. Install the recommended Python and Jupyter extensions. Open a notebook under
   `notebooks/`, click **Select Kernel → Python Environments**, and choose `.venv`.
5. Run the cells as you work through the lesson.

The archive contains the teaching notebooks, their Python environment and VS Code
settings. The current notebooks have no bundled input datasets: practice files are
created during the exercises, and the Feel++ example downloads its geometry.
Course pages and other project datasets remain on the course website.

Linux notebooks require Bash and the Unix utilities used in the lesson, including
`tree`. Use Linux, WSL or Gaya. Interactive editors run in the terminal; replace
example paths and read cells before executing them.

`notebooks/ROOT/jupyter.ipynb` also requires native Feel++ Python bindings on a
supported Linux host. Its visualization dependencies are installed with
`uv sync --locked --extra feelpp`; Xvfb must be available on that host. Select an
interpreter compatible with the installed Feel++ bindings. For system-installed
bindings, use:

```sh
uv venv --python /usr/bin/python3 --system-site-packages
uv sync --locked --python /usr/bin/python3 --extra feelpp
```

This does not install Feel++ itself. In Remote SSH, both the files
and the kernel must be on the remote host.
