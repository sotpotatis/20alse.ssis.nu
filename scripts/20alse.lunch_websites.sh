#20alse.lunch_websites.sh
#Prepares for publishing my lunch website. The repository contains two subfolders, but currently the only
#one that is supported is lunch/ (not lunch_legacy/)
rm .20alse.lunch_websites #Remove previous build artifacts
mv src/20alse.lunch_websites/lunch .20alse.lunch_websites-build  -T || exit 1