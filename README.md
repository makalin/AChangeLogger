# AutoChangelogger

AutoChangelogger is a Python-based tool for automatically generating and updating changelogs in your GitHub repositories. It leverages the GitHub API to fetch commit data and generate changelog files, simplifying the process of tracking changes over time.

## Features

- Automatically fetch commit messages from a GitHub repository.
- Generate a structured changelog with dates and commit details.
- Supports customization via command-line arguments.
- Easy integration with GitHub repositories.

## Prerequisites

- Python 3.7 or higher
- A GitHub personal access token with appropriate permissions to access the repository.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/autochangelogger.git
   cd autochangelogger
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command-Line Interface

The script supports the following command-line arguments:

- `--token` (required): Your GitHub personal access token.
- `--repo` (required): The GitHub repository name in the format `owner/repo`.
- `--output` (optional): The path to save the generated changelog file. Defaults to `CHANGELOG.md`.

Example usage:

```bash
python changelogup.py --token <your_github_token> --repo <owner/repo> --output ./CHANGELOG.md
```

### Script Integration

You can also integrate AutoChangelogger into your Python scripts. Here's an example:

```python
from changelogup import AutoChangelogger

# Initialize the AutoChangelogger
changelogger = AutoChangelogger(github_token="<your_github_token>", repo_name="owner/repo")

# Generate and save the changelog
changelogger.generate_changelog(output_path="./CHANGELOG.md")
```

## File Structure

- `changelogup.py`: The main script for generating changelogs.
- `requirements.txt`: Lists all dependencies required to run the script.

## Contributing

Contributions are welcome! If you'd like to contribute to this project:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -m 'Add your feature'`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Support

If you encounter any issues or have questions, feel free to open an issue on GitHub.

## Acknowledgments

Special thanks to the developers of the [PyGithub](https://github.com/PyGithub/PyGithub) library, which powers the GitHub API interactions in this project.

