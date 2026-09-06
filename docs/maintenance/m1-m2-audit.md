# Course architecture audit — 6 September 2026

## Decision: learning paths now, edition versioning later

Keep `course-project` and `csmi` unversioned (`version: ~`). M1 and M2 are concurrent curricula, not successive versions. Add `m1` and `m2` modules for workflow pages; retain existing module/file resource IDs. This preserves published URLs and cross-component links. Antora navigation registers only `ROOT/nav.adoc`; other nav files are currently inactive.

Antora versions can later represent frozen academic editions (for example `2026-2027`), with the same M1/M2 modules in each edition. Introducing that now would change URL routing without an agreed archive policy. When archives are required, set explicit quoted versions in tagged/branched editions, select those refs in the playbook, configure latest-version routing and old-URL redirects, and validate all editions together. Do not label versions M1/M2. See [Antora version key](https://docs.antora.org/antora/latest/component-version-key/) and [navigation assembly](https://docs.antora.org/antora/latest/navigation/).

## Existing structure and overlap

- `site.yml` collects both components from the current local checkout (`HEAD`), using the Feel++ UI and extensions. Notebook collector covers ROOT, linux and project-management. CI invokes `npm run antora`.
- Existing home/prerequisite/quick-start pages use three difficulty levels and contradict the new C++ prerequisite. Replace their orientation while retaining URLs.
- `git & github/pages/git-basics.adoc` is an exact duplicate of `git-github/pages/git-basics.adoc`; Docker Compose also appears twice. Keep compatibility pages pointing to canonical resources.
- ROOT GitHub/VS Code/Actions and the corresponding dedicated modules overlap; retain the older pages as reference and direct students to the dedicated modules.
- Apptainer intro uses an unconfigured `library://` source; tutorial has malformed source blocks and a Unicode dash in `--bind`. Replace with one practical scientific exercise. Installation material is a dated administrator recipe; retain as historical reference and add a current student entry.
- HPC material includes Karolina, MPI, self-hosted CI and old examples. Preserve as advanced reference with context; it is not the Gaya first-session procedure.
- CSMI topic pages are year/semester-specific; do not relabel the existing 2026 M1 S2 subjects as new assignments. The local registry/generated project work and analysis files predate this task and remain outside the redesign.
- `visualisation/hw.adoc` is a separate thermal-fin/ROM exercise; retain outside the main course route.

## Missing material

M1/M2 outcomes and routes; software/accounts; responsible AI; Gaya operations; Python/C++ environment; shared project/testing workflow; M2 reproducibility handoff; MLOps lifecycle, tracking, inference and project specification; competency-based assessment. Use sections for related deliverables rather than empty pages.

## Existing page inventory (before editing)

| Existing resource | Classification |
| --- | --- |
| `ROOT:antora.adoc` | Shared/reference |
| `ROOT:cmake.adoc` | Shared/reference |
| `ROOT:github.adoc` | Shared/reference |
| `ROOT:githubactions.adoc` | Shared/reference |
| `ROOT:index.adoc` | Shared/reference |
| `ROOT:instructor-guide.adoc` | Instructor (legacy schedule) |
| `ROOT:jupyter.adoc` | Shared/reference |
| `ROOT:overview.adoc` | Retirement candidate / compatibility reference |
| `ROOT:prerequisites.adoc` | Shared/reference |
| `ROOT:quick-start.adoc` | Shared/reference |
| `ROOT:rename.adoc` | Retirement candidate / compatibility reference |
| `ROOT:vscode.adoc` | Shared/reference |
| `cicd:gitlab.adoc` | M2 core / shared reference |
| `cicd:gitlab_handson.adoc` | M2 core / shared reference |
| `cicd:gitlab_slides.adoc` | M2 core / shared reference |
| `cicd:index.adoc` | M2 core / shared reference |
| `containers:apptainer/apptainer-install.adoc` | M2 core / shared reference |
| `containers:apptainer/index.adoc` | M2 core / shared reference |
| `containers:apptainer/tutorial.adoc` | M2 core / shared reference |
| `containers:docker/docker-architecture.adoc` | M2 core / shared reference |
| `containers:docker/docker-commands.adoc` | M2 core / shared reference |
| `containers:docker/docker-compose.adoc` | M2 core / shared reference |
| `containers:docker/docker-deploy.adoc` | M2 core / shared reference |
| `containers:docker/docker-install.adoc` | M2 core / shared reference |
| `containers:docker/docker-overview.adoc` | M2 core / shared reference |
| `containers:docker/docker-problems-solved.adoc` | M2 core / shared reference |
| `containers:docker/dockerfile-basics.adoc` | M2 core / shared reference |
| `containers:docker/hands-on/01-getting-started.adoc` | M2 core / shared reference |
| `containers:docker/hands-on/02-advanced-usage.adoc` | M2 core / shared reference |
| `containers:docker/hands-on/03-usecase-db.adoc` | M2 core / shared reference |
| `containers:docker/hands-on/04-compose.adoc` | M2 core / shared reference |
| `containers:docker/hands-on/06-githubactions.adoc` | M2 core / shared reference |
| `containers:docker/hands-on/docker-postgres.adoc` | M2 core / shared reference |
| `containers:docker/hands-on/index.adoc` | M2 core / shared reference |
| `containers:docker/index.adoc` | M2 core / shared reference |
| `containers:docker/what-are-containers.adoc` | M2 core / shared reference |
| `containers:hpc/advanced.adoc` | M2 core / shared reference |
| `containers:hpc/best-practices.adoc` | M2 core / shared reference |
| `containers:hpc/cicd.adoc` | M2 core / shared reference |
| `containers:hpc/hands-on/00-classroom.adoc` | M2 core / shared reference |
| `containers:hpc/hands-on/01-docker.adoc` | M2 core / shared reference |
| `containers:hpc/hands-on/02-apptainer.adoc` | M2 core / shared reference |
| `containers:hpc/hands-on/03-cicd-githubactions.adoc` | M2 core / shared reference |
| `containers:hpc/hands-on/03-docker-mpi.adoc` | M2 core / shared reference |
| `containers:hpc/hands-on/04-apptainer-cicd-app.adoc` | M2 core / shared reference |
| `containers:hpc/hands-on/04-docker-cicd-app.adoc` | M2 core / shared reference |
| `containers:hpc/hands-on/05-deploy.adoc` | M2 core / shared reference |
| `containers:hpc/hands-on/index.adoc` | M2 core / shared reference |
| `containers:hpc/index.adoc` | M2 core / shared reference |
| `containers:index.adoc` | M2 core / shared reference |
| `git & github:git-basics.adoc` | Retirement candidate / compatibility reference |
| `git-github:git-basics.adoc` | M1 core / shared reference |
| `git-github:git-branch.adoc` | M1 core / shared reference |
| `git-github:git-merges.adoc` | M1 core / shared reference |
| `git-github:git-remotes.adoc` | M1 core / shared reference |
| `git-github:git-repository-basics.adoc` | M1 core / shared reference |
| `git-github:git-starter.adoc` | M1 core / shared reference |
| `git-github:github-actions-cmake-eigen3.adoc` | M1 core / shared reference |
| `git-github:github-actions.adoc` | M1 core / shared reference |
| `git-github:github-collaborations.adoc` | M1 core / shared reference |
| `git-github:github-essentials.adoc` | M1 core / shared reference |
| `git-github:github-how-to-write-issues.adoc` | M1 core / shared reference |
| `git-github:github-review-projects-lab.adoc` | M1 core / shared reference |
| `git-github:github-start.adoc` | M1 core / shared reference |
| `git-github:index.adoc` | M1 core / shared reference |
| `linux:editing.adoc` | M1 core / shared reference |
| `linux:files.adoc` | M1 core / shared reference |
| `linux:index.adoc` | M1 core / shared reference |
| `linux:shell.adoc` | M1 core / shared reference |
| `linux:ssh/index.adoc` | M1 core / shared reference |
| `linux:ssh/remote-ssh-vscode.adoc` | M1 core / shared reference |
| `linux:ssh/ssh-commands.adoc` | M1 core / shared reference |
| `linux:ssh/ssh-setup.adoc` | M1 core / shared reference |
| `linux:text-processing.adoc` | M1 core / shared reference |
| `project-management:agile-best-practices.adoc` | M1 core / shared reference |
| `project-management:case-studies.adoc` | M1 core / shared reference |
| `project-management:collaboration-models-weather-lab.adoc` | M1 core / shared reference |
| `project-management:github.adoc` | M1 core / shared reference |
| `project-management:index.adoc` | M1 core / shared reference |
| `project-management:introduction.adoc` | M1 core / shared reference |
| `project-management:practical-examples.adoc` | M1 core / shared reference |
| `project-management:project-phases.adoc` | M1 core / shared reference |
| `project-management:project.adoc` | M1 core / shared reference |
| `project-management:tools-gantt.adoc` | M1 core / shared reference |
| `project-management:waterfall-basics.adoc` | M1 core / shared reference |
| `software:index.adoc` | M2 core / shared reference |
| `software:package-managers.adoc` | M2 core / shared reference |
| `software:python-e2e-weather-workshop.adoc` | M2 core / shared reference |
| `software:release-engineering-weather.adoc` | M2 core / shared reference |
| `software:repo/organization.adoc` | M2 core / shared reference |
| `visualisation:dash-weather.adoc` | Shared/reference |
| `visualisation:dash.adoc` | Shared/reference |
| `visualisation:hw.adoc` | Shared/reference |
| `visualisation:index.adoc` | Shared/reference |
| `vscode:basic-usage.adoc` | M1 core / shared reference |
| `vscode:cheatsheet.adoc` | M1 core / shared reference |
| `vscode:configure-vscode.adoc` | M1 core / shared reference |
| `vscode:extensions.adoc` | M1 core / shared reference |
| `vscode:index.adoc` | M1 core / shared reference |
| `vscode:install.adoc` | M1 core / shared reference |
| `vscode:python-jupyter.adoc` | M1 core / shared reference |
| `vscode:remote-ssh.adoc` | M1 core / shared reference |
| `vscode:wsl.adoc` | M1 core / shared reference |

All CSMI ROOT year/semester/topic pages: shared project-topic reference; preserve content. Local generated registry/provisioning pages: instructor/admin reference, owned by pre-existing work.

## Validation plan

Run the original build to establish baseline diagnostics. Build the redesigned site with Antora, check rendered local links and navigation, exercise the standalone scientific example, and inspect home/M2/tutorial/project pages in a browser. Validate again from a clean checkout of the focused commits so untracked local material cannot mask missing dependencies. Record runtime limitations explicitly.

## Refined scientific objective

The user clarified that Gaya + Slurm + Apptainer deployment of Feel++ is the practical target, followed by a parameterized simulation-to-ML pipeline. The final MLOps specification uses Feel++ thermal simulations to generate mean-temperature regression data, followed by held-out and independent solver-based verification. The CSV example is only an initial container smoke exercise.
