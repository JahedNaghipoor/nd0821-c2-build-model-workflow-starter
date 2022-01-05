#!/usr/bin/env python
"""
This script downloads a URL to a local destination
and load it to Weights & Biases
"""
import argparse
import logging
import os

import wandb
from wandb_utils.log_artifact import log_artifact

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    """
    go is the main function that is called when you run this script.

    Args:
        args: arguments to be passed to the function
    """
    run = wandb.init(job_type="download_file")
    run.config.update(args)

    logger.info(f"Returning sample {args.sample}")
    logger.info(f"Uploading {args.artifact_name} to Weights & Biases")
    log_artifact(
        args.artifact_name,
        args.artifact_type,
        args.artifact_description,
        os.path.join("data", args.sample),
        run,
    )

    logger.info("Data is loaded to Weights & Biases")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download URL to a local destination")

    parser.add_argument(
        "sample",
        type=str,
        help="Name of the sample to download")

    parser.add_argument(
        "artifact_name",
        type=str,
        help="Name for the output artifact")

    parser.add_argument(
        "artifact_type",
        type=str,
        help="Output artifact type.")

    parser.add_argument(
        "artifact_description",
        type=str,
        help="A brief description of this artifact")

    arguments = parser.parse_args()

    go(arguments)
