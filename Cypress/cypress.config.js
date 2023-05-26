const { defineConfig } = require('cypress')
const webpack = require("@cypress/webpack-preprocessor");
const preprocessor = require("@badeball/cypress-cucumber-preprocessor");

async function setupNodeEvents(on, config) {
  await preprocessor.addCucumberPreprocessorPlugin(on, config);
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
  return config;
}

module.exports = defineConfig({
  defaultCommandTimeout: 10000,
  pageLoadTimeout: 60000,
  requestTimeout: 10000,
  viewportHeight: 920,
  viewportWidth: 1152,  
  env: {},
  trashAssetsBeforeRuns: true,
  retries: {
    runMode: 1,
  },
  numTestsKeptInMemory: 20,
  projectId: 'not-real',
  e2e: {
    specPattern: 'cypress/e2e/**/*.feature',
    experimentalSessionAndOrigin: true,
    setupNodeEvents
  }
})


