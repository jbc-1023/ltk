Feature: Generic tests

    Scenario: Signup as a new user
        Given I go to the page "https://www.shopltk.com"
        Then I click on "Sign up"
        Then I enter a random email
        Then I enter a random password
        Then I wait 10 seconds
        Then I verify I landed on the page "https://www.shopltk.com/home/for-you"
        Then I logout

    Scenario: Test the SHOP menu
        Given I go to the page "https://www.shopltk.com"
        Then I click on "Log in"
        Then I enter the predefined email
        Then I enter the predefined password
        Then I wait 10 seconds
        Then I click on "Shop"
        And I verify the categories are correct
        And I verify the css of the categories are correct
