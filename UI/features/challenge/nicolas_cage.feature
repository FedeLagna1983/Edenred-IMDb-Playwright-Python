Feature: IMDb Nicolas Cage credits

  Scenario: Open the first completed upcoming Nicolas Cage title
    Given I search IMDb for the person "Nicolas Cage"
    When I open the "Nicolas Cage" person result
    And I open the first completed upcoming credit
    Then I should be on an IMDb title page

