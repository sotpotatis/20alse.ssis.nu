#20alse.yatzy-webbutveckling-slutprojekt.sh
#Builds my "Yatzy" project. It uses React via Vite.
echo "Building yatzy website..."
# Install dependencies
cd src/20alse.yatzy-webbutveckling-slutprojekt/frontend/yatzyprojekt || exit 1 # (we only want to build the frontend)
npm install
npm run build
echo "Website built. Copying..."
# Move back into root
cd ../../../../ || exit 1
rm .20alse.yatzy-webbutveckling-slutprojekt-build #Remove previous build artifacts
mv src/20alse.yatzy-webbutveckling-slutprojekt/frontend/yatzyprojekt/dist .20alse.yatzy-webbutveckling-slutprojekt-build  -T
echo "Website copied."