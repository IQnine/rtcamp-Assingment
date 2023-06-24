#import os
#import subprocess
#import sys
#
#DOCKER_INSTALL_SCRIPT = "curl -fsSL https://get.docker.com -o get-docker.sh"
#DOCKER_COMPOSE_INSTALL_SCRIPT = "sudo curl -L 'https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)' -o /usr/local/bin/docker-compose && sudo chmod +x /usr/local/bin/docker-compose"
#
#DOCKER_COMPOSE_FILE = """
#version: '3'
#services:
#  db:
#    image: mysql:latest
#    restart: always
#    volumes:
#      - db_data:/var/lib/mysql
#    environment:
#      MYSQL_ROOT_PASSWORD: example_root_password
#      MYSQL_DATABASE: wordpress
#      MYSQL_USER: wordpress
#      MYSQL_PASSWORD: example_password
#  wordpress:
#    depends_on:
#      - db
#    image: wordpress:latest
#    restart: always
#    volumes:
#      - ./wp:/var/www/html
#    ports:
#      - '0.0.0.0:80'
#    environment:
#      WORDPRESS_DB_HOST: db:3306
#      WORDPRESS_DB_USER: wordpress
#      WORDPRESS_DB_PASSWORD: example_password
#volumes:
#  db_data:
#"""
#
#HOSTS_FILE_ENTRY = "127.0.0.1 example.com"
#
#def check_command_exists(command):
#    try:
#        subprocess.check_output(f"which {command}", shell=True)
#        return True
#    except subprocess.CalledProcessError:
#        return False
#
#def install_docker():
#    print("Docker not found. Installing Docker...")
#    subprocess.call(DOCKER_INSTALL_SCRIPT, shell=True)
#
#def install_docker_compose():
#    print("Docker Compose not found. Installing Docker Compose...")
#    subprocess.call(DOCKER_COMPOSE_INSTALL_SCRIPT, shell=True)
#
#def create_site(site_name):
#    if not os.path.exists("wp"):
#        os.makedirs("wp")
#
#    with open("docker-compose.yml", "w") as compose_file:
#        compose_file.write(DOCKER_COMPOSE_FILE)
#
#    subprocess.call("docker-compose up -d", shell=True)
#    subprocess.call(f"sudo -- sh -c 'echo \"{HOSTS_FILE_ENTRY}\" >> /etc/hosts'", shell=True)
#
#def open_browser(site_name):
#    print(f"Please open http://{site_name} in your browser.")
#
#def stop_site():
#    subprocess.call("docker-compose stop", shell=True)
#
#def start_site():
#    subprocess.call("docker-compose start", shell=True)
#
#def delete_site():
#    subprocess.call("docker-compose down", shell=True)
#    subprocess.call("sudo sed -i '/example.com/d' /etc/hosts", shell=True)
#    if os.path.exists("wp"):
#        subprocess.call("sudo rm -rf wp", shell=True)
#
#def main():
#    if not check_command_exists("docker"):
#        install_docker()
#
#    if not check_command_exists("docker-compose"):
#        install_docker_compose()
#
#    if len(sys.argv) < 2:
#        print("Please provide a subcommand.")
#        sys.exit(1)
#
#    subcommand = sys.argv[1]
#
#    if subcommand == "create":
#        if len(sys.argv) < 3:
#            print("Please provide a site name.")
#            sys.exit(1)
#        site_name = sys.argv[2]
#        create_site(site_name)
#        open_browser(site_name)
#    elif subcommand == "enable":
#        start_site()
#    elif subcommand == "disable":
#        stop_site()
#    elif subcommand == "delete":
#        delete_site()
#    else:
#        print("Invalid subcommand.")
#
#if __name__ == "__main__":
#    main()



import subprocess
import argparse
import os

DOCKER_COMPOSE_FILE = "docker-compose.yml"
WORDPRESS_CONTAINER_NAME = "wordpress"
MYSQL_CONTAINER_NAME = "mysql"
ETC_HOSTS_FILE = "/etc/hosts"

def check_dependencies():
    try:
        subprocess.check_output(["docker", "--version"])
        subprocess.check_output(["docker-compose", "--version"])
        print("Docker and Docker Compose are already installed.")
    except OSError as e:
        print("Installing Docker and Docker Compose...")
        subprocess.call(["sudo", "apt", "update"])
        subprocess.call(["sudo", "apt", "install", "-y", "docker.io", "docker-compose"])

def create_wordpress_site(site_name):
    with open(DOCKER_COMPOSE_FILE, "w") as file:
        file.write(f"""
version: '3'
services:
  {MYSQL_CONTAINER_NAME}:
    image: mysql:latest
    environment:
      MYSQL_ROOT_PASSWORD: examplepass
      MYSQL_DATABASE: {site_name}
      MYSQL_USER: {site_name}
      MYSQL_PASSWORD: {site_name}pass
  {WORDPRESS_CONTAINER_NAME}:
    depends_on:
      - {MYSQL_CONTAINER_NAME}
    image: wordpress:latest
    ports:
      - "80:80"
    environment:
      WORDPRESS_DB_HOST: {MYSQL_CONTAINER_NAME}
      WORDPRESS_DB_NAME: {site_name}
      WORDPRESS_DB_USER: {site_name}
      WORDPRESS_DB_PASSWORD: {site_name}pass
""")
    subprocess.call(["docker-compose", "up", "-d"])
    print("WordPress site created successfully!")

def add_hosts_entry(site_name):
    with open(ETC_HOSTS_FILE, "a") as file:
        file.write(f"127.0.0.1\t{site_name}\n")

def open_in_browser(site_name):
    print(f"Open http://{site_name} in a browser.")

def enable_disable_site(enable):
    action = "start" if enable else "stop"
    subprocess.call(["docker-compose", action])

def delete_site():
    subprocess.call(["docker-compose", "down"])
    os.remove(DOCKER_COMPOSE_FILE)
    print("Site deleted successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WordPress site management script")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # Check Dependencies Command
    parser_check_deps = subparsers.add_parser("checkdeps", help="Check if Docker and Docker Compose are installed")
    
    # Create Site Command
    parser_create_site = subparsers.add_parser("create", help="Create a new WordPress site")
    parser_create_site.add_argument("site_name", type=str, help="Name of the site")
    
    # Add Hosts Entry Command
    parser_add_hosts = subparsers.add_parser("addhosts", help="Add /etc/hosts entry for the site")
    parser_add_hosts.add_argument("site_name", type=str, help="Name of the site")
    
    # Open in Browser Command
    parser_open_browser = subparsers.add_parser("openbrowser", help="Prompt to open the site in a browser")
    parser_open_browser.add_argument("site_name", type=str, help="Name of the site")
    
    # Enable/Disable Site Command
    parser_enable_disable_site = subparsers.add_parser("enabledisable", help="Enable or disable the site")
    parser_enable_disable_site.add_argument("enable", choices=["enable", "disable"], help="Enable or disable the site")
    
    # Delete Site Command
    parser_delete_site = subparsers.add_parser("delete", help="Delete the site")

    args = parser.parse_args()

    if args.command == "checkdeps":
        check_dependencies()
    elif args.command == "create":
        create_wordpress_site(args.site_name)
    elif args.command == "addhosts":
        add_hosts_entry(args.site_name)
    elif args.command == "openbrowser":
        open_in_browser(args.site_name)
    elif args.command == "enabledisable":
        enable_disable_site(args.enable == "enable")
    elif args.command == "delete":
        delete_site()
