import sys
import subprocess
import logging
from modules.logger import setup_logger

setup_logger()


def run_script(script_name):
    logging.info(f"Running {script_name}")
    result = subprocess.run(["python", script_name])
    return result.returncode


if len(sys.argv) < 2:
    print("Usage: python run.py [precheck|deploy|postcheck|validate|compare|rollback|full]")
    sys.exit(1)

mode = sys.argv[1]

if mode == "precheck":
    run_script("precheck.py")

elif mode == "deploy":
    run_script("deploy.py")

elif mode == "postcheck":
    run_script("postcheck.py")

elif mode == "validate":
    run_script("validation.py")

elif mode == "compare":
    run_script("comparison.py")

elif mode == "rollback":
    run_script("rollback.py")

elif mode == "full":
    logging.info("=== FULL AUTOMATION STARTED ===")

    if run_script("precheck.py") != 0:
        sys.exit("Precheck failed")

    if run_script("deploy.py") != 0:
        sys.exit("Deploy failed")

    if run_script("postcheck.py") != 0:
        sys.exit("Postcheck failed")

    # VALIDATION DECISION POINT
    validation_status = run_script("validation.py")

    if validation_status != 0:
        logging.error("Validation failed → stopping execution")
        sys.exit(1)

    # Only runs if validation success
    run_script("comparison.py")

    logging.info("=== FULL AUTOMATION COMPLETED SUCCESSFULLY ===")

else:
    print("Invalid option")