#20alse.svamphemsida-bootstrap.sh
#Builds my Bootstrap project about mushrooms
#Uses Parcel
echo "Building Bootstrap svamphemsida website..."
# Install dependencies
cd src/20alse.svamphemsida-bootstrap || exit 1
npm install
npm run build
echo "Website built. Adding to build directory..."
# Move back into root
cd ../../ || exit 1
rm .20alse.svamphemsida-bootstrap-build # Remove previous build artifacts
mv src/20alse.svamphemsida-bootstrap/dist .20alse.svamphemsida-bootstrap-build  -T
echo "Website was added into build directory. Building finished."