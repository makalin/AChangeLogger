import os
from datetime import datetime
from github import Github
import re
from pathlib import Path
import argparse

class AutoChangelogger:
    def __init__(self, github_token, repo_name):
        """
        Initialize the AutoChangelogger with GitHub credentials and repository info.
        
        Args:
            github_token (str): GitHub personal access token
            repo_name (str): Repository name in format "owner/repo"
        """
        self.github = Github(github_token)
        self.repo = self.github.get_repo(repo_name)
        self.categories = {
            'feature': '### ✨ New Features',
            'bug': '### 🐛 Bug Fixes',
            'docs': '### 📚 Documentation',
            'refactor': '### ♻️ Code Refactoring',
            'test': '### 🧪 Tests',
            'chore': '### 🔧 Maintenance',
            'breaking': '### ⚠️ Breaking Changes'
        }
        
    def get_merged_prs(self, since_date=None):
        """
        Fetch merged pull requests since the given date.
        
        Args:
            since_date (datetime): Date to fetch PRs from
            
        Returns:
            list: List of merged pull requests
        """
        query = "type:pr is:merged"
        if since_date:
            query += f" merged:>={since_date.strftime('%Y-%m-%d')}"
        
        prs = self.repo.get_pulls(state='closed', sort='updated', direction='desc')
        return [pr for pr in prs if pr.merged and (not since_date or pr.merged_at >= since_date)]

    def categorize_pr(self, pr):
        """
        Categorize a pull request based on its labels and description.
        
        Args:
            pr: GitHub pull request object
            
        Returns:
            str: Category name
        """
        # First check labels
        for label in pr.labels:
            label_name = label.name.lower()
            for category in self.categories.keys():
                if category in label_name:
                    return category
        
        # Check PR title and description for conventional commit format
        conventional_commit_pattern = r'^(feat|fix|docs|refactor|test|chore|breaking)(\(.+\))?: .+'
        if re.match(conventional_commit_pattern, pr.title):
            type_match = re.match(r'^(\w+)', pr.title)
            commit_type = type_match.group(1)
            type_mapping = {
                'feat': 'feature',
                'fix': 'bug',
                'docs': 'docs',
                'refactor': 'refactor',
                'test': 'test',
                'chore': 'chore',
                'breaking': 'breaking'
            }
            return type_mapping.get(commit_type, 'chore')
            
        return 'chore'  # Default category

    def format_changelog_entry(self, pr):
        """
        Format a single changelog entry for a pull request.
        
        Args:
            pr: GitHub pull request object
            
        Returns:
            str: Formatted changelog entry
        """
        authors = f"@{pr.user.login}"
        if pr.body:
            # Remove Markdown links to keep it clean
            description = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', pr.body.split('\n')[0])
        else:
            description = pr.title
            
        return f"- {description} (#{pr.number}) - {authors}"

    def update_changelog(self, output_file='CHANGELOG.md'):
        """
        Update the changelog file with new entries.
        
        Args:
            output_file (str): Path to the changelog file
        """
        changelog_path = Path(output_file)
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Read existing changelog if it exists
        if changelog_path.exists():
            existing_content = changelog_path.read_text()
            # Find the date of the last entry
            date_pattern = r'\d{4}-\d{2}-\d{2}'
            dates = re.findall(date_pattern, existing_content)
            last_update = datetime.strptime(dates[0], '%Y-%m-%d') if dates else None
        else:
            existing_content = "# Changelog\n\nAll notable changes to this project will be documented in this file.\n\n"
            last_update = None

        # Fetch and categorize new PRs
        prs = self.get_merged_prs(last_update)
        if not prs:
            print("No new changes to add to changelog.")
            return

        # Group PRs by category
        categorized_prs = {}
        for pr in prs:
            category = self.categorize_pr(pr)
            if category not in categorized_prs:
                categorized_prs[category] = []
            categorized_prs[category].append(pr)

        # Generate new changelog section
        new_section = f"\n## [{current_date}]\n\n"
        for category, category_header in self.categories.items():
            if category in categorized_prs and categorized_prs[category]:
                new_section += f"{category_header}\n\n"
                for pr in categorized_prs[category]:
                    new_section += f"{self.format_changelog_entry(pr)}\n"
                new_section += "\n"

        # Insert new section after the header
        header_end = existing_content.find("\n\n") + 2
        updated_content = (
            existing_content[:header_end] +
            new_section +
            existing_content[header_end:]
        )

        # Write updated changelog
        changelog_path.write_text(updated_content)
        print(f"Changelog updated successfully: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Automatically update CHANGELOG.md based on merged pull requests')
    parser.add_argument('--token', required=True, help='GitHub personal access token')
    parser.add_argument('--repo', required=True, help='Repository name (owner/repo)')
    parser.add_argument('--output', default='CHANGELOG.md', help='Output changelog file')
    
    args = parser.parse_args()
    
    updater = AutoChangelogger(args.token, args.repo)
    updater.update_changelog(args.output)

if __name__ == "__main__":
    main()
