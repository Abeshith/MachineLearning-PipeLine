import os
import yaml
from src.mlpipeline.logging import logger
import json
import joblib 
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
from box.exceptions import BoxValueError

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """_summary_

    Args:
        path_to_yaml (Path): _description_

    Returns:
        ConfigBox: _description_
    """
    try:
        with open(path_to_yaml) as yml:
            content = yaml.safe_load(yml)
            logger.info(f"yaml file: {path_to_yaml} loaded sucessfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    

@ensure_annotations
def create_directories(path_to_directories: list, verbose = True):
    """_summary_

    Args:
        path_to_directories (list): _description_
        verbose (bool, optional): _description_. Defaults to True.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok = True)
        if verbose:
            logger.info(f"Creating a Directory at: {path}")


@ensure_annotations
def save_json(path : Path, data: dict):
    """_summary_

    Args:
        path (Path): _description_
        data (dict): _description_
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    
    logger.info(f"json file saved at: {path}")


@ensure_annotations
def load_json(path : Path) -> ConfigBox:
    """_summary_

    Args:
        path (Path): _description_

    Returns:
        ConfigBox: _description_
    """
    with open(path) as f:
        content = json.load(f)

    logger.info(f"json file loaded seccessfully from {f}")
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path):
    """_summary_

    Args:
        data (Any): _description_
        path (path): _description_
    """

    joblib.dump(value = data, filename=path)
    logger.info(f"binary file at {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """_summary_

    Args:
        path (Path): _description_

    Returns:
        Any: _description_
    """
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data