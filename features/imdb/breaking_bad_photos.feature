Feature: IMDb Breaking Bad photos

  Scenario: Open the second Danny Trejo photo from Breaking Bad
    Given I open the IMDb top 250 TV page
    When I open the Breaking Bad title page
    And I open the Breaking Bad photo gallery
    And I filter the gallery by Danny Trejo
    And I open the second media photo
    Then I should be on an IMDb media viewer page

