Feature: IMDb celebrity birthday searches

  Scenario: Open the third celebrity born yesterday
    Given I open IMDb born today
    When I search for celebrities born yesterday
    And I open the third person result and capture "born_yesterday_third_person"
    Then the screenshot "born_yesterday_third_person" should exist

  Scenario: Open the first description link for a celebrity born exactly 40 years ago
    Given I open IMDb born today
    When I search for celebrities born exactly 40 years ago
    And I open the first description link and capture "born_40_years_ago_first_description_link"
    Then the screenshot "born_40_years_ago_first_description_link" should exist

