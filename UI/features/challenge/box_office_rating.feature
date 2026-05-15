Feature: IMDb top box office rating

  Scenario: Rate the second top box office movie with five stars
    Given I open the IMDb top box office page
    When I open the second box office movie
    And I select 5 stars in the rating prompt
    And I submit the rating
    Then I should be redirected to the IMDb sign in page

