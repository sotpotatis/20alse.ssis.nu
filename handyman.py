"""handyman.py
The Handyman does the things specified in README.md, which basically is:
1. Read everything in src.
2. For each app, run any build scripts.
3. Copy the artificact .{repo}-build directory into dist/
4. Handle routing by using the ROUTES folder to determine where to put stuff."""
import os, logging, sys, shutil, subprocess
from handyman_libs import route_file_parser, ignore_parser
# Initialize logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
# ...and handymanignore parser
handymanignore_parser = ignore_parser.HandymanIgnoreParser(version=1)
# Get paths
SOURCE_DIRECTORY = os.path.join(os.getcwd(), "src")
DIST_DIRECTORY = os.path.join(os.getcwd(), "dist")
SCRIPTS_DIRECTORY = os.path.join(os.getcwd(), "scripts")
ROUTES_FILE_PATH = os.path.join(os.getcwd(), "ROUTES")
MANDATORY_PATHS = [
    SOURCE_DIRECTORY, SCRIPTS_DIRECTORY, ROUTES_FILE_PATH
]
# Validate that all files exist
if not all([os.path.exists(mandatory_path) for mandatory_path in MANDATORY_PATHS]):
    raise FileNotFoundError(f"Missing one of the mandatory files: {MANDATORY_PATHS}. Please make sure that they exist.")
logger.debug("All mandatory files exist.")
# Parse the ROUTES file
logger.info("Parsing your ROUTES file...")
routes_parser = route_file_parser.RoutesFileParser(ROUTES_FILE_PATH, version=1)
mapped_routes = routes_parser.parse()
logger.info(f"Found {len(mapped_routes)} mapped routes:")
# Print each mapped route
for source_path, output_path in mapped_routes:
    logger.info(f"/{output_path}:retrieved from {source_path}")
# Clean dist folder
if os.path.exists(DIST_DIRECTORY):
    logger.info("Cleaning dist folder...")
    shutil.rmtree(DIST_DIRECTORY)
logger.info("Creating dist folder...")
os.mkdir(DIST_DIRECTORY)
logger.info("Dist folder created.")
# Start building
logger.info("Starting building...")
for source_path, output_path in mapped_routes:
    logger.info(f"Building {source_path}...")
    # Step 1: ensure that the source path exists
    source_path_full = os.path.join(SOURCE_DIRECTORY, source_path)
    if not os.path.exists(source_path_full):
        raise FileNotFoundError(f"Source {source_path_full} does not exist. The building can not continue with missing sources.")
    logger.debug("Source file exists.")
    # Step 2: Clean up the build directory. This artifact is only expected if the build failed.
    build_directory = os.path.join(os.getcwd(), f".{source_path}-build")
    if os.path.exists(build_directory):
        logger.info(f"Cleaning up artifacts from previous build for {source_path}...")
        shutil.rmtree(build_directory)
    # Step 3: Check if there is a .handymanignore file and if so parse it
    ignored_paths = handymanignore_parser.find_ignored_files(source_path_full)
    # Step 4: Check if a script is specified
    script_path_full = os.path.join(os.getcwd(), f"scripts/{source_path}.sh")
    if os.path.exists(script_path_full):
        logger.info(f"Running custom script for {source_path_full}...")
        script_path_full_bash_friendly = script_path_full.replace("\\", "/")
        return_code = subprocess.call(f"bash {script_path_full_bash_friendly}", shell=True)
        if return_code != 0:
            raise ChildProcessError(f"Running the custom script for {source_path_full} failed!")
        if not os.path.exists(build_directory): # All custom scripts must create a build directory.
            raise ChildProcessError(f"Running the custom script for {source_path_full} did not produce an build output directory {build_directory}!")
    else: # No script - just copy everything directly
        logger.info(f"{source_path_full} does not require a script.")
        os.mkdir(build_directory)
        # Copy all files (files hidden by handymanignore will be removed later)
        for filename in os.listdir(source_path_full):
            source_file_path = os.path.join(source_path_full, filename)
            target_file_path = os.path.join(build_directory, filename)
            source_is_directory = os.path.isdir(source_file_path)
            logger.info(f"+COPY {source_file_path}->{target_file_path} (directory: {source_is_directory})")
            if source_is_directory: # Ensure target is a directory if needed
                shutil.copytree(source_file_path, target_file_path)
            else:
                shutil.copy(source_file_path, target_file_path)
    # Step 5: Remove any ignored files
    logger.info(f"Build for {source_path_full} was completed. Removing ignored files...")
    logger.info(f"Found {len(ignored_paths)} ignored files from before.")
    handymanignore_parser.remove_ignored_files_in(build_directory, ignored_paths) # Remove all the paths
    # Step 6: Move into the dist/ folder
    logger.info(f"Build for {source_path} is now finished with the following artifacts: {os.listdir(build_directory)}")
    output_path_full = os.path.join(DIST_DIRECTORY, output_path)
    if not os.path.exists(output_path_full): # Create output directory
        os.mkdir(output_path_full)
    logger.info(f"Moving {build_directory} into {output_path_full}...")
    # Move all files
    for filename in os.listdir(build_directory):
        build_file_path = os.path.join(build_directory, filename)
        shutil.move(build_file_path, os.path.join(output_path_full, filename))
    # Step 7: clean up
    logger.info(f"Done. Removing artifacts for {source_path}...")
    shutil.rmtree(build_directory)
    logger.info(f"Distributing {source_path} finished.")
