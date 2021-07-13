const fs = require('fs');
const path_module = require('path');


function splitString(str) {
    return str.split(/(?=[A-Z])|[_\- ]/)
}


function find_files(searchPattern, index) {
    var searchPatterns = splitString(searchPattern)
    var result = []
    var path, pathParts, allPartsStart;

    for (path_object of index) {
        path = path_module.basename(path_object.path)
        pathParts = splitString(path);
        allPartsStart = searchPatterns
            // Check if each part starts with one pattern
            .map(pattern => pathParts.map(part => new RegExp(`^${pattern}`, 'i').test(part)))
            .every(x => x.some(x => x));


        if (allPartsStart) {
            result.push(path_object.path)
        }
    }
    return result
}

console.log(find_files('template tag', JSON.parse(fs.readFileSync(process.argv[2]))))