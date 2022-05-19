import time
import os
import re
import requests
import platform
import yaml
import subprocess

from utils import (
    get_arch,
    kubectl,
    wait_for_pod_state,
    kubectl_get,
    wait_for_installation,
    docker,
    update_yaml_with_arch,
    run_until_success,
)

def validate_gopaddle_lite():
    """
    Validate gopaddle-lite
    """
    wait_for_pod_state(
        "", "gp-lite", "running", label="released-by=gopaddle"
    )
