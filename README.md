# Academic Pages
**Academic Pages is a GitHub Pages template for personal and professional portfolio-oriented websites.**

![Academic Pages template example](images/themes/homepage-light.png "Academic Pages template example")

See more info at https://academicpages.github.io/

# Getting Started

## Using Docker

Working from a different OS, or just want to avoid installing dependencies? You can use the provided `Dockerfile` to build a container that will run the site for you if you have [Docker](https://www.docker.com/) installed.

You can build and execute the container by running the following command in the repository:

```bash
chmod -R 777 .
docker compose up
```

You should now be able to access the website from `localhost:4000`.


Stop with:

```bash
docker compose down
```

### Permissions

The container runs as uid 1000, so any file it needs to read must be readable by that uid. New files/directories you create on the host (via an editor, `mkdir`, a script, etc.) inherit your shell's `umask`, which on some systems defaults to owner-only (`600`/`700`) — unreadable by the container. Symptoms: the dev server silently stops picking up changes, or crashes outright with `Permission denied` in the `listen`/`rb-inotify` watcher.

**Permanent fix:** set `umask 022` in `~/.bashrc` (already done on this machine) so every new file/directory comes out world-readable (`644`/`755`) by default — no per-file `chmod` needed going forward. Only applies to new shells started after the change.

If you ever hit the symptom anyway (e.g. a file was created before the umask fix, or from a shell that predates it): `chmod -R 777 .`, then `docker compose restart` (not just `up` — an already-running container won't reload; `up` only recreates it if `docker-compose.yaml` changed).