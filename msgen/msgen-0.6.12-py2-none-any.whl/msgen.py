#!/usr/bin/python
# ----------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved. 
#  Licensed under the MIT License. See License.txt in the 
#  project root for license information.  If License.txt is 
#  missing, see https://opensource.org/licenses/MIT
# ----------------------------------------------------------

"""Microsoft Genomics Command-line Client - allows submission and management
 of genomics workflows on the Microsoft Genomics platform"""

import msgen_cli.malibuworkflow as malibuworkflow
import msgen_cli.malibuargs as malibuargs


print "Microsoft Genomics Command-line Client - Copyright 2016 Microsoft Corporation"

import sys

def main():
    """Main execution flow"""


    args_output = malibuargs.ArgsOutput()
    args_output.parse_args_from_command_line()
    args_output.validate()

    workflow_executor = malibuworkflow.WorkflowExecutor(args_output)

    if args_output.command == "SUBMIT":
        # Post new Workflow
        workflow_executor.post_workflow()
    elif args_output.command == "GETSTATUS":
        # Get workflow status
        workflow_executor.get_workflow_status()
    elif args_output.command == "CANCEL":
        # Cancel workflow
        workflow_executor.cancel_workflow()
    elif args_output.command == "LIST":
        # List workflows
        workflow_executor.list_workflows()
    else:
        print "Exiting due to permanent failure. Reason: No command specified."
        sys.exit(1000)

    sys.exit(workflow_executor.current_exit_status)


if __name__ == "__main__":
    main()
