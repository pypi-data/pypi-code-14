# vi:et:ts=4 sw=4 sts=4
#
# local-pipelines : run Bitbucket pipelines locally
# Copyright (C) 2016  Gary Kramlich <grim@reaperworld.com>
# Copyright (C) 2016  Sean Farley <sean@farley.io>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

import fnmatch
import os
import subprocess

from pipelines.step import Step


class Pipeline(object):
    def __init__(self, config, path, repo, run_shell=False, env=None):
        self.config = config
        self.build_path = os.path.abspath(path)
        self.repo = repo
        self.run_shell = run_shell
        self._env = env or {}

        # add special variables
        self._env["BITBUCKET_BRANCH"] = self.repo.branch
        self._env["BITBUCKET_COMMIT"] = self.repo.node
        self._env["BITBUCKET_REPO_OWNER"] = self.repo.owner
        self._env["BITBUCKET_REPO_SLUG"] = self.repo.slug

    @property
    def steps(self):
        ret = self.config["pipelines"]["default"]
        if "branches" in self.config["pipelines"]:
            branches = self.config["pipelines"]["branches"]

            for pattern, steps in branches.items():
                if fnmatch.fnmatch(self.repo.branch, pattern):
                    ret = steps
                    break

        return [Step.from_dict(s["step"]) for s in ret]

    @property
    def public_env(self):
        # dict of env vars that are not none
        return {k: v for k, v in self._env.items() if v is not None}

    @property
    def private_env(self):
        # dict of env vars that are none (grabbed from os.environ)
        return {k: os.environ.get(k, "") for k, v in self._env.items()
                if v is None}

    def _determine_image(self, step):
        return step.image or self.config.get("image")

    def _get_command(self, step, script):
        workdir = "/opt/atlassian/bitbucketci/agent/build"

        labels = [
            "com.atlassian.pipelines.agent=\"local\"",
        ]

        # docker on windows needs to convert to a posix path
        drive, spath = os.path.splitdrive(script)
        if drive:
            # strip off the colon, e.g. 'C:' -> 'C'
            drive = drive[:-1]
            # assemble the pieces together
            script = '/' + drive + spath.replace('\\', '/')

        script_internal = "/tmp/bitbucket-pipelines.sh"

        volumes = [
            "{filename}:{script_internal}:ro".format(
                filename=script,
                script_internal=script_internal,
            ),
            "{path}:{workdir}:rw".format(
                path=self.build_path,
                workdir=workdir,
            ),
        ]

        command = script_internal
        if self.run_shell:
            command = ""

        cmd = [
            "docker",
            "run",
            "--rm=true",
            "--entrypoint=/bin/bash",
            "--memory=2048m",
            "-it",
            " ".join(["-v " + v for v in volumes]),
            "-w {}".format(workdir),
            " ".join(["--label " + l for l in labels]),
            " ".join(["-e {}={}".format(k, v) for k, v in
                      self.public_env.items()]),
            " ".join(["-e " + k for k in self.private_env.keys()]),
            self._determine_image(step),
            command,
        ]

        return " ".join(cmd)

    def run(self):
        return_code = 0
        subenv = os.environ.copy()
        subenv.update(self.private_env)

        for n, step in enumerate(self.steps):
            script = step.script_file()
            command = self._get_command(step, script)

            try:
                print('+ {}'.format(command))
                proc = subprocess.Popen(command.split(),
                                        env=subenv)

                return_code = proc.wait()
                if return_code != 0:
                    return return_code
            except KeyboardInterrupt:
                # let's not stacktrace on ctrl-c
                proc.kill()
                return_code = 1
                break
            finally:
                try:
                    os.remove(script)
                except OSError:
                    pass

        return return_code
