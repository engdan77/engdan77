from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from count_code_lines import repos_summary, OutputFormat
from statistics import mean
import datetime
import base64


def main(): 
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('README.md.j2')

    x = repos_summary(['engdan77'], output_format=OutputFormat.JSON)
    chart = base64.b64decode(x['b64_mermaid_chart']).decode('utf-8')
    first_year = min([_['year'] for _ in x['engdan77']])
    this_year = datetime.datetime.now().year
    years_since_first_repo = this_year - first_year
    total_projects = len(x['engdan77'])
    code_lines_year = [_['lines_of_code'] for _ in x['engdan77']]
    total_code_lines = sum(code_lines_year)
    biggest_projects = sorted(x['engdan77'], key=lambda x: x['lines_of_code'], reverse=True)
    max_lines_of_code = f'{str(round(mean([_['lines_of_code'] for _ in biggest_projects[:3]]), -3))[0]}k'
    as_link = lambda x: f'[{x}](https://github.com/engdan77/{x}.git)'
    top_largest_projects = ', '.join([as_link(_['repo_name']) for _ in biggest_projects[:2]]) + f' and {as_link(biggest_projects[2]['repo_name'])}'
    last_run = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    d = {'total_code_lines': total_code_lines,
         'years_since_first_repo': years_since_first_repo,
         'total_projects': total_projects,
         'max_lines_of_code': max_lines_of_code,
         'top_largest_projects': top_largest_projects,
         'updated': last_run,
         'chart': chart,
         'last_run': last_run
         }

    rendered_readme = template.render(d=d)

    # Save to README.md
    with open("README.md", "w") as f:
        f.write(rendered_readme)


if __name__ == "__main__":
    main()
