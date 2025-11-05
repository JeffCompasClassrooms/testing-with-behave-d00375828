Feature: Pepper's Ghost DIY article is readable and useful
  As a Halloween builder
  I want the Pepper's Ghost tutorial to load with text, images, and sections
  So that I can follow the steps to build my ghost scene

  Background:
    Given I open the Pepper's Ghost tutorial
    And I dismiss any consent banner if asked

  # --- Page identity ---
  Scenario: Title mentions Pepper's Ghost
    Then the page title should mention "Pepper"

  Scenario: Main heading mentions Pepper's Ghost
    Then the main heading should mention "Pepper"

  Scenario: Served securely over HTTPS
    Then the current URL should start with "https://"

  # --- Basic structure & visibility ---
  Scenario: Body is visible
    Then the page body should be visible

  Scenario: The article has an Introduction
    Then I should see the word "Introduction" somewhere on the page

  Scenario: The site header shows primary sections
    Given I open the Pepper's Ghost tutorial
    And I dismiss any consent banner if asked
    Then I should see at least 1 nav link among "Projects, Contests, Teachers"
    
    Scenario: The article has subheadings
    Given I open the Pepper's Ghost tutorial
    And I dismiss any consent banner if asked
    Then I should find at least 1 elements matching "h2, h3"


  # --- Images & media ---
  Scenario: At least one build photo is present
    Then I should see at least 1 images on the page

  Scenario: Gallery has multiple photos
    Then I should see at least 3 images on the page

  Scenario: Images have a source URL
    Then at least 1 image should have a non-empty src

  # --- Lists / materials / links ---
  Scenario: There is at least one bullet list of materials or steps
    Then I should see at least 1 list items on the page

  Scenario: The article links to at least one external resource
    Then I should see at least 1 external links on the page

  # --- Scrolling & resilience ---
  Scenario: Scrolling does not break the article
    When I scroll down the page by 1500 pixels
    Then the page body should still be present

  Scenario: Revisit still shows the article
    When I reload the page
    Then the main heading should mention "Pepper"

  Scenario: Basic section elements exist
    Then I should find at least 1 elements matching "section, article"

  # --- SITE SEARCH USABILITY ---
  Scenario: The site search is usable from the header
    Given I open the Pepper's Ghost tutorial
    And I dismiss any consent banner if asked
    When I use the site search for "pepper ghost test"
    Then I should land on a search results page

  # --- TAGS / CATEGORIES VISIBILITY ---
  Scenario: The article shows tags or categories
    Given I open the Pepper's Ghost tutorial
    And I dismiss any consent banner if asked
    Then I should see at least 1 tag or category link

  # --- RICH MEDIA ---
  Scenario: The article includes embedded video or a media player
    Given I open the Pepper's Ghost tutorial
    And I dismiss any consent banner if asked
    Then I should see an embedded video or player

  # --- DOWNLOAD / PRINT SUPPORT ---
  Scenario: The article offers a printable or downloadable resource
    Given I open the Pepper's Ghost tutorial
    And I dismiss any consent banner if asked
    Then I should find a download or print option

  # --- STEP-BY-STEP INSTRUCTIONS ---
  Scenario: The tutorial provides step-by-step headings
    Given I open the Pepper's Ghost tutorial
    And I dismiss any consent banner if asked
    Then I should see at least 1 step heading
