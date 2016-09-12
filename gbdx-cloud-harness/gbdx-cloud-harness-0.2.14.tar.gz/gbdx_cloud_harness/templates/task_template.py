"""
This file is an example of an application that can be run with the GBDX CLI both locally and remotely.

To run the application: gbdx app run

"""
from gbdx_task_template import TaskTemplate, Task, InputPort, OutputPort


class ExampleApp(TaskTemplate):
    """
    The class for the example application. All GBDX Cloud Harness applications must be a subclass
     of TaskTemplate.
    """

    # Create a new Task for the application, takes a string which is the tasks name.
    task = Task("MyTask")

    # Add an input port of type directory to the
    task.input_data = InputPort(port_type="directory", value="/my/local/input/data")

    # Add an output port of type directory to the task.
    task.output_data = OutputPort(
        port_type="directory", value="/my/local/output/location"
    )

    # OPTIONALLY, output_data can be initialized with an S3 location for remote runs only.
    # task.output_data = OutputPort(
    #     port_type="directory", value="s3://mybucket/folder"
    # )

    # Add an output port of type string.
    task.output_param = OutputPort(
        port_type="string"
    )

    def invoke(self):

        # List files of a port with an extension filter.
        my_files = self.task.output_data.list_files(extensions=['.py', '.tif'])

        # Write Task Magic Here...

        msg = 'Found %s files in %s' % (len(my_files), self.task.input_data.value)
        print(msg)  # Send num files to stdout

        # Save value to output parameter
        self.task.output_param.value = len(my_files)

        # Write new files to an Output port that is type directory.
        self.task.output_data.write('my_output.txt', msg, overwrite=True)

        self.reason = 'Everything Completed Correctly'
