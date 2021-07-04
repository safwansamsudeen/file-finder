const fs = require('fs')
const path_module = require('path');
import *  as settings from './settings'

function indexer(dirs, index = null) {
    if (index === null) {
        index = [];
    }

    var subDirs;

    for (let dir of dirs) {
        subDirs = []
        for (let path of fs.readdirSync(dir).filter(pathBlackListConditions).sort()) {
            path = path_module.join(dir, path)
            if (is_folder(path)) indexer([path], index)
            index.push({
                path: fs.realpathSync(path),
            });
        }
    }
    return index;
}

function pathBlackListConditions(path) {
    return !(
        path_module.basename(path).startsWith('.') ||
        settings.EXCLUDED_PATHS.some(pattern => new RegExp(`${pattern}`).test(path)) ||
        settings.EXCLUDED_EXTS.some(ext => ext === path_module.extname(path))
    );
}

function is_folder(path) {
    if (settings.APP_EXTENTIONS.includes(path_module.extname(path))) {
        return false
    }
    try {
        fs.readdirSync(path)
    } catch (err) {
        return false;
    }
    return true;
}

fs.writeFileSync(process.argv[2], JSON.stringify(indexer(settings.DIRS)));
