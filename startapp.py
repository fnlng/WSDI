import sys
import click

from app import create_app


@click.command()
@click.option('--debug', '-d', flag_value=True, default=False, type=click.BOOL,
              help="start with debug mode")
def main(debug):
    app = create_app(debug)
    
    app.run(host='0.0.0.0', port=8000, debug=debug)


if __name__ == '__main__':
    main()