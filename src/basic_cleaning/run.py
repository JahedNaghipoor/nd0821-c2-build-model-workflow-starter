#!/usr/bin/env python
"""
This script download from W&B the raw dataset
and apply some basic data cleaning,
exporting the result to a new artifact
Author: Jahed Naghipoor
Date: December 2021
Pylint score: 9.67/10
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    """
    go is the main function that is called when you run this script.

    Args:
        args: arguments to be passed to the function
    """

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact.
    local_path = run.use_artifact(args.input_artifact).file()
    dataframe = pd.read_csv(local_path)

    idx = dataframe['price'].between(args.min_price, args.max_price)
    dataframe = dataframe[idx].copy()

    # Convert last_review to datetime
    if "last_review" in dataframe.columns:
        dataframe['last_review'] = pd.to_datetime(dataframe['last_review'])

    dataframe.to_csv(args.output_artifact, index=False)

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description
    )

    artifact.add_file(args.output_artifact)
    run.log_artifact(artifact)

    logger.info("Cleaned data is loaded to Weights & Biases")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Name of the input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="Name of the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="Output artifact type.",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Description of the output file",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="minimum price",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="maximum price",
        required=True
    )

    arguments = parser.parse_args()

    go(arguments)
