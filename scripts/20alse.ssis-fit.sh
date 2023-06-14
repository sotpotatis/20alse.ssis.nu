#20alse.ssis-fit
#Script for "building" the SSIS Fit website.
#The website is already built, so what this really does is cleans out
#everything but the website in the repo
echo "Building SSIS-Fit website..."
cd src/20alse.ssis-fit || exit 1
echo "Removing non-website related assets..."
rm -rf screenshots  || exit 1
rm -rf site || exit 1
echo "Non-website related assets have been removed."
cd ../.. || exit 1
rm .20alse.ssis-fit-build # Remove previous build artifacts
mv src/20alse.ssis-fit/website .20alse.ssis-fit-build  -T || exit 1
echo "Done building SSIS-fit website."