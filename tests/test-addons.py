import pytest
import os
import platform
import sh
import yaml

from validators import (
    validate_gopaddle_lite,
)

from utils import (
    microk8s_enable,
    wait_for_pod_state,
    wait_for_namespace_termination,
    microk8s_disable,
    microk8s_reset,
    is_container,
)
from subprocess import PIPE, STDOUT, CalledProcessError, check_call, run, check_output


class TestAddons(object):
    @pytest.fixture(scope="session", autouse=True)
    def clean_up(self):
        """
        Clean up after a test
        """
        yield
        microk8s_reset()

    @pytest.mark.skipif(
        platform.machine() != "x86_64",
        reason="gopaddle-lite tests are only relevant in x86 architectures",
    )

    def test_gopaddle_lite(self):
        """
        Sets up and validates gopaddle-lite.
        """
        print("Enabling gopaddle-lite")
        microk8s_enable("gopaddle-lite")
        print("Validating gopaddle-lite")
        validate_gopaddle_lite()
        print("Disabling gopaddle-lite")
        microk8s_disable("gopaddle-lite")
