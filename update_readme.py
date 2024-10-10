from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from count_code_lines import repos_summary, OutputFormat
import statistics


def main(): 
    updated_at = datetime.now().strftime('%Y-%m-%d %H:%M')

    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('README.md.j2')

    x = repos_summary(['engdan77'], output_format=OutputFormat.JSON)
    all_repos = [_['lines_of_code'] for _ in x['engdan77']]
    d = {
            'mean_across_repos': statistics.mean(all_repos),
            'max_across_repos': max(all_repos),
            'repos_count': len(x)
        }

    rendered_readme = template.render(updated_at=updated_at, d=d)

    # Save to README.md
    with open("README.md", "w") as f:
        f.write(rendered_readme)


if __name__ == "__main__":
    main()
