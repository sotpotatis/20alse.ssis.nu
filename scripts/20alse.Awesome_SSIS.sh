#20alse.awesome_ssis.sh
#Builds the Awesome SSIS website.
#The website is built using Jekyll.
echo "Building \"awesome_ssis\"-website..."
echo "Prepare: checking if Jekyll is installed..."
JEKYLL_INSTALLATION_RETURN=$(gem list | grep jekyll) # List gems and try to find jekyll in the list of installed things
bundler
if [[ ${#JEKYLL_INSTALLATION_RETURN} == 0 || $? != 0 ]];then
  echo "Prepare: Jekyll or bundler is not installed! Installing..."
  gem install jekyll bundler || exit 1
  echo "Prepare: Jekyll was installed."
else
  echo "Prepare: Jekyll is installed."
fi
cd src/20alse.Awesome_SSIS/awesome-ssis-site/ || exit 1
bundler update && bundler install
jekyll build -d production/
echo "Site built. Transferring..."
# Move back into root
cd ../../../ || exit 1
rm .20alse.awesome_ssis-build #Remove previous build artifacts
mv src/20alse.Awesome_SSIS/awesome-ssis-site/production .20alse.Awesome_SSIS-build  -T || exit 1

