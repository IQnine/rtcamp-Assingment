# rtcamp-Assingment

# WordPress Site Manager

This command-line script allows you to manage WordPress sites using a LEMP stack running inside Docker containers. It provides convenient subcommands to create, enable/disable, and delete WordPress sites.

## Prerequisites

- Docker
- Docker Compose

## Installation

1. Clone the repository:
git clone <repository-url>
2. Change to the project directory:
cd wordpress-site-manager
3. Ensure Docker and Docker Compose are installed:

./wordpress_manager.py checkdeps

If Docker and Docker Compose are not installed, the script will automatically attempt to install them.

## Usage

The script provides the following subcommands:

- `checkdeps`: Check if Docker and Docker Compose are installed.
- `create`: Create a new WordPress site.
- `addhosts`: Add an `/etc/hosts` entry for the site.
- `openbrowser`: Prompt to open the site in a browser.
- `enabledisable`: Enable or disable the site (start or stop the containers).
- `delete`: Delete the site.

### Create a New WordPress Site

To create a new WordPress site, use the `create` subcommand followed by the desired site name:

./wordpress_manager.py create example.com

This will create the necessary Docker containers and set up the WordPress site.

### Add `/etc/hosts` Entry

To add an entry in `/etc/hosts` for the site, use the `addhosts` subcommand followed by the site name:

./wordpress_manager.py addhosts example.com

This will add an entry in `/etc/hosts` mapping `example.com` to `localhost`.

### Open the Site in a Browser

To prompt opening the site in a browser, use the `openbrowser` subcommand followed by the site name:

./wordpress_manager.py openbrowser example.com

This will display a message with the URL to open in a browser.

### Enable or Disable the Site

To enable or disable the site (start or stop the containers), use the `enabledisable` subcommand followed by `enable` or `disable`:

./wordpress_manager.py enabledisable enable
./wordpress_manager.py enabledisable disable

### Delete the Site

To delete the site, use the `delete` subcommand:

./wordpress_manager.py delete

This will stop the containers and delete the site files.

## License

This project is licensed under the [MIT License](LICENSE).

