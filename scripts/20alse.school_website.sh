#20alse.school_website.sh
#Builds my personal school website.
#Uses Svelte
echo "Building school website..."
# Install dependencies
cd src/20alse.school_website || exit 1
npm install
npm run build
echo "Website built. Adding to build directory..."
# Move back into root
cd ../..
rm .20alse.school_website-build # Remove previous build artifacts
mkdir .20alse.school_website-build
mv src/20alse.school_website/build .20alse.school_website-build  -T || exit 1
echo "Website was added into build directory. Building finished."