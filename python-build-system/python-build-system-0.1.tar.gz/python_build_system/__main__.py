import argparse
from .project import Project


def main():
    parser = argparse.ArgumentParser(description="Python Build System")
    parser.add_argument("project_file", help="Specify project XML file")
    parser.add_argument("config", help="Specify project configuration")
    parser.add_argument("target", help="Specify configuration target")
    parser.add_argument("--build-dir", help="Specify project build directory")
    parser.add_argument("--simulation", help="Don't perform any operations. Only print expected commands",
                        action="store_true")
    args = parser.parse_args()
    if args.project_file:
        project = Project(file_name=args.project_file)
        if args.config in project.configs:
            config = project.configs[args.config]
            config.build(args.target, args.build_dir if args.build_dir else None, args.simulation)
        else:
            if args.config != '?':
                print("Configuration \"%s\" not found in the project" % args.config)
            print("Available project configurations:")
            for name in project.configs:
                print("-- %s" % name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
