# Contributing Guidelines

Thank you for your interest in contributing to the **Commercial Sub-Critical Hybrid Fission-Fusion Reactor Paradigm**.

## Code of Conduct & Academic Integrity
* All code, equations, and literature references must rely on non-classified, public domain scientific publications and open cross-section databases (e.g., IAEA, LLNL, ORNL).
* Maintain transparent attribution for human authorship and AI collaborative workflows.

## Development Workflow
1. **Fork & Clone:** Create a personal fork of the repository and clone it locally.
2. **Branching:** Create a feature branch following standard naming conventions:
   * `feature/add-openmc-coupling`
   * `fix/hydro-boundary-condition`
   * `docs/update-spec-sheet`
3. **Coding Standards:**
   * Write clean, vectorized Python code using `NumPy` and `SciPy`.
   * Apply `@njit(fastmath=True)` decorators for intensive grid loops via `Numba`.
   * Format Markdown content with standard HTML tags (`<sub>`, `<sup>`) for sub/superscripts to ensure clean cross-platform rendering.
4. **Pull Request Submission:** Submit a Pull Request targeting the `main` branch with a clear summary of modifications and corresponding benchmark verification plots.

## Semantic Versioning
This project uses Semantic Versioning (`MAJOR.MINOR.PATCH`):
* `MAJOR`: Architectural changes to reactor equations or breaking solver API updates.
* `MINOR`: Additional physics modules (e.g., 3D OpenMC neutron transport coupling).
* `PATCH`: Numerical bug fixes, parameter refinements, or documentation updates.
