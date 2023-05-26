/// <reference types="cypress" />

/**
 * @type {Cypress.PluginConfig}
 */
// eslint-disable-next-line no-unused-vars
module.exports = (on, config) => {
  on('before:browser:launch', (browser = {}, args) => {

    if (browser.name === 'chrome') {
      args.push('--remote-debugging-port=9222')

      // whatever you return here becomes the new args
      return args
    }

  })

  // in plugins file
  on('task', {
    log (message) {
      console.log(message)
      return null
    }
  })
}

// For Cucumber to use Gherkin
// const cucumber = require('@badeball/cypress-cucumber-preprocessor').default
// module.exports = (on, config) => {
//   on('file:preprocessor', cucumber())
// }

// import webpack from "@cypress/webpack-preprocessor";

const webpack = require("@cypress/webpack-preprocessor");

module.exports =  (on, config) => {
  on(
    "file:preprocessor",
    webpack({
      webpackOptions: {
        resolve: {
          extensions: [".ts", ".js"],
        },
        module: {
          rules: [
            {
              test: /\.ts$/,
              exclude: [/node_modules/],
              use: [
                {
                  loader: "ts-loader",
                },
              ],
            },
            {
              test: /\.feature$/,
              use: [
                {
                  loader: "@badeball/cypress-cucumber-preprocessor/webpack",
                  options: config,
                },
              ],
            },
          ],
        },
      },
    })
  );
};

// const { defineConfig } = require("cypress");
// const webpack = require("@cypress/webpack-preprocessor");
// const preprocessor = require("@badeball/cypress-cucumber-preprocessor");

// async function setupNodeEvents(on, config) {
//   await preprocessor.addCucumberPreprocessorPlugin(on, config);

//   on(
//     "file:preprocessor",
//     webpack({
//       webpackOptions: {
//         resolve: {
//           extensions: [".ts", ".js"],
//         },
//         module: {
//           rules: [
//             {
//               test: /\.ts$/,
//               exclude: [/node_modules/],
//               use: [
//                 {
//                   loader: "ts-loader",
//                 },
//               ],
//             },
//             {
//               test: /\.feature$/,
//               use: [
//                 {
//                   loader: "@badeball/cypress-cucumber-preprocessor/webpack",
//                   options: config,
//                 },
//               ],
//             },
//           ],
//         },
//       },
//     })
//   );

//   // Make sure to return the config object as it might have been modified by the plugin.
//   return config;
// }

// module.exports =  (on, config) => {
//   setupNodeEvents;
//   };


module.exports = defineConfig({
  e2e: {
    // specPattern: "**/*.feature",
    // supportFile: false,
    setupNodeEvents,
  },
});