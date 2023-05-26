import { Then } from "@badeball/cypress-cucumber-preprocessor";

let expected_categories = {
    "category-item/category-ltkfind": "LTK Find",
    "category-item/category-seasonal": "Summer Trends",
    "category-item/category-ltku": "LTK-U",
    "category-item/category-home": "Home",
    "category-item/category-salealert": "Deal Alert",
    "category-item/category-under50": "Under $50",
    "category-item/category-under100": "Under $100",
    "category-item/category-styletip": "Style Tips",
    "category-item/category-beauty": "Beauty",
    "category-item/category-fit": "Fitness",
    "category-item/category-curves": "Curves",
    "category-item/category-video": "Shoppable Video",
    "category-item/category-workwear": "Workwear",
    "category-item/category-swim": "Swim",
    "category-item/category-travel": "Travel",
    "category-item/category-shoecrush": "Shoe Crushes",
    "category-item/category-itbag": "It Bags",
    "category-item/category-baby": "Baby",
    "category-item/category-bump": "Bump",
    "category-item/category-kids": "Kids",
    "category-item/category-family": "Family",
    "category-item/category-mens": "Mens",
    "category-item/category-wedding": "Weddings",
    "category-item/category-europe": "Europe",
    "category-item/category-brasil": "Brasil"
}

let css_to_check = {
    "align-items": "center",
    "flex-direction": "row",
    "display": "inline-flex",
    "cursor": "pointer",
    "color": "rgb(0, 0, 0)",
    "background-color": "rgba(0, 0, 0, 0)"
}

// Generate a random string of a specific length
function generateRandomString(length=8) {
    const letters = 'abcdefghijklmnopqrstuvwxyz';
    let randomString = '';
  
    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * letters.length);
        const randomLetter = letters.charAt(randomIndex);
        randomString += randomLetter;
    }
  
    return randomString;
}

Then("I go to the page {string}", (url) => {
    cy.visit(url);
})

Then("I click on {string}", (button_name) => {
    cy.log(button_name);
    cy
        .contains(button_name)
        .first()
        .should('be.visible', {timeout: 10*1000})
        .click();
})

Then("I enter a random email", () => {
    let email = "joshuabchu+"+generateRandomString(length=8)+"@gmail.com";
    cy
        .get("input[name='email']", {timeout: 10*1000})
        .first()
        .type(email+"{enter}");
    Cypress.env("email", email);  // Save the value to be used later
})

Then("I enter a random password", () => {
    let password = generateRandomString(length=8);
    cy
        .get("input[name='password']", {timeout: 10*1000})
        .first()
        .type(password+"{enter}", {sensitve: true});
    Cypress.env("password", password);  // Save the value to be used later
})

Then("I wait {int} seconds", (wait_sec) =>{
    cy.wait(wait_sec*1000);
})

Then("I verify I landed on the page {string}", (expected_url) => {
    cy.url().then((url) => {
        cy.log(url);
        assert(expected_url == url);
    });
});

Then("I logout", () => {
    cy.visit("https://www.shopltk.com/logout");
})

Then("I enter the predefined email", () => {
    cy
        .get("input[name='email']", {timeout: 10*1000})
        .first()
        .type(Cypress.env("email")+"{enter}")  // Get the locally set value or the one gotten from earlier test
})

Then("I enter the predefined password", () => {
    cy
        .get("input[name='password']", {timeout: 10*1000})
        .first()
        .type(Cypress.env("password")+"{enter}", {sensitive: true})    // Get the locally set value or the one gotten from earlier test
})

Then("I verify the categories are correct", () => {
    Object.keys(expected_categories).forEach((key) => {
        cy.get(`a[data-test-id="${key}"]`).invoke("text").then((text) => {
            assert(text.trim() == expected_categories[key].trim());
        })
    })
})

Then("I verify the css of the categories are correct", () => {
    Object.keys(expected_categories).forEach((dataTestId) => {
        Object.keys(css_to_check).forEach((css) => {
            cy.get(`a[data-test-id="${dataTestId}"]`).invoke("css", css).then((css_value) => {
                cy.log(`Expecting ${css} to be ${css_to_check[css].trim()} and got ${css_value.trim()}`);
                cy.log(css_value.trim() == css_to_check[css].trim());
                assert(css_value.trim() == css_to_check[css].trim());
            })
        })
    })
})