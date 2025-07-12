import os
import subprocess
import zipfile
from pathlib import Path
from src.mlpipeline.entity.config_entity import DataIngestionConfig
from src.mlpipeline.logging import logger

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        if not os.path.exists(self.config.load_data_file):
            try:
                logger.info("Downloading from Kaggle...")
                subprocess.run([
                    "kaggle", "competitions", "download",
                    "-c", self.config.source_url,
                    "-f", os.path.basename(self.config.load_data_file),
                    "-p", os.path.dirname(self.config.load_data_file)
                ], check=True)
                logger.info(f"Downloaded to: {self.config.load_data_file}")

                # Unzip if needed
                zip_file = self.config.load_data_file.with_suffix(".csv.zip")
                if zip_file.exists():
                    with zipfile.ZipFile(zip_file, "r") as zip_ref:
                        zip_ref.extractall(self.config.unzip_dir)
                    os.remove(zip_file)

            except subprocess.CalledProcessError as e:
                logger.error(f"Download failed: {e}")
                raise e
        else:
            logger.info(f"{self.config.load_data_file} already exists. Skipping download.")

    def extract_zip_file(self):
        """Extract zip files in the data ingestion directory"""
        try:
            # Look for zip files in the root directory
            zip_files = list(Path(self.config.root_dir).glob("*.zip"))
            
            if not zip_files:
                logger.info("No zip files found to extract.")
                return
            
            for zip_file in zip_files:
                logger.info(f"Extracting {zip_file} to {self.config.unzip_dir}")
                with zipfile.ZipFile(zip_file, "r") as zip_ref:
                    zip_ref.extractall(self.config.unzip_dir)
                logger.info(f"Successfully extracted {zip_file}")
                
                # Optionally remove the zip file after extraction
                # os.remove(zip_file)
                
        except Exception as e:
            logger.error(f"Error extracting zip files: {e}")
            raise e




