# 20alse.ssis.nu

This repository backs up my personal school website, https://20alse.ssis.nu, which will be shut down
after I have graduated. It not only preserves all the pages on the original routes that were used to access them,
it also handles CI/CD to automatically build, install and push applications.

**The repository you're currently viewing acts as a "parent repository" containing submodule links to other repositories
that starts with `20alse.` and are used for structuring the different projects that are backed up.** Some deviations from this naming convention
exist and that is because some repositories already existed on GitHub before I started bacing up things that didn't.
## List of all backed up websites and projects

### Web projects: visible on https://20alse.albins.website/

| Name                                                                            | Description                                                                                                                                   |
|---------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| [School website](https://github.com/sotpotatis/20alse.school_website)           | The homepage that was the first thing you saw when going into https://20alse.ssis.nu.                                                         |
| [School website (Old)](https://github.com/sotpotatis/20alse.school_website_old) | Old version of "School website" from circa 2021.                                                                                              |
| [Awesome SSIS](https://github.com/sotpotatis/Awesome_SSIS)                      | Webpage showing awesome resources and helpful links for students attending Stockholm Science & Innovation School (SSIS)                       |
| [Click the happy man](https://github.com/sotpotatis/20alse.click-the-happy-man) | Iconic "cookie clicker"-style game.                                                                                                           |
| [Portfolio](https://github.com/sotpotatis/20alse.portfoliohemsida)              | Portfolio website made in CSS for an assignment in a web development course.                                                                  |
| [SSIS Fit](https://github.com/sotpotatis/ssis-fit)                              | Website for my project [SSIS Fit](https://github.com/sotpotatis/ssis-fit), a Fitbit app related to the school                                 |
| [Lunch](https://github.com/sotpotatis/20alse.lunch_websites)                    | Webpage to show the lunch menu in the school.                                                                                                 |
| [Bootstrap Svamphemsida](https://github.com/sotpotatis/)                        | Bootstrap assignment for a web development course. An informative website about picking mushrooms.                                            |
| [Yatzy](https://github.com/sotpotatis/20alse.yatzy-webbutveckling-slutprojekt)  | Final project for web development and interface design courses. A yatzy project made using React with both in-browser and online multiplayer. |
| [Start page assets](https://github.com/sotpotatis/20alse.start_page_assets)     | Images and videos used by the school websites.                                                                                                |
| [Pentry](https://github.com/sotpotatis/20alse.pentry)                           | (Legacy) website for showing who has responsibility for the school pentries.                                                                  |
| [Distans](https://github.com/sotpotatis/20alse.distans)                         | (Legacy, from COVID times) website for showing which group has distance education.                                                            |

### Non-web projects
| Name                                                                         | Description                                                                                                                |
|------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| [SkySpy](https://github.com/sotpotatis/SkySpy)                               | My graduation project: a custom and modular weather station system using own PCBs, own firmware, own backend and frontend. |
| [SSIS Discord RPC](https://github.com/sotpotatis/ssis-discord-rpc)           | Unfinished project showing what lesson you are currently attending in your Discord status.                                 |
| [SSIS.nu CSS Themes](https://github.com/sotpotatis/20alse.ssis.nu-css-teman) | CSS themes for the Stockholm Science & Innvation School homepage.                                                          |

## About building and publishing web projects

### Installing
This repository contains submodules according to the structure above. Make sure to check them out to get all subpages!

### Deta

This website is designed to run on [Deta](https://deta.space), however, it is really a very generic build process.
By simply running the script `prepare-and-run-handyman.sh` (tested on Debian and Ubuntu), a build environment containing the following will be created:
* Python 3 and pip (latest available versions)
* Node.js and NPM (20.\<latest available subversion>)
* Ruby and Bundler

not only that, the script will also run `handyman.py` to create a `dist` directory based on the mapping in the `ROUTES` file
and the scripts inside the `scripts/` directory (read on for more information about that).

#### Pushing to Deta and updating submodules

On Windows, running `.\push_to_deta.bat` will update submodules and push the whole code to Deta.

#### Note regarding Deta

In order for routing of the [Yatzy](https://github.com/sotpotatis/20alse.yatzy-webbutveckling-slutprojekt) game to work properly, it is pushed as a separate micro.
See the [Spacefile](Spacefile) for reference.

### Handyman, the builder 🔨

Since I am such a creative guy (smiley face), there is a bunch of toolsets, dependencies and other stuff
that every application depends on. To create a streamlined interface, I have created building scripts for each repository.
They can be found in the `scripts` folder. These building scripts produce a folder named `.build` which is then uploaded
via my custom Python script. Routing is done in the ROUTES file.

#### How to handyman

##### How Handyman works1. Check out the repository you want to add in `src` or add it manually.
2. If it does not need any build scripts, do not add anything in the `scripts/` folder.
Otherwise. create a script with `.sh` ending (Bash) and add the build scripts that you need to execute.
3. Edit `ROUTES.md` to control where the built dist (outputted to a `.{repo/folder name}-build` directory *relative to the working directory*) ends up in the `dist`. Note: examples for this can be found by looking at the [scripts/](scripts) directory in this repository.
4. Run the `handyman.py` script to generate output.

##### Ignoring files

You can add a `.handymanignore`-file in any directory in `src`. Here is its format:

```
# Comment, will be ignored
(dir) path_to_directory/
(file) file.extension
```