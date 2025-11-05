Feature: Check if today is Christmas on the Is It Christmas website
  As a curious visitor
  I want the site to load and show a clear answer
  So that I immediately know if it is Christmas

  Background:
    Given I open the url "https://isitchristmas.com/"

  # URL & reachability
  Scenario: Page is reachable over HTTPS
    Then I expect the url to contain "https://"

  Scenario: Domain is correct
    Then I expect the url to contain "isitchristmas.com"

  Scenario: Root path is served
    Then I expect that the path is "/"

  # Basic structure present
  Scenario: HTML element exists
    Then I expect that element "html" does exist

  Scenario: HEAD element exists
    Then I expect that element "head" does exist

  Scenario: BODY element exists and is visible
    Then I expect that element "body" does exist
    And I expect that element "body" is visible

  # Content shows up
  Scenario: Body has some text
    Then I expect that element "body" contains any text

  Scenario: Page becomes ready within default wait
    Then I wait on element "body" to exist

  # Navigating again still works
  Scenario: Revisit the site directly
    When I open the url "https://isitchristmas.com/"
    Then I expect the url to contain "isitchristmas.com"

    Scenario: HTTP redirects to HTTPS
    When I open the url "http://isitchristmas.com/"
    Then I expect the url to contain "https://"

  Scenario: Title element exists
    Given I open the url "https://isitchristmas.com/"
    Then I expect that element "title" does exist

  Scenario: At least one meta tag exists
    Given I open the url "https://isitchristmas.com/"
    Then I expect that element "meta" does exist

  Scenario: HTML element is visible
    Given I open the url "https://isitchristmas.com/"
    Then I expect that element "html" is visible

  Scenario: Body becomes visible
    Given I open the url "https://isitchristmas.com/"
    Then I wait on element "body" to be visible