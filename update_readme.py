from datetime import datetime
from jinja2 import Environment, FileSystemLoader


def main(): 
    updated_at = datetime.now().strftime('%Y-%m-%d %H:%M')

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('README.md.j2')

    # Render and merge templates
    rendered_readme = template.render(updated_at=updated_at)

    # Save to README.md
    with open("README.md", "w") as f:
        f.write(rendered_readme)


if __name__ == "__main__":
    main()
