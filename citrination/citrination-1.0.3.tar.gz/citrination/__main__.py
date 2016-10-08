import command_router
from citrination.commands import upload
from citrination.commands import create_dataset_version
from citrination.commands import create_dataset

app = command_router.CommandRouter()
app.register(upload.App, ['upload'])
app.register(create_dataset.App, ['create_dataset'])
app.register(create_dataset_version.App, ['create_dataset_version'])


def main():
    """
    Run the application.
    """
    app.run()

if __name__ == "__main__":
    main()
