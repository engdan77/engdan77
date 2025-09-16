# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "count_code_lines@git+https://github.com/engdan77/count_code_lines.git",
#     "jinja2",
# ]
# ///
from collections import defaultdict
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from count_code_lines import repos_summary, OutputFormat
from statistics import mean
import datetime
import base64


def get_projects_by_year(repos) -> dict[dict]:
    projects_by_year = defaultdict(list)
    for repo in repos:
        year = repo['year']
        if year not in projects_by_year:
            projects_by_year[year] = []
        projects_by_year[year].append(repo)
    return projects_by_year


def get_projects_per_year_as_markdown(projects_by_year, username='engdan77'):
    markdown = ''
    for year, projects in sorted(projects_by_year.items(), reverse=True, key=lambda x: x[0]):
        repos = []
        for p in projects:
            repo_name = p['repo_name']
            project_url = f'https://github.com/{username}/{repo_name}'
            repos.append(f'[{repo_name}]({project_url})')
        markdown += f'- **{year}**: {", ".join(repos)}\n'
    return markdown


def main(): 
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('README.md.j2')
    repo = 'engdan77'

    x = repos_summary([repo], output_format=OutputFormat.JSON, exclude_project=('jrnl',))
    chart = base64.b64decode(x['b64_mermaid_chart']).decode('utf-8')
    first_year = min([_['year'] for _ in x[repo]])
    this_year = datetime.datetime.now().year
    years_since_first_repo = this_year - first_year
    total_projects = len(x[repo])
    code_lines_year = [_['lines_of_code'] for _ in x[repo]]
    total_code_lines = sum(code_lines_year)
    biggest_projects = sorted(x[repo], key=lambda x: x['lines_of_code'], reverse=True)
    max_lines_of_code = f'{str(round(mean([_['lines_of_code'] for _ in biggest_projects[:3]]), -3))[0]}k'
    as_link = lambda x: f'[{x}](https://github.com/engdan77/{x}.git)'
    top_largest_projects = ', '.join([as_link(_['repo_name']) for _ in biggest_projects[:2]]) + f' and {as_link(biggest_projects[2]['repo_name'])}'
    last_run = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    all_projects_by_year = get_projects_by_year(x[repo])
    projects_markdown = get_projects_per_year_as_markdown(all_projects_by_year, username=repo)

    d = {'total_code_lines': total_code_lines,
         'years_since_first_repo': years_since_first_repo,
         'total_projects': total_projects,
         'max_lines_of_code': max_lines_of_code,
         'top_largest_projects': top_largest_projects,
         'updated': last_run,
         'chart': chart,
         'last_run': last_run,
         'projects_markdown': projects_markdown
         }

    rendered_readme = template.render(d=d)

    # Save to README.md
    with open("README.md", "w") as f:
        f.write(rendered_readme)


if __name__ == "__main__":
    main()
