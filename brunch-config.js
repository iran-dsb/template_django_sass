// See http://brunch.io for documentation.

exports.paths = {
    public: "frontend_build/static",
    watched: [
        "frontend_source"
    ]
};

exports.files = {
  javascripts: {
    joinTo: {
      'js/vendor.js': /^(?!frontend_source)/, // Files that are not in `frontend_source` dir.
      'js/app.js': /^frontend_source/
    }
  },
  stylesheets: {joinTo: 'css/app.css'}
};

exports.plugins = {
  babel: {presets: ['latest']}
};

exports.plugins = {
    sass: {
      includePaths: ["node_modules/font-awesome/scss"], //Funciona sem essa linha também
      mode: 'native'
    }
};

exports.modules = {
    autoRequire: {
      "js/app.js": ["frontend_source/js/initialize"]
    }
};

exports.npm = {
    globals: { // Bootstrap's JavaScript requires both '$' and 'jQuery' in global scope
      $: 'jquery',
      jQuery: 'jquery'
    },
    styles: {
      lightbox2: ['dist/css/lightbox.min.css']
    }
};

exports.plugins = {
  copycat:{
    "fonts" : ["node_modules/font-awesome/fonts"],
    "images": ['node_modules/lightbox2/dist/images'],
    verbose : true, //shows each file that is copied to the destination directory
    onlyChanged: true //only copy a file if it's modified time has changed (only effective when using brunch watch)
  }
};

//exports.conventions = {
//    assets: [
//        /^(node_modules\/lightbox2\/dist\/images)/,
//        /^(frontend_source\/assets)/
//    ]
//};